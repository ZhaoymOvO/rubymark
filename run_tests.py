#!/usr/bin/env python3
"""
Automated tests for RubyMark refactoring
"""

import sys
import os
import re
from funcs.explainer import explain

def normalize_html(html_str):
    # Extract body if it's a full HTML page
    if "<body>" in html_str and "</body>" in html_str:
        html_str = html_str.split("<body>")[1].split("</body>")[0]

    # Strip Pygments spans
    html_str = re.sub(r'<span[^>]*>', '', html_str)
    html_str = re.sub(r'</span>', '', html_str)

    # Standardize code block wrappers
    html_str = re.sub(r'<div class="codehilite">\s*<pre>\s*(?:<span></span>\s*)?<code>', '<pre class="codehilite"><code>', html_str)
    html_str = re.sub(r'</code>\s*</pre>\s*</div>', '</code></pre>', html_str)

    # Standardize code blocks that didn't have pygments but had language classes
    html_str = re.sub(r'<code class="[^"]*">', '<code>', html_str)

    # Normalize by stripping whitespace from lines and removing empty lines
    lines = [line.strip() for line in html_str.splitlines()]
    return "\n".join(line for line in lines if line)

def run_tests():
    test_cases = [
        ("testRuby.md", "testRuby.htm"),
        ("test.md", "test.htm"),
        ("test/ruby.md", "test/ruby.htm"),
        ("test/歌詞/パレード.md", "test/歌詞/パレード.htm"),
        ("test/歌詞/白虎野の娘.md", "test/歌詞/白虎野の娘.htm"),
    ]

    print("Running regression tests...")
    failed = False

    for md_path, htm_path in test_cases:
        if not os.path.exists(md_path) or not os.path.exists(htm_path):
            print(f"[SKIP] {md_path} or {htm_path} does not exist.")
            continue

        print(f"Testing {md_path} -> {htm_path} ...", end=" ")

        with open(md_path, "r", encoding="utf-8") as f:
            md_text = f.read()
        with open(htm_path, "r", encoding="utf-8") as f:
            expected_html = f.read()

        generated_html = explain(md_text)

        norm_gen = normalize_html(generated_html)
        norm_exp = normalize_html(expected_html)

        if norm_gen == norm_exp:
            print("PASS")
        else:
            print("FAIL")
            print("--- Expected (normalized) ---")
            print(norm_exp)
            print("--- Generated (normalized) ---")
            print(norm_gen)
            print("-----------------------------")
            failed = True

    # Test code blocks and inline code protection
    print("Testing code block and inline code protection ...", end=" ")
    code_test_md = """
This is code: `{not ruby}(text)` and `~~not del~~`.

```python
# Fenced code block
def test():
    x = {ruby}(annotation)
    y = ~~strikethrough~~
```
"""
    code_gen_html = explain(code_test_md)
    if "<ruby>" in code_gen_html or "<del>" in code_gen_html:
        print("FAIL")
        print("Generated HTML containing unwanted conversion:")
        print(code_gen_html)
        failed = True
    else:
        print("PASS")

    if failed:
        sys.exit(1)
    else:
        print("All tests passed successfully!")
        sys.exit(0)

if __name__ == "__main__":
    run_tests()
