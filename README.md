# python semantic version checking

Python Semantic Version Checker ("verge")

Basic idea:

- dump all the representation of python modules to json (ast2json)
- Generate unit tests off the modules from the json file
- Run the unit tests

Make things readable