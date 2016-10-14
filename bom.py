#!/usr/bin/env python3

import sys
import os
import re

ZSHRC = os.path.expanduser("~/.zshrc")

rx_hash_command = re.compile(r'^\s*hash\s+-d\s+([\w_-]+)="?(.+)"?$')


def show_hashes():
    hashes = read_hashes_from_file()
    sorted_hashes = sorted([(hashes[h], h) for h in hashes])
    for t, h in sorted_hashes:
        print("{0} → {1}".format(h, t))


def add_hash(args):
    if len(args) == 0:
        new_target = os.path.realpath(os.getcwd()) + "/"
        new_hash = os.path.basename(os.path.dirname(new_target))
    elif len(args) == 1:
        if os.path.isdir(os.path.realpath(args[0])):
            new_target = os.path.realpath(args[0]) + "/"
            new_hash = os.path.basename(os.path.dirname(new_target))
        else:
            new_hash = args[0]
            new_target = os.path.realpath(os.getcwd()) + "/"
    elif len(args) == 2:
        new_hash = args[0]
        new_target = os.path.realpath(args[1]) + "/"
    else:
        print("Error: too many arguments")
        return

    if not re.match(r"^[\w_-]+$", new_hash):
        print("Error: The chosen bookmark {0} contains unsupported characters. Allowed are alphanumeric characters, '-' and '_'.".format(new_hash))
        return

    if re.match(r"^-|^\d+$", new_hash):
        print("Error: The chosen bookmark {0} is of illegal format. It must not start with '-' or consist only of numbers.".format(new_hash))
        return

    if not os.path.isdir(new_target):
        print("Hint: the directory {0} doesn't exist".format(new_target))

    hashes = read_hashes_from_file()
    if new_hash in hashes:
        print("Error: ~{0} already points to {1}".format(new_hash, hashes[new_hash]))
        return
    if new_target in hashes.values():
        already_defined = " and ".join(["~"+h for (h, t) in hashes.items() if t == new_target])
        print("Hint: {0} points to {1}, too".format(already_defined, new_target))
    hashes[new_hash] = new_target
    write_hashes_to_file(hashes)
    print('zshexec: hash -d {0}="{1}"'.format(new_hash, new_target))
    print("Created the bookmark ~{0} for {1}".format(new_hash, new_target))


def remove_hash(args):
    for to_be_removed in args:
        hashes = read_hashes_from_file()
        if to_be_removed not in hashes:
            print("There is no such bookmark: ~{0}".format(to_be_removed))
            continue
        removed_target = hashes.pop(to_be_removed)
        write_hashes_to_file(hashes)
        print("zshexec: unhash -d {0}".format(to_be_removed))
        print("Removed the bookmark ~{0} for {1}".format(to_be_removed, removed_target))


def read_hashes_from_file():
    result = {}
    with open(ZSHRC, "r") as hash_file:
        for line in hash_file:
            match = rx_hash_command.match(line)
            if match:
                h = match.group(1)
                target = match.group(2)
                target = target.strip('"')
                result[h] = target
    return result


def write_hashes_to_file(hashes):
    with open(ZSHRC, "r") as hash_file:
        zsh_content = hash_file.readlines()
        zsh_content = [line for line in zsh_content if not rx_hash_command.match(line)]
    for h in hashes:
        zsh_content.append('hash -d {0}="{1}"\n'.format(h, hashes[h]))
    with open(ZSHRC, "w") as hash_file:
        hash_file.writelines(zsh_content)


def show_help():
    print("""bom -- A simple bookmark manager for the zsh

Usage:

bom show                  shows all bookmarks
bom add foo /over/there/  creates a new bookmark ~foo for the directory /over/there/
bom add foo               creates a new bookmark ~foo for the current directory
bom add /over/there/      creates a new bookmark ~there (i.e. the last component) for the directory /over/there/
bom add                   creates a new bookmark for the current direcory, the name is the path's last component
bom rm foo bar            removes the bookmarks ~foo and ~bar

BTW: when adding or removing bookmarks, don't include the tilde in the
bookmark's name, that is, write 'bom add foo', not 'bom add ~foo'. That's
because the tilde is expanded by the Zsh.
""")
    exit()


def main():
    if len(sys.argv) <= 1:
        show_help()

    subcommand = sys.argv[1]

    if subcommand == "show":
        show_hashes()
    elif subcommand == "add":
        add_hash(sys.argv[2:])
    elif subcommand == "rm":
        remove_hash(sys.argv[2:])
    else:
        show_help()


if __name__ == "__main__":
    main()
