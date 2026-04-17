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
    result: str = markdown.markdown(markdownText, output_format="html")
    rubyList: list[str] = re.findall(r"\{.+?\}\(.+?\)", result)
    logging.debug(rubyList)
    for ruby in rubyList:
        rubyText: str = re.findall(r"\((.+?)\)", ruby)[0]
        rubyBase: str = re.findall(r"\{(.+?)\}", ruby)[0]
        logging.debug(f"rubyText: {rubyText}; rubyBase: {rubyBase}")
        result = result.replace(
            ruby, f"<ruby>{rubyText}<rp> (</rp><rt>{rubyBase}</rt><rp>) </rp></ruby>"
        )
    return result
