FILE_NAME = r'C:\Users\Oscar\GIT\3D-CRCP-embedded-sbar\3D_CRCP_XYPlot.rpt'

TITLE_FROM = 2
TITLE_UNTIL = 3

VALUE_FROM = 5

def main():
    i = 1
    with open(FILE_NAME, 'r') as f:
        # go to title
        f, i = skipUntil(f, i, TITLE_FROM)

        # read and pass to function to process
        contents = []
        while i <= TITLE_UNTIL:
            contents.append(f.readline())
            i += 1
        titles = readTitle(contents)

        # go to content for values
        f, i = skipUntil(f, i, VALUE_FROM)

        # read and pass to functino to process
        contents = f.readlines()
        values = readValues(contents)

        ######################################
        # output to csv format
    with open(FILE_NAME+'.csv', 'w') as f:
        f.write(','.join(titles) + '\n')
        for v in values:
            f.write(','.join(v) + '\n')


def readTitle(contents):
    titles = []
    # spliy by white space
    for c in contents:
        titles.append(c.strip().split())
    maxLength = len(titles[-1])
    # pad the titles as some are splitted
    for i in range(len(titles)):
        while len(titles[i]) < maxLength:
            titles[i].insert(0, '')
    # join the splitted title together
    finalTitle = []
    for i in range(maxLength):
        column = ''
        for t in titles:
            column += t[i]
        finalTitle.append(column)
    return finalTitle



def readValues(contents):
    values = []
    for c in contents:
        v = c.strip().split()
        # filter out NoValue and replace as BLANK
        v = [i if i != 'NoValue' else '#N/A' for i in v ]
        values.append(v)
    return values

def skipUntil(file, counter, skip_until):
    while counter < skip_until:
        file.readline()
        counter += 1
    return file, counter


main()
