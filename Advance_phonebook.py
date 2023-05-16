import streamlit as st
import json

CONTACTS_FILE = "contacts.json"
RECYCLE_BIN_FILE = "recycle_bin.json"


# Function to load contacts from file
def load_contacts():
    try:
        with open(CONTACTS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


# Function to save contacts to file
def save_contacts(contacts):
    with open(CONTACTS_FILE, "w") as f:
        json.dump(contacts, f)


# Function to load recycle bin from file
def load_recycle_bin():
    try:
        with open(RECYCLE_BIN_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


# Function to save recycle bin to file
def save_recycle_bin(recycle_bin):
    with open(RECYCLE_BIN_FILE, "w") as f:
        json.dump(recycle_bin, f)


# Initialize phonebook dictionary
phonebook = load_contacts()

# Initialize recycle bin list
recycle_bin = load_recycle_bin()

# Function to add a contact
def add_contact(name, phone, email, dob):
    contact = {
        "name": name,
        "phone": phone,
        "email": email,
        "dob": dob
    }
    phonebook[name] = contact
    save_contacts(phonebook)


# Function to delete a contact
def delete_contact(name):
    if name in phonebook:
        deleted_contact = {name: phonebook[name]}
        recycle_bin.append(deleted_contact)
        del phonebook[name]
        save_contacts(phonebook)
        save_recycle_bin(recycle_bin)
        return True
    return False


# Function to permanently delete a contact from recycle bin
def permanently_delete_contact(name):
    for contact in recycle_bin:
        if name in contact:
            recycle_bin.remove(contact)
            save_recycle_bin(recycle_bin)
            return True
    return False


# Function to restore a contact from recycle bin
def restore_contact(name):
    for contact in recycle_bin:
        if name in contact:
            phonebook[name] = contact[name]
            recycle_bin.remove(contact)
            save_contacts(phonebook)
            save_recycle_bin(recycle_bin)
            return True
    return False


# Function to search for a contact
def search_contact(name):
    if name in phonebook:
        return phonebook[name]
    return None


# Streamlit app
def main():
    st.title("Phonebook Application")

    # Sidebar menu
    menu = st.sidebar.selectbox("Menu", ["Add Contact", "View Contact List", "Search Contact", "Delete Contact", "Recycle Bin"])

    if menu == "Add Contact":
        st.header("Add Contact")
        name = st.text_input("Name")
        phone = st.text_input("Phone")
        email = st.text_input("Email")
        dob = st.text_input("Date of Birth")
        if st.button("Add"):
            add_contact(name, phone, email, dob)
            st.success("Contact added successfully!")

    elif menu == "View Contact List":
        st.header("View Contact List")
        if phonebook:
            st.table(phonebook.values())
        else:
            st.warning("Contact list is empty.")

    elif menu == "Search Contact":
        st.header("Search Contact")
        name = st.text_input("Name")
        if st.button("Search"):
            result = search_contact(name)
            if result:
                st.success(f"Contact found: {name} - Phone: {result['phone']}- Email: {result['email']} - DOB: {result['dob']}")
            else:
                st.warning("Contact not found.")

    elif menu == "Delete Contact":
        st.header("Delete Contact")
        name = st.text_input("Name")
        if st.button("Delete"):
            if delete_contact(name):
                st.success("Contact deleted and moved to recycle bin.")
            else:
                st.warning("Contact not found.")

    elif menu == "Recycle Bin":
        st.header("Recycle Bin")
        if recycle_bin:
            st.table(recycle_bin)
            name = st.text_input("Name")
            if st.button("Restore"):
                if restore_contact(name):
                    st.success("Contact restored successfully!")
                else:
                    st.warning("Contact not found in recycle bin.")
            if st.button("Permanently Delete"):
                if permanently_delete_contact(name):
                    st.success("Contact permanently deleted from recycle bin.")
                else:
                    st.warning("Contact not found in recycle bin.")
        else:
            st.warning("Recycle bin is empty.")


if __name__ == "__main__":
    main()