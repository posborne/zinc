# SVD Conversion Utility

The `svdconvert.py` script aids in the conversion of [CMSIS-SVD hardware
descriptions](http://www.keil.com/pack/doc/CMSIS/SVD/html/index.html)
to `ioregs!` register modules for use within Zinc.  This automates some
of the most tedious work required when adding support for peripherals
on various platforms.

## Install Dependencies

The svdconvert.py script has a few dependencies that need to be installed
in order for it to operate correctly.  These should be installed in a virtualenv
in order to avoid installing conflicting python libraries at the system level.
Assuming you are running an Ubuntu system or similar, you may do the following
to prepare for setting up the virtualenv:

```sh
sudo apt-get install python-virtualenv python-pip
```

To create and activate the virtualenv:

```sh
virtualenv env
source env/bin/activate
```

To install required dependencies into the virtualenv:

```sh
pip install -U -r requirements.txt
```

## Running the conversion

With your virtualenv activated, you can simply do

```sh
python svdconvert.py path/to/svd.xml
```

There are additional options available in the tool.  You can see those
by doing `svdconvert.py --help`.

## Running the tests

The SVD conversion tool has its own tests.  To run these, just run the following
with the virtualenv activated.

```sh
nosetests .
```
