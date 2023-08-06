PyMultition
========

|pypi| |travis| |docs|

A Multiton Class for preventing duplicate instances based on serializing init values.

-  Free software: MIT license

Features
--------

-  Instanciate a class again and get the first instance with the same value back.

Quickstart
----------
.. code-block:: python

    import PyMultition
    
    
    class Test:
        def __init__(self, attr):
            self.attr = attr
    
    
    a = PyMultition.MultitionInstanceFactory.get_instance(Test, '1')
    b = PyMultition.MultitionInstanceFactory.get_instance(Test, '2')
    c = PyMultition.MultitionInstanceFactory.get_instance(Test, '2')
    assert(a is not b)
    assert(b is c)


Credits
-------

This package was created with `Cookiecutter`_ and the
`udreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _udreyr/cookiecutter-pypackage: https://github.com/audreyr/cookiecutter-pypackage

.. |pypi| image:: https://img.shields.io/pypi/v/multiton.svg
   :target: https://pypi.python.org/pypi/multiton
.. |travis| image:: https://img.shields.io/travis/laundmo/multiton.svg
   :target: https://travis-ci.com/laundmo/multiton
.. |docs| image:: https://readthedocs.org/projects/multiton/badge/?version=latest
   :target: https://multiton.readthedocs.io/en/latest/?badge=latest