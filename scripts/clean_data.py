#!/usr/bin/env python3
"""Excel/CSVデータ整形ツール

使い方:
    python3 scripts/clean_data.py 入力ファイル.xlsx
    python3 scripts/clean_data.py 入力ファイル.csv --out 出力フォルダ
    python3 scripts/clean_data.py 入力ファイル.xlsx --sheet シート名

やること:
    1. 全角/半角の表記ゆれを統一(NFKC正規化)
    2. セル前後の余分な空白を削除
    3. 完全に空の行・列を削除
    4. 完全重複行を削除(--no-dedupe で無効化)
    5. 整形済みファイル + データサマリー(件数・空欄・数値統計)を出力

安全設計:
    - 元ファイルは絶対に上書きしない(別名で保存)
    - 出力先に同名ファイルがある場合は --force がない限り停止する
"""

import argparse
import sys
import unicodedata
from pathlib import Path

import pandas as pd


def load(path: Path, sheet: str | None) -> pd.DataFrame:
    if path.suffix.lower() in (".xlsx", ".xlsm", ".xls"):
        return pd.read_excel(path, sheet_name=sheet or 0)
    if path.suffix.lower() == ".csv":
        for enc in ("utf-8-sig", "cp932", "utf-8"):
            try:
                return pd.read_csv(path, encoding=enc)
            except UnicodeDecodeError:
                continue
        raise ValueError("文字コードを判定できませんでした(UTF-8/Shift_JISのどちらでもありません)")
    raise ValueError(f"対応していない形式です: {path.suffix}(.xlsx / .csv に対応)")


def normalize_cell(v):
    if isinstance(v, str):
        v = unicodedata.normalize("NFKC", v).strip()
        return pd.NA if v == "" else v
    return v


def clean(df: pd.DataFrame, dedupe: bool) -> tuple[pd.DataFrame, list[str]]:
    log = []
    rows0, cols0 = df.shape

    df.columns = [unicodedata.normalize("NFKC", str(c)).strip() for c in df.columns]
    df = df.map(normalize_cell)
    log.append("表記ゆれを統一しました(全角英数→半角、前後空白の削除)")

    df = df.dropna(how="all").dropna(axis=1, how="all")
    if df.shape[0] < rows0:
        log.append(f"空の行を {rows0 - df.shape[0]} 行削除しました")
    if df.shape[1] < cols0:
        log.append(f"空の列を {cols0 - df.shape[1]} 列削除しました")

    if dedupe:
        before = len(df)
        df = df.drop_duplicates()
        if len(df) < before:
            log.append(f"重複行を {before - len(df)} 行削除しました")

    converted = []
    for col in df.columns:
        if df[col].dtype == object or pd.api.types.is_string_dtype(df[col]):
            s = pd.to_numeric(df[col].astype(str).str.replace(",", ""), errors="coerce")
            if s.notna().eq(df[col].notna()).all() and df[col].notna().any():
                df[col] = s.convert_dtypes()
                converted.append(str(col))
    if converted:
        log.append(f"数値として扱える列を数値に変換しました: {', '.join(converted)}")

    return df.reset_index(drop=True), log


def summary_text(df: pd.DataFrame, src: Path, log: list[str]) -> str:
    lines = [
        f"=== データサマリー: {src.name} ===",
        f"行数: {len(df)} / 列数: {len(df.columns)}",
        "",
        "--- 整形内容 ---",
        *[f"- {m}" for m in log],
        "",
        "--- 列ごとの空欄 ---",
    ]
    for col in df.columns:
        n = int(df[col].isna().sum())
        mark = " ←要確認" if n > 0 else ""
        lines.append(f"- {col}: 空欄 {n} 件{mark}")

    num = df.select_dtypes("number")
    if not num.empty:
        lines += ["", "--- 数値列の統計 ---"]
        for col in num.columns:
            s = num[col]
            lines.append(
                f"- {col}: 合計 {s.sum():,.4g} / 平均 {s.mean():,.4g} / 最小 {s.min():,.4g} / 最大 {s.max():,.4g}"
            )
    lines += ["", "※空欄や異常値は元データを確認してください。この整形は機械処理であり、内容の正しさは保証しません。"]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Excel/CSVデータ整形ツール(元ファイルは変更しません)")
    ap.add_argument("input", help="入力ファイル(.xlsx / .csv)")
    ap.add_argument("--sheet", help="Excelのシート名(省略時は先頭シート)")
    ap.add_argument("--out", help="出力フォルダ(省略時は入力ファイルと同じ場所)")
    ap.add_argument("--no-dedupe", action="store_true", help="重複行の削除をしない")
    ap.add_argument("--force", action="store_true", help="出力先に同名ファイルがあっても上書きする")
    args = ap.parse_args()

    src = Path(args.input)
    if not src.exists():
        print(f"エラー: ファイルが見つかりません: {src}", file=sys.stderr)
        return 1

    out_dir = Path(args.out) if args.out else src.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    out_data = out_dir / f"{src.stem}_整形済み{'.csv' if src.suffix.lower() == '.csv' else '.xlsx'}"
    out_sum = out_dir / f"{src.stem}_サマリー.txt"

    if not args.force:
        for p in (out_data, out_sum):
            if p.exists():
                print(f"エラー: 出力先に {p.name} が既にあります。上書きするには --force を付けてください。", file=sys.stderr)
                return 1

    try:
        df = load(src, args.sheet)
    except Exception as e:
        print(f"エラー: 読み込みに失敗しました: {e}", file=sys.stderr)
        return 1

    df, log = clean(df, dedupe=not args.no_dedupe)

    if out_data.suffix == ".csv":
        df.to_csv(out_data, index=False, encoding="utf-8-sig")
    else:
        df.to_excel(out_data, index=False)
    out_sum.write_text(summary_text(df, src, log), encoding="utf-8")

    print(f"完了: {out_data}")
    print(f"完了: {out_sum}")
    print("※元ファイルは変更していません。整形結果を必ず目で確認してから使ってください。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
