
from ._CustomMatcher import CustomMatcher

STATE_LITERAL = "LITERAL"
STATE_PATTERN = "PATTERN"

EOF = ''

class CustomPattern(object):

    def __init__(self, debug=False):
        self._state = STATE_LITERAL
        self._literal = ""
        self._pattern = ""
        self._ast = []
        self._debug = debug

    def _register(self, node_type, node_value):
       self._ast.append((node_type, node_value))

    def makeError(self, msg: str) -> str:
        """ Make error message
        """
        parts = []
        parts.append(msg)
        if self._debug:
            parts.append("State: {state!r}".format(state=self._state))
            parts.append("AST: {ast!r}".format(ast=self._ast))
            parts.append("Escape: {escape!r}".format(escape=self._escape))
            parts.append("Literal: {literal!r}".format(literal=self._literal))
            parts.append("Pattern: {pattern!r}".format(pattern=self._pattern))
        result = "\n".join(parts)
        return result


    def _parse_rune(self, rune):
        if self._state == STATE_LITERAL:
            if rune in [' ', '\t', EOF]:
                if self._literal:
                    self._register(STATE_LITERAL, self._literal)
                self._literal = ""
            elif rune == '}':
                raise SyntaxError(self.makeError('Unexpected }'))
            elif rune == '{':
                if self._literal:
                    raise SyntaxError(self.makeError('Unexpected {'))
                #
                self._state = STATE_PATTERN
            else:
                self._literal += rune
        elif self._state == STATE_PATTERN:
            if rune in [EOF]:
                raise SyntaxError(self.makeError('Unexpected EOF'))
            elif rune == '{':
                raise SyntaxError(self.makeError('Unexpected {'))
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
