import itertools
import re
import html.entities

from django.utils import encoding
from importlib import import_module


def convert_dict_to_ascii(x):
    """
    >>> convert_dict_to_ascii({'a':u'ni\xf1era'})
    {'a': 'niera'}

    >>> convert_dict_to_ascii({u'ni\xf1era': 'a'})
    {'niera': 'a'}
    """
    return dict([
        (convert_unicode_to_string(y[0]), convert_unicode_to_string(y[1]))
        for y in x.items()])


def convert_unicode_to_string(x):
    """
    >>> convert_unicode_to_string(u'ni\xf1era')
    'niera'
    """
    return encoding.smart_str(x, encoding='ascii', errors='ignore')


def remove_null_bytes(x):
    return x.replace('\x00', '')


def convert_dict_to_utf8(x):
    return dict([
    (convert_unicode_to_utf8(y[0]), convert_unicode_to_utf8(y[1]))
    for y in x.items()])


def convert_unicode_to_utf8(x):
    return encoding.smart_str(x, encoding='utf-8', errors='ignore')


def html_unescape(text):
    """Removes HTML or XML character references and entities from a text string.

    @param text The HTML (or XML) source text.
    @return The plain text, as a Unicode string, if necessary.

    >>> html_unescape("Jack &amp; Jill")
    'Jack & Jill'
    """
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return chr(int(text[3:-1], 16))
                else:
                    return chr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = chr(html.entities.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)


def make_random_string(minlength=12,maxlength=18):
    import io, random
    alpha = '' + \
          ''.join([chr(x) for x in range(ord('a'),ord('z')+1)]) + \
          ''.join([chr(x) for x in range(ord('A'),ord('Z')+1)]) + \
          ''.join([str(x) for x in range(0,10)])
    res = ''
    res = io.StringIO()
    for i in range(random.randint(minlength, maxlength)):
        res.write(random.choice(alpha))
    res.seek(0)
    return res.read()


def split_long_words(words, length=45):
    """Adds spaces to long words

    >>> split_long_words("in the beginning there won't be enough "
    ...                  "amateurs so pro models will win and it "
    ...                  "will be an easy $20")
    "in the beginning there won't be enough amateurs so pro models will win and it will be an easy $20"
    """
    parts = []
    for word in words.split(' '):
        parts.append(split_long_word(word))
    return ' '.join(itertools.chain(*parts))


def split_long_word(word, length=45):
    return (word[n:n+length] for n in range(0, len(word), length))


def string_to_symbol(str):
    parts = str.split('.')
    module = import_module('.'.join(parts[:-1]))
    return getattr(module, parts[-1])


if __name__ == '__main__':
    import doctest
    print("Running doctest . . .")
    doctest.testmod()