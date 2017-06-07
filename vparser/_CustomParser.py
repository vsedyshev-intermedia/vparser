#

from __future__ import absolute_import

STATE_LITERAL = "LITERAL"
STATE_STRING  = "STRING"

class CustomParser(object):

    def __init__(self):
        self._state = STATE_LITERAL
        self._literal = ""
        self._ast = []
        self._escape = False

    def _register(self, node_type, node_value):
       self._ast.append((node_type, node_value))

    def _parse_rune(self, rune):
        if self._state == STATE_LITERAL:
            if rune == ' ':
                if self._literal:
                    self._register(STATE_LITERAL, self._literal)
                self._literal = ""
            elif rune == '"':
                if self._literal:
                    self._register(STATE_LITERAL, self._literal)
                self._literal = ""
                #
                self._state = STATE_STRING
            else:
                self._literal += rune
        elif self._state == STATE_STRING:
            if all([self._escape == False, rune == '"']):
                self._register(STATE_STRING, self._literal)
                self._literal = ""
                #
                self._state = STATE_LITERAL
            elif all([self._escape == False, rune == '\\']):
                self._escape = True
            else:
                self._literal += rune
                self._escape = False
        else:
            raise RuntimeError

    def parse(self, string):
        runes = list(string)
        while runes:
            rune = runes.pop(0)
            self._parse_rune(rune)
        #
        return self._ast

