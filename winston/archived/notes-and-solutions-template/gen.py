# Version: 2020 Feb 04

"""
Changelog:
    2020 Jan 12: Created
"""

"""
Usage:
  - Update COMPACT_REPR to reflect the structure of the text.
  - Run this file, piping STDOUT to a file "outline.str"
  - Write chapter and section names into the outline file.
  - Run this script again (it will overwrite "outline.str.tex" with the structure)
  - Manually copy pieces of the generated tex file into the project structure.
      This allows me to type out the outline.str partially, if I don't need everything.
"""


import re
import pprint

REGEX_CHAPTER = '\d+\. (.*)'
REGEX_SECTION = '(\d+\.){2} (.*)' # TODO syntax for exactly two repetitions?
COMPACT_REPR = (8,4,8,6,5,5,6,8,7,8,12)


def compact_to_str(tup):
    """
    The numbers in the tuple should correspond to
    the number of sections in each chapter.

    (4, 3, 7) means Chapter 1 has 4 sections, Chapter 2 has 3 sections, Chapter 3 has 7 sections
    
    """

    out = ""
    chap = 1
    for i in tup:
        out += "{}. \n".format(chap)
        for j in range(i):
            out += "{}.{}. \n".format(chap, j + 1)
        chap += 1

    return out
        

def convert_line(line):
    m = re.match(REGEX_CHAPTER, line)
    if m:
        return '\chapter{%s}' % m.group(1)
    m = re.match(REGEX_SECTION, line)
    if m:
        return "\section{%s}" % m.group(2)

def convert_to_latex(lines):
    return list(map(convert_line, lines))


def append_comments(lines):
    ctr_chapter = 0
    ctr_section = 0

    for i in range(len(lines)):
        line = lines[i]
        if line.startswith("\chapter"):
            ctr_chapter += 1
            line += f' % {ctr_chapter}.'
            ctr_section = 0
        if line.startswith("\section"):
            ctr_section += 1
            line += f' % {ctr_chapter}.{ctr_section}.'
        lines[i] = line

    #print(list(lines))
    return lines
    

with open("outline.str") as f:
    global lines
    lines = f.readlines()

# not going to check that the typed numbers are correct.

converted = convert_to_latex(lines)
#print(list(converted))

appended = append_comments(converted)
#print(list(appended))
    
    
output = '\n\n'.join(appended)

# print(output)

with open('outline.str.tex','w') as f:
    f.write(output)


print("Exported to outline.str.tex")

print(compact_to_str(COMPACT_REPR))
