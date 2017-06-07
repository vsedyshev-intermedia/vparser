#!/usr/bin/python
# -*- coding: utf-8 -*-

from logging import basicConfig, DEBUG

from vparser import CustomPattern, CustomParser, CustomMatcher

basicConfig(level=DEBUG)

pattern_string = 'Hello {name} my age is {value} and I have {flag} live'

pattern = CustomPattern()
print pattern.parse(pattern_string)

string = 'Hello "ZAO \\"PROM\\"" my age is 25 and I have true live'
parser = CustomParser()
print parser.parse(string)


matcher = CustomMatcher(pattern=pattern._ast)
print matcher.match(parser._ast)
