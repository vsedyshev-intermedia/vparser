#!/usr/bin/env -S python3

from unittest import TestCase, main

from vparser import CustomPattern, CustomParser, CustomMatcher

class Test1(TestCase):
    def runTest(self):

        pattern_string = 'As a user {username} I want use {tech} with my computer {device} and then I will be {mod} as expected'

        # Step 1. Compile pattern
        pattern = CustomPattern()
        p = pattern.parse(pattern_string)

        string = 'As a user "Vitold Sedyshev \"vit1251@gmail.com\"" I want use "BDD" with my computer "notebook Intel Celeron" and then I will be "happy" as expected'

        # Step 2. Parse string
        parser = CustomParser()
        ast = parser.parse(string)

        # Step 3. Match
        matcher = CustomMatcher(pattern=ast._ast)
        matcher.match(parser._ast)


if __name__ == "__main__":
    main()
