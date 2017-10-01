import re
import collections


'''
Below we define functions that are going to be executed on the text to
compute some value of interest. These function handles will then be added
to the query dictionary below.
'''


def _get_student_info(text):
    name, studient_id, full_program = text.strip().split('\n')[:3]
    year_and_program = full_program.split(',')[0]
    year, program = year_and_program.split(' ', 1)
    first = " ".join(name.split()[:-1])
    last = name.split()[-1]
    student_info = {'first': first,
                    'last': last,
                    'id':   studient_id,
                    'year': year,
                    'program': program}
    return student_info


def get_first(text):
    return _get_student_info(text)['first']


def get_last(text):
    return _get_student_info(text)['last']


def get_id(text):
    return _get_student_info(text)['id']


def get_year(text):
    return _get_student_info(text)['year']


def get_program(text):
    return _get_student_info(text)['program']


def get_avg(text):
    '''
    Get the student's average by parsing UW's Unofficial Grade Report for
    the average of each term, and averaging them.
    Term Averages of N/A will be ignored, and -1 will be returned for
    students who do not currently have an average (most likely 1A)
    '''
    term_avgs = re.findall("(?<=Term Average:)[\n]*[0-9.]+", text)
    try:
        return int(round(sum(map(float, term_avgs))/len(term_avgs)))
    except ZeroDivisionError:
        # Student does not have an average (e.g. 1A)
        return -1


query = collections.OrderedDict([
    ('last', get_last),
    ('first', get_first),
    ('id', get_id),
    ('year', get_year),
    ('program', get_program),
    ('average', get_avg),
    ('python', 'python'),
    ('machine learning', 'machine learning|neutral net|artificial intelligence'),
    ('git', 'git'),
    ('cover letter', 'rave'),
    ('music', 'music|instrument'),
    ('linux', 'linux|command line|bash'),
])

# delimiter separating cvs
delimiter = "University of Waterloo\n"\
            "Co-operative Work Terms"


if __name__ == '__main__':
    import documentparser
    import sys
    cvs = sys.argv[-2]
    outfile = sys.argv[-1]
    DP = documentparser.DocumentParser(
            query,
            delimiter,
            discard=1)

    DP.parse_document(cvs, outfile=outfile)
