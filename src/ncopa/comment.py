import shlex

text = """
# test.py
foo bar;
one two three;
#More comment
""".strip()

lex = shlex.shlex(text, posix=False)
lex.commenters = ""
lex.wordchars += "."
comment_line = []
comment_line_number = None
for token in lex:
    print(f"line={lex.lineno}, {token=}")
    if token == "#":
        comment_line = [token]
        comment_line_number = lex.lineno
        for token in lex:
            comment_line.append(token)
            if lex.lineno > comment_line_number:
                break
        print(f"{comment_line=}")
        print(f"{comment_line_number=}")
        print("---")
