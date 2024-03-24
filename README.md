# python semantic version checking

Python Semantic Version Checker ("verger")

Basic idea:

- dump all the representation of python modules to dict (ast2dict)
- Generate checks off the AST representation

Goals:

- Make things readable
- Only use stdlib as part of the core implementation

Example Output:

```
my_module.py:3:5 Additional FunctionDef found (my_func)
```

# Influences

- `ast2json` project, where the implementation of `ast2dict` module is adapted from.
- `pycodestyle` project, I learnt a lot about structuring and CLI experience for
  generating linters off a small clean database