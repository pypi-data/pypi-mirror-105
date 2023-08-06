==============
package_parser
==============
Python utility for parsing packages names and versions from wheel filename, sdist filenames, or setup.py files


Example
=======

Manually import py files or .pyd files

.. code-block:: python

    import package_parser

    attrs = package_parser.package_parserparse('class-property-1.0.0-py3-none-any.whl')
    assert attrs['name'] == 'class-property'
    assert attrs['version'] == '1.0.0'
