dewbrick
========

Building and running the app
----------------------------

To install the right python dependencies and run the main app, use the ``run`` make target::
    $ make run

Setting your Majestic.com API key
---------------------------------

Either set the environment variable ``MAJESTIC_API_KEY`` or provide it to Make as a param::
    $ make run MAJESTIC_API_KEY=foo
