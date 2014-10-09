lar1evd: LAr1-ND event display
==============================

**LAR1EVD IS CURRENTLY IN ITS ALPHA TESTING STAGES**

LAr1-ND code: https://cdcvs.fnal.gov/redmine/projects/lar1ndcode/wiki

Requirements
------------

- A computer

Dependencies
------------

lar1evd is written in C++, Python 2.7 and [Cython][cython], and depends
on the following libraries

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

The first thing we should do is run `brew update` and `brew doctor`, and
make sure that we have the appropriate version of Xcode and Command Line
Tools installed.

Second, we should run the following commands to add additional repos to
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

And then the rest are just Python packages

    $ brew install numpy
    $ brew install matplotlib
    $ brew install scipy
    $ pip install pyopengl
    $ pip install pyqtgraph
    $ pip install cython

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
12. `pip install cython`

### Other operating systems

Instructions on how to install the dependencies on other operation
systems will soon follow. Hooray for `apt-get` and `yum`!

Building the code
-----------------

First, clone the repository onto your computer

    $ git clone https://github.com/lar1nd/lar1evd.git

To build the code, run the following commands

    $ cd lar1evd/src/python
    $ cython --cplus --fast-fail --line-directives dispatch.pyx
    $ python setup.py build_ext --inplace
    $ rm -rf build dispatch.cpp

Alternatively, you could use the provided Bash scripts

    $ cd lar1evd/src/python
    $ bash build.sh && bash clean.sh

You should end up with a shared object file named `dispatch.so` in your
working directory.

Running the event display
-------------------------

To run the event display in its current (messy) state

    $ ./view2d.py [path to LArSoft-generated ROOT file] --entry [entry number]

for the 2D view. For the 3D view

    $ ./view3d.py [path to LArSoft-generated ROOT file] --entry [entry number]

Currently, the event display does not have the ability to scroll through
the entries. This will be implemented sometime in the near future.

### The 2D view

The event display is interactive, and you should be able to zoom in and
out using the scroll wheel of your mouse (or trackpad scrolling). You
can also use left-click for panning the view. To reset the view,
right-click and select "View All" from the pop-up menu.

#### matplotlib backend

You can also use matplotlib as the backend for the 2D view

    $ ./matplotlib_view2d.py [path to LArSoft-generated ROOT file] --entry [entry number]

The image quality of matplotlib is higher than pyqtgraph (used in the
the normal 2D event display), but pyqtgraph is faster for displaying
interactive elements. If you want to use an image from the 2D view for
a presentation, I would suggest using matplotlib to export the image
as a PDF file!

I plan to have an 'export to PDF' option in the main 2D event display
in the future where it will use matplotlib to perform the export.

### The 3D view

You can use the scroll wheel to zoom in and out, the left-click to
rotate the view, and the scroll wheel button (MOUSE3, press down and
hold) to pan the view (change the center of where the camera is
pointed).


[root]:http://root.cern.ch
[qt]:https://qt-project.org
[numpy]:http://numpy.org
[matplotlib]:http://matplotlib.org
[scipy]:http://scipy.org
[pyqt]:http://riverbankcomputing.com/software/pyqt
[pyside]:http://qt-project.org/wiki/PySide
[pyqtgraph]:http://pyqtgraph.org
[cython]:http://cython.org
[homebrew]:http://brew.sh
[macports]:https://macports.org
