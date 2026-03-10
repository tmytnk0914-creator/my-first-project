// =============================================================
// Google Apps Script — インフルエンサーSNS URL自動取得スクリプト
// Gemini API (gemini-2.5-flash) を使用
// =============================================================

// ★ 重要: APIキーは漏洩防止のためスクリプトプロパティに保存してください
//   1. GASエディタ → プロジェクトの設定 → スクリプトプロパティ
//   2. プロパティ名: GEMINI_API_KEY  値: あなたのAPIキー
//   を設定した上で、以下のように取得してください:
//
//   const API_KEY = PropertiesService.getScriptProperties().getProperty("GEMINI_API_KEY");
//
// 以下は動作確認用の直書き例です（本番運用時はスクリプトプロパティを使用してください）:
const API_KEY = "YOUR_API_KEY_HERE";

function runUrlExtraction() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("1. 調査対象");
  if (!sheet) {
    SpreadsheetApp.getUi().alert("シート「1. 調査対象」が見つかりません。");
    return;
  }

  const data = sheet.getDataRange().getValues();
  const cleanKey = API_KEY.trim();

  // ★ 修正箇所1: APIバージョンを v1beta に変更
  // ★ 修正箇所2: モデル名を gemini-2.5-flash に変更（gemini-1.5-flash は2025年9月に廃止済み）
  const url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=" + cleanKey;

  for (let i = 1; i < data.length; i++) {
    const rowNum = i + 1;
    const name = data[i][0];
    if (!name || data[i][9] === "URL取得済") continue;

    const promptText =
      "あなたはSNS調査の専門家です。以下のインフルエンサー名から、公式SNSアカウントのURLを調査してください。\n" +
      "インフルエンサー名: " + name + "\n\n" +
      "以下のJSON形式のみで回答してください。URLが見つからない場合は \"-\" を入れてください。\n" +
      "マークダウンのコードブロック(```)は使わず、純粋なJSONのみ出力してください。\n" +
      "{\"x_url\": \"URL\", \"insta_url\": \"URL\", \"tiktok_url\": \"URL\", \"fb_url\": \"URL\", \"other_url\": \"URL\"}";

    const payload = {
      "contents": [
        {
          "parts": [{ "text": promptText }]
        }
      ],
      "generationConfig": {
        "responseMimeType": "application/json"
      }
    };

    const options = {
      "method": "post",
      "contentType": "application/json",
      "payload": JSON.stringify(payload),
      "muteHttpExceptions": true
    };

    try {
      const response = UrlFetchApp.fetch(url, options);
      const statusCode = response.getResponseCode();
      const resText = response.getContentText();

      if (statusCode !== 200) {
        sheet.getRange(rowNum, 10).setValue("エラー(" + statusCode + "): " + resText.substring(0, 200));
        continue;
      }

      const json = JSON.parse(resText);

      if (json.candidates && json.candidates.length > 0) {
        let resultText = json.candidates[0].content.parts[0].text;
        // コードブロックが含まれている場合の安全策
        resultText = resultText.replace(/```json/g, "").replace(/```/g, "").trim();
        const result = JSON.parse(resultText);
        sheet.getRange(rowNum, 4, 1, 5).setValues([
          [
            result.x_url || "-",
            result.insta_url || "-",
            result.tiktok_url || "-",
            result.fb_url || "-",
            result.other_url || "-"
          ]
        ]);
        sheet.getRange(rowNum, 10).setValue("URL取得済");
      } else {
        sheet.getRange(rowNum, 10).setValue("エラー: レスポンスにcandidatesがありません - " + resText.substring(0, 200));
      }
    } catch (e) {
      sheet.getRange(rowNum, 10).setValue("解析失敗: " + e.message);
    }

    Utilities.sleep(1500);
  }
}
