import doctest
import luca
import os
import pytest
from glob import glob

def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(luca))
    return tests

# @pytest.mark.parametrize('yaml_filename,output_filename', [
#     ('rules0.yaml', 'output0.txt'),
#     ])
# def test_docs_input_output(yaml_filename, output_filename):
#     thisdir = os.path.dirname(__file__)
#     docsdir = os.path.join(os.path.dirname(thisdir), 'docs')
#     statements = glob(os.path.join(docsdir, 'statement-*.txt'))

def find_rules_files():
    this_dir = os.path.dirname(__file__)
    docs_dir = os.path.join(os.path.dirname(this_dir), 'docs')

    rules_paths = glob(os.path.join(docs_dir, 'rules*.yaml'))
    statement_paths = tuple(glob(os.path.join(docs_dir, 'statement-*.txt')))
    # tuple() because otherwise py.test dies terribly

    return [(rules_path, statement_paths) for rules_path in rules_paths]

@pytest.fixture(params=find_rules_files())
def rules_statements_output(request):
    rules_path, statement_paths = request.param
    output_path = rules_path.replace('rules','output').replace('.yaml','.txt')
    return rules_path, list(statement_paths), output_path

def test_docs_input_output(rules_statements_output):

    from blessings import Terminal
    from docopt import docopt
    from luca import commandline

    rules_path, statement_paths, output_path = rules_statements_output

    terminal = Terminal(kind='ansi', force_styling=True)
    terminal._height_and_width = lambda: (24, 48)

    argv = ['tally', rules_path] + statement_paths
    if rules_path.endswith('t.yaml'):
        argv.append('-t')
    args = docopt(commandline.__doc__, argv)

    lines = list(commandline._main(args, terminal))
    lines.append('')
    output = '\n'.join(lines)

    with open(output_path) as output_file:
        expected = output_file.read()

    assert expected == output
