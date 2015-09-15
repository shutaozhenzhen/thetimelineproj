Guidlines
=========

How to write a problem description
----------------------------------

* Write brief description of the problem in ticket title
* Write an extended description in the ticket text (not all the below items
  need to be entered)

    * Elaborate the description
    * Describe similar problems
    * Attach a screenshot illustrating the problem
    * Motivate why this problem is important to solve

* Add suggested solutions in comments to the ticket using the following
  syntax::

    **Suggested solution**: ...

Code style
----------

We try to follow PEP 8 with some exceptions: https://www.python.org/dev/peps/pep-0008/

Exceptions:

* We allow longer lines than 79 characters. But preferably not longer than 120
* We prefer to have double quoted strings

How to write tests
------------------

The idea of having a guideline for how to write tests is that if they all look
the same, they are easier to understand.

Here are the guidelines:

* All test classes should inherit a custom test case class
