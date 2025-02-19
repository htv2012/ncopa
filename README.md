# ncopa

ncopa is short for **n**ginx.**co**nf **pa**rser. It offers a Python library for parsing an nginx.conf file.


# Install

```bash
pip install ncopa
```


# Usage

```python
import ncopa

with open("nginx.conf") as stream:
    content = stream.read()

directives = ncopa.parse(content)
```

`directives` is a list of `ncopa.Directive` objects.


# The `ntree` Command

This package provides the `ntree` command which summarizes a nginx.conf directives in a tree format. 
To use it:

```bash
ntree <path to nginx.conf>
```
