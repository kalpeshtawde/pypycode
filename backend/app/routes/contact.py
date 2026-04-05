from flask import Blueprint, jsonify, request
from app.models import Contact
from app import db
from datetime import datetime, timezone

contact_bp = Blueprint("contact", __name__)


def contact_to_dict(contact: Contact):
    return {
        "id": contact.id,
        "name": contact.name,
        "email": contact.email,
        "subject": contact.subject,
        "message": contact.message,
        "status": contact.status,
        "createdAt": contact.created_at.isoformat(),
        "updatedAt": contact.updated_at.isoformat(),
    }


@contact_bp.post("/", strict_slashes=False)
def create_contact():
    """Create a new contact query."""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ["name", "email", "subject", "message"]
        for field in required_fields:
            if field not in data or not data[field].strip():
                return jsonify({"error": f"{field} is required"}), 400
        
        # Basic email validation
        email = data["email"].strip()
        if "@" not in email or "." not in email:
            return jsonify({"error": "Invalid email address"}), 400
        
        # Create new contact
        contact = Contact(
            name=data["name"].strip(),
            email=email,
            subject=data["subject"].strip(),
            message=data["message"].strip(),
            status="pending"
        )
        
        db.session.add(contact)
        db.session.commit()
        
        return jsonify({
            "message": "Contact query submitted successfully",
            "contact": contact_to_dict(contact)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to submit contact query"}), 500


@contact_bp.get("/", strict_slashes=False)
def get_contacts():
    """Get all contact queries (admin endpoint)."""
    try:
        contacts = Contact.query.order_by(Contact.created_at.desc()).all()
        return jsonify([contact_to_dict(contact) for contact in contacts])
    except Exception as e:
        return jsonify({"error": "Failed to fetch contacts"}), 500


@contact_bp.put("/<contact_id>")
def update_contact_status(contact_id):
    """Update contact status (admin endpoint)."""
    try:
        contact = Contact.query.filter_by(id=contact_id).first_or_404()
        data = request.get_json()
        
        if "status" in data and data["status"] in ["pending", "read", "responded"]:
            contact.status = data["status"]
            contact.updated_at = datetime.now(timezone.utc)
            db.session.commit()
            
            return jsonify({
                "message": "Contact status updated successfully",
                "contact": contact_to_dict(contact)
            })
        else:
            return jsonify({"error": "Invalid status"}), 400
            
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to update contact status"}), 500
