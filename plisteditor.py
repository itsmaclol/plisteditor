import argparse
import plistlib
from collections.abc import MutableMapping

entry_types = {
    "dict": {},
    "bool": False,
    "int": 0,
    "float": 0.0,
    "data": b"",
    "string": "",
    "array": [],
}


def load_plist(file_path):
    with open(file_path, 'rb') as plist_file:
        return plistlib.load(plist_file)


def save_plist(file_path, plist_data):
    with open(file_path, 'wb') as plist_file:
        plistlib.dump(plist_data, plist_file)


def delete_entry(plist_data, entry_path, silent=False):
    keys = entry_path.split('.')
    current_data = plist_data
    for key in keys[:-1]:
        current_data = current_data[key]
    deleted_value = current_data.pop(keys[-1], None)
    if not silent:
        if deleted_value is not None:
            print(f"Entry '{entry_path}' deleted successfully.")
        else:
            print(f"Entry '{entry_path}' not found.")


def add_entry(plist_data, entry_path, entry_type, silent=False):
    keys = entry_path.split('.')
    current_data = plist_data
    for key in keys[:-1]:
        if key not in current_data:
            current_data = current_data[int(key)]
        else:
            current_data = current_data[key]

    last_key = keys[-1]

    if isinstance(current_data, list) and last_key.isdigit():
        current_data.append(None)
        last_key = int(last_key)
        current_data[last_key] = create_entry(entry_type)
    else:
        current_data[last_key] = create_entry(entry_type)

    if not silent:
        print(f"Entry '{entry_path}' as '{entry_type}' added successfully.")


def create_entry(entry_type):
    try:
        return entry_types[entry_type]
    except KeyError:
        raise ValueError("Invalid entry type")


def set_entry(plist_data, entry_path, entry_type, entry_value, silent=False):
    keys = entry_path.split('.')
    current_data = plist_data
    for key in keys[:-1]:

        if isinstance(current_data, list):
            current_data = current_data[int(key)]
        else:
            current_data = current_data[key]

    if keys[-1] not in current_data:
        raise ValueError(f"Entry '{entry_path}' does not exist")

    if entry_type == 'bool':
        if entry_value.lower() == 'true':
            current_data[keys[-1]] = True
        elif entry_value.lower() == 'false':
            current_data[keys[-1]] = False
        else:
            raise ValueError("Invalid bool value")
    elif entry_type == "int":
        current_data[keys[-1]] = int(entry_value)
    elif entry_type == 'float':
        current_data[keys[-1]] = float(entry_value)
    elif entry_type == 'data':
        current_data[keys[-1]] = bytes.fromhex(entry_value)
    elif entry_type == 'string':
        current_data[keys[-1]] = entry_value
    else:
        raise ValueError("Invalid entry type")

    if not silent:
        print(f"Entry '{entry_path}' set as '{entry_value}' of type '{entry_type}' successfully.")


def change_entry_type(plist_data, entry_path, new_type, silent=False):
    keys = entry_path.split('.')
    current_data = plist_data
    for key in keys[:-1]:
        current_data = current_data[key]

    if keys[-1] not in current_data:
        raise ValueError(f"Entry '{entry_path}' does not exist")

    current_value = current_data[keys[-1]]
    new_value = create_entry(new_type)

    current_data[keys[-1]] = new_value
    if not silent:
        print(f"Entry '{entry_path}' changed to '{new_type}' type successfully.")


def print_entry(plist_data, entry_path):
    keys = entry_path.split('.')
    current_data = plist_data
    for key in keys:
        try:
            if isinstance(current_data, MutableMapping):
                current_data = current_data[key]
            elif isinstance(current_data, list) and key.isdigit():
                current_data = current_data[int(key)]
            else:
                raise ValueError(f"Entry '{entry_path}' does not exist")
        except (KeyError, IndexError):
            raise ValueError(f"Entry '{entry_path}' does not exist")

    print(f"{current_data}")


def append_to_string(plist_data, entry_path, entry_type, entry_value, silent=False):
    keys = entry_path.split('.')
    current_data = plist_data
    for key in keys:
        try:
            if isinstance(current_data, MutableMapping):
                current_data = current_data[key]
            elif isinstance(current_data, list) and key.isdigit():
                current_data = current_data[int(key)]
            else:
                raise ValueError(f"Entry '{entry_path}' does not exist")
        except (KeyError, IndexError):
            raise ValueError(f"Entry '{entry_path}' does not exist")

    if entry_type != 'string':
        raise ValueError("Can only append to string entries")

    if not isinstance(current_data, str):
        raise ValueError(f"Entry '{entry_path}' is not a string")

    current_data += entry_value  # Use += to append the value to the string

    # Update the original plist_data with the modified string
    keys = entry_path.split('.')
    parent_data = plist_data
    for key in keys[:-1]:
        parent_data = parent_data[key]

    parent_data[keys[-1]] = current_data

    if not silent:
        print(f"Appended '{entry_value}' to '{entry_path}' successfully.")

def remove_value_from_string(plist_data, entry_path, entry_type, entry_value, silent=False):
    keys = entry_path.split('.')
    current_data = plist_data
    for key in keys:
        try:
            if isinstance(current_data, MutableMapping):
                current_data = current_data[key]
            elif isinstance(current_data, list) and key.isdigit():
                current_data = current_data[int(key)]
            else:
                raise ValueError(f"Entry '{entry_path}' does not exist")
        except (KeyError, IndexError):
            raise ValueError(f"Entry '{entry_path}' does not exist")

    if entry_type != 'string':
        raise ValueError("Can only remove from string entries")

    if not isinstance(current_data, str):
        raise ValueError(f"Entry '{entry_path}' is not a string")

    if entry_value not in current_data:
        raise ValueError(f"'{entry_value}' not found in '{entry_path}'")

    current_data = current_data.replace(entry_value, '').strip()  # Use strip() to remove extra spaces

    current_data = current_data.replace(entry_value, '')

    # Update the original plist_data with the modified string
    keys = entry_path.split('.')
    parent_data = plist_data
    for key in keys[:-1]:
        parent_data = parent_data[key]

    parent_data[keys[-1]] = current_data

    if not silent:
        print(f"Removed '{entry_value}' from '{entry_path}' successfully.")

def main():
    parser = argparse.ArgumentParser(description="CLI Plist Editor")
    parser.add_argument("action", choices=["delete", "add", "set", "change", "print", "append", "remvalue"],
                        help="Action to perform")
    parser.add_argument("entry_path", help="Path to the plist entry")
    parser.add_argument("--type", help="Type of plist entry (for 'add' action)")
    parser.add_argument("--new_type", help="New type of plist entry (for 'change' action)")
    parser.add_argument("--value", help="Value of plist entry (for 'set' action)")
    parser.add_argument("--path", required=True, help="Path to the plist file")
    parser.add_argument("-s", "--silent", action="store_true", help="Silent mode (no success messages)")

    args = parser.parse_args()

    plist_data = load_plist(args.path)

    if args.action == 'delete':
        delete_entry(plist_data, args.entry_path, args.silent)
    elif args.action == 'add':
        add_entry(plist_data, args.entry_path, args.type.lower(), args.silent)
    elif args.action == 'set':
        set_entry(plist_data, args.entry_path, args.type.lower(), args.value, args.silent)
    elif args.action == 'change':
        change_entry_type(plist_data, args.entry_path, args.new_type.lower(), args.silent)
    elif args.action == 'print':
        print_entry(plist_data, args.entry_path)
    elif args.action == 'append':
        append_to_string(plist_data, args.entry_path, args.type.lower(), args.value, args.silent)
    elif args.action == 'remvalue':
        remove_value_from_string(plist_data, args.entry_path, args.type.lower(), args.value, args.silent)

    save_plist(args.path, plist_data)


if __name__ == "__main__":
    main()