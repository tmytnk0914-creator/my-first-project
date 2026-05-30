#!/usr/bin/env python3
"""新作ゲーム ローンチ・マーケティング戦略 の .pptx を生成する。
Google スライドへは Drive にアップロード →「Google スライドで開く」で変換できる。"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# --- デザイントークン -------------------------------------------------
NAVY   = RGBColor(0x0F, 0x17, 0x2A)
NAVY2  = RGBColor(0x1E, 0x29, 0x3B)
CARD   = RGBColor(0x17, 0x20, 0x33)
BLUE   = RGBColor(0x3B, 0x82, 0xF6)
CYAN   = RGBColor(0x22, 0xD3, 0xEE)
TEXT   = RGBColor(0xE2, 0xE8, 0xF0)
MUTED  = RGBColor(0x94, 0xA3, 0xB8)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
LINE   = RGBColor(0x33, 0x41, 0x55)
FONT   = "Noto Sans JP"

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
SW, SH = prs.slide_width, prs.slide_height
BLANK = prs.slide_layouts[6]


def bg(slide, color=NAVY):
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = color


def accent_bar(slide):
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, SH - Pt(8), SW, Pt(8))
    bar.fill.solid(); bar.fill.fore_color.rgb = BLUE
    bar.line.fill.background()


def textbox(slide, l, t, w, h, anchor=MSO_ANCHOR.TOP):
    tb = slide.shapes.add_textbox(l, t, w, h)
    tf = tb.text_frame; tf.word_wrap = True; tf.vertical_anchor = anchor
    return tf


def setpara(p, text, size, color, bold=False, align=PP_ALIGN.LEFT, space=6):
    p.text = text; p.alignment = align; p.space_after = Pt(space)
    r = p.runs[0]; f = r.font
    f.size = Pt(size); f.bold = bold; f.color.rgb = color; f.name = FONT
    return p


def kicker(slide, text):
    tf = textbox(slide, Inches(0.9), Inches(0.55), Inches(11), Inches(0.5))
    setpara(tf.paragraphs[0], text.upper(), 14, CYAN, bold=True)


def title(slide, text, size=34):
    tf = textbox(slide, Inches(0.9), Inches(1.05), Inches(11.5), Inches(1.3))
    setpara(tf.paragraphs[0], text, size, WHITE, bold=True)


def note(slide, text):
    tf = textbox(slide, Inches(0.9), Inches(6.55), Inches(11.5), Inches(0.7))
    setpara(tf.paragraphs[0], "▍ " + text, 12, MUTED)


def bullets(slide, items, top=2.5, size=18, left=0.9, width=11.5, height=3.6):
    tf = textbox(slide, Inches(left), Inches(top), Inches(width), Inches(height))
    for i, it in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        setpara(p, "● " + it, size, TEXT, space=12)
        p.runs[0].font.color.rgb = TEXT
        # 行頭マーカーを色付けに
        p.runs[0].font.color.rgb = TEXT
    return tf


def card(slide, l, t, w, h, head, body):
    sh = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, l, t, w, h)
    sh.fill.solid(); sh.fill.fore_color.rgb = CARD
    sh.line.color.rgb = LINE; sh.line.width = Pt(1)
    tf = sh.text_frame; tf.word_wrap = True
    tf.margin_left = Inches(0.25); tf.margin_right = Inches(0.25)
    tf.margin_top = Inches(0.2)
    setpara(tf.paragraphs[0], head, 16, CYAN, bold=True, space=8)
    p = tf.add_paragraph(); setpara(p, body, 12.5, MUTED, space=2)
    return sh


# === Slide 1 : Title ==================================================
s = prs.slides.add_slide(BLANK); bg(s)
kicker(s, "Game Marketing Strategy")
tf = textbox(s, Inches(0.9), Inches(2.4), Inches(11.5), Inches(2.2))
setpara(tf.paragraphs[0], "新作ゲーム", 44, WHITE, bold=True, space=2)
p = tf.add_paragraph(); setpara(p, "ローンチ・マーケティング戦略", 44, WHITE, bold=True)
tf2 = textbox(s, Inches(0.9), Inches(4.7), Inches(11.5), Inches(1.2))
setpara(tf2.paragraphs[0], "コミュニティ起点 × データドリブンで、混雑市場を勝ち抜く", 20, CYAN)
p = tf2.add_paragraph(); setpara(p, "マーケティングチーム / 2026", 14, MUTED)
accent_bar(s)

# === Slide 2 : Hook ===================================================
s = prs.slides.add_slide(BLANK); bg(s)
kicker(s, "Hook ・ 市場の現状"); title(s, "今、ゲーム市場で起きていること")
tf = textbox(s, Inches(0.9), Inches(2.6), Inches(4.5), Inches(2.5))
setpara(tf.paragraphs[0], "90%+", 72, CYAN, bold=True, space=4)
p = tf.add_paragraph(); setpara(p, "の新作が初週で埋もれ、\n認知を獲得できない", 16, MUTED)
bullets(s, [
    "年間リリース数は過去5年で約2倍に増加",
    "ユーザーの可処分時間とウィッシュリストは飽和状態",
    "「作れば売れる」時代は終わった",
], top=2.8, left=6.0, width=6.4)
note(s, "危機感を共有し、聴衆を引き込む。"); accent_bar(s)

# === Slide 3 : Problem ================================================
s = prs.slides.add_slide(BLANK); bg(s)
kicker(s, "Problem ・ 課題"); title(s, "私たちが直面する課題")
bullets(s, [
    "開発品質は高いが、発売前の認知がほぼゼロ",
    "広告に頼った獲得は、CAC（獲得コスト）が高騰し続けている",
    "発売後のスタートダッシュ依存はリスクが大きい",
], top=2.8, size=20)
note(s, "「良いゲーム＝売れる」ではない構造を明示する。"); accent_bar(s)

# === Slide 4 : Insight ================================================
s = prs.slides.add_slide(BLANK); bg(s)
kicker(s, "Insight ・ 洞察"); title(s, "データが示す本質的な洞察")
bullets(s, [
    "成功タイトルの共通点は発売“前”のコミュニティ規模",
    "ウィッシュリスト登録数と初週売上に強い相関",
    "勝負は発売日ではなく、発売6か月前から始まる",
], top=2.8, left=0.9, width=6.5)
c = card(s, Inches(7.7), Inches(2.7), Inches(4.7), Inches(2.8),
         "視点の転換", "「発売日」から「育成期間」へ")
tf = c.text_frame.add_paragraph()
setpara(tf, "前 → 後", 40, CYAN, bold=True, align=PP_ALIGN.CENTER)
note(s, "聴衆の視点を転換させる、最重要スライド。"); accent_bar(s)

# === Slide 5 : Solution overview ======================================
s = prs.slides.add_slide(BLANK); bg(s)
kicker(s, "Solution ・ 全体像"); title(s, "マーケティング戦略の全体像")
w = Inches(3.9); h = Inches(2.9); top = Inches(2.7); gap = Inches(0.25)
card(s, Inches(0.9), top, w, h, "① コミュニティ育成", "発売前からファンを育て、自然拡散の土台をつくる。")
card(s, Inches(0.9)+w+gap, top, w, h, "② データドリブン獲得", "指標を週次で回し、CACを継続的に最適化する。")
card(s, Inches(0.9)+2*(w+gap), top, w, h, "③ 持続的エンゲージメント", "発売後も関係を維持し、LTVを最大化する。")
note(s, "一貫したブランドメッセージで全フェーズを貫く。"); accent_bar(s)

# === Slide 6 : Target =================================================
s = prs.slides.add_slide(BLANK); bg(s)
kicker(s, "Solution ・ 詳細1"); title(s, "ターゲット & ポジショニング")
bullets(s, [
    "主要ターゲット: コアゲーマー（18〜34歳）＋ 配信視聴層",
    "ポジショニング: 「ジャンル × 独自メカニクス」で差別化",
    "競合マップ上の空白地帯を狙う",
    "一言で言えるバリュープロポジションを定義",
], top=2.8, size=19)
note(s, "「誰に・なぜ刺さるか」をペルソナとマップで語る。"); accent_bar(s)

# === Slide 7 : Channel ================================================
s = prs.slides.add_slide(BLANK); bg(s)
kicker(s, "Solution ・ 詳細2"); title(s, "チャネル & コンテンツ戦略")
w = Inches(3.9); h = Inches(2.2); top = Inches(2.6); gap = Inches(0.25)
card(s, Inches(0.9), top, w, h, "Earned（拡散）", "配信者シーディング、Discordコミュニティ運営。")
card(s, Inches(0.9)+w+gap, top, w, h, "Owned（資産）", "ストアページ最適化、開発ブログ、SNS。")
card(s, Inches(0.9)+2*(w+gap), top, w, h, "Paid（刈り取り）", "リターゲティング中心の効率的広告運用。")
bullets(s, ["コンテンツ設計: 開発舞台裏 → デモ → トレーラー の段階展開"], top=5.1, size=17)
note(s, "「無料で広がる仕組み」を先に作り、広告は後半に集中。"); accent_bar(s)

# === Slide 8 : Timeline ===============================================
s = prs.slides.add_slide(BLANK); bg(s)
kicker(s, "Solution ・ 詳細3"); title(s, "ローンチ・タイムライン")
phases = [("Phase 1 ・ 6〜3か月前", "認知 & ウィッシュリスト獲得"),
          ("Phase 2 ・ 3〜0か月前", "デモ配信 & 予約促進"),
          ("Phase 3 ・ 発売〜3か月後", "ローンチ施策 & レビュー & 継続運用")]
w = Inches(3.9); h = Inches(2.6); top = Inches(2.8); gap = Inches(0.25)
for i, (tag, body) in enumerate(phases):
    card(s, Inches(0.9)+i*(w+gap), top, w, h, tag, body)
note(s, "各フェーズにマイルストーンと担当を明記する。"); accent_bar(s)

# === Slide 9 : KPI ====================================================
s = prs.slides.add_slide(BLANK); bg(s)
kicker(s, "Proof ・ KPI"); title(s, "KPIと測定フレームワーク")
rows = [("区分", "指標"),
        ("先行指標", "ウィッシュリスト数 / コミュニティ規模 / デモDL数"),
        ("結果指標", "初週売上 / CAC / ROAS / リテンション"),
        ("運用", "週次ダッシュボードでPDCAを高速回転")]
tbl = s.shapes.add_table(4, 2, Inches(0.9), Inches(2.7), Inches(11.5), Inches(3.0)).table
tbl.columns[0].width = Inches(3.0); tbl.columns[1].width = Inches(8.5)
for r, (a, b) in enumerate(rows):
    for c, val in enumerate((a, b)):
        cell = tbl.cell(r, c)
        cell.fill.solid(); cell.fill.fore_color.rgb = CARD if r else NAVY2
        tfc = cell.text_frame; tfc.word_wrap = True
        setpara(tfc.paragraphs[0], val, 15, CYAN if r == 0 else TEXT, bold=(r == 0))
note(s, "「何をもって成功とするか」を数値で合意する。"); accent_bar(s)

# === Slide 10 : Budget ================================================
s = prs.slides.add_slide(BLANK); bg(s)
kicker(s, "Proof ・ 予算"); title(s, "予算とリソース配分")
bullets(s, [
    "費目別配分: コミュニティ / コンテンツ / ペイド / ツール",
    "投資カーブ: 前半は育成、後半は刈り取り",
    "ROIシミュレーション: 投資 → 想定売上 をレンジで提示",
], top=2.8, size=19)
note(s, "円グラフ＋シナリオ別ROIで投資判断を後押しする。"); accent_bar(s)

# === Slide 11 : Risk ==================================================
s = prs.slides.add_slide(BLANK); bg(s)
kicker(s, "補強 ・ Risk"); title(s, "リスクと対応策")
quads = [("発売延期", "→ スケジュールにバッファを設計"),
         ("競合の同時期ローンチ", "→ 差別化メッセージを徹底"),
         ("炎上リスク", "→ 危機対応フローを事前整備"),
         ("認知不足", "→ 早期コミュニティ施策で先回り")]
w = Inches(5.7); h = Inches(1.6); top = Inches(2.7); gx = Inches(0.25); gy = Inches(0.25)
for i, (head, body) in enumerate(quads):
    l = Inches(0.9) + (i % 2) * (w + gx)
    t = top + (i // 2) * (h + gy)
    card(s, l, t, w, h, head, body)
note(s, "リスクを先回りで示し、戦略の信頼性を高める。"); accent_bar(s)

# === Slide 12 : Next Action ===========================================
s = prs.slides.add_slide(BLANK); bg(s)
kicker(s, "Conclusion ・ Next Action"); title(s, "ネクストアクション")
bullets(s, [
    "本日の決定事項: 戦略承認 / 予算承認 / キックオフ日",
    "直近30日のアクション（担当・期日つき）",
    "次回レビューのタイミングを設定",
], top=2.8, size=20)
note(s, "明確なCTAで会議を「決定」で締める。"); accent_bar(s)

# === Slide 13 : Q&A ===================================================
s = prs.slides.add_slide(BLANK); bg(s)
kicker(s, "Q & A")
tf = textbox(s, Inches(0.9), Inches(2.7), Inches(11.5), Inches(2.0), MSO_ANCHOR.MIDDLE)
setpara(tf.paragraphs[0], "ご質問・ご意見をお願いします", 40, WHITE, bold=True)
tf2 = textbox(s, Inches(0.9), Inches(4.6), Inches(11.5), Inches(0.8))
setpara(tf2.paragraphs[0], "補足資料・詳細データは付録をご参照ください", 18, MUTED)
accent_bar(s)

# === Slide 14 : Appendix ==============================================
s = prs.slides.add_slide(BLANK); bg(s)
kicker(s, "Appendix ・ 付録"); title(s, "付録")
bullets(s, [
    "詳細データ / 競合分析 / 用語集",
    "過去タイトルのベンチマーク",
    "質疑応答時の根拠資料",
], top=2.8, size=20)
accent_bar(s)

prs.save("game-marketing-presentation.pptx")
print("saved game-marketing-presentation.pptx :", len(prs.slides.__iter__.__self__._sldIdLst), "slides")
