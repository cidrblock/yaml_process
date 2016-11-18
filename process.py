import os
import yaml
from pprint import pprint

dir = 'preprocessed/host_vars'
standards_dir = 'preprocessed/standards'

def recurse(file):
    response = []
    with open(file) as file:
        lines = file.read().splitlines()
        response.append(lines)
        matches = filter(lambda x: "<<:" in x, reversed(lines))
        matches = set(map(lambda x: x.strip(), matches))
        for match in matches:
            resp = dive(match)
            for r in resp:
                response.append(r)
    return response

def dive(match):
    standard_file = os.path.join(standards_dir, match.split('*')[1] + '.yaml')
    return recurse(standard_file)

for filename in os.listdir(dir):
    new_contents = recurse(os.path.join(dir, filename))
    new_file = ''
    for chunk in reversed(new_contents):
        new_file += ('\n').join(chunk)
        new_file += ('\n')
        new_file += ('\n')
    print new_file
    with open(os.path.join('host_vars', filename), 'w') as f:
        f.write(new_file)
