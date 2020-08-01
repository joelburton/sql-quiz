SQL Quiz
========

WIP.

Walkthrough
-----------

::

    $ python main.py movies
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


Todo
----

- Finish main app

- Figure out a nice way to deal with annoying colorization of headers

- Subclass to get "open quiz" (ie, they can see answers) and "closed quiz" (no answers).
  Obviously, for closed quiz, we'll need a way for it to have the expected output in the
  json on load, rather than the sql that can created the expected output.

