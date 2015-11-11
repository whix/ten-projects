#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from util import *
import sys


print '<html><head><title>No Title</title><body>'
h1 = True
for block in blocks(sys.stdin):
    block = re.sub(r'\*(.+?)\*', r'<em>\1</em>', block)
    if h1:
        print '<h1>'
        print block
        print '</h1>'
        h1 = False
    else:
        print '<p>'
        print block
        print '</p>'
print '</body></html>'
