"""Extra command-line behaviors for developing Luca."""

import subprocess
import sys
from fdfgen import forge_fdf

def main():
    """Fill in each field in a PDF form with its own name."""

    path = sys.argv[1]
    data = subprocess.check_output(['pdftk', path, 'dump_data_fields'])
    with open('fields.txt', 'w') as f:
        f.write(data)

    names = [ line.split(' ', 1)[1] for line in data.splitlines()
              if line.startswith('FieldName: ') ]

    fields = [ (name, name.split('.')[-1]) for name in names ]
    # verbose: fields = [ (name, name) for name in names ]

    fdf = forge_fdf('', fields, [], [], [])
    fdf_file = open('data.fdf', 'w')
    fdf_file.write(fdf)
    fdf_file.close()

    subprocess.check_call(['pdftk', path, 'fill_form', 'data.fdf',
                           'output', 'fields.pdf'])

if __name__ == '__main__':
    try:
        main()
    except subprocess.CalledProcessError as e:
        sys.stderr.write('\nFailed command: {}\nReturn code: {}\n'.format(
                ' '.join(e.cmd), e.returncode))
        sys.exit(e.returncode)
