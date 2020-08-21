#!/usr/bin/env python3
"""
Test
"""
import argparse
import os
from glob import glob
import shutil
import tarfile


USER_PATH = os.path.expanduser('~')

try:
    os.makedirs(f'{USER_PATH}/.provim/profiles/', exists_ok=True)
except OSError:
    print(f'Could not create {USER_PATH}/.provim/profiles/. Aborting!')
    exit(1)


def get_active_profile(profiles):
    if not os.path.islink(
            f'{USER_PATH}/.vim') or not os.path.islink(f'{USER_PATH}/.vimrc'):
        return None

    for p in profiles:
        if f'{USER_PATH}/.provim/profiles/{p}/' == os.readlink(
                f'{USER_PATH}/.vim') and f'{USER_PATH}/.provim/profiles/{p}/.vimrc' == os.readlink(f'{USER_PATH}/.vimrc'):
            return p

    return None


def find_profiles():
    for profile in glob(f'{USER_PATH}/.provim/profiles/*/'):
        yield profile.split('/')[-2]


def switch_profile(profile):
    if os.path.exists(
            f'{USER_PATH}/.vim/') or os.path.exists(f'{USER_PATH}/.vimrc'):
        if not os.path.islink(
                f'{USER_PATH}/.vim') or not os.path.islink(f'{USER_PATH}/.vimrc'):
            print(
                f'{USER_PATH}/.vimrc and {USER_PATH}/.vim/ are not handled by provim! Please remove them to continue!')
            print('As an alternative you can migrate them with the -m flag')
            return None

        os.remove(f'{USER_PATH}/.vim')
        os.remove(f'{USER_PATH}/.vimrc')

    os.symlink(f'{USER_PATH}/.provim/profiles/{profile}/', f'{USER_PATH}/.vim')
    os.symlink(
        f'{USER_PATH}/.provim/profiles/{profile}/.vimrc',
        f'{USER_PATH}/.vimrc')


def create_profile(profile):
    os.mkdir(f'{USER_PATH}/.provim/profiles/{profile}')
    open(f'{USER_PATH}/.provim/profiles/{profile}/.vimrc', 'a').close()


def migrate_vim():
    if os.path.exists(f'{USER_PATH}/.vim'):
        shutil.move(
            f'{USER_PATH}/.vim/',
            f'{USER_PATH}/.provim/profiles/migrated/')

    if os.path.exists(f'{USER_PATH}/.vimrc'):
        shutil.move(
            f'{USER_PATH}/.vimrc',
            f'{USER_PATH}/.provim/profiles/migrated/.vimrc')
    else:
        open(f'{USER_PATH}/.provim/profiles/migrated/.vimrc', 'a').close()


def export_profile(profile):
    with tarfile.TarFile(f'{profile}.tar', mode='w') as archive:
        archive.add(
            f'{USER_PATH}/.provim/profiles/{profile}',
            arcname=profile,
            recursive=True)


def import_profile(filename):
    tar_file = tarfile.TarFile(f'{filename}', mode='r')
    tar_file.extractall(f'{USER_PATH}/.provim/profiles/')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--list', action='store_true')
    parser.add_argument('-c', '--create')
    parser.add_argument('-d', '--delete')
    parser.add_argument('-s', '--switch')
    parser.add_argument('-m', '--migrate', action='store_true')
    parser.add_argument('-e', '--export_profile')
    parser.add_argument('-i', '--import_profile')

    arguments = parser.parse_args()

    profiles = list(find_profiles())
    active_profile = get_active_profile(profiles)

    if arguments.list:
        for p in profiles:
            print(f'{"*" if active_profile == p else ""}{p}')
    elif arguments.switch:
        if arguments.switch not in profiles:
            print(f'{arguments.switch} is not a valid profile!')
        else:
            switch_profile(arguments.switch)
    elif arguments.create:
        create_profile(arguments.create)
    elif arguments.migrate:
        migrate_vim()
        switch_profile('migrated')

    elif arguments.export_profile:
        export_profile(arguments.export_profile)

    elif arguments.import_profile:
        import_profile(arguments.import_profile)


if __name__ == '__main__':
    main()
