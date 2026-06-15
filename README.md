# RubyMark

RubyMark 是一款支援 Ruby 旁註（振假名/注音）的 Markdown 轉換工具，目前同時支援 **Python (CLI)** 與 **Web (瀏覽器端)** 雙平台。

---

## 語法提示

除了標準 Markdown 語法外，RubyMark 還提供以下額外語法支援：

### 1. Ruby 旁註標記（振假名/注音）
用於漢字標音或提供額外解釋說明。
- **語法**：`{文字}(旁註)`
- **範例**：`{RubyMark}(ルビマーク)`、`{特定字號}(5¼)`
- **產生的 HTML**：
  ```html
  <ruby>RubyMark<rp> (</rp><rt>ルビマーク</rt><rp>) </rp></ruby>
  ```

### 2. 刪除線
用於標記刪除或修改的文字。
- **語法**：`~~被刪除的文字~~`
- **範例**：`~~舊內容~~`
- **產生的 HTML**：
  ```html
  <del>舊內容</del>
  ```

### 3. 程式碼保護
在行內程式碼或多行程式碼塊中，上述語法會被自動保護而不被解析。
- **範例**：`{not ruby}(text)` 和 `~~not del~~` 將會保持原樣輸出。

---

## Python 使用方法 (CLI)

### 命令列參數

```plaintext
usage: rubymark.py [-h] [-f FILE] [-o OUTPUT] [--verbose]

RubyMark，支持 Ruby 旁注的 Markdown 轉換工具

options:
  -h, --help           顯示此幫助訊息並退出
  -f, --file FILE      輸入檔案
  -o, --output OUTPUT  輸出檔案，預設為標準輸出 (stdout)
  -v, --verbose        輸出詳細資訊
```

### 執行測試
```bash
python3 run_tests.py
```

---

## Web 網頁使用方法

RubyMark 提供客戶端 JavaScript 庫 `rubymark.js`，讓您能在網頁中輕鬆渲染 RubyMark Markdown。

### 1. 引入 JavaScript 腳本
在網頁中載入 `rubymark.js`，它會自動從 CDN 載入並配置 `marked.js` 解析器：
```html
<script src="rubymark.js"></script>
```

### 2. 使用 Custom Element（推薦）
使用標準自訂元素 `<ruby-mark>` 包裹您的 Markdown 內容：
```html
<ruby-mark>
# {Ruby}(振假名) 測試
這是一段包含 {旁註}(輔助說明) 的段落。
</ruby-mark>
```

### 3. 使用 Legacy Tag
為了向後相容或書寫方便，您也可以直接使用 `<rubymark>` 標籤（庫中透過 `MutationObserver` 進行動態掃描與解析）：
```html
<rubymark>
使用 `{漢字}(かんじ)` 來標註旁註。
</rubymark>
```

### 4. 動態屬性綁定
您可以利用 `content` 屬性動態更新內容：
```html
<ruby-mark id="viewer" content="這是動態 {內容}(Content)"></ruby-mark>

<script>
  document.getElementById('viewer').setAttribute('content', '# 新的 {標題}(Title)');
</script>
```

### 5. JS API 使用
您也可以直接透過 JavaScript 調用 `RubyMark` API 來手動渲染文字：
```javascript
// 異步渲染
RubyMark.render("# {測試}(Test)").then(html => {
  console.log(html); // 輸出轉換後的 HTML 程式碼
});
```

---

## 互動式遊樂場 (Playground)

本項目內置了一個即時互動預覽的網頁。您可以在本機啟動伺服器並進行體驗：
```bash
python3 -m http.server 8080
```
接著在瀏覽器中開啟 `http://localhost:8080/index.html` 即可使用。
