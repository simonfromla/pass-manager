# pass-manager
A simple password manager. Store and retrieve passwords or password hints through the command line. Copies password or password hint directly to the clipboard.


**Usage:**
On root, create a file named `info.txt` initialized with an empty dictionary, '{}'

**Commands:**
- `python3 pw.py accountName` to retrieve the accountName's info and copy to clipboard
- `python3 pw.py ls` to list all accountNames (dictionary keys).
- `python3 pw.py accountName del` to delete the accountName
- `python3 pw.py accountName hint/password` to add a new accountName and hint or password entry into `info.txt`

Usage tips:
Store hints for value instead of actual password for optimum security. Store passwords in plain text at your own risk.
