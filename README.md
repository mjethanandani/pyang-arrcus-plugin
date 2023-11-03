# A pyang plugin to validate Arrcus native YANG models.

This pyang plugin validates Arrcus device specific YANG modules per the naming conventions established within Arrcus.



```
$ pyang --arrcus arcos-aft-types.yang 
arcos-aft-types.yang:1: error: RFC 8407: 4.8: statement "module" must have a "contact" substatement
arcos-aft-types.yang:1: error: RFC 8407: 4.8: statement "module" must have a "organization" substatement
arcos-aft-types.yang:1: error: RFC 8407: 4.8: statement "module" must have a "description" substatement
arcos-aft-types.yang:1: error: RFC 8407: 4.8: statement "module" must have a "revision" substatement
arcos-aft-types.yang:6: error: RFC 8407: 4.13,4.14: statement "typedef" must have a "description" substatement
```

To build this package use the command:

`$ python setup.py sdist bdist_wheel`

To install the package locally:

`$ pip install .`

