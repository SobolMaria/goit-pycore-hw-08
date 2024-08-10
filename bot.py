from classes import AddressBook, Record
import pickle


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Enter the argument for the command"
        except KeyError:
            return "Name is not in the list of contacts"
        except IndexError:
            return "Input correct arguments please"

    return inner

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, contacts: AddressBook):
    name, phone, *_ = args
    record = contacts.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        contacts.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_contact(args, contacts: AddressBook):
    name, old_phone, new_phone = args
    record = contacts.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return "Contact change."
    else:
        return "Name was not found"

@input_error    
def show_phone(args, contacts):
    name, = args
    record = contacts.find(name)
    if record:
        return record
    else: 
        return "Name was not found"
    
@input_error
def add_birthday(args, contacts):
    name, day = args
    record = contacts.find(name)
    if record:
        record.add_birthday(day)
        return "Birthday added"
    else:
        "Name was not found"

@input_error
def show_birthday(args, contacts):
    name, = args
    record = contacts.find(name)
    if record and record.birthday:
        return f"Birthday for {name}: {record.birthday}"
    else:
        return "Birthday not found."

@input_error
def birthdays(contacts, days=7):
    return contacts.get_upcoming_birthdays(days)
 
def all(contacts):
    return contacts


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()
    

def main():
    contacts = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(all(contacts))
        elif command == "add-birthday":
            print(add_birthday(args, contacts))
        elif command == "show-birthday":
            print(show_birthday(args, contacts))
        elif command == "birthdays":
            print(birthdays(contacts))
        else:
            print("Invalid command.")

    save_data(contacts)

if __name__ == "__main__":
    main()

