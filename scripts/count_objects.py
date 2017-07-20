#!/usr/bin/env python3

import subprocess

if __name__ == '__main__':
    cmd = subprocess.Popen("ldapsearch -x -b 'dc=my-domain,dc=com' '(objectclass=*)'", shell=True, stdout=subprocess.PIPE)
    for line in cmd.stdout:
        if b"numEntries" in line:
            new = line.decode("utf-8").rstrip()[-1:]
            print(new)