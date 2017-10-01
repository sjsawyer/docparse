'''
Example of applying DocumentParser to a book.

The file '2city10.txt' can be obtained from
http://www.textfiles.com/etext/FICTION/2city10.txt.
'''

import collections
import re

# Separate by chapters
delimiter = "[IVX]+\r\n\r\n[^\r\n]+"

# Functions to apply
def get_chapter(text):
    delimiter_parsed = re.search(delimiter, text).group()
    return delimiter_parsed.split('\r\n\r\n')[0]

def get_title(text):
    delimiter_parsed = re.search(delimiter, text).group()
    return delimiter_parsed.split('\r\n\r\n')[1]

def count(word):
    def count_word(text):
        return len(re.findall(word, text))
    return count_word

def most_common_word(text):
    word_list = map(lambda x: x.lower(),
                    re.findall('\w+', text, re.IGNORECASE))
    d = {}
    for word in word_list:
        d[word] = d.get(word, 0) + 1
    most_common = ""
    occurences = 0
    omit = ['a', 'about', 'after', 'all', 'an', 'and', 'as', 'at', 'be', 'but', 'by', 'for', 'from', 'had', 'have', 'he', 'her', 'her', 'him', 'his', 'i', 'in', 'into', 'is', 'it', 'my', 'not', 'of', 'on', 'one', 'or', 'over', 's', 'said', 'she', 'so', 'that', 'the', 'their', 'them', 'there', 'they', 'this', 'to', 'up', 'was', 'were', 'what', 'which', 'will', 'with', 'would', 'you', 'your']

    for word in omit:
        d[word] = 0
    for word in word_list:
        if d[word] > occurences:
            most_common = word
            occurences = d[word]
    return most_common


query = collections.OrderedDict([
    ('chapter', get_chapter),
    ('title', get_title),
    ('color', 'red|orange|yellow|blue|green|purple|black|white'),
    ('vowel count', count('a|e|i|o|u')),
    ('word count', count('\w+')),
    ('most common word', most_common_word)
])


if __name__ == '__main__':
    from os.path import dirname, abspath
    import sys
    sys.path.append(dirname(dirname(abspath(__file__))))
    import documentparser

    DP = documentparser.DocumentParser(query, delimiter)
    DP.parse_document('2city10.txt', 'out.csv')
