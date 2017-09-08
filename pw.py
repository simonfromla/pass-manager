import argparse
import json
import pyperclip
import os
import sys


def add_new():
    """Add a new account and pass combination into the dictionary"""
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),
              "info.txt")) as acc_file:
        ACCOUNT_DATA = json.load(acc_file)

    new_acc, new_pw = sys.argv[1], sys.argv[2]

    confirm_new = input('Add "{new_acc}" with "{new_pw}" to the dictionary?'
                        '\ny or n\n'.format(new_acc=new_acc, new_pw=new_pw))
    if confirm_new == "y":
        ACCOUNT_DATA[new_acc] = new_pw
        with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                  "info.txt"), "r+") as acc_file:
            json.dump(ACCOUNT_DATA, acc_file)
        print("You have added {} to your dictionary".format(new_acc))
    else:
        print("You have not added a new account")


def retrieve():
    """Retrieve the value for a given account and copy it to the clipboard"""
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),
              "info.txt")) as acc_file:
        ACCOUNT_DATA = json.load(acc_file)
    account = sys.argv[1]
    if account in ACCOUNT_DATA:
        pyperclip.copy(ACCOUNT_DATA[account])
        print("Password for '{}' copied to clipboard.".format(account))
    else:
        print("There is no account named '{}'".format(account))


def update():
    """Update an existing account with a new value"""
    print("An account with this name already exists.")
    confirm_update = input('Update "{new_acc}" with "{new_pw}"?\n'
                           .format(new_acc=sys.argv[1], new_pw=sys.argv[2]))
    if confirm_update == "y":
        with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                  "info.txt"), "r+") as acc_file:
            ACCOUNT_DATA = json.load(acc_file)
            ACCOUNT_DATA.update({str(sys.argv[1]): sys.argv[2]})
            acc_file.truncate(0)
            acc_file.seek(0)
            json.dump(ACCOUNT_DATA, acc_file)
            print("{} has been updated.".format(sys.argv[1]))
    else:
        print("Not updated")


def delete():
    """Delete the given account from the dictionary"""
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),
              "info.txt"), "r+") as acc_file:
        ACCOUNT_DATA = json.load(acc_file)
        if sys.argv[1] in ACCOUNT_DATA:
            confirm_delete = input("Delete {}?\n".format(sys.argv[1]))
            if confirm_delete == "y":
                del ACCOUNT_DATA[sys.argv[1]]
                acc_file.truncate(0)
                acc_file.seek(0)
                json.dump(ACCOUNT_DATA, acc_file)
                print("{} has been removed from the dictionary.".format
                      (sys.argv[1]))
        else:
            print("Account does not exist. Did not delete.")


def main():
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),
              "info.txt")) as acc_file:
        ACCOUNT_DATA = json.load(acc_file)

    if len(sys.argv) < 2:
        print('usage: python3 {} account - copy account '
              'password\naccount: name of account whose pw to '
              'retrieve'.format(sys.argv[0]))
        sys.exit()

    elif sys.argv[1] == "ls":
        print("Usernames:")
        for key in ACCOUNT_DATA:
            print("-", key)

    elif len(sys.argv) == 3 and sys.argv[2] == "del":
        delete()
        sys.exit()

    elif len(sys.argv) == 2:
        retrieve()
        sys.exit()

    elif len(sys.argv) == 3 and not sys.argv[1] in ACCOUNT_DATA:
        add_new()
        sys.exit()

    elif len(sys.argv) == 3 and sys.argv[1] in ACCOUNT_DATA:
        update()
        sys.exit()

    elif len(sys.argv) > 3:
        print('Too many arguments passed. Try again.')


if __name__ == "__main__":
    main()
