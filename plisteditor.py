import argparse
import plistlib
import os

def delete_entry(plist_path, entry_path, silent=False):
    try:
        with open(plist_path, 'rb') as plist_file:
            plist_data = plistlib.load(plist_file)
        
        entry_keys = entry_path.split('.')
        current_dict = plist_data
        for key in entry_keys[:-1]:
            current_dict = current_dict[key]
        del current_dict[entry_keys[-1]]
        
        with open(plist_path, 'wb') as plist_file:
            plistlib.dump(plist_data, plist_file)
        
        if not silent:
            print(f"Deleted entry '{entry_path}' from '{plist_path}'")
    except Exception as e:
        if not silent:
            print(f"Error: {e}")

def add_entry(plist_path, entry_path, entry_type, silent=False):
    try:
        with open(plist_path, 'rb') as plist_file:
            plist_data = plistlib.load(plist_file)
        
        entry_keys = entry_path.split('.')
        current_dict = plist_data
        for key in entry_keys[:-1]:
            if key not in current_dict:
                current_dict[key] = {}
            current_dict = current_dict[key]
        
        if entry_type == "dict":
            current_dict[entry_keys[-1]] = {}
        elif entry_type == "bool":
            current_dict[entry_keys[-1]] = False
        elif entry_type == "number":
            current_dict[entry_keys[-1]] = 0
        elif entry_type == "data":
            current_dict[entry_keys[-1]] = ""
        elif entry_type == "string":
            current_dict[entry_keys[-1]] = ""
        else:
            if not silent:
                print("Invalid entry type")
            return
        
        with open(plist_path, 'wb') as plist_file:
            plistlib.dump(plist_data, plist_file)
        
        if not silent:
            print(f"Added entry '{entry_path}' with type '{entry_type}' to '{plist_path}'")
    except Exception as e:
        if not silent:
            print(f"Error: {e}")

def set_entry(plist_path, entry_path, entry_type, value, silent=False):
    try:
        with open(plist_path, 'rb') as plist_file:
            plist_data = plistlib.load(plist_file)
        
        entry_keys = entry_path.split('.')
        current_dict = plist_data
        for key in entry_keys[:-1]:
            current_dict = current_dict[key]
        
        existing_type = type(current_dict[entry_keys[-1]]).__name__
        
        if entry_type == "string":
            current_dict[entry_keys[-1]] = value  # Directly set as a string without type conversion
        elif entry_type == "data":
            if existing_type == "str":
                current_dict[entry_keys[-1]] = value.encode('utf-8')
            elif existing_type == "bytes":
                try:
                    current_dict[entry_keys[-1]] = bytes.fromhex(value)
                except ValueError:
                    if not silent:
                        print("Cannot convert to data")
                    return
            else:
                if not silent:
                    print(f"Error: Existing type '{existing_type}' does not match specified type '{entry_type}'")
                return
        elif entry_type != existing_type:
            if entry_type == "string" and existing_type != "str":
                if not silent:
                    print(f"Error: Existing type '{existing_type}' does not match specified type '{entry_type}'")
                return
            elif entry_type == "bool":
                current_dict[entry_keys[-1]] = value.lower() == "true"
            elif entry_type == "number":
                current_dict[entry_keys[-1]] = float(value)
            else:
                if not silent:
                    print("Invalid entry type")
                return
        else:
            if entry_type == "bool":
                current_dict[entry_keys[-1]] = value.lower() == "true"
            elif entry_type == "number":
                current_dict[entry_keys[-1]] = float(value)
            elif entry_type == "data":
                current_dict[entry_keys[-1]] = value.encode('utf-8')  # This line handles setting data as a string
            else:
                current_dict[entry_keys[-1]] = value
        
        with open(plist_path, 'wb') as plist_file:
            plistlib.dump(plist_data, plist_file)
        
        if not silent:
            print(f"Set entry '{entry_path}' to '{value}' with type '{entry_type}' in '{plist_path}'")
    except Exception as e:
        if not silent:
            print(f"Error: {e}")

def change_entry(plist_path, entry_path, new_type, silent=False):
    try:
        with open(plist_path, 'rb') as plist_file:
            plist_data = plistlib.load(plist_file)
        
        entry_keys = entry_path.split('.')
        current_dict = plist_data
        for key in entry_keys[:-1]:
            current_dict = current_dict[key]
        
        if entry_keys[-1] not in current_dict:
            if not silent:
                print(f"Error: Entry '{entry_path}' does not exist")
            return
        
        existing_type = type(current_dict[entry_keys[-1]]).__name__
        if existing_type == new_type:
            if not silent:
                print(f"Entry '{entry_path}' is already of type '{new_type}'")
            return
        
        current_value = current_dict[entry_keys[-1]]
        if new_type == "bool":
            try:
                current_value = current_value.lower() == "true"
            except AttributeError:
                if not silent:
                    print("Cannot convert to bool")
                return
        elif new_type == "number":
            try:
                current_value = float(current_value)
            except ValueError:
                if not silent:
                    print("Cannot convert to number")
                return
        elif new_type == "data":
            if existing_type == "string":
                try:
                    current_value = current_value.encode('utf-8')
                except AttributeError:
                    if not silent:
                        print("Cannot convert to data")
                    return
            else:
                try:
                    current_value = bytes.fromhex(current_value)
                except AttributeError:
                    if not silent:
                        print("Cannot convert to data")
                    return
        elif new_type == "string":
            try:
                current_value = str(current_value)
            except ValueError:
                if not silent:
                    print("Cannot convert to string")
                return
        else:
            if not silent:
                print("Invalid entry type")
            return
        
        current_dict[entry_keys[-1]] = current_value
        
        with open(plist_path, 'wb') as plist_file:
            plistlib.dump(plist_data, plist_file)
        
        if not silent:
            print(f"Changed entry '{entry_path}' to type '{new_type}' in '{plist_path}'")
    except Exception as e:
        if not silent:
            print(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(description="CLI Plist Editor")
    parser.add_argument("command", choices=["delete", "add", "set", "change"], help="Command to perform")
    parser.add_argument("entry_path", help="Path to the plist entry")
    parser.add_argument("--path", required=True, help="Path to the plist file")
    parser.add_argument("--type", help="Type of plist entry (used for 'add' command)")
    parser.add_argument("--value", help="Value to set (used for 'set' command)")
    parser.add_argument("--new_type", help="New type to change the entry to (used for 'change' command)")
    parser.add_argument("-s", "--silent", action="store_true", help="Suppress output for certain actions")
    args = parser.parse_args()
    
    if not os.path.exists(args.path):
        if not args.silent:
            print(f"Error: Plist file '{args.path}' does not exist")
        return
    
    if args.command == "delete":
        delete_entry(args.path, args.entry_path, args.silent)
    elif args.command == "add":
        if not args.type:
            if not args.silent:
                print("Error: You must specify the type for 'add' command")
            return
        add_entry(args.path, args.entry_path, args.type, args.silent)
    elif args.command == "set":
        if not args.type or not args.value:
            if not args.silent:
                print("Error: You must specify the type and value for 'set' command")
            return
        set_entry(args.path, args.entry_path, args.type, args.value, args.silent)
    elif args.command == "change":
        if not args.new_type:
            if not args.silent:
                print("Error: You must specify the new type for 'change' command")
            return
        change_entry(args.path, args.entry_path, args.new_type, args.silent)
    else:
        if not args.silent:
            print("Invalid command")
        return

if __name__ == "__main__":
    main()
