# TODO fix doctests, they aren't passing in python 3.4

A collection of functions for forcing strings to be in a format that I want.

These functions will throw away data to force the result they want. For example,
a "ń" might get removed from the string entirely. For this reason, they are not safe
for many use-cases.

These functions were written around the time of python 2.5, and have been
ported for use in python 3.4+. I probably should throw them away and embrace
unicode, but I have some personal code that I don't want to update so I'm
porting these.
