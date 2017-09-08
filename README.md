# pass-manager
A simple password manager. Store and retrieve passwords or password hints through the command line.
Copies password or password hint directly to the clipboard.


##### Usage:
Beside the main program, a file named `info.txt` initialized with an empty dictionary, '{}', must exist.


**Commands:**
- `python pw.py accountName hint/password` to add a new accountName and hint or password entry into `info.txt`
- `python pw.py accountName` to retrieve the accountName's info and copy to clipboard
- `python pw.py ls` to list all accountNames (dictionary keys).
- `python pw.py accountName del` to delete the accountName


**_Useful tip:_** to avoid typing `python pw.py` into the command line every time, I suggest you add the /path/to/the/mainFile to your $PATH variable.
An interpreter, or shebang is also required, which I have added in the first line of the main file (specify a specific version if needed). Then, simply rename `pw.py` to `pw`.
You may type `pw arg1 arg2` from anywhere in your shell. Enjoy.

##### Warning:
Store hints for value instead of your actual password for optimum security. Store passwords in plain text at your own risk.
