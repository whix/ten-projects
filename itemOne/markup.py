#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import re
from handlers import *
from util import *
from rules import *


class Parser(object):
    def __init__(self, my_handler):
        self.handler = my_handler
        self.rules = []
        self.filters = []

    def add_rule(self, rule):
        self.rules.append(rule)

    def add_filter(self, pattern, name):
        def the_filter(block, the_handler):
            return re.sub(pattern, the_handler.sub(name), block)
        self.filters.append(the_filter)

    def parse(self, the_file):
        self.handler.start('document')
        for block in blocks(the_file):
            for the_filter in self.filters:
                block = the_filter(block, self.handler)
            for rule in self.rules:
                if rule.condition(block):
                    last = rule.action(block, self.handler)
                    if last:
                        break
        self.handler.end('document')


class BasicTextParser(Parser):
    def __init__(self, my_handler):
        Parser.__init__(self, my_handler)
        self.add_rule(ListRule())
        self.add_rule(ListItemRule())
        self.add_rule(TitleRule())
        self.add_rule(HeadingRule())
        self.add_rule(ParagraphRule())

        self.add_filter(r'\*(.+?)\*', 'emphasis')
        self.add_filter(r'(http://[\.a-z0-9A-Z/]+)', 'url')
        self.add_filter(r'([\.a-zA-Z0-9]+@[\.a-zA-Z0-9]+)', 'mail')

if __name__ == '__main__':
    handler = HTMLRenderer()
    parser = BasicTextParser(handler)
    parser.parse(sys.stdin)

