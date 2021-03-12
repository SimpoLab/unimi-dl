from os import listdir
import re


def filename_number(prefix):
    ls = listdir("unimi-dl_output")
    file_regex = re.compile(prefix + r'_\d\d\d\.', re.IGNORECASE)
    number_regex = re.compile(r'\d+')
    retval = 1
    for file in ls:
        match = file_regex.match(file)
        if match:
            num = int(number_regex.search(match.group(0)).group(0))
            if num >= retval:
                retval = num+1
    return '%03d' % retval
