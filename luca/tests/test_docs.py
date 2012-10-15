import doctest
import luca

def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(luca))
    return tests
