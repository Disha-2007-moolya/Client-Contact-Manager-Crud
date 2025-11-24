import csv
import os
from typing import List, Optional 
Contact_File = "Contacts_data.csv"
FieldNames = ["id","name","phone","email","company"]
class Contact:
    
    def __init__(self,id: int, name: str, phone: str, email: str, company: str):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.company = company
    
    def __str__(self):
        return f"ID: {self.id:<3} | Name: {self.name:<20} | Phone: {self.phone}"
    def to_dict(self) -> dict:
        return {
            "id" : self.id,
            "name" : self.name,
            "phone": self.phone,
            "email": self.email,
            "company": self.company


        }
    @staticmethod
    def from_dict(data: dict) -> 'Contact':
        return Contact(
            id=int(data['id']),
            name=data['name'],
            phone=data['phone'],
            email=data['email'],
            comapny=data['company'],

        )
class ContactManger:
    def __init__(self, filename: str):
        self.filename = filename
        self.contacts: List[Contact]=[]
        self._load_contact()
        self._next_id = self._get_next_id()
    def _get_next_id(self) -> int:
        return max([c.id for c in self.contacts] +[0]) + 1
    def _load_contact(self):
        if not os.path.exists(self.filename):
            return
        with open(self.filename,mode="r",newline='',encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    self.contacts.append(Contact.from_dict(row))
                except Exception as e:
                    print(f"Skipping malformed row: {row}. Error: {e}")
    def _save_contacts(self):
        with open(self.filename,mode='w',newline="",encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames =FieldNames)
            writer.writeheader()
            for contact in self.contacts:
                writer.writerow(contact.to_dict())
    def add(self ,name:str , phone: str , email:str , company: str) -> Contact:
        new_contact = Contact(self._next_id ,name,phone,email,company)
        self.contacts.append(new_contact)
        self._next_id += 1
        self._save_contacts()
        return new_contact
    def get_all(self) -> List[Contact]:
        return self.contacts
    def get(self,contact_id: int) -> Optional[Contact]:
        return next((c for c in self.contacts if c.id == contact_id), None)
    def update(self , contact_id: int, **kwargs) -> bool:
        contact = self.get(contact_id)
        if not contact:
            return False
        for key, value in kwargs.items():
            if hasattr(contact,key):
                setattr(contact , key,value)

        self._save_contacts()
        return True
    def delete(self,contact_id: int) -> bool:
        initial_count=len(self.contacts)
        self.contacts=[c for c in self.contacts if c.id != contact_id]

        if len(self.contacts) < initial_count:
            self._save_contacts()
            return True
        return False
if __name__ == "__main__":
    manager= ContactManger(Contact_File)
    print("--ADDING CONTACTS--")
    c=manager.add("Disha Moolya", "9875457845","Disha@gmail.com","Thathappinessproject")
    d=manager.add("Soumya","8754128745","soumya@gmail.com","Global Ventures")

    print("\n--ALL CONTACTS--")
    for c in manager.get_all():
        print(c)
    print("\n--Updating Disha--")
    manager.update(c.id,phone="9875457845",email="Disha@gmail.com")
    print(manager.get(c.id))
    print("\n--Deleting Soumya--")
    manager.delete(d.id)
    print("\n--Final List--")
    for c in manager.get_all():
        print(c)
