
from ._CustomMatcher import CustomMatcher

STATE_LITERAL = "LITERAL"
STATE_PATTERN = "PATTERN"

EOF = ''

class CustomPattern(object):

    def __init__(self):
        self._state = STATE_LITERAL
        self._literal = ""
        self._pattern = ""
        self._ast = []

    def _register(self, node_type, node_value):
       self._ast.append((node_type, node_value))

    def _parse_rune(self, rune):
        if self._state == STATE_LITERAL:
            if rune in [' ', '\t', EOF]:
                if self._literal:
                    self._register(STATE_LITERAL, self._literal)
                self._literal = ""
            elif rune == '}':
                raise SyntaxError('Unexpected } after "{literal}"'.format(literal=self._literal))
            elif rune == '{':
                if self._literal:
                    raise SyntaxError('Unexpected { after "{literal}"'.format(literal=self._literal))
                #
                self._state = STATE_PATTERN
            else:
                self._literal += rune
        elif self._state == STATE_PATTERN:
            if rune in [EOF]:
                raise SyntaxError('Unexpected EOF')
            elif rune == '{':
                raise SyntaxError('Unexpected { after "{pattern}"'.format(pattern=self._pattern))
            elif rune == '}':
                self._register(STATE_PATTERN, self._pattern)
                self._pattern = ""
                #
                self._state = STATE_LITERAL
            else:
                self._pattern += rune
        else:
            raise RuntimeError("Invalid state")

    def match(self, value):
        matcher = CustomMatcher(pattern=self)
        return matcher.match(value)

    def parse(self, pattern):
        runes = list(pattern)
        while runes:
            rune = runes.pop(0)
            self._parse_rune(rune)
        self._parse_rune(EOF)
        return self._ast
