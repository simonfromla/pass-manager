#!/usr/bin/env python
from cryptography.fernet import Fernet
import json
import pyperclip
import os
import sys

# DEFAULT_LOCATION = os.environ.get('INFO_LOCATION') or os.path.join(
#     os.path.abspath(os.path.dirname(__file__)), "info.txt")


def encrypt(pw, f):
    token = f.encrypt(bytes(pw, "utf-8"))
    return token


def decrypt(token, f):
    return f.decrypt(token)


def load_manager():
    with open("storage.json", "a+") as file:
        if os.stat("storage.json").st_size == 0:
            file.write("{}")
        file.seek(0)
        storage = json.load(file)
        return storage

def write_to_file(data, fp=None):
    """json-serializes data and writes it to filepath."""
    # if fp is None:
    #     fp = DEFAULT_LOCATION
    # maybe write to a temp file first here, then move it instead
    with open("storage.json", 'w') as file:
        file.truncate(0)
        json.dump(data, file)
        # file.seek(0)


def add_new(account, new_value, f, fp=None):
    """Add a new account and pass combination into the dictionary"""
    account_dict = load_manager()
    # if account in account_dict:
    #     raise ValueError("Account {} is already a managed account."
    #                       "Use update instead.".format(account))

    account_dict["accounts"].append({account: encrypt(new_value, f).decode("utf-8")})
    try:
        write_to_file(account_dict, fp)
        print("Saved new entry!")
    except Exception as e:
        print("Something went wrong: {}".format(e))


def retrieve(account, f, fp=None):
    """Retrieve the value for a given account and copy it to the clipboard"""
    storage = load_manager()
    if exist_in_storage(account, storage):
        for accounts in storage["accounts"]:
            if account in accounts:
                token_string = accounts.get(account)
                token = bytes(token_string, "utf-8")
                decrypted_pw_bytes = decrypt(token, f)
                pyperclip.copy(decrypted_pw_bytes.decode("utf-8"))
                print("Value for '{}' copied to clipboard.".format(account))
    else:
        print("There is no account named '{}'.".format(account))


def update(account, new_value, f, fp=None):
    """Update an existing account with a new value"""
    account_dict = load_manager()
    new_enc_val = encrypt(new_value, f)
    enc_str = new_enc_val.decode("utf-8")
    for i in account_dict["accounts"]:
        if account in i:
            i[account] = enc_str

    try:
        write_to_file(account_dict, fp)
        print("Updated the entry!")
    except Exception as e:
        print("Something went wrong: {}".format(e))


def delete(account, fp=None):
    """Delete the given account from the dictionary"""
    account_dict = load_manager()
    for i in account_dict["accounts"]:
        if account in i:
            del i[account]
            print(account_dict)
    try:
        write_to_file(account_dict, fp)
        print("'{}' has been removed from the dictionary.".format(
            account))
    except Exception as e:
        print("Something went wrong: {}".format(e))


def exist_in_storage(arg, account_dict):
    for i in account_dict["accounts"]:
        if arg in i:
            return True
    return False


def main():
    account_dict = load_manager()
    if not account_dict["key"]:
        key = Fernet.generate_key()
    else:
        key = account_dict["key"]
        bytes(key, "utf-8")
        f = Fernet(key)
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
            {print("- {}".format(key)) for key in sorted(account_dict)}
        else:
            retrieve(sys.argv[1], f)
            sys.exit()

    # Delete
    elif num_args == 3:
        if sys.argv[1] == "del":
            # Delete
            if exist_in_storage(sys.argv[2], account_dict):
                confirm_delete = input("Delete '{}'?\n(y/n)\n".format(
                    sys.argv[2]))
                if confirm_delete == "y":
                    delete(sys.argv[2])
                    sys.exit()
                else:
                    print("Did not delete.")
            else:
                print("{} does not exist. Did not delete.".format(sys.argv[2]))

        # Add new
        # elif sys.argv[1] not in [print(key) for key in account_dict["accounts"]]:
        elif not exist_in_storage(sys.argv[1], account_dict):
            # Add new
            confirm_new = input('Add "{new_acc}" with "{new_val}" to the '
                                'dictionary?\n(y/n)\n'.format(
                                    new_acc=sys.argv[1], new_val=sys.argv[2]))
            if confirm_new == "y":
                add_new(sys.argv[1], sys.argv[2], f)
                # sys.exit()

        # Update
        elif exist_in_storage(sys.argv[1], account_dict):
            print("An account with this name already exists.")
            confirm_update = input('Update "{new_acc}" with "{new_val}"?\n'
                                   '(y/n)\n'.format(
                                       new_acc=sys.argv[1],
                                       new_val=sys.argv[2]))
            if confirm_update == "y":
                update(sys.argv[1], sys.argv[2], f)
                sys.exit()
            else:
                print("Not updated.")
    else:
        print('Too many arguments passed. Try again.')




if __name__ == "__main__":
    main()
