import re

# TODO: combine header, assets and search functions into one
# SORTED dictionary containing either a string for regex match or
# function for a function call on the text

header = ['last', 'first', 'id', 'year', 'program', 'average', 'python',
          'machine learning', 'git', 'cover letter', 'music', 'linux']

# regex to search for
assets = {'python': 'python',
          'machine learning': 'machine learning|neutral net|artificial intelligence',
          'git': 'git',
          'cover letter': 'rave',
          'music': 'music|instrument',
          'linux': 'linux|command line|bash'}

# delimiter separating cvs
delimiter = "University of Waterloo\n"\
            "Co-operative Work Terms"


# custom functions to apply on the text
def get_avg(text):
    term_avgs = re.findall("(?<=Term Average:)[\n]*[0-9.]+", text)
    try:
        return int(round(sum(map(float, term_avgs))/len(term_avgs)))
    except ZeroDivisionError:
        # Student does not have an average (e.g. 1A)
        return -1


def get_identifiers(text):
    name, studient_id, full_program = text.strip().split('\n')[:3]
    year_and_program = full_program.split(',')[0]
    year, program = year_and_program.split(' ', 1)
    first, last = name.split(' ', 1)
    identifiers = {'first': first,
                   'last': last,
                   'id':   studient_id,
                   'year': year,
                   'program': program}
    return identifiers


def get_first(text):
    return get_identifiers(text)['first']


def get_last(text):
    return get_identifiers(text)['last']


def get_id(text):
    return get_identifiers(text)['id']


def get_year(text):
    return get_identifiers(text)['year']


def get_program(text):
    return get_identifiers(text)['program']


search_functions = {'average': get_avg,
                    'first': get_first,
                    'last': get_last,
                    'id': get_id,
                    'year': get_year,
                    'program': get_program}


if __name__ == '__main__':
    import documentparser
    import sys
    cvs = sys.argv[-1]
    DP = documentparser.DocumentParser(
            assets,
            search_functions,
            delimiter,
            header,
            discard=1)

    DP.parse_document(cvs, outfile="cvdata.csv")
