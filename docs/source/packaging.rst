================
 PACKAGING
================

How to create a new version of the BIONIC TOOLS library?

- Update the version number
- Go into the root direcotry where the "setup.py" file is located
- Enter the following command:

`python3 setup.py sdist bdist_wheel`

- Then install it like a normal pip package

`sudo -H pip3 install dist/bionic_tools_pkg-1.0.1-py3-none-any.whl`

Informations from
https://packaging.python.org/tutorials/packaging-projects/

Temporary installation for development
--------------------------------------
In the main folder:

` $ sudo -H pip3 install --editable . `