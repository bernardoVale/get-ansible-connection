#!/usr/bin/env python

import sys
from ansible import inventory
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.constants import load_config_file

def load_ssh_args():
    """
    Read ansible.cfg and get only the the ssh_args parameter
    if defined
    :return: Output of ansible ssh_args
    """
    config, _ = load_config_file()
    # It's easier to ask for forgiveness than permission
    try:
        ssh_section = config._sections['ssh_connection']
        return ssh_section['ssh_args']
    except KeyError:
        return None

class SSHInventory:

    def __init__(self):

        variable_manager = VariableManager()
        loader = DataLoader()
        self.inventory = Inventory(loader=loader, variable_manager=variable_manager)


    def get_host(self, host):
        return self.inventory.get_host(host)

    def get_ssh_cmd(self, host):
        port = "22"
        user = "root"
        options = ""

        if 'ansible_port' in host.vars:
            port = host.vars['ansible_port']

        if 'ansible_ssh_port' in host.vars:
            port = host.vars['ansible_ssh_port']

        if 'ansible_user' in host.vars:
            user = host.vars['ansible_user']

        if 'ansible_ssh_user' in host.vars:
            user = host.vars['ansible_ssh_user']

        ssh_args = load_ssh_args()
        if ssh_args:
            options += ssh_args

        if 'ansible_ssh_private_key_file' in host.vars:
            options += " -i %s" % host.vars['ansible_ssh_private_key_file']

        return "ssh {}@{} -p {} {}".format(user, host.address, port, options)

def main(args):
    pattern = args[0]
    inv = SSHInventory()
    hosts = inv.inventory.get_hosts(pattern)
    for host in hosts:
        print "Server:%s" % host.name
        print inv.get_ssh_cmd(host)

if __name__ == '__main__':
    main(sys.argv[1:])
