import json
import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict

@dataclass
class Contact:
    id: int
    first_name: str
    last_name: str
    email: str
    phone: str
    company: str
    relationship_strength: int  
    last_contact_date: str
    personal_notes: str
    preferred_contact_method: str  
    birthday: str
    interests: List[str]
    last_interaction_notes: str

class ClientContactManager:
    def __init__(self, filename: str = "client_contacts.json"):
        self.filename = filename
        self.contacts = self.load_contacts()
        self.next_id = max([c.id for c in self.contacts], default=0) + 1

    def load_contacts(self) -> List[Contact]:
        """Load contacts from JSON file with error handling"""
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                return [Contact(**contact) for contact in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_contacts(self):
        """Save contacts to JSON file"""
        with open(self.filename, 'w') as f:
            json.dump([asdict(contact) for contact in self.contacts], f, indent=2)

    def create_contact(self) -> Contact:
        """Create a new contact with personal touches"""
        print("\n" + "=" * 50)
        print("ADD NEW CLIENT CONNECTION")
        print("=" * 50)
        
        contact = Contact(
            id=self.next_id,
            first_name=input("First name: ").strip(),
            last_name=input("Last name: ").strip(),
            email=input("Email: ").strip(),
            phone=input("Phone: ").strip(),
            company=input("Company: ").strip(),
            relationship_strength=self._get_relationship_strength(),
            last_contact_date=datetime.datetime.now().strftime("%Y-%m-%d"),
            personal_notes=input("Personal notes (hobbies, family, interests): ").strip(),
            preferred_contact_method=self._get_preferred_contact_method(),
            birthday=input("Birthday (YYYY-MM-DD, optional): ").strip() or "Unknown",
            interests=input("Interests (comma-separated): ").strip().split(','),
            last_interaction_notes=input("Initial meeting notes: ").strip()
        )
        
        self.contacts.append(contact)
        self.next_id += 1
        self.save_contacts()
        
        print(f"\nSUCCESS! {contact.first_name} has been added to your network.")
        return contact

    def _get_relationship_strength(self) -> int:
        """Get relationship strength with user-friendly prompts"""
        while True:
            try:
                strength = int(input("Relationship strength (1-10, where 10 is closest): "))
                if 1 <= strength <= 10:
                    return strength
                print("Please enter a number between 1 and 10")
            except ValueError:
                print("Please enter a valid number")

    def _get_preferred_contact_method(self) -> str:
        """Get preferred contact method"""
        methods = {"1": "email", "2": "phone", "3": "in_person"}
        print("\nPreferred contact method:")
        print("1. Email")
        print("2. Phone")
        print("3. In Person")
        
        while True:
            choice = input("Choose (1-3): ").strip()
            if choice in methods:
                return methods[choice]
            print("Please choose 1, 2, or 3")

    def list_contacts(self):
        """Display all contacts with relationship insights"""
        if not self.contacts:
            print("\nYour contact list is empty. Let's add your first connection!")
            return
        
        print(f"\nYOUR NETWORK ({len(self.contacts)} connections)")
        print("=" * 80)
        
        for contact in sorted(self.contacts, key=lambda x: x.relationship_strength, reverse=True):
            self._display_contact_summary(contact)

    def _display_contact_summary(self, contact: Contact):
        """Display a friendly contact summary"""
        days_since_contact = self._days_since_last_contact(contact.last_contact_date)
        
       
        if contact.relationship_strength >= 8:
            relationship_indicator = "[STRONG]"
        elif contact.relationship_strength >= 5:
            relationship_indicator = "[GOOD]"
        else:
            relationship_indicator = "[NEW]"
        
       
        if days_since_contact > 90:
            follow_up = "*** Time to reconnect! ***"
        elif days_since_contact > 30:
            follow_up = "Consider checking in soon"
        else:
            follow_up = "Recently connected"
        
        print(f"\n{relationship_indicator} {contact.first_name} {contact.last_name}")
        print(f"   Company: {contact.company}")
        print(f"   Relationship: {contact.relationship_strength}/10")
        print(f"   Last contact: {days_since_contact} days ago - {follow_up}")
        print(f"   Preferred: {contact.preferred_contact_method.replace('_', ' ').title()}")

    def search_contacts(self):
        """Search contacts with flexible matching"""
        if not self.contacts:
            print("\nNo contacts to search.")
            return
        
        search_term = input("\nSearch by name, company, or interests: ").lower().strip()
        
        matches = []
        for contact in self.contacts:
            search_fields = [
                contact.first_name.lower(),
                contact.last_name.lower(),
                contact.company.lower(),
                ' '.join(contact.interests).lower()
            ]
            if any(search_term in field for field in search_fields):
                matches.append(contact)
        
        if matches:
            print(f"\nFound {len(matches)} matching contact(s):")
            for contact in matches:
                self._display_contact_summary(contact)
        else:
            print("\nNo matching contacts found.")

    def update_contact(self):
        """Update contact information with thoughtful prompts"""
        if not self.contacts:
            print("\nNo contacts to update.")
            return
        
        self.list_contacts()
        
        try:
            contact_id = int(input("\nEnter the ID of the contact to update: "))
            contact = self._find_contact_by_id(contact_id)
            
            if not contact:
                print("Contact not found.")
                return
            
            print(f"\nUpdating {contact.first_name}'s information")
            print("(Press Enter to keep current value)")
            
          
            contact.first_name = input(f"First name [{contact.first_name}]: ") or contact.first_name
            contact.last_name = input(f"Last name [{contact.last_name}]: ") or contact.last_name
            contact.email = input(f"Email [{contact.email}]: ") or contact.email
            contact.phone = input(f"Phone [{contact.phone}]: ") or contact.phone
            contact.company = input(f"Company [{contact.company}]: ") or contact.company
            
            
            new_notes = input(f"\nLatest interaction notes: ")
            if new_notes:
                contact.last_interaction_notes = new_notes
                contact.last_contact_date = datetime.datetime.now().strftime("%Y-%m-%d")
            
            contact.personal_notes = input(f"Personal notes [{contact.personal_notes}]: ") or contact.personal_notes
            
            self.save_contacts()
            print(f"\nSUCCESS! {contact.first_name}'s information has been updated!")
            
        except ValueError:
            print("Please enter a valid contact ID.")

    def delete_contact(self):
        """Delete contact with confirmation"""
        if not self.contacts:
            print("\nNo contacts to delete.")
            return
        
        self.list_contacts()
        
        try:
            contact_id = int(input("\nEnter the ID of the contact to remove: "))
            contact = self._find_contact_by_id(contact_id)
            
            if not contact:
                print("Contact not found.")
                return
            
            confirm = input(f"\nWARNING: Are you sure you want to remove {contact.first_name} {contact.last_name}? (yes/no): ")
            if confirm.lower() == 'yes':
                self.contacts.remove(contact)
                self.save_contacts()
                print(f"\n{contact.first_name} has been removed from your contacts.")
            else:
                print("Deletion cancelled.")
                
        except ValueError:
            print("Please enter a valid contact ID.")

    def get_relationship_insights(self):
        """Provide insights about relationships"""
        if not self.contacts:
            print("\nNo contacts for insights.")
            return
        
        total_contacts = len(self.contacts)
        strong_relationships = len([c for c in self.contacts if c.relationship_strength >= 8])
        needs_attention = len([c for c in self.contacts if self._days_since_last_contact(c.last_contact_date) > 60])
        
        print("\nRELATIONSHIP INSIGHTS")
        print("=" * 50)
        print(f"Total connections: {total_contacts}")
        print(f"Strong relationships (8+): {strong_relationships}")
        print(f"Contacts needing attention: {needs_attention}")
        
     
        old_contacts = [c for c in self.contacts if self._days_since_last_contact(c.last_contact_date) > 90]
        if old_contacts:
            print(f"\nConsider reconnecting with:")
            for contact in old_contacts[:3]: 
                days = self._days_since_last_contact(contact.last_contact_date)
                print(f"   - {contact.first_name} ({days} days since last contact)")

    def _find_contact_by_id(self, contact_id: int) -> Optional[Contact]:
        """Find contact by ID"""
        return next((c for c in self.contacts if c.id == contact_id), None)

    def _days_since_last_contact(self, last_contact_date: str) -> int:
        """Calculate days since last contact"""
        if last_contact_date == "Unknown":
            return 999
        last_date = datetime.datetime.strptime(last_contact_date, "%Y-%m-%d")
        return (datetime.datetime.now() - last_date).days

def main():
    """Main program loop with clean interface"""
    manager = ClientContactManager()
    
    print("\n" + "=" * 60)
    print("        WELCOME TO CLIENT RELATIONSHIP MANAGER")
    print("=" * 60)
    print("\nThis is more than a contact list - it's your relationship")
    print("companion. Let's build meaningful connections together!")
    
    while True:
        print("\n" + "=" * 50)
        print("MAIN MENU")
        print("=" * 50)
        print("1. Add a new connection")
        print("2. View all connections")
        print("3. Search connections")
        print("4. Update a connection")
        print("5. Remove a connection")
        print("6. Get relationship insights")
        print("7. Exit")
        print("=" * 50)
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == '1':
            manager.create_contact()
        elif choice == '2':
            manager.list_contacts()
        elif choice == '3':
            manager.search_contacts()
        elif choice == '4':
            manager.update_contact()
        elif choice == '5':
            manager.delete_contact()
        elif choice == '6':
            manager.get_relationship_insights()
        elif choice == '7':
            print("\nThank you for using the Client Relationship Manager!")
            print("Remember: The best connections are built with care and consistency.")
            break
        else:
            print("Please enter a valid number between 1-7.")

if __name__ == "__main__":
    main()