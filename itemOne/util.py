#!/usr/bin/env python
# -*- coding: utf-8 -*-


def lines(file_name):
    for line in file_name:
        yield line
    yield '\n'


def blocks(files):
    block = []
    for line in lines(files):
        if line.strip():
            block.append(line)
        elif block:
            yield ''.join(block).strip()
            block = []

