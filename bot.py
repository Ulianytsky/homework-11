from adressbook import Name, Record, AdressBook, PhoneNumber


address_book = AdressBook()


def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except IndexError:
            return 'Not enough params. Print "help"'
    return inner


def help(*args):
    return '''How can I help you? For adding type add, name, and phone number.
To change phone number type change, name, and old phone number " " new phone number.
To show all contacts type show all.
To search type search, name or phone number.
To exit type exit.
'''


@input_error
def add(*args):
    list_of_param = args[0].split()
    name = Name(list_of_param[0])
    phone_numbers = [PhoneNumber(number) for number in list_of_param[1:]]
    if name.value in address_book:
        record = address_book[name.value]
        record.add_phone(*phone_numbers)
    else:
        record = Record(name)
        record.add_phone(*phone_numbers)
        address_book.add_record(record)
    return f'{name}, phone number {", ".join(str(phone) for phone in phone_numbers)} added to the address book.'


@input_error
def change(*args):
    list_of_param = args[0].split()
    name = Name(list_of_param[0])
    old_phone = PhoneNumber(list_of_param[1])
    new_phone = PhoneNumber(list_of_param[2])
    record = address_book.data.get(name.value)
    if record:
        try:
            record.edit_phone(old_phone, new_phone)
            return f'Phone number {old_phone} for {name} updated to {new_phone}.'
        except ValueError as e:
            return str(e)
    else:
        return f'There is no record with name {name}.'


@input_error
def phone(*args):
    name = Name(args[0])
    if name.value not in address_book:
        return f'Contact {name} does not exist in the list.'
    record = address_book[name.value]
    return f'Phone number(s) for {name}: {record.phones}'


def search(*args):
    search_str = args[0].lower()
    result = []
    for name, record in address_book.items():
        if search_str in name or search_str in record.phones:
            result.append(record)
    output = ''
    if not result:
        return 'No records found.'
    for record in result:
        output += str(record) + '\n'
    return output


def show_all(*args):
    if not address_book:
        return 'There are no contacts in the list.'
    output = ''
    for name, record in address_book.items():
        phones_str = ', '.join(str(phone) for phone in record.phones)
        output += f'{name}: {phones_str}\n'
    return output


def exit(*args):
    return 'Bye!'


def no_command(*args):
    return 'Unknown command, try again.'


COMMANDS = {
    help: 'help',
    add: 'add',
    change: 'change',
    phone: 'phone',
    search: 'search',
    show_all: 'show all',
    exit: 'exit'
}


def command_handler(text):
    for command, kword in COMMANDS.items():
        if text.startswith(kword):
            return command, text.replace(kword, '').strip()
    return no_command, None


def main():
    print(help())
    while True:
        user_input = input('>>>')
        command, data = command_handler(user_input)
        print(command(data))
        if command == exit:
            break


if __name__ == '__main__':
    main()
