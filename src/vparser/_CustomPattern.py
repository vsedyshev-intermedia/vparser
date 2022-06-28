#

from __future__ import absolute_import

from ._CustomMatcher import CustomMatcher

STATE_LITERAL = "LITERAL"
STATE_PATTERN = "PATTERN"

class CustomPattern(object):


    def __init__(self):
        self._state = STATE_LITERAL
        self._literal = ""
        self._ast = []

    def _register(self, node_type, node_value):
       self._ast.append((node_type, node_value))

    def _parse_rune(self, rune):
        if self._state == STATE_LITERAL:
            if rune == ' ':
                if self._literal:
                    self._register(STATE_LITERAL, self._literal)
                self._literal = ""
            elif rune == '{':
                if self._literal:
                    self._register(STATE_LITERAL, self._literal)
                self._literal = ""
                #
                self._state = STATE_PATTERN
            else:
                self._literal += rune
        elif self._state == STATE_PATTERN:
            if rune == '}':
                self._register(STATE_PATTERN, self._literal)
                self._literal = ""
                #
                self._state = STATE_LITERAL
            else:
                self._literal += rune
        else:
            raise RuntimeError

    def match(self, value):
        matcher = CustomMatcher(pattern=self)
        return matcher.match(value)

    def parse(self, pattern):
        runes = list(pattern)
        while runes:
            rune = runes.pop(0)
            self._parse_rune(rune)
        return self._ast

