[nodes]
${nodes}
[insecuressh:children]
nodes

[insecuressh:vars]
ansible_ssh_common_args='-o StrictHostKeyChecking=no'
