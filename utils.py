# -*- coding: utf-8 -*-
__author__ = 'AlexStarov'

import random
import copy
import re


replacement = re.compile('(\[[\[a-z|A-Z0-9\-\_\.]+\]])', re.MULTILINE)

# ccc('aaa [[bbb|111]] ccc [[ddd|222]] eee [[fff|333|444|555|666]] ggg')
def ccc(tmpl, ):
    three = re.split(replacement, tmpl)

    nodes = {}
    for pos, block in enumerate(three):
        if block.startswith('[[') and block.endswith(']]'):
            keys = block.strip('[[]]').split('|')

            value = keys[random.randrange(start=0, stop=len(keys))]

            if pos not in nodes:
                nodes[pos] = value

    three = copy.copy(three)
    for pos, value in nodes.iteritems():

        three[pos] = value

    print '!!!!!!!!!!!!!!!!!', ''.join(three)


tokenizer = re.compile('(\{{[a-zA-Z0-9\-\_\.]+\}})', re.MULTILINE)


#bbb('aaa {{aaa1}} ccc {{bbb2}} eee {{ccc3}} ggg', {'aaa1': '1aaa', 'bbb2': 'bb2b', 'ccc3': 'ccc333ccc', })
def bbb(tmpl, context={}, ):
    three = re.split(tokenizer, tmpl)

    nodes = {}
    for pos, block in enumerate(three):
        if block.startswith('{{') and block.endswith('}}'):
            key = block.strip('{{}}')
            if key not in nodes:
                nodes[key] = []
            nodes[key].append(pos)
    keys = nodes.keys()
    three = copy.copy(three)
    for key, value in context.iteritems():
        if key in keys:
            for pos in nodes[key]:
                three[pos] = value

    print '!!!!!!!!!!', ''.join(three)
