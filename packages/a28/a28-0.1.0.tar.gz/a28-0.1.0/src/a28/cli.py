#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: encoding=utf-8 ts=4 et sts=4 sw=4 tw=79 fileformat=unix nu wm=2

#    _                ___ ___   _____       _             _           _
#   /_\  _ _ ___ __ _|_  | _ ) |_   _|__ __| |_  _ _  ___| |___  __ _(_)___ ___
#  / _ \| '_/ -_) _` |/ // _ \   | |/ -_) _| ' \| ' \/ _ \ / _ \/ _` | / -_|_-<
# /_/ \_\_| \___\__,_/___\___/   |_|\___\__|_||_|_||_\___/_\___/\__, |_\___/__/
#                                                               |___/

"""
Build packages to be submitted to Area28.
"""

# built-in
import argparse
import logging

# project
import a28


# enable logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)


def main():
    """Main command line entry point."""

    parser = argparse.ArgumentParser(description="package manager")
    subparsers = parser.add_subparsers(
        dest='action',
        required=True,
        help="actions"
    )

    parser_build = subparsers.add_parser(
        "build",
        help="build package"
    )
    parser_build.set_defaults(func=build)
    parser_build.add_argument(
        "--src",
        required=True,
        help="plugin source directory"
    )
    parser_build.add_argument(
        "--dest",
        default="",
        help="destination directory"
    )

    parser_install = subparsers.add_parser(
        "install",
        help="install package"
    )
    parser_install.set_defaults(func=install)
    parser_install.add_argument(
        "--pkg",
        required=True,
        help="plugin a28 package file"
    )

    args = parser.parse_args()
    args.func(args)


def build(args):
    """ Build package. """
    src = args.src
    dest = args.dest
    meta = a28.get_info(src)
    pkg = a28.package(src, dest, meta)
    print(pkg)


def install(args):
    """ install / update the local package. """
    pkg_hash = a28.generate_hash(args.pkg)
    meta = a28.extract_meta(args.pkg)
    meta["hash"] = pkg_hash
    a28.install(args.pkg, meta)
    print("installed {}".format(meta["name"]))
