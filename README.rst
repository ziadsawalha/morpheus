Morpheus |Build Status| |Coverage Status|
=========================================

Morpheus helps you define schemas for your dict-based classes and
perform validation, migration, and generate documentation. It tries to
make this normally unfun task painless and easy.

Design Goals
~~~~~~~~~~~~

**Readable.** Like a docstring at the top of your class definition, a
schema definition should be readable and understandable.

**Transparent.** You know how to work with dicts. You should be able to
keep using dicts. And you should be able to import morpheus or leave it
out and your code should still work.

**Flexible.** You get to pick which backend you use (sqlalchemy, sqlite,
NoSQL, etc...), so morpheus operates on native python dicts and doesn't
touch your data store.

Features
~~~~~~~~

-  Intuitive schema definition using pythonic idioms
-  Optional schema validation and inspection controlled globally or per
   class
-  Automatic or on-demand migration from an older schema to the current
   one
-  Generates schema documentation for developers and users
-  DRY definition of schemas. Do it once. Do it in one place. Use it
   anywhere (docs, data store, and code)
-  Zero dependencies required
-  Enable/disable it with a single line
-  Passes all python tests for a dict (including json and pickle
   serialization)
-  Painless, pain-free, simple and easy!

Install
~~~~~~~

.. code:: bash

    $ pip install morpheus

Usage
~~~~~

Here is a simple example of a schema definition on a dict-based class.

.. code:: python

    # Let's import MorpheusDict as dict in our module
    from morpheus import MorpheusDict as dict
    # Note: Comment this last line out to completely disable morpheus. No code
    # changes needed.


    #
    # Let's limit the keys allowed on our dict-based class by adding a __schema__
    # entry
    #
    class Foo(dict):
        __schema__ = ['id', 'name', 'state']

    #
    # Now let's make sure this really works
    #
    try:
        Foo(sneaky='git blame someone for this!')
    except AttributeError as exc:
        print "Thank you, Morpheus! You caught an error: %s" % exc

    # Prints:
    #
    # Thank you, Morpheus! You caught an error: 'sneaky' is not a permitted
    # attribute for a 'Foo'
    #

Here is a more involved example, demonstrating multiple schemas,
validation, and migration.

.. code:: python


    from morpheus import MorpheusDict, Schema, Defn

    class Foo(dict):
        __schema__ = Schema(
            id=Defn(int, required=True),
            statoos=basestring,
            state=as_of(0.7).is_replaced_by('statoos')
        )

    print Foo({'id': 1, 'state': 'DEPRECATED'})

    # Prints:
    #
    # {'id': 1, 'statoos': 'DEPRECATED'}
    #

    Foo({})
    # Generates ValidationError("Missing required key 'id'")

Performance
~~~~~~~~~~~

To test performance, run ``python tests/test_performance.py``

The current performance is ~14 times slower than native dict.

Versus the following implementations:

-  Simple: 1392.72517321% (from 0.0004 to 0.006)
-  Subclass: 1358.45980888% (from 0.0004 to 0.006)
-  Mapping: 439.377796719% (from 0.001 to 0.006)
-  List: 10094.0655908% (from 0.0005 to 0.05)
-  Complex: 7229.4047619% (from 0.0008 to 0.06)

Contributing
~~~~~~~~~~~~

Ziad Sawalha (ziadsawalha) is the creator and current maintainer of
Morpheus. Pull requests are always welcome.

Before submitting a pull request, please ensure you have added/updated
the appropriate tests (and that all existing tests still pass with your
changes), and that your coding style follows PEP 8 and doesn't cause
pyflakes to complain.

rst doc generated from markdown with::

::

    pandoc --from=markdown --to=rst --output=README.rst README.md

Legal
~~~~~

Copyright 2013 by Ziad Sawalha.

Licensed under the Apache License, Version 2.0 (the "License"); you may
not use this file except in compliance with the License. You may obtain
a copy of the License at

::

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

.. |Build Status| image:: https://travis-ci.org/ziadsawalha/morpheus.png
   :target: https://travis-ci.org/ziadsawalha/morpheus
.. |Coverage Status| image:: https://coveralls.io/repos/ziadsawalha/morpheus/badge.png?branch=master
   :target: https://coveralls.io/r/ziadsawalha/morpheus
