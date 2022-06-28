
STATE_LITERAL = "LITERAL"
STATE_STRING  = "STRING"

EOF = ''

class CustomParser(object):

    def __init__(self):
        self._state = STATE_LITERAL
        self._literal = ""
        self._string = ""
        self._ast = []
        self._escape = False

    def _register(self, node_type, node_value):
       self._ast.append((node_type, node_value))

    def _parse_rune(self, rune):
        if self._state == STATE_LITERAL:
            if rune in [' ', '\t', EOF]:
                if self._literal:
                    self._register(STATE_LITERAL, self._literal)
                self._literal = ""
            elif rune == '"':
                if self._literal:
                    raise SyntaxError('Unexpected " after {literal}'.format(literal=self._literal))
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
                    raise SyntaxError("Unexpected EOF after {string}".fromat(string=self._string))
                elif rune == '\\':
                    self._escape = True
                else:
                    self._string += rune
        else:
            raise RuntimeError

    def parse(self, string):
        runes = list(string)
        while runes:
            rune = runes.pop(0)
            self._parse_rune(rune)
        self._parse_rune(EOF)
        return self._ast

