def display_menu():
    """Displays the main menu options to the user."""
    print("\n--- Contact Book Menu ---")
    print("1. Add Contact")
    print("2. View Contact List")
    print("3. Search Contact")
    print("4. Update Contact")
    print("5. Delete Contact")
    print("6. Exit")
    print("-------------------------")

def add_contact(contacts):
    """
    Adds a new contact to the contact book.
    Prompts the user for name, phone number, email, and address.
    """
    print("\n--- Add New Contact ---")
    name = input("Enter Name: ").strip()
    if not name:
        print("Name cannot be empty. Contact not added.")
        return

    # Check if contact already exists by name
    if name.lower() in [c['name'].lower() for c in contacts.values()]:
        print(f"Contact with name '{name}' already exists. Please use a unique name.")
        return

    phone = input("Enter Phone Number: ").strip()
    email = input("Enter Email (optional): ").strip()
    address = input("Enter Address (optional): ").strip()

    # Generate a simple unique ID for the contact
    contact_id = str(len(contacts) + 1)
    while contact_id in contacts: # Ensure ID is unique if contacts are deleted and re-added
        contact_id = str(int(contact_id) + 1)

    contacts[contact_id] = {
        "name": name,
        "phone": phone,
        "email": email if email else "N/A",
        "address": address if address else "N/A"
    }
    print(f"Contact '{name}' added successfully with ID: {contact_id}")

def view_contact_list(contacts):
    """
    Displays a list of all saved contacts with their ID, name, and phone number.
    If the contact book is empty, it prints a message.
    """
    if not contacts:
        print("\nYour contact book is empty.")
        return

    print("\n--- Contact List ---")
    print(f"{'ID':<5} | {'Name':<20} | {'Phone Number':<15}")
    print("-" * 45)
    for contact_id, details in contacts.items():
        print(f"{contact_id:<5} | {details['name']:<20} | {details['phone']:<15}")
    print("--------------------")

def search_contact(contacts):
    """
    Searches for contacts by name or phone number.
    Displays detailed information for matching contacts.
    """
    if not contacts:
        print("\nContact book is empty. Nothing to search.")
        return

    query = input("Enter name or phone number to search: ").strip().lower()
    found_contacts = []

    for contact_id, details in contacts.items():
        if query in details['name'].lower() or query in details['phone']:
            found_contacts.append((contact_id, details))

    if found_contacts:
        print("\n--- Search Results ---")
        for contact_id, details in found_contacts:
            print(f"ID: {contact_id}")
            print(f"Name: {details['name']}")
            print(f"Phone: {details['phone']}")
            print(f"Email: {details['email']}")
            print(f"Address: {details['address']}")
            print("-" * 20)
    else:
        print(f"No contacts found matching '{query}'.")

def update_contact(contacts):
    """
    Updates details of an existing contact based on their ID.
    Prompts the user for the contact ID and then new details.
    """
    if not contacts:
        print("\nContact book is empty. Nothing to update.")
        return

    view_contact_list(contacts)
    contact_id = input("Enter the ID of the contact to update: ").strip()

    if contact_id in contacts:
        current_details = contacts[contact_id]
        print(f"\n--- Update Contact (ID: {contact_id}, Name: {current_details['name']}) ---")
        print("Leave field blank to keep current value.")

        new_name = input(f"Enter New Name ({current_details['name']}): ").strip()
        new_phone = input(f"Enter New Phone Number ({current_details['phone']}): ").strip()
        new_email = input(f"Enter New Email ({current_details['email']}): ").strip()
        new_address = input(f"Enter New Address ({current_details['address']}): ").strip()

        if new_name:
            # Check if new name conflicts with existing contacts (excluding itself)
            name_exists = False
            for cid, details in contacts.items():
                if cid != contact_id and new_name.lower() == details['name'].lower():
                    name_exists = True
                    break
            if name_exists:
                print(f"Error: Contact with name '{new_name}' already exists. Update aborted.")
                return
            current_details['name'] = new_name
        if new_phone:
            current_details['phone'] = new_phone
        if new_email:
            current_details['email'] = new_email
        if new_address:
            current_details['address'] = new_address

        print(f"Contact ID {contact_id} updated successfully.")
    else:
        print("Invalid Contact ID. Please try again.")

def delete_contact(contacts):
    """
    Deletes a contact from the contact book based on their ID.
    Asks for confirmation before deletion.
    """
    if not contacts:
        print("\nContact book is empty. Nothing to delete.")
        return

    view_contact_list(contacts)
    contact_id = input("Enter the ID of the contact to delete: ").strip()

    if contact_id in contacts:
        contact_name = contacts[contact_id]['name']
        confirmation = input(f"Are you sure you want to delete '{contact_name}' (ID: {contact_id})? (yes/no): ").lower()
        if confirmation == 'yes':
            del contacts[contact_id]
            print(f"Contact '{contact_name}' (ID: {contact_id}) deleted successfully.")
        else:
            print("Deletion cancelled.")
    else:
        print("Invalid Contact ID. Please try again.")

def main():
    """Main function to run the Contact Book application."""
    contacts = {} # Dictionary to store contacts: {id: {name, phone, email, address}}

    while True:
        display_menu()
        choice = input("Enter your choice (1-6): ").strip()

        if choice == '1':
            add_contact(contacts)
        elif choice == '2':
            view_contact_list(contacts)
        elif choice == '3':
            search_contact(contacts)
        elif choice == '4':
            update_contact(contacts)
        elif choice == '5':
            delete_contact(contacts)
        elif choice == '6':
            print("Exiting Contact Book. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")
