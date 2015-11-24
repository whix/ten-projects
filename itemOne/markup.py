#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import re
from handlers import *
from util import *
from rules import *


class Parser(object):
    def __init__(self, handler):
        self.handler = handler
        self.rules = []
        self.filters = []

    def add_rule(self, rule):
        self.rules.append(rule)

    def add_filter(self, pattern, name):
        def filter(block, handler):
            return re.sub(pattern, handler.sub(name), block)
        self.filters.append(filter)

    def parse(self, file):
        self.handler.start('document')
        for block in blocks(file):
            for filter in self.filters:
                block = filter(block, self.handler)
            for rule in self.rules:
                if rule.condition(block):
                    last = rule.action(block, self.handler)
                    if last:
                        break
        self.handler.end('document')


class BasicTextParser(Parser):
    def __init__(self, handler):
        Parser.__init__(self, handler)
        self.add_rule(ListRule())
        self.add_rule(ListItemRule())
        self.add_rule(TitleRule())
        self.add_rule(HeadingRule())
        self.add_rule(ParagraphRule())

        self.add_filter(r'\*(.+?)\*', 'emphasis')
        self.add_filter(r'(http://[\.a-z0-9A-Z]+', 'url')
        self.add_filter(r'[\.a-zA-Z0-9]+@[\.a-zA-Z0-9]+', 'mail')

handler = HTMLRenderer()
parser = BasicTextParser(handler)

parser.parse(sys.stdin)

