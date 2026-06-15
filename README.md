# RubyMark

RubyMark 是支持 Ruby 旁註（振假名/注音）的 Python Markdown 轉換工具。

## 使用方法

```plaintext
usage: rubymark.py [-h] [-f FILE] [-o OUTPUT] [--verbose]

RubyMark，支持 Ruby 旁注的 Markdown 轉換工具

options:
  -h, --help           顯示此幫助訊息並退出
  -f, --file FILE      輸入檔案
  -o, --output OUTPUT  輸出檔案，預設為標準輸出 (stdout)
  --verbose            輸出詳細資訊
```

## 語法提示

除了標準 Markdown 語法外，RubyMark 還提供以下額外語法支持：

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
