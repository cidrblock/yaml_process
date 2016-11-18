#!/usr/bin/env python
'''
Ansible module to run a commadn using netmiko.

By default, run a show version
'''
import os
import yaml
import q

from ansible.module_utils.basic import *
from netmiko import ConnectHandler

class ExplicitDumper(yaml.SafeDumper):
    """
    A dumper that will never emit aliases.
    """
    def ignore_aliases(self, data):
        return True

host_vars_dir = 'preprocessed/host_vars'
standards_dir = 'preprocessed/standards'

@q
def main():
    '''
    Ansible module to preprocess yaml

    '''

    module = AnsibleModule(
        argument_spec=dict(
            process=dict(required=False, default='true')
        ),
        supports_check_mode=False)
    try:

        for filename in os.listdir(host_vars_dir):
            new_contents = recurse(os.path.join(host_vars_dir, filename))
            new_file = ''
            for chunk in reversed(new_contents):
                new_file += ('\n').join(chunk)
                new_file += ('\n')
                new_file += ('\n')
            result = yaml.load(new_file)
            with open(os.path.join('host_vars', filename), 'w') as f:
                yaml.dump(result, f, default_flow_style=False, Dumper=ExplicitDumper)
        module.exit_json(msg='successful')

    except Exception, e:
        q(e)
        excType = e.__class__.__name__
        module.fail_json(msg='failed')

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


if __name__ == "__main__":
    main()
