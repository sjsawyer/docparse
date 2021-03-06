import textract
import re


class DocumentParser():
    '''
    Parser to parse the text of almost any text file type (to that of the
    extent of `textract`.

    Parameters
    ----------
    query : collections.OrderedDict
        An ordered dictionary in which the keys are the categories to parse
        the text into, and the values are either functions to apply on the
        text, or regex expressions to search for.
    delimiter : string
        A string that separates blocks of text to individually parse.
    '''
    def __init__(self, query, delimiter):
        self._query_functions = self._set_query_functions(query)
        self._compiled_query_regex = self._compile_regex(query)
        self._header = query.keys()
        # Wrap the delimiter in parentheses to keep it in the parsing
        self._delimiter = re.compile("({})".format(delimiter))

    def _compile_regex(self, query):
        '''
        Convert any regex in the query dict into compiled regex patterns.
        '''
        q_reg = {}
        for q in query.keys():
            if isinstance(query[q], basestring):
                q_reg[q] = re.compile(query[q], re.IGNORECASE)
        return q_reg

    def _set_query_functions(self, query):
        ''' Set the functions to apply on the text. '''
        q_funcs = {}
        for q in query.keys():
            if callable(query[q]):
                q_funcs[q] = query[q]
        return q_funcs

    def _parse_text(self, text):
        ''' Parse after setting the functions and regex. '''
        parsed = {}
        # Apply functions to text
        for q in self._query_functions.keys():
            parsed[q] = self._query_functions[q](text)
        _cqr = self._compiled_query_regex
        # Search text for regex
        for k in _cqr.keys():
            # pattern _cqr[k] will return None if not found
            parsed[k] = _cqr[k].search(text) is not None
        return parsed

    def parse_document(self, text_document, outfile=""):
        '''
        Apply the initialized DocumentParser to a text document.

        Parameters
        ----------
        text_document : string
            Path to the document.
        outfile : string, optional
            File which to write the parsed data. Note the data will be written
            in csv format.

        Returns
        -------
        If `outfile` specified, data will be written to it in csv format.
        Otherwise, data will be returned as a list of dictionarys.

        '''
        text = textract.process(text_document)
        # TODO: refactor as a generator using re.finditer
        text_chunks = self._delimiter.split(text)
        # append the delimiter to the beginning of each text_chunk
        text_chunks = [text_chunks[i] + text_chunks[i+1]
                       for i in xrange(1, len(text_chunks), 2)]
        parsed = []
        for text_chunk in text_chunks:
            parsed.append(self._parse_text(text_chunk))
        if not outfile:
            return parsed
        # write to outfile
        with open(outfile, 'wb') as f:
            f.write(','.join(self._header) + '\n')
            for p in parsed:
                # write key values out in the order specified by user
                f.write(",".join(map(lambda k: str(p[k]), self._header))+'\n')
        return outfile

    def __call__(self, text_document, outfile=""):
        ''' Optional call method of DocumentParser. '''
        return self.parse_document(text_document, outfile=outfile)
