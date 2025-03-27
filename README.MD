# CLI Plist Editor in Python3

# Installation
You can either clone this repo by
`git clone https://github.com/itsmaclol/plisteditor.git` or download the script from the repo

# Examples
Adding a new plist entry:
```
python3 plisteditor.py add path.to.plist.entry --type type.of.plist.entry --path path/to/plist/file.plist
```
Deleting an existing plist entry:
```
python3 plisteditor.py delete path.to.plist.entry --path path/to/plist/file.plist
```
Setting an existing plist entry to something else:
```
python3 plisteditor.py set path.to.plist.entry --type type.of.plist.entry --value value_you_want_to_set --path path/to/plist/file.plist
```
Changing an exising plist entry to another type:
```
python3 plisteditor.py change path.to.plist.entry --new_type type_of_plist_entry --path path/to/plist/file.plist
```

# Flags
The `-s` flag can be used to make the script not output a message after its done running

Made with <3 by Mac, BibiFire, ChatGPT
