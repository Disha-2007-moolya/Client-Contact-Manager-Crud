PROJECT TITLE -  Client Contact CRUD Manager

PROJECT OVERVIEW : CLIENT CONTACT CRUD MANAGER
This code creates a client contact crud manager designed to handle the basic operations for managing a list of contacts. This included CRUD (Create , Read , Update , Delete)application that involves key feature of CSV File.
- The primary goal of this system is to maintain a well defined record of all the contacts. 
Operation    Methods
Create        manager.add()
Read          manager.get()
Update        manager.update()
Delete        manager.delete()
- Architectural Component
The progect is structured around two python classes,following the Object - Oriented Programming (OOP).
1. CONTACT Class (Data Model)
-> Role: Represents a single contact entity
2. CONTACTMANAGER class (Business Logic Access layer)
-> Role: Acts as the central hub for managing the collection of contacts and handling file I/O.
- Data Persistence 
The system uses the buit-in Python csv module for file handling.
-Technology stack
Language : Python
Module : csv,os,typing
Data Format : Comma-separated values(csv)
-Future Enhancements
While the current code is functional, a complete application would typically include features such as:
-> Search/Filter 
-> Input Validation
-> User Interface 

PROJECT FEATURE : CLIENT CONTACT CRUD MANAGER
1. Data Model (contact class)
- Structured data : Defines a consistent structure for each contact (ID , NAME , PHONE , EMAIL , COMPANY)
-Data Conversion : Handles conversion between Python objects and dictionary format for file I/O.
2. Core Functionality (ContactManager class)
- CRUD operations 
-> Create - add
-> Read - get_all,get
-> Update - update
-> Delete - delete
3. Persistence 
- CSV Storage : uses csv file to store all the data
- Automated I/O : Loads contacts from the file on startup and saves all the changes immediately 


PROJECT TECHNOLOGIES USED :  CLIENT CONTACT CRUD MANAGER
1. Structured data: uses the contact cladss as an OOP data model to define contact attributes.
2. CRUD opertaions : The ContactManager handles all the create, Read , Update and delete.
3. Unique IDS: Automatically generates and manages unique, sequential IDs for new contact.
4. CSV Persistence: Uses the built-in csv module to load data on startup and save changes instantly to a CSV file.


PROJECT STEPS AND INSTALLATION
Installation Steps

Install Python: Ensure you have Python installed on your system.
Save Code: Save the entire Python script into a file named, for example, contact_manager.py.

Run Project Steps
Open Terminal: Open your operating system's command prompt or terminal.
Navigate: Change the directory to the location where you saved contact_manager.py.
Execute: Run the script using the Python interpreter command:
python contact_manager.py

Result

The code will execute the demonstration logic in the if __name__ == "__main__": block (adding, updating, and deleting contacts).
A file named Contacts_data.csv will be created or updated in the same directory, persisting the final contact data.


PROJECT INSTRUCTIONS FOR TESTING 
- Test Case: Create (Add)
Action: Run the script (which adds contacts).

Verification: Confirm two new contacts are printed with sequential IDs (1 and 2). Check that Contacts_data.csv is created and contains two rows.

- Test Case: Read (Get)
Action: 1. Get a specific ID (e.g., manager.get(1)). 2. Get a non-existent ID (e.g., manager.get(99)).

Verification: 1. The correct contact object is returned. 2. None is returned.

- Test Case: Persistence
Action: 1. Comment out all manager.add() calls. 2. Run the script again.

Verification: 1. The manager successfully loads the existing two contacts from Contacts_data.csv. 2. The manager assigns the next ID as 3.

- Test Case: Update
Action: Call manager.update(ID, attribute="new value").

Verification: 1. The changes are visible when reading the contact back in memory. 2. Inspect Contacts_data.csv to confirm the specific row was modified.

- Test Case: Delete
Action: Call manager.delete(ID).

Verification: 1. The contact is removed from the list (get_all() shows one less contact). 2. Inspect Contacts_data.csv to confirm the contact's row has been permanently removed from the file.
