import shlex

from ncopa import Directive

text = """
# File: simple.conf

# Default use which iteracts with the system
user nginx;

worker_processes auto;
http {
    # default type
	default_type application/octet-stream;
}
""".strip()

print(text)
print("---")

lex = shlex.shlex(text, posix=False)
lex.commenters = ""
lex.wordchars += ".:"
comment_line = []
comment_line_number = None
for token in lex:
    print(f"line={lex.lineno}, {token=}")
    if token == "#":
        lineno = lex.lineno
        args = []
        for token in lex:
            args.append(token)
            if lex.lineno != lineno:
                break
        di = Directive("#", args)
        print(f">>> {di=}")
