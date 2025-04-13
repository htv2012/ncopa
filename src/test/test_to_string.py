import pytest

from ncopa import parse, to_string


@pytest.mark.parametrize(
    ["infile", "outfile"],
    [
        pytest.param(
            "src/test/data/poor_format.conf",
            "src/test/data/formatted.conf",
            id="poor_format",
        ),
        pytest.param(
            "src/test/data/with_blank_lines.conf",
            "src/test/data/without_blank_lines.conf",
            id="remove_blank_lines",
        ),
    ],
)
def test_format(infile, outfile):
    with open(infile, "r") as stream:
        content = stream.read()
    directives = parse(content)
    actual = to_string(directives)

    with open(outfile, "r") as stream:
        expected = stream.read()

    assert actual == expected
