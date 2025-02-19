# ncopa

ncopa is short for nginx.conf parser. It offers a Python library for parsing an nginx.conf file.


# Usage

```python
import ncopa

with open("nginx.conf") as stream:
    content = stream.read()

directives = ncopa.parse(content)
```

`directives` is a list of `ncopa.Directive` objects.
