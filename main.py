# -*- coding: utf-8 -*-

import sys
import addressbook_pb2

# In[]

def BasicConcept():
  person = addressbook_pb2.Person()

  person.id = 99
  person.name = "Naming"
  person.email = "naming@example.com"

  phone = person.phones.add()
  phone.number = "080-0123"
  phone.type = addressbook_pb2.Person.WORK

  print(person)

  print("WORK ID: {}".format(addressbook_pb2.Person.WORK))
  print("WORK ID: {}".format(addressbook_pb2.Person.PhoneType.WORK))

  if person.IsInitialized():
    serialMsg = person.SerializeToString()
    print(serialMsg)

  another_person = addressbook_pb2.Person()
  print("Before parsing:\n{}".format(another_person))

  another_person.ParseFromString(serialMsg)
  print("After parsing:\n{}".format(another_person))

# In[]

def PromptForPerson(person):
  person.id = int(input("Enter the person ID: "))
  person.name = str(input("Enter the person name: "))

  email = str(input("Enter the person's email: "))
  if len(email) > 0:
    person.email = email
  
  while True:
    number = str(input("Enter a phone number (or leave blank to finish): "))
    if len(number) < 1:
      break
    
    phone_number = person.phones.add()
    phone_number.number = number

    phone_type = str(input("Enter the phone type: [mobile/home/work] "))
    if phone_type == "mobile":
      phone_number.type = addressbook_pb2.Person.PhoneType.MOBILE
    elif phone_type == "home":
      phone_number.type = addressbook_pb2.Person.PhoneType.HOME
    elif phone_type == "work":
      phone_number.type = addressbook_pb2.Person.PhoneType.WORK
    else:
      print("Unsupported phone type.")

def AddPerson(address_book_path):

  ADDRESS_BOOK = addressbook_pb2.AddressBook()

  try:
    # read the existing address book serialized data
    with open(address_book_path, "rb") as fin:
      ADDRESS_BOOK.ParseFromString(fin.read())
  except Exception as err:
    print("Failed in loading the address book {}.".format(address_book_path))
    print("Can't load the address book. Create a new now.")

  PromptForPerson(ADDRESS_BOOK.people.add())

  # write the serialized data to the local file
  with open(address_book_path, "wb") as fout:
    fout.write(ADDRESS_BOOK.SerializeToString())

def ListPerson(address_book_path):
  ADDRESS_BOOK = addressbook_pb2.AddressBook()

  try:
    with open(address_book_path, "rb") as fin:
      ADDRESS_BOOK.ParseFromString(fin.read())
  except Exception as err:
    print("Can't parse the address book.")
    return

  for person in ADDRESS_BOOK.people:
    print("Person ID: {}".format(person.id))
    print("\tName: {}".format(person.name))
    
    if person.HasField('email'):
      print("\tEmail: {}".format(person.email))
    
    for phone_number in person.phones:
      if phone_number.type == addressbook_pb2.Person.PhoneType.MOBILE:
        print("\tMobile: {}".format(phone_number.number))
      elif phone_number.type == addressbook_pb2.Person.PhoneType.HOME:
        print("\tHome: {}".format(phone_number.number))
      elif phone_number.type == addressbook_pb2.Person.PhoneType.WORK:
        print("\tWork: {}".format(phone_number.number))

# In[]

if __name__ == '__main__':
  if len(sys.argv) != 3:
    print("Usage:\n\tpython3 main.py <binary_file_path> <operation>\n\n\toperation: add|list")
    sys.exit(-1)
  else:
    print("Use the '{}' address book.".format(sys.argv[1]))

  if sys.argv[2] == "add":
    AddPerson(sys.argv[1])
  elif sys.argv[2] == "list":
    ListPerson(sys.argv[1])

