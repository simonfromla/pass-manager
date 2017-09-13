#!/usr/bin/env python
import json
import pyperclip
import os
import sys

DEFAULT_LOCATION = os.environ.get('INFO_LOCATION') or os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "info.txt")


def load_manager(fp=None):
    """logic for loading account dict from file. Uses
        json module to unserialize data in the file"""
    if fp is None:
        fp = DEFAULT_LOCATION
    with open(fp) as file:
        acc_dict = json.load(file)
    return acc_dict


def write_to_file(data, fp=None):
    """json-serializes data and writes it to filepath."""
    if fp is None:
        fp = DEFAULT_LOCATION
    with open(fp, 'w') as file:
        file.truncate(0)
        json.dump(data, file)
        # file.seek(0)


def add_new(account, new_value, fp=None):
    """Add a new account and pass combination into the dictionary"""
    account_dict = load_manager(fp)
    account_dict[account] = new_value
    try:
        write_to_file(account_dict, fp)
        print("Saved new entry!")
    except Exception as e:
        print("Something went wrong: {}".format(e))


def retrieve(account, fp=None):
    """Retrieve the value for a given account and copy it to the clipboard"""
    account_dict = load_manager(fp)
    if account in account_dict:
        pyperclip.copy(account_dict[account])
        print("Value for '{}' copied to clipboard.".format(account))
    else:
        print("There is no account named '{}'.".format(account))


def update(account, new_value, fp=None):
    """Update an existing account with a new value"""
    account_dict = load_manager(fp)
    account_dict.update({account: new_value})

    try:
        write_to_file(account_dict, fp)
        print("Updated the entry!")
    except Exception as e:
        print("Something went wrong: {}".format(e))


def delete(account, fp=None):
    """Delete the given account from the dictionary"""
    account_dict = load_manager(fp)
    del account_dict[account]
    try:
        write_to_file(account_dict, fp)
        print("'{}' has been removed from the dictionary.".format(
            account))
    except Exception as e:
        print("Something went wrong: {}".format(e))


def main():
    account_dict = load_manager()
    num_args = len(sys.argv)
    if num_args < 2:
        print('usage: python3 {} account - copy corresponding account '
              'value\naccount: name of account whose value to '
              'retrieve'.format(__file__))
        sys.exit()

    elif num_args == 2:
        # List
        if sys.argv[1] == "ls":
            print("Usernames:")
            for key in account_dict:
                print("-", key)
        else:
            retrieve(sys.argv[1])
            sys.exit()

    elif num_args == 3:
        if sys.argv[1] == "del":
            # Delete
            if sys.argv[2] in account_dict:
                confirm_delete = input("Delete '{}'?\n(y/n)\n".format(
                    sys.argv[2]))
                if confirm_delete == "y":
                    delete(sys.argv[2])
                    sys.exit()
                else:
                    print("Did not delete.")
            else:
                print("{} does not exist. Did not delete.".format(sys.argv[2]))

        elif sys.argv[1] not in account_dict:
            # Add new
            confirm_new = input('Add "{new_acc}" with "{new_val}" to the '
                                'dictionary?\n(y/n)\n'.format(
                                    new_acc=sys.argv[1], new_val=sys.argv[2]))
            if confirm_new == "y":
                add_new(sys.argv[1], sys.argv[2])
                sys.exit()

        elif sys.argv[1] in account_dict:
            # Update
            print("An account with this name already exists.")
            confirm_update = input('Update "{new_acc}" with "{new_val}"?\n'
                                   '(y/n)\n'.format(
                                       new_acc=sys.argv[1],
                                       new_val=sys.argv[2]))
            if confirm_update == "y":
                update(sys.argv[1], sys.argv[2])
                sys.exit()
            else:
                print("Not updated.")
    else:
        print('Too many arguments passed. Try again.')


if __name__ == "__main__":
    main()
