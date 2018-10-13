#!/usr/bin/env python3

import json
from datetime import datetime
from sys import exit
from os.path import isfile, getsize
# python-slugify
# by Val Neekman @ Neekware Inc. [@vneekman]
# v1.2.6
# https://github.com/un33k/python-slugify
import re
import unicodedata
import types
import sys

try:
    from htmlentitydefs import name2codepoint
    _unicode = unicode
    _unicode_type = types.UnicodeType
except ImportError:
    from html.entities import name2codepoint
    _unicode = str
    _unicode_type = str
    unichr = chr

# try:
#     import unidecode
# except ImportError:
#     import text_unidecode as unidecode

CHAR_ENTITY_PATTERN = re.compile('&(%s);' % '|'.join(name2codepoint))
DECIMAL_PATTERN = re.compile('&#(\d+);')
HEX_PATTERN = re.compile('&#x([\da-fA-F]+);')
QUOTE_PATTERN = re.compile(r'[\']+')
ALLOWED_CHARS_PATTERN = re.compile(r'[^-a-z0-9]+')
ALLOWED_CHARS_PATTERN_WITH_UPPERCASE = re.compile(r'[^-a-zA-Z0-9]+')
DUPLICATE_DASH_PATTERN = re.compile('-{2,}')
NUMBERS_PATTERN = re.compile('(?<=\d),(?=\d)')
DEFAULT_SEPARATOR = '-'


def smart_truncate(string, max_length=0, word_boundaries=False, separator=' ', save_order=False):
    """
    Truncate a string.
    :param string (str): string for modification
    :param max_length (int): output string length
    :param word_boundaries (bool):
    :param save_order (bool): if True then word order of output string is like input string
    :param separator (str): separator between words
    :return:
    """

    string = string.strip(separator)

    if not max_length:
        return string

    if len(string) < max_length:
        return string

    if not word_boundaries:
        return string[:max_length].strip(separator)

    if separator not in string:
        return string[:max_length]

    truncated = ''
    for word in string.split(separator):
        if word:
            next_len = len(truncated) + len(word)
            if next_len < max_length:
                truncated += '{0}{1}'.format(word, separator)
            elif next_len == max_length:
                truncated += '{0}'.format(word)
                break
            else:
                if save_order:
                    break
    if not truncated: # pragma: no cover
        truncated = string[:max_length]
    return truncated.strip(separator)


def slugify(text, entities=True, decimal=True, hexadecimal=True, max_length=0, word_boundary=False,
            separator=DEFAULT_SEPARATOR, save_order=False, stopwords=(), regex_pattern=None, lowercase=True):
    """
    Make a slug from the given text.
    :param text (str): initial text
    :param entities (bool):
    :param decimal (bool):
    :param hexadecimal (bool):
    :param max_length (int): output string length
    :param word_boundary (bool):
    :param save_order (bool): if parameter is True and max_length > 0 return whole words in the initial order
    :param separator (str): separator between words
    :param stopwords (iterable): words to discount
    :param regex_pattern (str): regex pattern for allowed characters
    :param lowercase (bool): activate case sensitivity by setting it to False
    :return (str):
    """

    # ensure text is unicode
    if not isinstance(text, _unicode_type):
        text = _unicode(text, 'utf-8', 'ignore')

    # replace quotes with dashes - pre-process
    text = QUOTE_PATTERN.sub(DEFAULT_SEPARATOR, text)

    # decode unicode
    # text = unidecode.unidecode(text)
    # I removed the unidecode dependency
    text = ''.join([char if ord(char) < 128 else '_' for char in text])

    # ensure text is still in unicode
    if not isinstance(text, _unicode_type):
        text = _unicode(text, 'utf-8', 'ignore')

    # character entity reference
    if entities:
        text = CHAR_ENTITY_PATTERN.sub(lambda m: unichr(name2codepoint[m.group(1)]), text)

    # decimal character reference
    if decimal:
        try:
            text = DECIMAL_PATTERN.sub(lambda m: unichr(int(m.group(1))), text)
        except Exception:
            pass

    # hexadecimal character reference
    if hexadecimal:
        try:
            text = HEX_PATTERN.sub(lambda m: unichr(int(m.group(1), 16)), text)
        except Exception:
            pass

    # translate
    text = unicodedata.normalize('NFKD', text)
    if sys.version_info < (3,):
        text = text.encode('ascii', 'ignore')

    # make the text lowercase (optional)
    if lowercase:
        text = text.lower()

    # remove generated quotes -- post-process
    text = QUOTE_PATTERN.sub('', text)

    # cleanup numbers
    text = NUMBERS_PATTERN.sub('', text)

    # replace all other unwanted characters
    if lowercase:
        pattern = regex_pattern or ALLOWED_CHARS_PATTERN
    else:
        pattern = regex_pattern or ALLOWED_CHARS_PATTERN_WITH_UPPERCASE
    text = re.sub(pattern, DEFAULT_SEPARATOR, text)

    # remove redundant
    text = DUPLICATE_DASH_PATTERN.sub(DEFAULT_SEPARATOR, text).strip(DEFAULT_SEPARATOR)

    # remove stopwords
    if stopwords:
        if lowercase:
            stopwords_lower = [s.lower() for s in stopwords]
            words = [w for w in text.split(DEFAULT_SEPARATOR) if w not in stopwords_lower]
        else:
            words = [w for w in text.split(DEFAULT_SEPARATOR) if w not in stopwords]
        text = DEFAULT_SEPARATOR.join(words)

    # smart truncate if requested
    if max_length > 0:
        text = smart_truncate(text, max_length, word_boundary, DEFAULT_SEPARATOR, save_order)

    if separator != DEFAULT_SEPARATOR:
        text = text.replace(DEFAULT_SEPARATOR, separator)

    return text
# //


def main():
    title = input('Title: ')
    author = input('Author: ')
    description = input('Description: ')
    today = datetime.now()
    today_str = '{}-{}-{}'.format(today.year, today.month, today.day)
    publication = input(
        'Publication Date [{}]: '.format(today_str)
    ) or today_str
    id_ = ''.join([d if d.isdigit() else '' for d in publication])
    id_ += '-' + slugify(title) if title else ''
    postid = input('ID [{}]: '.format(id_)) or id_

    postmeta = {
        'id': postid,
        'title': title,
        'author': author,
        'description': description,
        'publication': publication,
        'modification': publication,
    }

    print('\nPost metadata:')
    print(json.dumps(postmeta, indent=4))

    insert = input('\nInsert into posts.json file? [y/N]: ')
    if insert == 'y':
        exists = isfile('posts.json') and getsize('posts.json') > 0
        mode = 'rt+' if exists else 'w'
        with open('posts.json', mode, encoding='utf-8') as metafile:
            postsmeta = json.load(metafile) if exists else []
            metafile.seek(0)
            json.dump([postmeta] + postsmeta, metafile, indent=4,
                      ensure_ascii=False)
            metafile.truncate()
    return 0


if __name__ == '__main__':
    exit(main())
