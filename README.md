py-allthesame: Are all elements in a sequence the same?
=======================================================

Today in my Reading Room (yes, the one with the porcelain seat) I was
browsing Python blogs and came across the post [Determining if all
Elements in a List are the Same in Python][determining]. This is
interesting in the number of different techniques it shows, but my
first thought, as a professional software developer, was along a
somewhat different tack: “How would I write this for a production
application?” This blog post describes my process and gives you the
code I came up with.

(By the way, it's likely that there are various things relating to
Python and its ecosystem that could be improved here. Through I've
been doing software development for a long, long time, I started
programming in Python only about half a year ago, and haven't actually
even done all that much of it yet.)


1 Git
-----

Real Developers™ always put their code in a version control system
(VCS) such as [Git]. In fact, they put _everything_ in Git, which is
why you're probably [reading this blog post from a Git repo right
now][post]. Yes, my blog posts are Git repos. You don't get much more
Real Developer™ than that.


2 Test Framework
----------------

People concerned about whether or not their code actually works also
almost invariably include a test framework and some tests. To be worthwhile,
especially if others using your code are not people you work with every
day, these should be easy to run (“Just push one button”) and not require
any special setup on the part of the developer.

I try to achieve that here (and in most of my projects) by having a
script or program named [`Test`] at the top level that takes
care of getting everything set up and running all the tests. So open
up a command line window running Bash (“Git Bash” if you're using
Windows and [Git for Windows][gitwin]) and run the script with
`./Test` if it's in your current directory or by typing the path to it
if it's not. This doesn't cover everything (you'll still need a Python
3 interpreter installed), but it covers a lot more than, “Here's a
`.py` file; good luck.” I encourage you to read it for ideas. (And
steal whatever parts of it you like.)

That said and done, someone can always come up with an environment that
breaks the most well-intended test framework developer. Hopefully it's
obvious from reading the code that if [`Test`] is failing or can't
be run for whatever, you can do your own thing to set up Pytest on
your system and just run `pytest *.py` to run the tests.

If you go back through the history of this repo by looking at the Git
logs, you'll notice that this was indeed the first thing I set up,
before I even began committing code. If your test framework is saving
you time, you should be using it from the start. If it's not, that's a
problem you should be fixing.

By the way, you'll note I'm using [Pytest] here, not the built-in
[`unittest`] framework. Pytest is so much better in so many ways that
you should never be using `unittest` at all. (And Pytest will even run
your `unittest` and `doctest` tests as well, to help you if you're
converting.)

Now that we're through all that basic setup (which actually took less
time than writing these last two sections of this post), we can move
on to the actual problem at hand.


XXX To-do
---------

* Blog post comments: file an issue! (And lets add a link to all the
  issues, including closed ones, for this project on GitHub, calling
  it “Comments.”



[Git]: https://git-scm.com/
[`Test`]: Test
[determining]: https://www.blog.pythonlibrary.org/2018/05/09/determining-if-all-elements-in-a-list-are-the-same-in-python/
[gitwin]: https://git-scm.com/download/win
[post]: https://github.com/0cjs/py-allthesame
