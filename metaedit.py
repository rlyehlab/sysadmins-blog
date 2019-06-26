#!/usr/bin/env python3

import json
from datetime import datetime
from os.path import isfile, getsize
from sys import exit

# python-slugify
# https://github.com/un33k/python-slugify

# The MIT License
#
# Copyright (c) Val Neekman @ Neekware Inc. http://neekware.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# v3.0.2
# Some parts of the code have been slightly modified to fit here --hackan
import re
import unicodedata
import sys
from html.entities import name2codepoint

_unicode = str
_unicode_type = str
unichr = chr

CHAR_ENTITY_PATTERN = re.compile(r'&(%s);' % '|'.join(name2codepoint))
DECIMAL_PATTERN = re.compile(r'&#(\d+);')
HEX_PATTERN = re.compile(r'&#x([\da-fA-F]+);')
QUOTE_PATTERN = re.compile(r'[\']+')
ALLOWED_CHARS_PATTERN = re.compile(r'[^-a-z0-9]+')
ALLOWED_CHARS_PATTERN_WITH_UPPERCASE = re.compile(r'[^-a-zA-Z0-9]+')
DUPLICATE_DASH_PATTERN = re.compile(r'-{2,}')
NUMBERS_PATTERN = re.compile(r'(?<=\d),(?=\d)')
DEFAULT_SEPARATOR = '-'


def smart_truncate(string, max_length=0, word_boundary=False, separator=' ', save_order=False):
    """
    Truncate a string.
    :param string (str): string for modification
    :param max_length (int): output string length
    :param word_boundary (bool):
    :param save_order (bool): if True then word order of output string is like input string
    :param separator (str): separator between words
    :return:
    """

    string = string.strip(separator)

    if not max_length:
        return string

    if len(string) < max_length:
        return string

    if not word_boundary:
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
            separator=DEFAULT_SEPARATOR, save_order=False, stopwords=(), regex_pattern=None, lowercase=True,
            replacements=()):
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
    :param replacements (iterable): list of replacement rules e.g. [['|', 'or'], ['%', 'percent']]
    :return (str):
    """

    # user-specific replacements
    if replacements:
        for old, new in replacements:
            text = text.replace(old, new)

    # ensure text is unicode
    if not isinstance(text, _unicode_type):
        text = _unicode(text, 'utf-8', 'ignore')

    # replace quotes with dashes - pre-process
    text = QUOTE_PATTERN.sub(DEFAULT_SEPARATOR, text)

    # decode unicode
    # I removed the unidecode dependency --hackan
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

    # finalize user-specific replacements
    if replacements:
        for old, new in replacements:
            text = text.replace(old, new)

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
    today_isodate = datetime.today().date().isoformat()
    pubdate = input(
        'Publication Date [{}]: '.format(today_isodate)
    ) or today_isodate
    pubdate_parsed = ''.join(filter(lambda d: d.isdigit(), pubdate))
    id_ = '{}-{}'.format(pubdate_parsed, slugify(title)) if title else pubdate_parsed
    post_id = input('ID [{}]: '.format(id_)) or id_

    post_meta = {
        'id': post_id,
        'title': title,
        'author': author,
        'description': description,
        'publication': pubdate,
        'modification': pubdate,
    }

    print('\nPost metadata:', json.dumps(post_meta, indent=4))

    insert = input('\nInsert into posts.json file? [y/N]: ')
    if insert == 'y':
        exists = isfile('posts.json') and getsize('posts.json') > 0
        mode = 'rt+' if exists else 'w'
        with open('posts.json', mode, encoding='utf-8') as metafile:
            posts_meta = json.load(metafile) if exists else []
            metafile.seek(0)
            json.dump([post_meta] + posts_meta, metafile, indent=4,
                      ensure_ascii=False)
            metafile.truncate()
    return 0


if __name__ == '__main__':
    exit(main())
