SSH Connect
============

Simple wrapper to SSH to client machines from your Ansible controller.

How it Works
===============
This wrapper simple reads your inventory file looking for ssh ports, hostname and default username.


Why this is useful
=================
Sometimes it's difficult to remember what port does that specific host connects, the username as well.
I'm too lazy to read the file every damn time so I decided to write this wrapper for that work.