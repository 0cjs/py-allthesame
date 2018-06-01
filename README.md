py-allthesame: How to Write a Function in Python
================================================

Today in my Reading Room (yes, the one with the porcelain seat) I was
browsing Python blogs and came across the post [Determining if all
Elements in a List are the Same in Python][determining]. This is very
interesting in the number of different techniques it shows, and does
indeed show the power of Python (albeit somewhat undermining the
“there should be only one way to do it” idea).

But my first thought, as a professional software developer, was along
a different tack: “How would I write this for a production
application?” This blog post describes my process, focusing not much
on the function itself but instead what goes around the function: the
infrastructure that supports it and the environment in which it's
tested and run.

One note: it's likely that there are various things relating to Python
and its ecosystem that could be improved here. Through I've been doing
software development for a long, long time, I started programming in
Python only about half a year ago, and even at that haven't actually
written much code yet.


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


3 The First Test and Immutability
---------------------------------

My first concern, when looking at the wide variety of techniques
in the [original blog post][determining], was the “creative” solution
number 6 which mentioned rearranging the elements. This always makes
me nervous because if I create a list `[ 'ham', 'cheese', 'eggs' ]` and
later come back to find it's now `[ 'cheese', 'eggs', 'ham' ]`, I hate
wondering “Who Moved My Cheese?” (and trying to track down the culprit).
Python code written by non-expert Python programmers can be particularly
prone to this due to issues such as the difference between the more obvious
[`list.sort()`] and somewhat more hidden [`sorted()`] function.

So I'm going to write a simple set of initial test cases, but use
immutable [tuples] instead of mutable [lists] to make sure that
whatever function I write or call is not trying to change its
parameter:

    def test_allthesame_tuples():
        for xs in [ (), (3,), (3,3), (3,3,3), (3,3,3,3,3,3) ]:
            assert allthesame(xs) is True
        for ys in [ (3,4), (3,4,3), (3,3,3,3,3,4) ]:
            assert allthesame(ys) is False

Testing the two versions of `all_the_same()` given in section 6 against
the code above indicates that, though they build separate lists in
different orders, they fortunately don't try to mutate the original
list. It's nice to have the confidence in this that the test brings.

You'll note here that though the function is a predicate and one might
consider it reasonable to return a “truthy” or “falsy” values, I
explicitly test that it's returning `True` or `False`. This is
deliberate: we don't have any need for other return values and so why
worry about the kind of edge cases that might be triggered from
something like that? This test documents that we return only two
things and we can always change it if we decide at some point we do
want to expand the range of return values. (It's also much easier to
expand that range than contract it once you have other users out there
that might depend, perhaps unwittingly, on particular return values
outside of `True` and `False`.)

At this point you may want to try writing a version of the function,
using any of the techniques from the original blog post or something
you've thought up on your own, and run the above test against it. I'll
leave that as an exercise for the reader.


4 The Second Test: More Generalization
--------------------------------------

Especially for utility functions like this one, it's nice to make them
as general as possible. We've already seen a bit of generalization by
using a tuple in the previous section: both tuples and lists are
[sequence types]. Let's take sequence type with a greater difference than
that between tuples and lists and try that one out:

    def test_allthesame_strs():
        assert allthesame('')     is True
        assert allthesame('wwww') is True
        assert allthesame('bad')  is False

If you're an even moderately experienced Python programmer and you've
written a version of the `allthesame` function, you probably won't be
surprised to see that your function already passes this test. It's not
clear that working on strings is particularly useful, but you never
know what sort of other custom sequence types someone might come up
with.


5 The Third Test: Even More Generalization
------------------------------------------

But wait, why are we restricting ourselves to list-like things? Surely
it's perfectly reasonable to do an `allthesame` test against other
collections and data structures, such as [trees] or [hash tables] or
[bags], right? Or even something that [generates] a collection of values.

Python and its libraries already support this idea with the concept of
[iterators]. There's a standard [iteration interface] that is
supported by all sequence types and lots of other things as well, and
you may have already noticed that functions like [`all` and `any`]
take an _iterable_ rather than a list or sequence. Even the built-in
`for x in xs` construct built in to the language uses the iteration
interface.

So let's write a test that makes something quite different that can be
iterated over, a generator, and passes that to `allthesame`. To be
extra clever, let's make it never terminate because, as we'll see
below, we should still work on something that iterates forever so long
as it comes up with a different value from the first one at some
point.

    def test_allthesame_infinite():
        def intgenerator():
            '   Return a hundred or so 0s, then a hundred or so 1s, ...   '
            #   We could be more clever here but that's not what this
            #   tutorial is about.
            n = 0
            while True:
                yield int(n)
                n += 0.01

        #   And a little test of the generator for anybody who's nervous.
        #   It's infinite, but we can look at a finite slice of the output.
        assert [0, 0, 1, 1, 2, 2, 2, 3, 3, 4] \
            == list(islice(intgenerator(), 0, 500, 50))

        assert not allthesame(intgenerator())


6 Writing the Code: Getting an Iterator
---------------------------------------

We've carefully considered all sorts of things such as immutability,
generality and the Python language and standard library ecosystem, and
we've encoded our thoughts into several tests. At this point if we can
write something that passes it's likely to be fairly general and
robust. So let's finally get on with the `allthesame` function itself!
(Or get on with writing a new version, if you've already written one
against some of the tests above but it doesn't pass all of them, which
would be quite a normal way to program.)

It's going to take a sequence, a generator, or any kind of iterable
thing, so the first step is to get an iterator that will iterate
across that thing:

        def allthesame(iterable):
            iterator = iterable.__iter__()

Now this may seem a bit confusing at first: what's the difference
between an _iterable_ and an _iterator_? Well the _iterable_ is the
collection or generator of values, and an _iterator_ based on that is
what allows us to step through using the `__next__()` function, with
the _iterator_ keeping track of where we are in the sequence of values
that we are iterating through. Think of the iterator as an object that
does the same work a _for_ loop does for you. The iterator just reads
from the iterable collection without (usually) affecting it at all,
and it's quite normal to go get another fresh iterator when you want
to start going through the values again, even if you haven't finished
with the first one yet.

But what if someone passes in an _iterator_ instead of an iterable,
either through confusion or because that's all they have? No fear
here; in a clever little recursive loop an iterator itself is
iterable, and has an `__iter__()` method that returns itself.


7 Writing the Code: The Algorithm
---------------------------------

We hadn't considered too much about how the function itself will work,
so it's time now to take a moment and do some thinking about the
algorithm.

Many of the methods presented in [the original post][determining]
(remember that?) can be rather inefficient and take much longer than
necessary on some large collections of values. The problem with most
of the solutions on that page is that they examine every value in the
collection. But clearly that's not always necessary: through we have
to check every value if they're all the same, if we can find _any_ two
values that are not the same, we can immediately stop and say that the
values are not _all_ the same.

So what we're going to do is simple: take the first value and go
through the remaining ones looking for the first one that's not equal,
and, when we find it, stop right there and return `False`. If we get
through all the values and haven't found one that's not equal to the
first one, we can return `True.`

There are probably some even more efficient ways to do this in special
cases, depending on the data structure we're actually using, but the
most general version of our function can't use those. In the spirit of
avoiding premature optimization, we'll leave those cases for the
moment and think about looking at them later, if it seems worthwhile.


8 Writing the Code: The Function
--------------------------------

So here's our function, including the first couple of lines we'd
already written above:

    def allthesame(iterable):
        iterator = iterable.__iter__()
        #   We don't care exactly what value we get back if the iterator is already
        #   exhausted, since we won't be comparing it against anything anyway.
        x0 = next(iterator, None)
        for x in iterator:
            if x != x0: return False
        return True

We start by setting _x₀_ to the first value returned by the iterator,
or `None` if the iterator has no values. We then compare that to every
subsequent value, _x_ and see if we can find something that isn't
equal (our definition of “the same”). If we go through them all
without finding one, we return True.

If the iterator has no values available we don't care what value we
assign to _x₀_ since we'll never be comparing it with anything anyway.

This is basically the same solution as number 5 from [the original
post][determining] except that I don't confusingly name the iterator
`el`. (_el_ is traditional shorthand for _element_, and the iterator
is not an element, it returns elements. Things like this are important
because even a tiny chance that confusion would occur with any
invdividual variable name adds up pretty quick when you think about
how many variable names a full-time developer reads in a day.)

You'll note that the tests were careful to provide the corner cases:
no values and just one value, as well as the general case of more than
one value. You should try changing the function above around to see
what happens if you remove certain parts of it or rewrite it in a
different way.

If you look back through the Git logs, by the way, you'll see that
this isn't my first solution. I originally had something longer and
more complex that threw and caught `StopIteration` because in my
initial [study of iterators][sedoc-iter] I'd missed that `next()` has
an optional second argument. (See? I really am a beginner at Python.)
The corner cases provided by the tests made it easy to be confident
that this new version worked properly: it actually took me longer to
type the function in than to fully test it.


9 Non-termination
-----------------

You'll notice that in [`allthesame.py`] there's one test that's marked
to be skipped. Do you wonder why? Remove or comment out the
`@pytest.mark.skip` line and run the test. I'll wait.

Are you back? You've probably figured out at this point why the test
is marked as skipped because it “takes too long to run”: it actually
takes _literally forever_ to run. (Yes, the real “literally,” not the
“I just want to kinda emphasize this” literally.) Due to the
definition of our problem, we can't possibly tell (at least by
testing) if an infinite collection has any non-equal values because,
no matter how many values we look at there are always more, and one
of those might be non-equal.

This starts to head into what we call “interesting” (read: “hard”)
Problems in Computing Science, but it also shows some of the power of
Python: it can and is in fact designed to be able to deal with
infinite things when necessary, though we're responsible for providing
the techniques to deal as best we can with that in finite time.

10 The Program
--------------

As touched on above, all the code, including the tests, is in one file
in this repo: [`allthesame.py`]. This may strike some people as odd,
but so long as it's compatible with your release and delivery
mechanisms you generally want the tests as close as possible to the
code they're testing. Too many developers thing of tests as some sort
of separate thing that should be hidden away, but not only does this
not promote test-driven development (developers modifying code are
going to work only so hard to find hidden tests), but the tests
themselves, as we can see here, serve to document how the function is
supposed to behave and some of the assumptions embedded in the
function (such as working on infinite collections only when the
elements are not all the same).


11 Wrapping Up
--------------

Overall, the implementation of the function itself is probably the
least important part of the problem when your code is part of a large
system being released to others. Putting that code into a supportive
environment is the key, and once you've done that you may well rework
it or change it out (as I've already done, see section 8 above) almost
trivially.

Specific things comprising professional development practices that
we've looked at here are:

1. Using Git, even for the small stuff, and even when that stuff is
   not “code” in the traditional sense.
2. Using a test framework and, in fact, _starting_ with a test
   framework. And putting the tests close to the code.
3. Making the test framework have minimal dependencies on the
   developer's environment. Making that framework it easy and obvious
   to use (“one click” or, in this case, one command with no
   parameters necessary).
4. Using [Pytest] because it rocks. (It's not only Python's finest
   unit test framework, it's one of the nicest to use in any language.
   For dedicated TDD folks using similar “scripting” languages such
   as Ruby, it's almost a reason to switch to Python.)
5. Writing tests that use corner cases and assert behaviour about side
   effects (or lack thereof). Noting that this can make improving the
   code much, much easier.
6. Generalizing functions to make them more broadly usable, where that
   makes sense. This can also make them easier to reason about.
7. Understanding and using the _iterator_ generalization in Python.
8. Thinking about algorithmic behaviour: not just efficiency, but also
   being able to work in cases where more naïve algorithms wouldn't
   (infinite collections that do have values that differ).

Any professional Python programmer will no doubt find more things in
this post that I didn't cover and areas where things could be improved.
That's usually true of almost any code. But I hope that this post has
provided some insight into the various things a professional developer
thinks about and does even for such a simple function as this.

You're probably feeling pretty tired after reading all this, and it
must seem like this “professional” approach is a lot of work. Well, it
probably is at the start, but once these things become habits they're
very quick to do. Writing this blog post was several hours of work,
but building the Git repo, test framework, tests and the function
itself took less than twenty minutes, most of which was spent
designing the tests (in other words, understanding the function I was
trying to write).


Comments
--------

If you have a comment, please start a thread or comment on one in the
[comments section]. You'll need a GitHub account to do this.

(If you're confused because the comments section looks just like the
issues/PRs section for this repo on GitHub, that is indeed what it is.
We're all developers here and are already used to this tool for
commenting on things, so why use something else?)


Licenses
--------

No warranties are given for any of the material in this repo.

This file (`README.md`) is Copyright 2018 by Curt J. Sampson
<cjs@cynic.net> and licensed under a [Creative Commons Attribution 4.0
International License][cc-by-4.0] (CC BY 4.0). Roughly: you are free
to share (copy and redistribute in any format) and adapt (remix,
transform and build upon the material for any purpose, even
commercially), so long as you give appropriate credit, indicate if any
changes were made and do not suggest that I endorse your use of it.
Further, you may not restrict these rights from others to whom you
pass this material.

All other files in this repository (including `Test`, `activate` and
`allthesame.py`) are written by me and dedicated to the public domain:
do whatever you like with them. If you need further legal support for
this please contact me and I will help you out with a [CC0 1.0 Public
Domain Dedication][CC0-1.0] or similar.



[CC-BY-4.0]: https://creativecommons.org/licenses/by/4.0/
[CC0-1.0]: https://creativecommons.org/publicdomain/zero/1.0/
[Git]: https://git-scm.com/
[Pytest]: https://pytest.org/
[`Test`]: Test
[`all` and `any`]: https://docs.python.org/3/library/functions.html#all
[`allthesame.py`]: allthesame.py
[`list.sort()`]: https://docs.python.org/3/library/stdtypes.html#list.sort
[`sorted()`]: https://docs.python.org/3/library/functions.html#sorted
[`unittest`]: https://docs.python.org/3/library/unittest.html
[bags]: https://en.wikipedia.org/wiki/Bag_(mathematics)
[comments section]: https://github.com/0cjs/py-allthesame/issues?q=
[determining]: https://www.blog.pythonlibrary.org/2018/05/09/determining-if-all-elements-in-a-list-are-the-same-in-python/
[generates]: https://docs.python.org/3/glossary.html#term-generator
[gitwin]: https://git-scm.com/download/win
[hash tables]: https://en.wikipedia.org/wiki/Hash_table
[iteration interface]: https://docs.python.org/3/library/stdtypes.html#typeiter
[iterators]: https://docs.python.org/3/glossary.html#term-iterator
[lists]: https://docs.python.org/3/library/stdtypes.html#lists
[post]: https://github.com/0cjs/py-allthesame
[sedoc-iter]: https://github.com/0cjs/sedoc/blob/master/lang/python/iter.md
[sequence types]: https://docs.python.org/3/library/stdtypes.html#sequence-types-list-tuple-range
[trees]: https://en.wikipedia.org/wiki/Tree_(data_structure)
[tuples]: https://docs.python.org/3/library/stdtypes.html#tuples
