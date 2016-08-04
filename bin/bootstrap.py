#!/usr/bin/env python

from subprocess import call
import ipdb
import sys,os
import json

fabfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fabfile.py")
call(["fab", "-f", fabfile, "ensure_virtualenv"])
call(["fab", "-f", fabfile, "install_requirements"])
call(["fab", "-f", fabfile, "install_dependencies"])