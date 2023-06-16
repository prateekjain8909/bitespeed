from datetime import datetime
from typing import List, Dict
from models import Contact
from database import db


def create_contact(existing_emails: List[Contact], existing_phone_numbers: List[Contact], email: str, phoneNumber: str) -> None:
    """
    Creates a new contact with the given email and phone number, linked to an existing primary contact.

    Args:
        existing_emails (List[Contact]): Existing email addresses.
        existing_phone_numbers (List[Contact]): Existing phone numbers.
        email (str): Email address of the new contact.
        phoneNumber (str): Phone number of the new contact.

    Returns:
        None
    """
    existing_contacts = set(existing_emails + existing_phone_numbers)
    primary_contact = None

    for existing_contact in existing_contacts:
        if existing_contact.linkPrecedence == "primary":
            primary_contact = existing_contact
        else:
            primary_contact = Contact.query.filter(Contact.id == existing_contact.linkedId).first()

    new_contact = Contact(phoneNumber=phoneNumber, email=email, linkPrecedence='secondary', linkedId=primary_contact.id)
    db.session.add(new_contact)
    db.session.commit()


def update_contacts(existing_emails: List[Contact], existing_phone_numbers: List[Contact]) -> None:
    """
    Updates contacts by linking them to the primary contact based on creation timestamp.

    Args:
        existing_emails (List[Contact]): Existing email addresses.
        existing_phone_numbers (List[Contact]): Existing phone numbers.

    Returns:
        None
    """
    all_contacts = list(set(existing_emails + existing_phone_numbers))
    all_contacts.sort(key=lambda x: x.createdAt)
    primary_contact = all_contacts[0]
    all_contacts = set(all_contacts)

    while all_contacts:
        contact = all_contacts.pop()

        if primary_contact.id == contact.id:
            continue

        if contact.linkPrecedence == "primary":
            all_contacts.update(Contact.query.filter(Contact.linkedId == contact.id).all())
            contact.linkPrecedence = "secondary"
            contact.linkedId = primary_contact.id
            contact.updatedAt = datetime.utcnow()

        elif contact.linkedId != primary_contact.id:
            contact.linkedId = primary_contact.id
            contact.updatedAt = datetime.utcnow()

    db.session.commit()


def get_consolidated_contacts_details(phoneNumber: str, email: str) -> Dict[str, any]:
    """
    Retrieves consolidated contact details based on the provided phone number and email.

    Args:
        phoneNumber (str): The phone number to search for.
        email (str): The email to search for.

    Returns:
        dict: A dictionary containing consolidated contact details, including primary contact ID,
              emails (with duplicates eliminated and order preserved), phone numbers (with duplicates
              eliminated and order preserved), and secondary contact IDs.

    Raises:
        ValueError: If no primary contact is found.

    """
    primary_contact = Contact.query.filter(
        (Contact.linkPrecedence == 'primary') & ((Contact.email == email) | (Contact.phoneNumber == phoneNumber))
    ).first()

    if not primary_contact:
        raise ValueError("No primary contact found.")

    secondary_contacts = Contact.query.filter(
        (Contact.linkPrecedence == 'secondary') & (Contact.linkedId == primary_contact.id)
    ).all()

    emails = [primary_contact.email]
    phone_numbers = [primary_contact.phoneNumber]
    secondary_contact_ids = set()

    secondary_emails = set()
    secondary_phone_numbers = set()

    for contact in secondary_contacts:
        if contact.email != primary_contact.email:
            secondary_emails.add(contact.email)
        if contact.phoneNumber != primary_contact.phoneNumber:
            secondary_phone_numbers.add(contact.phoneNumber)
        if contact.id != primary_contact.id:
            secondary_contact_ids.add(contact.id)

    emails.extend(list(secondary_emails))
    phone_numbers.extend(list(secondary_phone_numbers))

    consolidated_contacts_details = {
        "primaryContactId": primary_contact.id,
        "emails": emails,
        "phoneNumbers": phone_numbers,
        "secondaryContactIds": list(secondary_contact_ids)
    }

    return consolidated_contacts_details

