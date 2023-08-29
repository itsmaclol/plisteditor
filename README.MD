# CLI Plist Editor in Python3

# Installation
The script can either be found here on this github repo or [on my cdn](https://cdn.itsmac.eu.org/plisteditor.py)

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

Made with <3 by Mac
