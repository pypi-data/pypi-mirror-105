# zxpy

Shell scripts made simple

> Note: Work in progress. Most of the functionality will be added pretty soon

## Installation

`pip install zxpy`

## Example

```python
#! /usr/bin/env zxpy
~'echo Hello world!'

file_count = ~'ls -1 | wc -l'

~'echo -n File count is:'
print(file_count)
```

Output:

```console
Hello world!
File count is:
9
```
