import re

def convert_non_ascii(string):
        nfkd_form = unicodedata.normalize('NFKD', string)
        return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])

def remove_non_ascii(string):
    return re.sub(r'[^\x00-\x7F]+', ' ', string)

def remove_non_numeric(string):
    return re.sub('[^0-9]+', '', string)

def rws(str):
    if str:
        return ' '.join(str.split())
    else:
        return None

def titleize(string):
    if string:
        return string.title()
    else:
        return None
