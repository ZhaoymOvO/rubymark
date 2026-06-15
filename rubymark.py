#!/usr/bin/env python3
"""
RubyMark main entry point
"""

import argparse
import logging
import os
import sys

import coloredlogs

from funcs.explainer import explain

parser = argparse.ArgumentParser(
    description="RubyMark，支持 Ruby 旁註（振假名/注音）的 Markdown 轉換工具"
)
parser.add_argument("-f", "--file", help="輸入檔案")
parser.add_argument("-o", "--output", help="輸出檔案，預設為標準輸出 (stdout)")
parser.add_argument("--verbose", action="store_true", help="輸出詳細資訊")
args = parser.parse_args()


def check_input_file(filepath: str) -> None:
    """檢查輸入檔案是否可用"""
    if not os.path.exists(filepath):
        logging.critical(f"錯誤：輸入檔案不存在 '{filepath}'")
        sys.exit(1)
    if os.path.isdir(filepath):
        logging.critical(f"錯誤：輸入路徑是目錄而非檔案 '{filepath}'")
        sys.exit(1)
    if not os.access(filepath, os.R_OK):
        logging.critical(f"錯誤：沒有權限讀取輸入檔案 '{filepath}'")
        sys.exit(1)


def check_output_file(filepath: str) -> None:
    """檢查輸出路徑是否可用"""
    if os.path.isdir(filepath):
        logging.critical(f"錯誤：輸出路徑是目錄，無法作為檔案寫入 '{filepath}'")
        sys.exit(1)

    parent_dir = os.path.dirname(filepath)
    if parent_dir and not os.path.exists(parent_dir):
        logging.critical(f"錯誤：輸出路徑的父目錄不存在 '{parent_dir}'")
        sys.exit(1)

    if os.path.exists(filepath):
        if not os.access(filepath, os.W_OK):
            logging.critical(f"錯誤：沒有權限寫入輸出檔案 '{filepath}'")
            sys.exit(1)
    else:
        check_dir = parent_dir if parent_dir else "."
        if not os.access(check_dir, os.W_OK):
            logging.critical(f"錯誤：沒有權限在目錄中建立輸出檔案 '{check_dir}'")
            sys.exit(1)


if __name__ == "__main__":
    if args.verbose:
        coloredlogs.install(level="DEBUG")
    else:
        coloredlogs.install(level="WARNING")

    if not args.file:
        logging.critical("必須指定 --file 參數")
        parser.print_help()
        sys.exit(1)

    # 執行檔案與路徑檢查
    check_input_file(args.file)
    if args.output:
        check_output_file(args.output)

    # 讀取輸入檔案
    try:
        with open(args.file, encoding="utf-8") as file:
            text: str = "".join(file.readlines())
    except Exception as e:
        logging.critical(f"讀取輸入檔案時發生錯誤: {e}")
        sys.exit(1)

    # 解析並輸出
    try:
        html_content = explain(text)
    except Exception as e:
        logging.critical(f"解析 Markdown 時發生錯誤: {e}")
        sys.exit(1)

    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as file:
                file.write(html_content)
        except Exception as e:
            logging.critical(f"寫入輸出檔案時發生錯誤: {e}")
            sys.exit(1)
    else:
        print(html_content)
