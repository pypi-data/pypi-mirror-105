# pid-file-checker

```
$ pfc --help
usage: pfc [-h] pid_file

Check for the presence of a pid file. The file must contain one and only one
integer which must be the pid of a running process. Otherwise, return a code
!= 0. Meant to be used in a healthcheck context like with Docker or
Kubernetes.

positional arguments:
  pid_file    The pid file you want to monitor

optional arguments:
  -h, --help  show this help message and exit

Brought to you by IT4NW@ITSF.
```
