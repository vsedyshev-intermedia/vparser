#!/usr/bin/env -S python3

from logging import basicConfig, debug, DEBUG
from unittest import TestCase, main

from vparser import CustomPattern, CustomParser, CustomMatcher

class CustomParserTest(TestCase):
    def runTest(self):

        pattern_string = 'As a user {username} I want use {tech} with my computer {device} and then I will be {mod} as expected'

        # Step 1. Compile pattern
        pattern = CustomPattern()
        p = pattern.parse(pattern_string)

        string = 'As a user "Vitold Sedyshev <vit1251@gmail.com>" I want use "BDD" with my computer "notebook Intel Celeron" and then I will be "happy" as expected'

        parser = CustomParser()
        got = parser.parse(string)

        want = [
            ('LITERAL', 'As'),
            ('LITERAL', 'a'),
            ('LITERAL', 'user'),
            ('STRING', 'Vitold Sedyshev <vit1251@gmail.com>'),
            ('LITERAL', 'I'),
            ('LITERAL', 'want'),
            ('LITERAL', 'use'),
            ('STRING', 'BDD'),
            ('LITERAL', 'with'),
            ('LITERAL', 'my'),
            ('LITERAL', 'computer'),
            ('STRING', 'notebook Intel Celeron'),
            ('LITERAL', 'and'),
            ('LITERAL', 'then'),
            ('LITERAL', 'I'),
            ('LITERAL', 'will'),
            ('LITERAL', 'be'),
            ('STRING', 'happy'),
            ('LITERAL', 'as'),
            ('LITERAL', 'expected'),
        ]

        self.assertEqual(got, want)


if __name__ == "__main__":
    basicConfig(level=DEBUG)
    main()
