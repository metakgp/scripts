# Ensure file is exported in tab-seperated-value format
# If year is not present, you may add it from here
import csv
def wiki(num, q, a, p, y):
#     print list
    new = '\n'
    val = '|' + str(num) + new + '|' + q + new + '|' + a + new + '|' + p + new + '|' + y + new
    return val

step = '|-\n'

start = '''
== B. Tech. ==
{| class="wikitable"
|-
! #
! Question
! Answer
! Professor
! Year
|-
'''

end = '''|}'''


def getData(filename, q_col_idx, a_col_idx, p_col_idx, y_col_idx=None, year=None):
    tsvfile = open(filename, 'rb')
    spamreader = csv.reader(tsvfile, dialect="excel-tab")
    a = []
    for row in spamreader:
        a.append(row)
    t = a[0]
    b = a[1:]
    q = [i[q_col_idx] for i in b]
    a = [i[a_col_idx] for i in b]
    p = [i[p_col_idx] for i in b]
    y = [i[y_col_idx] if y_col_idx else year for i in b]
    return q, a, p, y

def getMarkdown(filename, q, a, p, y=None):
    num = 1
    v = ''
    for i in range(len(q)):
        if q[i]:
            v += wiki(num, q[i], a[i], p[i], y[i]) + step
            num += 1
    g = open(filename, 'w')
    g.write(start + v + end)
    g.close()

if __name__ == '__main__':
    q, a, p, y = getData('Downloads/CSE GV - Sheet1.tsv', 0, 1, 2, 3)
    getMarkdown('cse.md', q, a, p, y)