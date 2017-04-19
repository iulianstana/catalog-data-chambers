

def beautify_romanian(string):
    symbols = (u"ǎţşŢŞ",
               u"ățșȚȘ")
    tr = {ord(a): ord(b) for a, b in zip(*symbols)}
    return string.translate(tr)
