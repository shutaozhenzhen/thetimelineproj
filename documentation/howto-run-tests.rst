Run automated tests (unit tests)
================================

We like automated test. All of Timeline's automated tests can be run with a
single command::

    python3 tools/execute-specs.py

If you are working on a specific feature and only want to run a subset of the
tests, you can do it like this::

    python3 tools/execute-specs.py --only specs.Event. specs.Category.

Some tests have a bit of randomness to them. So running them multiple times
might give different results. We have a script to run the tests a number of
times in sequence::

    python3 tools/execute-specs-repeat.py

It works for a subset as well::

    python3 tools/execute-specs-repeat.py --only specs.Event. specs.Category.
