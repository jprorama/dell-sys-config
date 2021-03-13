# dell-sys-config

A set of ansible playbooks to configure Dell boxes via the Redfish APIs.

## Set up the ansible environment

After cloning this repo, create a python env:
```
python3 -m venv venv --system-site-packages
```
Note: the site packages arg fixes an error when [writing result files in 
selinux environments](https://stackoverflow.com/a/64513211/8928529).


Activate the venv:
```
. venv/bin/activate
```

Install the base ansible modules:
```
pip install wheel
pip install ansible
pip install omsdk
```

## Install the Dell OpenManage collection

These playbooks rely on the [Dell OpenManage Collection](https://galaxy.ansible.com/dellemc/openmanage)

The installs use -p to direct the collection install to the `collection` directory in the project dir.  This makes it a bit easier to keep track of what you have installed and doesn't mess with expectations of other envs you may have.

Because this is a non-standard collections location, [update the `ANSIBLE_COLLECTIONS_PATH` to include this directory](https://docs.ansible.com/ansible/latest/reference_appendices/config.html#envvar-ANSIBLE_COLLECTIONS_PATH).
```
export ANSIBLE_COLLECTIONS_PATH=`pwd`/collections
```
Install the collection from the galaxy distro:

```
ansible-galaxy collection install  dellemc.openmanage --collections collections/
```

You can install the collection directly from github with:
```
ansible-galaxy collection install git+https://github.com/dell/dellemc-openmanage-ansible-modules.git,collections --collections collections/
```

## Set Up Your Hosts and Variables

Create hosts file that includes the idrac endpoint info for your nodes.   If you are managing multiple cluster you may want to put each under it's own heading for ease of references.

```
[bmc_nodes]
n01 idrac_ip='192.168.1.1' idrac_user='root' idrac_password='calvin'
n02 idrac_ip='192.168.1.2' idrac_user='root' idrac_password='calvin'
n03 idrac_ip='192.168.1.3' idrac_user='root' idrac_password='calvin'
```

Create a variables file to support your hosts.  For example in `group_vars/all`
```
VENV_PYTHON: "/path/to/venv/bin/python"
idrac_files_path="/absolute/path/for/output-and-input-files"
```

The rest of the variables are designed to specify on the command line, in particular for host selection of the playbook.

## Run a playbook

Get the configuration of a node
```
ansible-playbook -i hosts --extra-vars "host=n01" scp-export.yml
```
Note, you can replace `n01` with any host or host group in hosts. 


This will save a server configuration profile in your files_path location named for the IP address of the idrac card and timestamp.

The playbooks also save the output of the play to a file in the files_path named for the name in the hosts file a tag based on the playbook and a timestamp.  This can be helpful to inspect and is critical output for some playbooks.

## Customize Firmware Configuration

Learn more about working with server configuration profiles (scp) from the
[Server Cloning Guide](https://downloads.dell.com/solutions/dell-management-solution-resources/ServerCloning_SCP%20v2_50%28DTC%20copy%29.pdf).
This is a good read to familiarize yourself with the concepts and vocabulary.

A basic workflow with this playbooks is to export the SCP with `scp_export.yml`.
Edit the xml file to create a custom configuration profile that only needs to
include the specific configurations to change.  Then import that configuration
with `scp_import.yml`.  If the command result is not success, you can review
the Lifecycle Controller logs with `lc_log.yml` for information specfic to the
import job id (see the result file for job id).

You can see an example scp change configuration that switches the PXE boot port
from port 1 to port 3, for a machine with an embedded NIC that has 10G sfp
ports 1 & 2 and Cat5/6 ports 3 & 4.

