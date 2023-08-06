PyMultition
================

A Multiton Class for preventing duplicate instances based on serializing init values.

-  Free software: MIT license

Features
--------

-  Return the same instance if instanciate class with same init value 

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
