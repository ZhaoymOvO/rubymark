"""
RubyMark explainer
"""

import xml.etree.ElementTree as ET

import markdown
from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor


class RubyInlineProcessor(InlineProcessor):
    """
    Processes {base}(text) into:
    <ruby>base<rp> (</rp><rt>text</rt><rp>) </rp></ruby>
    """
    def handleMatch(self, m, data):
        ruby_base = m.group('base')
        ruby_text = m.group('text')

        ruby = ET.Element('ruby')
        ruby.text = ruby_base

        rp1 = ET.SubElement(ruby, 'rp')
        rp1.text = ' ('

        rt = ET.SubElement(ruby, 'rt')
        rt.text = ruby_text

        rp2 = ET.SubElement(ruby, 'rp')
        rp2.text = ') '

        return ruby, m.start(0), m.end(0)


class DelInlineProcessor(InlineProcessor):
    """
    Processes ~~text~~ into:
    <del>text</del>
    """
    def handleMatch(self, m, data):
        el = ET.Element('del')
        el.text = m.group('text')
        return el, m.start(0), m.end(0)


class RubyMarkExtension(Extension):
    """
    Python-Markdown Extension for RubyMark syntax
    """
    def extendMarkdown(self, md):
        # We match {base}(text) where base has no curly braces, text has no closing parenthesis
        ruby_pattern = r'\{(?P<base>[^{}]+)\}\((?P<text>[^)]+)\)'
        # We match ~~text~~ where text has no tildes (non-greedy)
        del_pattern = r'~~(?P<text>.+?)~~'

        md.inlinePatterns.register(RubyInlineProcessor(ruby_pattern, md), 'rubymark', 175)
        md.inlinePatterns.register(DelInlineProcessor(del_pattern, md), 'delmark', 176)


def explain(markdown_text: str) -> str:
    """Explain markdown text

    Args:
        markdown_text (str): markdown text input

    Returns:
        str: html text output
    """
    result: str = markdown.markdown(
        markdown_text,
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
            RubyMarkExtension(),
        ],
    )

    return result
