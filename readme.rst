SQL Quiz
========

System combining both a friendly CLI for PostgreSQL with a quiz-like system.

Walkthrough
-----------

::

    $ pip install https://github.com/joelburton/sql-quiz.git
    $ sql_quiz --quiz sample.yaml movies
    movies # \question
      (shows question0
    movies # SELECT 7;
      (rewards with cheerful window)
    movies # \next
      (shows next question)
    ... work, struggle ...
    movies # \question
      (shows question & expected again, in we need it)
    movies # \solution
      (shows solution)
    movies # \next
      (all done, gives congrats msg)

To take a quiz and make a "closed version" (without solutions), use the
command ``\export_closed_quiz new-closed-quiz.yaml``

Todo
----

- Nothing at the moment :)
