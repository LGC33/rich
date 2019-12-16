from __future__ import annotations

import re
from typing import List, Union


from .text import Text


class Highlighter:
    def __call__(self, text: Union[str, Text]) -> Text:
        if isinstance(text, str):
            highlight_text = Text(text)
        elif isinstance(text, Text):
            highlight_text = text
        else:
            raise TypeError(f"str or Text instance required, not {text!r}")
        return self.highlight(highlight_text)

    def highlight(self, text: Text) -> Text:
        pass


class RegexHighlighter(Highlighter):
    highlights: List[str] = []
    base_style: str = ""

    def highlight(self, text: Text) -> Text:
        str_text = str(text)
        base_style = self.base_style
        stylize = text.stylize
        for highlight in self.highlights:
            for match in re.finditer(highlight, str_text):
                for name, _value in match.groupdict().items():
                    start, end = match.span(name)
                    if start != -1:
                        stylize(start, end, f"{base_style}{name}")
        return text


class ReprHighlighter(RegexHighlighter):
    base_style = "repr."
    highlights = [
        r"(?P<brace>[\{\[\]\}])",
        r"(?P<tag_start>\<)(?P<tag_name>\w*)(?P<tag_contents>.*?)(?P<tag_end>\>)",
        r"(?P<attrib_name>\w+?)=(?P<attrib_value>\"?\w+\"?)",
        r"(?P<bool_true>True)|(?P<bool_false>False)|(?P<none>None)",
        r"(?P<number>\-?[0-9]+\.?[0-9]*)",
        r"(?P<double_str>b?\"\"\".*?\"\"\"|b?\".*?\")",
        r"(?P<single_str>b?\'\'\'.*?\'\'\'|b?\'.*?\')",
    ]


if __name__ == "__main__":
    from .console import Console

    console = Console()

    highlighter = ReprHighlighter()

    console.print(
        highlighter(
            '''"""hello True""" print("foo", egg=5) <div class=foo bar=4>  <div class="foo"> [1, 2, 3,4] a=None qwewe True False'''
        )
    )

    from .default_styles import MARKDOWN_STYLES
    from pprint import PrettyPrinter

    pp = PrettyPrinter(indent=4, compact=False)

    # console.print(highlighter(pp.pformat(MARKDOWN_STYLES)))

    t = Text('''"""hello True""" <div class=foo>''')

    t.stylize(9, 13, "bold")

    t.stylize(0, 16, "red not bold nomerge")

    console.print(t)