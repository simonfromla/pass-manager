# A simple password retriever
import os
import json
import sys
import pyperclip


def addNew():

    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),
              "info.txt")) as accFile:
        ACCOUNT_DATA = json.load(accFile)

    newAcc = sys.argv[1]
    newPw = sys.argv[2]
    confirmNew = input("Add \"{0}\" with \"{1}\" to the dictionary?"
                       "\ny or n\n".format(newAcc, newPw))

    if confirmNew == "y":
        ACCOUNT_DATA[newAcc] = newPw
        print("You have added {} to your dictionary".format(newAcc))
    else:
        print("You have not added a new account")

    accString = json.dumps(ACCOUNT_DATA)

    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),
              "info.txt"), "r+") as accFile:
        accFile.write(accString)


def retrieve():

    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),
              "info.txt")) as accFile:
        ACCOUNT_DATA = json.load(accFile)

    account = sys.argv[1]

    if account in ACCOUNT_DATA:
        pyperclip.copy(ACCOUNT_DATA[account])
        print("Password for '{}' copied to clipboard.".format(account))
    else:
        print("There is no account named '{}'".format(account))


def update():

    print("An account with this name already exists.")

    accFile = open(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                   "info.txt"), "r+")

    ACCOUNT_DATA = json.load(accFile, strict=False)
    confirmUpdate = input("Update '{0}' with '{1}'?\n"
                          .format(sys.argv[1], sys.argv[2]))
    if confirmUpdate == "y":
        ACCOUNT_DATA.update({str(sys.argv[1]): sys.argv[2]})
    else:
        print("Not updated")

    accString = json.dumps(ACCOUNT_DATA)
    accString.replace('“', '"')
    accFile.truncate(0)
    accFile.seek(0)
    accFile.write(accString)
    accFile.close()
    print("{} has been updated.".format(sys.argv[1]))


def main():

    accFile = open(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                   "info.txt"))
    ACCOUNT_DATA = json.load(accFile, strict=False)
    accFile.close()

    if len(sys.argv) < 2:
        print('usage: python3 {} account - copy account '
              'password\naccount: name of account whose pw to '
              'retrieve'.format(sys.argv[0]))
        sys.exit()

# TO-DO
# if len==3, and argv2==del, func()--> if argv1 in Dict, del. else "acc not exist"
    elif len(sys.argv) == 3 and sys.argv[1] in ACCOUNT_DATA and sys.argv[2] == "del":
        confirmDelete = input("Delete {}?".format(sys.argv[1]))
        if confirmDelete == "y":
            del ACCOUNT_DATA[sys.argv[1]]
            with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                      "info.txt"), "r+") as accFile:
                accString = json.dumps(ACCOUNT_DATA)
                accFile.truncate(0)
                accFile.seek(0)
                accFile.write(accString)
        else:
            sys.exit()

    elif len(sys.argv) == 2:
        retrieve()
        sys.exit()

    elif len(sys.argv) == 3 and not sys.argv[1] in ACCOUNT_DATA:
        addNew()
        sys.exit()

    elif len(sys.argv) == 3 and sys.argv[1] in ACCOUNT_DATA:
        update()
        sys.exit()

    elif len(sys.argv) > 3:
        print('Too many arguments passed. Try again.')

    elif sys.argv[1] == "ls":
        print("Usernames:")
        for key in ACCOUNT_DATA.keys():
            print("-", key)


if __name__ == "__main__":
    main()

# print(__file__)
# print(os.path.join(os.path.dirname(__file__), '..'))
# print(os.path.dirname(os.path.realpath(__file__)))
# print(os.path.abspath(os.path.dirname(__file__)))
