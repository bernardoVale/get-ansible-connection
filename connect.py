import sys
from ansible import inventory
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory


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

        if 'ansible_port' in host.vars:
            port = host.vars['ansible_port']
        if 'ansible_ssh_port' in host.vars:
            port = host.vars['ansible_ssh_port']
        if 'ansible_user' in host.vars:
            user = host.vars['ansible_user']
        if 'ansible_ssh_user' in host.vars:
            user = host.vars['ansible_ssh_user']

        return "ssh {}@{} -p {} -F /etc/ansible/ssh.config".format(user, host.address, port)

def main(args):
    pattern = args[0]
    inv = SSHInventory()
    hosts = inv.inventory.get_hosts(pattern)
    for host in hosts:
        print inv.get_ssh_cmd(host)

if __name__ == '__main__':
    main(sys.argv[1:])
