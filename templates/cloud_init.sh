#cloud-config
timezone: America/Los_Angeles
ssh_pwauth: True
disable_root: false
password: c0ntrail123
chpasswd:
  list: |
    root:c0ntrail123
  expire: False

runcmd:
  - sed -i -e '/^PermitRootLogin/s/^.*$/PermitRootLogin yes/' /etc/ssh/sshd_config
  - service sshd restart
