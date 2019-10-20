..
    Copyright 2019 RoadrunnerWMC

    This file is part of ndspy.

    ndspy is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    ndspy is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with ndspy.  If not, see <https://www.gnu.org/licenses/>.

Tutorial 0: Getting Started
===========================

This "tutorial" just helps you get set up and ready to follow the other
tutorials.

Before anything else, if you don't already have Python 3.6 or newer and ndspy
installed, please see the :ref:`installation` section.

Writing a test script
---------------------

The tutorials aren't intended to be done in the interactive Python shell;
they instead demonstrate writing short script files, which is my preferred way
of getting things done with ndspy. Thus, it's a good idea to check that you're
able to do that.

Make a new Python file (say, ``test.py``), open it with with your favorite text
editor, and insert the following:

.. code-block:: python
    :linenos:

    import ndspy

    print('Hello world!')

Then try running it with the copy of Python you installed ndspy in. Your text
editor might provide a built-in way to do that, or you may need to run it from
the terminal / command prompt using a command like one of these:

.. code-block:: text

    python3 test.py

    py -3 -m test.py

If the script prints ``Hello world!`` and exits, everything's good.

.. tip::

    If you get an error like this:

    .. code-block:: text

        Traceback (most recent call last):
          File "temp.py", line 1, in <module>
            import ndspy
        ModuleNotFoundError: No module named 'ndspy'

    Then you're running a copy of Python that doesn't have ndspy installed. Try
    putting the first two digits of the version of Python you installed into
    the command instead of just ``3`` -- for example, ``python3.6 test.py``.
