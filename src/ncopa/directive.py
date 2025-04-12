import dataclasses
from collections.abc import Sequence
import io

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
        return self.name == "" and self.bottom_comment
    
    def __str__(self):
        buf = io.StringIO()
        if self.is_comment():
            buf.write(f"{self.bottom_comment}\n")
        


def to_string(directive: Directive) -> str:
    pass