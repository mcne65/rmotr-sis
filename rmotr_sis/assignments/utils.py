import re
import pep8
import requests
try:
    from io import StringIO
except ImportError:
    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO


def run_code(code):
    url = "http://execute.rmotr.com/compile"
    resp = requests.post(url, data={"language": 0, "stdin": "", "code": code})
    return resp.json()


def check_pep8_errors(code):
    """Runs PEP8 validation for given chunck of code using an in-memory file.
       Returns the pep8 Report object with the result of the validation.
       http://pep8.readthedocs.org/en/latest/api.html#pep8.BaseReport
    """
    mem_file = StringIO(code)
    fchecker = pep8.Checker(lines=mem_file.readlines(), show_source=True)
    fchecker.check_all()
    return fchecker.report


def format_pep8_report(report):
    """Given a pep8 Report object, it builds the proper string output displaying
       errors with specific error codes and line number.
    """
    # NOTE: This functionality was duplicated from `pep8` source code, as there's
    #       no way to get the formated output as a string. It only prints it in
    #       the stdout.
    #       https://github.com/PyCQA/pep8/blob/e73d8fbe4151345ab78b69300cdeea5d9b67840b/pep8.py#L1743
    output = ''
    for line_number, offset, code, text, doc in report._deferred_print:
        output += report._fmt % {
            'path': report.filename,
            'row': report.line_offset + line_number, 'col': offset + 1,
            'code': code, 'text': text,
        } + '\n'
        if report._show_source:
            if line_number > len(report.lines):
                line = ''
            else:
                line = report.lines[line_number - 1]
            output += line.rstrip() + '\n'
            output += re.sub(r'\S', ' ', line[:offset]) + '^\n'
    return output
