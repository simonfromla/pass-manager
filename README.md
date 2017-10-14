# pass-manager
A simple password manager. Store and retrieve passwords through the command line without having your passwords saved in plain text.
Encryption obfuscates your passwords. On password retrieval, password is directly copied to your clipboard and available for immediate pasting.  


#### Usage:
Run the main program __pw.py__ and it will create and initialize __storage.json__ for you. __storage.json__ contains the key necessary to decrypt your passwords, as well as a dictionary of your account names + encrypted passwords.   

**Commands:**
- `python pw.py accountName hint/password` to add a new accountName and hint or password entry into __storage.json__
- `python pw.py accountName` to retrieve the accountName's info and copy to clipboard
- `python pw.py ls` to list all accountNames (dictionary keys).
- `python pw.py del accountName` to delete the accountName


**_tip:_** avoid typing `python pw.py` into the command line every time by adding the /path/to/the/mainFile to your $PATH variable.  
An interpreter, or shebang is also required, which has been added to the first line of the main file (specify a specific version if needed). Then, simply rename `pw.py` to `pw`.  
You may now type `pw arg1 arg2` from anywhere in your shell.
