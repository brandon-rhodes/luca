'''Run the forms in the ../samples/ directory as tests.'''

import os
from luca.forms import actions, formlib

# Since standard Python unit tests are not easy to parameterize, we
# write these in the style that pytest supports; this means that they
# will only run when I invoke the tests as "py.test luca".

import pytest

# We run the test against every sample JSON file.

sampledir = os.path.dirname(__file__) + '/../samples'
sample_filing_paths = []
for filename in os.listdir(sampledir):
    path = os.path.join(sampledir, filename)
    if os.path.isfile(path):
        sample_filing_paths.append(path)

@pytest.fixture(scope='module', params=sample_filing_paths)
def sample_filing_path(request):
    return request.param

def test_sample_filing(sample_filing_path):
    print "arg is", sample_filing_path
    with open(sample_filing_path) as f:
        json_data = f.read()
    form, form_module = actions.process(json_data)
    json_output = formlib.dump_json(form).encode('utf-8')
    assert json_data == json_output
