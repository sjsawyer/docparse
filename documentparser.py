import textract
import re


class DocumentParser():
    ''' Parse class '''
    def __init__(self, search_regex, search_functions, delimiter, header,
                 discard=0):
        self.search_functions = search_functions
        self.delimiter = delimiter
        self.search_regex = search_regex
        self.header = header
        self.discard = discard
        # compile the user specified regex
        self._compiled_search_regex = self._create_regex(search_regex)

    def _create_regex(self, search_regex):
        '''
        convert the search_catgories dictionary into a new dictionary
        containing compiled regex patterns
        '''
        return dict(map(lambda cat: (cat, re.compile(self.search_regex[cat], re.IGNORECASE)),
                        self.search_regex))

    def _parse_text(self, text):
        parsed = {}
        for sf in self.search_functions.keys():
            res = self.search_functions[sf](text)
            parsed[sf] = res
        _csr = self._compiled_search_regex
        for k in _csr.keys():
            # pattern _csr[k] will return None if not found
            parsed[k] = True if _csr[k].search(text) else False
        return parsed

    def parse_document(self, text_document, outfile=""):
        text = textract.process(text_document)
        text_chunks = text.split(self.delimiter)
        if self.discard:
            # Throw away the first `discard` text chunks
            text_chunks = text_chunks[self.discard:]
        parsed = []
        for text_chunk in text_chunks:
            parsed.append(self._parse_text(text_chunk))
        if not outfile:
            return parsed
        # write to outfile
        with open(outfile, 'wb') as f:
            f.write(','.join(self.header) + '\n')
            for p in parsed:
                # write key values out in the order they appear in `header`
                f.write(",".join(map(lambda k: str(p[k]), self.header))+'\n')
        return outfile

    def __call__(self, text_document, outfile=""):
        ''' optional call method of DocumentParser '''
        return self.parse_document(text_document, outfile=outfile)
