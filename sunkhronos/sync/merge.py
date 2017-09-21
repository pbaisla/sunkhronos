# Modified from http://www.nmr.mgh.harvard.edu/~you2/dramms/dramms-1.4.3-source/build/bundle/src/BASIS/src/utilities/python/diff3.py

from sunkhronos.sync.diff3lib import diff, diff3

def merge(yourtext, origtext, theirtext):
    body = []
    d3 = diff3(yourtext, origtext, theirtext)
    text3 = (yourtext, theirtext, origtext)
    i2 = 1
    for r3 in d3:
        for lineno in range(i2, r3[5]):
            body.append(text3[2][lineno - 1])
        if r3[0] == '0':
            for lineno in range(r3[1], r3[2] + 1):
                body.append(text3[0][lineno - 1])
        elif r3[0] != 'A':
            for lineno in range(r3[3], r3[4] + 1):
                body.append(text3[1][lineno - 1])
        else:
            body = _conflict_range(text3, r3, body)
        i2 = r3[6] + 1
    for lineno in range(i2, len(text3[2]) + 1):
        body.append(text3[2][lineno - 1])
    return body

def _conflict_range(text3, r3, body):
    text_a = [] # their text
    for i in range(r3[3], r3[4] + 1):
        text_a.append(text3[1][i - 1])
    text_b = [] # your text
    for i in range(r3[1], r3[2] + 1):
        text_b.append(text3[0][i - 1])
    d = diff(text_a, text_b)
    if _assoc_range(d, 'c') and r3[5] <= r3[6]:
        for lineno in range(r3[1], r3[2] + 1):
            body.append(text3[0][lineno - 1])
        for lineno in range(r3[5], r3[6] + 1):
            body.append(text3[2][lineno - 1])
        for lineno in range(r3[3], r3[4] + 1):
            body.append(text3[1][lineno - 1])
        return body
    ia = 1
    for r2 in d:
        for lineno in range(ia, r2[1]):
            body.append(text_a[lineno - 1])
        if r2[0] == 'c':
            for lineno in range(r2[3], r2[4] + 1):
                body.append(text_b[lineno - 1])
            for lineno in range(r2[1], r2[2] + 1):
                body.append(text_a[lineno - 1])
        elif r2[0] == 'a':
            for lineno in range(r2[3], r2[4] + 1):
                body.append(text_b[lineno - 1])
        ia = r2[2] + 1
    for lineno in range(ia, len(text_a)):
        body.append(text_a[lineno - 1])
    return body

def _assoc_range(diff, diff_type):
    for d in diff:
        if d[0] == diff_type: return d
    return None

