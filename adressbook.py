from collections import UserDict


class Field:

    def __init__(self, value):
        if not isinstance(value, str):
            raise ValueError("Value must be a string")
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    pass


class PhoneNumber(Field):
    def __init__(self, number):
        self.number = number

    def __str__(self):
        return str(self.number)

    def __repr__(self):
        return self.number


class Record:
    def __init__(self, name: Name, phone: PhoneNumber = None):
        self.name = name
        self.phones = [phone] if phone else []

    def add_phone(self, *phones):
        self.phones.extend([str(phone) for phone in phones])

    def remove_phone(self, phone):
        if phone in self.phones:
            self.phones.remove(phone)
        else:
            raise ValueError(
                "The provided phone number does not exist for this record.")

    def edit_phone(self, old_phone, new_phone):
        if old_phone in self.phones:
            index = self.phones.index(old_phone)
            self.phones[index] = new_phone

    def __str__(self):
        return f'{self.name}: {", ".join(str(phone) for phone in self.phones)}'


class AdressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def search(self, **kwargs):
        result = []
        for record in self.data.values():
            found = True
            for key, value in kwargs.items():
                if key == 'name':
                    if record.name.value.lower() != value.lower():
                        found = False
                        break
                elif key == 'phone':
                    phones = [phone.value for phone in record.phones]
                    if value not in phones:
                        found = False
                        break
            if found:
                result.append(record)
        return result


if __name__ == '__main__':

    adressbook = AdressBook()
