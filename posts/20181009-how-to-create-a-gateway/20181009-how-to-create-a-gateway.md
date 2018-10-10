# Gateway

A gateway is a jump-only host that serves the purpose of exposing a little bit of the infrastructure to the Internet, in a secure manner, so that the internal infrastructure can be accessed.

There are several options for this, like VPNs, but we choose SSH for its simplicity and being a standard.

## Implementation

We used Alpine Linux for it's very low resource usage to create a VM and expose it to the Internet. This guide is specifically written for Alpine but any other modern distro can be used.

## Configuration overview

The system is a default Alpine Linux with UFW for firewall and SSH.  
The following two user groups are created:

* `ssh-user`: VM administrators, that require being able to log in.
* `ssh-jumper`: Regular users that are not allowed to log in.

These are regular user groups in Linux but we will use them to configure SSH.

### Setting up firewall

UFW is very easy to use and acts as an iptables CLI front-end. We are going to set up a very strict IN/OUT policy: limit SSH access, disable any other access and allow only HTTP(S), DNS and SSH requests to leave the system.

Once enabled, you can list current rules with `ufw status numbered` which will list them with an index. To delete a rule, issue `ufw delete {index}`. *Be careful because the index changes every time the command is executed! So issue again `ufw status numbered` after every `delete`*.

Run as root and respect the order or you might end up kicked-out of the machine:

```shell
ufw disable
ufw default deny incoming
ufw default deny outgoing
ufw limit in ssh/tcp
ufw allow out ssh/tcp
ufw allow out dns         # both TCP and UDP
ufw allow out ntp/udp
ufw allow out http/tcp
ufw allow out https/tcp
# List rules and verify all is OK
ufw show added
# Enable now
ufw enable
```

### Creating admin users

An admin user must have a standard terminal such as `/bin/ash` and must belong to `ssh-user` group.

```shell
adduser -s /bin/ash admin
adduser admin ssh-user
```

### Creating jumper users

A regular "jumper" user must not have a terminal set, such as `/bin/false`, and must belong to `ssh-jumper` group.

```shell
adduser -s /bin/false jumper
adduser jumper ssh-jumper
```

### SSH configuration

A standard SSH config can be used, we'll do a slight modification to it. We recommend using this [modern secure SSH configuration](https://gist.github.com/HacKanCuBa/fe3653d4fe4eed35e41dcc9a380499c2).  
The necessary modifications are as follow:

```
AllowAgentForwarding yes    # This allows jumping
AllowTcpForwarding yes      # This allows TCP tunnelling
X11Forwarding no            # This is VERY insecure, always disable
Compression no              # Disable compression whenever possible to prevent attacks on crypto

AllowGroups ssh-user ssh-jumper    # Allow both groups
# But restrict jumpers
Match Group ssh-jumper
	ForceCommand echo 'This account can only be used for host jump'    # This is just a precaution
	PermitTTY no
	PermitUserRC no
```

