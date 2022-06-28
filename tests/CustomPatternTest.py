#!/usr/bin/env -S python3

from logging import basicConfig, debug, DEBUG
from unittest import TestCase, main

from vparser import CustomPattern, CustomParser, CustomMatcher

class CustomPatternTest(TestCase):
    def runTest(self):

        pattern_string = 'As a user {username} I want use {tech} with my computer {device} and then I will be {mod} as expected'

        # Step 1. Compile pattern
        pattern = CustomPattern()
        got = pattern.parse(pattern_string)

        want = [
            ('LITERAL', 'As'),
            ('LITERAL', 'a'),
            ('LITERAL', 'user'),
            ('PATTERN', 'username'),
            ('LITERAL', 'I'),
            ('LITERAL', 'want'),
            ('LITERAL', 'use'),
            ('PATTERN', 'tech'),
            ('LITERAL', 'with'),
            ('LITERAL', 'my'),
            ('LITERAL', 'computer'),
            ('PATTERN', 'device'),
            ('LITERAL', 'and'),
            ('LITERAL', 'then'),
            ('LITERAL', 'I'),
            ('LITERAL', 'will'),
            ('LITERAL', 'be'),
            ('PATTERN', 'mod'),
            ('LITERAL', 'as'),
            ('LITERAL', 'expected'),
        ]

        self.assertEqual(got, want)


if __name__ == "__main__":
    basicConfig(level=DEBUG)
    main()
