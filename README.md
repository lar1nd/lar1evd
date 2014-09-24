lar1evd: LAr1-ND event display
==============================

**LAR1EVD IS CURRENTLY IN ITS ALPHA TESTING STAGE**

LAr1-ND code: https://cdcvs.fnal.gov/redmine/projects/lar1ndcode/wiki

Requirements
------------

- A computer

Dependencies
------------

lar1evd is written in C++ and Python 2.7, and depends on the following
libraries

- [ROOT 5.34][root]
- [Qt 4.8][qt]
- [NumPy][numpy]
- [matplotlib][matplotlib]
- [SciPy][scipy]
- [PyQt4][pyqt] or [PySide][pyside]
- [pyqtgraph][pyqtgraph]

All of these dependencies are already installed on the lar1nd gpvm
interactive nodes. To set them up, run the command

    $ source /lar1nd/app/lar1evd/setup.sh

Getting the dependencies installed
----------------------------------

[ Maybe this section would be more suitable on a wiki page. ]

### On Mac OS X 10.8+

For users who are running Mac OS X, it is highly recommended that you
install one of the following package managers as it will make the
installation of the dependencies a breeze

- [Homebrew][homebrew]
- [MacPorts][macports]

Homebrew will be used in the instructions that follow. The procedure
should be similar in MacPorts (Corey, could you verify and update this
README?). This guide assumes that Homebrew is set up correctly and is
ready to be used.

First, we should run the following commands to add additional repos to
`brew`

    $ brew tap homebrew/python
    $ brew tap homebrew/science

To avoid using the system-installed version of Python in OS X, we will
have to install a separate version of Python using `brew`. The reason
for doing this is that the Python libraries that we need will be much,
much easier to install. To install Python, simply run the following
command:

    $ brew install python

Once Python is installed, `brew` will print out a block of text labeled
**Caveats** which provides some important information about the recently
installed package. Pay close attention to these!

Next we will install ROOT. Again, read the **Caveats** section
carefully!

    $ brew install root

Once ROOT is installed, we should verify that PyROOT is working with
Python. To do this, start up the `python` interpreter and try importing
ROOT with

    >>> import ROOT

If Python does not complain, then PyROOT is working as expected. The
next things we want to install are Qt4 and PyQt4

    $ brew install qt4
    $ brew install pyqt4

And then the rest are just Python libraries

    $ brew install numpy
    $ brew install matplotlib
    $ brew install scipy
    $ pip install pyopengl
    $ pip install pyqtgraph

Super quick summary

1. `brew tap homebrew/python`
2. `brew tap homebrew/science`
3. `brew install python`
4. `brew install root`
5. `brew install qt4`
6. `brew install pyqt4`
7. `brew install numpy`
8. `brew install matplotlib`
9. `brew install scipy`
10. `pip install pyopengl`
11. `pip install pyqtgraph`

### Other operating systems

Instructions on how to install the dependencies on other operation
systems will soon follow. Hooray for `apt-get` and `yum`!

[root]:http://root.cern.ch
[qt]:https://qt-project.org
[numpy]:http://numpy.org
[matplotlib]:http://matplotlib.org
[scipy]:http://scipy.org
[pyqt]:http://riverbankcomputing.com/software/pyqt
[pyside]:http://qt-project.org/wiki/PySide
[pyqtgraph]:http://pyqtgraph.org
[homebrew]:http://brew.sh
[macports]:https://macports.org
