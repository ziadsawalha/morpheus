Morpheus [![Build Status](https://travis-ci.org/ziadsawalha/morpheus.png)](https://travis-ci.org/ziadsawalha/morpheus) [![Coverage Status](https://coveralls.io/repos/ziadsawalha/morpheus/badge.png?branch=master)](https://coveralls.io/r/ziadsawalha/morpheus)
========

Morpheus helps you define schemas for your dict-based classes and perform validation, migration, and generate documentation. It tries to make this normally unfun task painless and easy.

### Design Goals ###

**Readable.** Like a docstring at the top of your class definition, a schema definition should be readable and understandable.

**Transparent.** You know how to work with dicts. You should be able to keep using dicts. And you should be able to import morpheus or leave it out and your code should still work.

**Flexible.** You get to pick which backend you use (sqlalchemy, sqlite, NoSQL, etc...), so morpheus operates on native python dicts and doesn't touch your data store.

### Features ###

* Intuitive schema definition using pythonic idioms
* Optional schema validation and inspection controlled globally or per class
* Automatic or on-demand migration from an older schema to the current one
* Generates schema documentation for developers and users
* DRY definition of schemas. Do it once. Do it in one place. Use it anywhere (docs, data store, and code)
* Zero dependencies required
* Enable/disable it with a single line
* Passes all python tests for a dict (including json and pickle serialization)
* Painless, pain-free, simple and easy!

### Install ###

```bash
$ pip install morpheus
```

### Usage ###

Here is a simple example of a schema definition on a dict-based class.

```python
# Comment this line out to completely disable morpheus. No code changes needed.
from morpheus import MorpheusDict as dict


class Foo(dict):
    __schema__ = ['id', 'name', 'state']

try:
    Foo(sneaky='git blame someone for this!')
except AttributeError as exc:
    print "Thank you, Morpheus! You caught an error: %s" % exc

# Prints: Thank you, Morpheus! You caught an error: 'sneaky' is not a permitted
#         attribute for a 'Foo'
```


### Contributing ###

Ziad Sawalha (ziadsawalha) is the creator and current maintainer of Morpheus. Pull requests are always welcome.

Before submitting a pull request, please ensure you have added/updated the appropriate tests (and that all existing tests still pass with your changes), and that your coding style follows PEP 8 and doesn't cause pyflakes to complain.


### Legal ###

Copyright 2013 by Ziad Sawalha.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
