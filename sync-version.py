#!/usr/bin/env python

from simpledbfbrowser import EksplorasiDbf
import re

if __name__ == "__main__":
    main_file = "simpledbfbrowser.py"
    iss_file = "simpledbfbrowser.iss"
    cx_file = "setup.py"

    versi = EksplorasiDbf.version

    # iss
    f = open(iss_file, "r")
    content = f.read()
    f.close()

    pattern = re.compile(r'^#define MyAppVersion ".*"', re.MULTILINE)
    new_content = re.sub(pattern, r'#define MyAppVersion "%s"' % versi, content, 1)

    f = open(iss_file, "w")
    f.write(new_content)
    f.close()

    # cx
    f = open(cx_file, "r")
    content = f.read()
    f.close()

    pattern = re.compile(r'(^.*version = )(".*")(,)', re.MULTILINE)

    #m = re.search(pattern, content)
    #print m.group(3)

    new_content = re.sub(pattern, r'\1"%s"\3' % versi, content, 1)
    #print new_content

    f = open(cx_file, "w")
    f.write(new_content)
    f.close()






