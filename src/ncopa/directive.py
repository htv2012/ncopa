import dataclasses
import io
from collections.abc import Sequence


@dataclasses.dataclass()
class Directive(Sequence):
    """A nginx.conf directive, which could contain nested directives."""

    name: str
    args: list[str] = dataclasses.field(default_factory=list)
    top_comment: str = dataclasses.field(default_factory=str)
    bottom_comment: str = dataclasses.field(default_factory=str)
    children: list = dataclasses.field(default_factory=list, repr=False)

    @classmethod
    def from_list(cls, lst):
        return cls(lst[0], lst[1:])

    def __iter__(self):
        return iter(self.children)

    def __len__(self):
        return len(self.children)

    def __getitem__(self, index: int):
        return self.children[index]

    def is_comment(self) -> bool:
        return self.name == "" and self.bottom_comment != ""

    def has_top_comment(self) -> bool:
        return self.top_comment != ""

    def has_bottom_comment(self) -> bool:
        return self.bottom_comment != ""

    def is_context(self) -> bool:
        return self.children != []

    def __str__(self):
        buf = io.StringIO()
        if self.is_comment():
            buf.write(f"{self.bottom_comment}\n")


def _to_string(directive: Directive, level: int, indent: str, buf):
    """
    Helper to function to_string
    """
    buf.write(indent * level)

    # Handle stand-alone comment
    if directive.is_comment():
        buf.write(directive.bottom_comment)
        buf.write("\n")
        return

    buf.write(f"{directive.name}")
    args = " ".join(directive.args)
    if args:
        buf.write(f" {args}")

    # Handle directive without children
    if not directive.is_context():
        buf.write(";\n")
        return

    # Handle directive with children
    buf.write(" {")
    if directive.has_top_comment():
        buf.write(f" {directive.top_comment}")
    buf.write("\n")

    for child_directive in directive:
        _to_string(child_directive, level + 1, indent, buf)

    buf.write(indent * level)
    buf.write("}")
    if directive.has_bottom_comment():
        buf.write(f" {directive.bottom_comment}")
    buf.write("\n")


def to_string(directives: list[Directive], indent="    ") -> str:
    buf = io.StringIO()
    for directive in directives:
        _to_string(directive, level=0, indent=indent, buf=buf)
    with open("/tmp/out.conf", "w") as stream:
        stream.write(buf.getvalue())
    return buf.getvalue()
