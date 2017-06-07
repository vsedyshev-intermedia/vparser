#

from __future__ import absolute_import

from logging import getLogger


class Match(object):
    def __init__(self):
        self._values = {}

    def set(self, name, value):
        self._values[name] = value

    def __repr__(self):
        return "<Match values={values!r}>".format(values=self._values)


class CustomMatcher(object):
    def __init__(self, pattern):
        self.__log = getLogger('vparser.matcher')
        self._pattern = pattern

    def _match_pattern_string(self, match, pattern_name, node):
        result = False
        #
        self.__log.debug("_match_pattern_string: pattern_name = {pattern_name!r}, node = {node!r}".format(pattern_name=pattern_name, node=node))
        node_type, node_value = node
        if node_type == 'STRING':
            match.set(pattern_name, node_value)
            result = True
        elif node_type == 'LITERAL':
            match.set(pattern_name, node_value)
            result = True
        #
        return result
        
    def _match_pattern_number(self, match, pattern_name, node):
        result = False
        #
        self.__log.debug("_match_pattern_number: pattern_name = {pattern_name!r}, node = {node!r}".format(pattern_name=pattern_name, node=node))
        node_type, node_value = node
        #
        if node_type == 'LITERAL':
            try:
                match.set(pattern_name, int(node_value))
                result = True
            except Exception as err:
                self.__log.exception(err)
        #
        return result

    def _match_pattern_boolean(self, match, pattern_name, node):
        result = False
        #
        self.__log.debug("_match_pattern_boolean: pattern_name = {pattern_name!r}, node = {node!r}".format(pattern_name=pattern_name, node=node))
        node_type, node_value = node
        #
        if node_type == 'LITERAL':
            if node_value in ['1', 'yes', 'Yes', 'Y', 'ON', 'True', 'true']:
                match.set(pattern_name, True)
                result = True
            elif node_value in ['0', 'no', 'No', 'N', 'OFF', 'False', 'false']:
                match.set(pattern_name, False)
                result = True
        #
        return result

    def _match_pattern(self, match, pattern, node):
        self.__log.debug("_match_pattern: pattern={pattern!r}, node={node!r}".format(pattern=pattern, node=node))
        #
        result = False
        #
        if ":" in pattern:
            pattern_name, pattern_type = pattern.split(":", 1)
        else:
            pattern_name, pattern_type = pattern, "string"
        #
        self.__log.debug("pattern_name = {pattern_name!r}, pattern_type = {pattern_type!r}".format(pattern_name=pattern_name, pattern_type=pattern_type))
        #
        if pattern_type == "string":
            result = self._match_pattern_string(match, pattern_name, node)
        elif pattern_type == "number":
            result = self._match_pattern_number(match, pattern_name, node)
        elif pattern_type == "boolean":
            result = self._match_pattern_boolean(match, pattern_name, node)
        #
        return result
        

    def match(self, nodes):
        """ Search match
        """
        result = Match()
        #
        pattern_size = len(self._pattern)
        size = len(nodes)
        #
        if pattern_size != size:
            return None
        #
        for pattern_node, value_node in zip(self._pattern, nodes):
            self.__log.debug("pattern_node={pattern_node!r} value_node={value_node!r}".format(pattern_node=pattern_node, value_node=value_node))
            pattern_node_type, pattern_node_value = pattern_node
            value_node_type, value_node_value = value_node
            #
            if all([pattern_node_type == 'LITERAL', value_node_type == 'LITERAL', pattern_node_value == value_node_value]):
                pass
            elif all([pattern_node_type == 'PATTERN']):
                if self._match_pattern(result, pattern_node_value, value_node):
                    pass
                else:
                    result = None
                    break
            else:
                result = None
                break
        #
        return result
