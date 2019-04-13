# DjangoGoat

An intentionally vulnerable Django app, to help Django developers learn
security testing.

There are two main branches in this repo: `master` and `broken`.

The `master` branch shouldn't contain many vulnerabilities, and the `broken`
branch should contain some. If you look at the commit history of the `broken`
branch, you'll see vulnerabilities introduced into it one commit at a time.
This should help you understand what each vulnerability looks like, and how to
fix it.


## Getting started

### Install ZAP

Mac users: please ensure you've enabled installing applications from 
unidentified developers. You can find how to do this [here](https://www.mcvsd.org/tips/powerteacher/osx_unidentified_developers.html).

Installation options are here:
https://github.com/zaproxy/zaproxy/wiki/Downloads

Installation with `snap` seems to be straightforward::

    $ snap install zaproxy --classic

### Install Python packages

Make a virtualenv::

    $ mkvirtualenv --python=`which python3` djangogoat

Install the requirements::

    $ cd /path/to/djangogoat
    $ pip install -r requirements_app.txt
    $ pip install -r requirements_tests.txt

### Start the app

Initialise the database::

    $ ./manage.py migrate

Collect static files and then start the server::

    $ ./manage.py collectstatic
    $ gunicorn --certfile=dg-server.crt --keyfile=dg-server.key djangogoat.wsgi

Remember to restart `gunicorn` after you switch branches in this repo, or after
you make any changes to the app's code.

### Start testing it

Please make sure you use `https://localhost:8000` for the connection. Otherwise a 400
error might occur.

If you're on the `master` branch, you should see no ZAP alerts when you run the
tests.

If you're on the `broken` branch, you should see ZAP alerts.

Open a new terminal window, and then run the tests::

    $ cd /path/to/djangogoat
    $ workon djangogoat
    $ behave

Note that every time you restart the tests the database is flushed.


## Contributing

Developers and security people are encouraged to contribute to this project.

How can you get involved?
 - Look at our open issues, and work on one of those.
 - Submit an issue if there's a change you'd like to say, or a bug you've found.
 - Give us a PR if you find any typos, inconsistencies or spelling mistakes.

Guide to contributions:
 - Please make sure you branch from the right place. `master` should be your
   starting point for any security, documentation, or testing improvements.
   `broken` is the starting point for adding new vulnerabilities.
   The correct branch will be mentioned in the ticket.

 - We don't currently have our own code of conduct, but for the meantime, all
   contributors should follow the Django Project code of conduct, found here:
   https://www.djangoproject.com/conduct/
