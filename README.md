# docparse

docparse can be used to split a text document into multiple subsets and examine
each subset for a set of words, so long as there is some kind of delimiter
between the subsets.

docparse was originally developed to search through one large pdf containing
many resumes, looking for keywords of interest.

## Setup

### Ubuntu/Debian

docparse requires [textract](http://textract.readthedocs.io/en/latest/installation.html), and so you must first install its dependencies.

  apt-get install python-dev libxml2-dev libxslt1-dev antiword unrtf \
      poppler-utils pstotext tesseract-ocr flac ffmpeg lame libmad0 \
      libsox-fmt-mp3 sox libjpeg-dev swig libpulse-dev

  pip install textract
