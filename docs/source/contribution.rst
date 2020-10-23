*************
CONTRIBUTION
*************

Release
************

How to create a new release of the phand_python_libs?

- Update the version number
- Go into the root direcotry where the "setup.py" file is located
- | Enter the following command 
  | ``python3 setup.py sdist bdist_wheel``
- | Then install it like a normal pip package
  | ``sudo -H pip3 install dist/bionic_tools_pkg-1.0.1-py3-none-any.whl``

Informations from
https://packaging.python.org/tutorials/packaging-projects/

Development
*************

**Temporary installation for development**

In the main folder:

``sudo -H pip3 install --editable .``

This enables to directly update and use the in the library without the need to everytime build the package and install it.