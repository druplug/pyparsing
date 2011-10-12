from pyparsing import *

# define an expression for the body of a line of text - use a parse action to reject any
# empty lines
def mustBeNonBlank(s,l,t):
    if not t[0]:
        raise ParseException(s,l,"line body can't be empty")
lineBody = SkipTo(lineEnd).setParseAction(mustBeNonBlank)

# now define a line with a trailing lineEnd, to be replaced with a space character
textLine = lineBody + Suppress(lineEnd).setParseAction(replaceWith(" "))

# define a paragraph, with a separating lineEnd, to be replaced with a double newline
para = OneOrMore(textLine) + Suppress(lineEnd).setParseAction(replaceWith("\n\n"))


# run a test
test = """
    Now is the
    time for
    all
    good men
    to come to

    the aid of their
    country.
"""
print para.transformString(test)

# process an entire file
# z = para.transformString(file("Successful Methods of Public Speaking.txt").read())
# file("Successful Methods of Public Speaking(2).txt","w").write(z)

