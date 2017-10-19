#!/usr/bin/env python3
import json
import pyperclip
import os
import sys
from cryptography.fernet import Fernet


def add_new(account, new_value, storage, f, fp=None):
    """Add a new account and pass combination into the dictionary"""
    storage["accounts"].append({account: encrypt(
                                new_value, f).decode("utf-8")})
    try:
        write_to_file(storage, fp)
        print("Saved new entry!")
    except Exception as e:
        print("Something went wrong: {}".format(e))


def decrypt(token, f):
    return f.decrypt(token)


def delete(account, storage, fp=None):
    """Delete the given account from the dictionary"""
    storage["accounts"] = [d for d in storage["accounts"]
                           if account not in d]  # reconstruct dict
    try:
        write_to_file(storage, fp)
        print("'{}' has been removed from the dictionary.".format(
            account))
    except Exception as e:
        print("Something went wrong: {}".format(e))


def encrypt(pw, f):
    token = f.encrypt(bytes(pw, "utf-8"))
    return token


def exist_in_storage(arg, storage):
    for i in storage:
        if arg in storage:
            return True
    if storage["accounts"]:
        for i in storage["accounts"]:
            if arg in i:
                return True
    return False


def initialize():
    with open("storage.json", "w") as file:
        if os.stat("storage.json").st_size == 0:
            file.write("{}")
    return


def initialize_storage():
    storage = load_manager()
    key = Fernet.generate_key()
    f = Fernet(key)
    key = key.decode("utf-8")
    storage["key"] = key
    storage["accounts"] = []
    write_to_file(storage)
    return f


def load_manager():
    with open("storage.json", "r") as file:
        storage = json.load(file)
        return storage


def ls(storage):
    print("*****Usernames*****")
    sorted_list = sorted([list(i.keys())[0] for i in storage["accounts"]])
    for a in sorted_list:
        print(" -", a)


def retrieve(account, storage, f, fp=None):
    """Retrieve the value for a given account and copy it to the clipboard"""
    if exist_in_storage(account, storage):
        for accounts in storage["accounts"]:
            if account in accounts:
                token_string = accounts.get(account)
                token = bytes(token_string, "utf-8")
                decrypted_pw_bytes = decrypt(token, f)
                pyperclip.copy(decrypted_pw_bytes.decode("utf-8"))
                print("Value for '{}' copied to clipboard.".format(account))
                return pyperclip.paste()
    else:
        print("There is no account named '{}'.".format(account))


def update(account, new_value, storage, f, fp=None):
    """Update an existing account with a new value"""
    new_enc_val = encrypt(new_value, f)
    enc_str = new_enc_val.decode("utf-8")
    for i in storage["accounts"]:
        if account in i:
            i[account] = enc_str

    try:
        write_to_file(storage, fp)
        print("Updated the entry!")
    except Exception as e:
        print("Something went wrong: {}".format(e))


def write_to_file(data, fp=None):
    """json-serializes data and writes it to filepath."""
    with open("storage.json", 'w') as file:
        file.truncate(0)
        json.dump(data, file)


def main():
    if not os.path.exists("storage.json"):
        initialize()
        f = initialize_storage()
        storage = load_manager()
    else:
        storage = load_manager()
        key = storage["key"]
        bytes(key, "utf-8")
        f = Fernet(key)

    num_args = len(sys.argv)

    if num_args < 2:
        print('usage: python3 {} account - copy corresponding account '
              'value\naccount: name of account whose value to '
              'retrieve'.format(__file__))
        sys.exit()
    # List
    elif num_args == 2:
        if sys.argv[1] == "ls":
            ls(storage)
        # Retrieve
        else:
            retrieve(sys.argv[1], storage, f)
            sys.exit()

    # Delete
    elif num_args == 3:
        if sys.argv[1] == "del":
            if exist_in_storage(sys.argv[2], storage):
                confirm_delete = input("Delete '{}'?\n(y/n)\n".format(
                    sys.argv[2]))
                if confirm_delete == "y":
                    delete(sys.argv[2], storage)
                else:
                    print("Did not delete.")
            else:
                print("{} does not exist. Did not delete.".format(sys.argv[2]))

        # Add new
        elif not exist_in_storage(sys.argv[1], storage):
            confirm_new = input('Add "{new_acc}" with "{new_val}" to the '
                                'dictionary?\n(y/n)\n'.format(
                                    new_acc=sys.argv[1], new_val=sys.argv[2]))
            if confirm_new == "y":
                add_new(sys.argv[1], sys.argv[2], storage, f)

        # Update
        elif exist_in_storage(sys.argv[1], storage):
            print("An account with this name already exists.")
            confirm_update = input('Update "{new_acc}" with "{new_val}"?\n'
                                   '(y/n)\n'.format(
                                       new_acc=sys.argv[1],
                                       new_val=sys.argv[2]))
            if confirm_update == "y":
                update(sys.argv[1], sys.argv[2], storage, f)
            else:
                print("Not updated.")
    else:
        print('Too many arguments passed. Try again.')


if __name__ == "__main__":
    main()
