#!/usr/bin/env python

from fabric.api import local, lcd
import os
import sys
import json

def ensure_virtualenv():
    """
    Ensures that the project is running within a virtual env
    """
    if not hasattr(sys, "real_prefix"):
        raise Exception("You MUST run your projects inside a virtualenv!")
    return True

def install_requirements(proj_dir = "."):
    proj_dir = os.path.abspath(proj_dir)
    req_file = os.path.join(proj_dir, "requirements.txt")
    if os.path.isfile(req_file):
        with lcd(proj_dir):
            local("mkdir -p lib")
            local("pip install -r %s --root lib" % req_file)

def install_dependencies(proj_dir = "."):
    """
    Installs the dependencies as described in the project's (at proj_dir) package_spec.json file
    """
    proj_dir = os.path.abspath(proj_dir)
    pkg_file = os.path.join(proj_dir, "package_spec.json")
    if os.path.isfile(pkg_file):
        deps_dir = os.path.join(proj_dir, "deps")
        local("mkdir -p %s" % deps_dir)

        # use a temp dir locally
        currdir = os.path.abspath(os.curdir)
        package_spec = json.loads(open("./package_spec.json").read())

        appengine_config_path = os.path.join(proj_dir, "appengine_config.py")
        config_lines = [l.strip() for l in open(appengine_config_path).read().split("\n") if l.strip()]

        for dep in package_spec.get("dependencies", []):
            name = dep["name"]
            repo = dep["repo"]
            srcroot = dep.get("srcroot", name)

            with lcd(deps_dir):
                local("rm -Rf %s" % name)
                # clone it first
                local("git clone %s" % repo)

                vendor_line = "vendor.add('deps/%s')" % srcroot
                if vendor_line not in config_lines:
                    config_lines += vendor_line

        # Modify the appengine_config.py file to include these dependencies
        with open(appengine_config_path, "w") as configfile:
            configfile.write("\n".join(config_lines))
