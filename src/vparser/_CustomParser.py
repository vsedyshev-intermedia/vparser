
STATE_LITERAL = "LITERAL"
STATE_STRING  = "STRING"

EOF = ''

class CustomParser(object):

    def __init__(self, debug=False):
        self._state = STATE_LITERAL
        self._literal = ""
        self._string = ""
        self._ast = []
        self._escape = False
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
            parts.append("String: {string!r}".format(string=self._string))
        result = "\n".join(parts)
        return result

    def _parse_rune(self, rune):
        if self._state == STATE_LITERAL:
            if rune in [' ', '\t', EOF]:
                if self._literal:
                    self._register(STATE_LITERAL, self._literal)
                self._literal = ""
            elif rune == '"':
                if self._literal:
                    raise SyntaxError(self.makeError('Unexpected "'))
                #
                self._state = STATE_STRING
            else:
                self._literal += rune
        elif self._state == STATE_STRING:
            if self._escape is True:
                self._string += rune
                self._escape = False
            else:
                if rune == '"':
                    self._register(STATE_STRING, self._string)
                    self._string = ""
                    #
                    self._state = STATE_LITERAL
                elif rune == EOF:
                    raise SyntaxError(self.makeError('Unexpected EOF'))
                elif rune == "\\":
                    self._escape = True
                else:
                    self._string += rune
        else:
            raise RuntimeError(self.makeError('Unexpected state'))

    def parse(self, string):
        runes = list(string)
        while runes:
            rune = runes.pop(0)
            self._parse_rune(rune)
        self._parse_rune(EOF)
        return self._ast

