from flask import jsonify, request
from contacts import create_contact, update_contacts, get_consolidated_contacts_details
from models import Contact
from database import db


def identify_contact():
    # Route implementation...
    data = request.get_json()
    email = data.get('email')
    phoneNumber = data.get('phoneNumber')

    if not email and not phoneNumber:
        return jsonify({'error': 'Both email and phoneNumber cannot be empty'}), 400

    existing_emails = Contact.query.filter((Contact.email == email)).all()
    existing_phone_numbers = Contact.query.filter((Contact.phoneNumber == phoneNumber)).all()

    perfect_match = Contact.query.filter((Contact.email == email) & (Contact.phoneNumber == phoneNumber)).first()

    if not existing_phone_numbers and not existing_emails:
        # Create a new primary contact
        new_contact = Contact(phoneNumber=phoneNumber, email=email, linkPrecedence='primary')
        db.session.add(new_contact)
        db.session.commit()

        return jsonify({
            'contact': {
                'primaryContactId': new_contact.id,
                'emails': [new_contact.email],
                'phoneNumbers': [new_contact.phoneNumber],
                'secondaryContactIds': []
            }
        })

    elif perfect_match:
        consolidated_contacts_details = get_consolidated_contacts_details(phoneNumber, email)
        return jsonify({"contact": consolidated_contacts_details}), 200

    elif not existing_phone_numbers or not existing_emails:
        create_contact(existing_emails, existing_phone_numbers, email, phoneNumber)
        consolidated_contacts_details = get_consolidated_contacts_details(phoneNumber, email)
        return jsonify({"contact": consolidated_contacts_details}), 200

    else:
        update_contacts(existing_emails, existing_phone_numbers)
        consolidated_contacts_details = get_consolidated_contacts_details(phoneNumber, email)
        return jsonify({"contact": consolidated_contacts_details}), 200
