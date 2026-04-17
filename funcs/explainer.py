"""
RubyMark explainer
"""

import re
import logging
import markdown


def explain(markdownText: str) -> str:
    """explain markdown file

    Args:
        markdownText (str): markdown text input

    Returns:
        str: html text output
    """
    result: str = markdown.markdown(
        markdownText,
        output_format="html",
        extensions=[
            "extra",
            "tables",
            "toc",
            "fenced_code",
            "nl2br",
            "sane_lists",
            "codehilite",
            "meta",
        ],
    )

    rubyList: list[str] = re.findall(r"\{.+?\}\(.+?\)", result)
    logging.debug(rubyList)
    for ruby in rubyList:
        rubyText: str = re.findall(r"\((.+?)\)", ruby)[0]
        rubyBase: str = re.findall(r"\{(.+?)\}", ruby)[0]
        logging.debug(f"rubyText: {rubyText}; rubyBase: {rubyBase}")
        result = result.replace(
            ruby, f"<ruby>{rubyBase}<rp> (</rp><rt>{rubyText}</rt><rp>) </rp></ruby>"
        )

    delList: list[str] = re.findall(r"~~.+?~~", result)
    for delBlock in delList:
        result = result.replace(delBlock, f"<del>{delBlock[2:-2]}</del>")

    return result
