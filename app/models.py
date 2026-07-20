from datetime import datetime

from sqlalchemy import Enum
from app import db

user_roles = ('client', 'agent', 'admin')

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    role = db.Column(Enum(*user_roles, name='user_roles'), default='client', nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    avatar = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    email_verified = db.Column(db.Boolean, default=False)
    email_verified_at = db.Column(db.DateTime, nullable=True)
    email_verification_code = db.Column(db.String(255), nullable=True)
    email_verification_expiry = db.Column(db.DateTime, nullable=True)
    email_verification_attempts = db.Column(db.Integer, default=0)


    agent_profile = db.relationship('AgentProfile', backref='user', uselist=False)

    property = db.relationship('Property', backref='user', lazy=True)

    favorites = db.relationship('Property', secondary='favorites', backref='favorited_by')

    contact_messages = db.relationship('ContactMessage', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.username} role={self.role}>"


class AgentProfile(db.Model):
    __tablename__ = 'agentprofile'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(30), nullable=True)
    office_address = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(255), nullable=True)
    state = db.Column(db.String(255), nullable=True)
    zip_code = db.Column(db.String(20), nullable=True)
    avatar = db.Column(db.String(255), nullable=True)
    rating = db.Column(db.Float, nullable=True)
    properties_sold = db.Column(db.Integer, default=0)
    reviews_count = db.Column(db.Integer, default=0)
    years_experience = db.Column(db.Integer, nullable=True)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    license_number = db.Column(db.String(50), nullable=True)
    bio = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Agentprofile user_id={self.user_id} title={self.title}>"


class Property(db.Model):
    __tablename__ = 'property'

    id = db.Column(db.Integer, primary_key=True)
    property_type_id = db.Column(db.Integer, db.ForeignKey('property_type.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(12, 2), nullable=False)
    address = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(255), nullable=True)
    state = db.Column(db.String(255), nullable=True)
    zip_code = db.Column(db.String(20), nullable=True)
    bedrooms = db.Column(db.Integer, nullable=True)
    bathrooms = db.Column(db.Integer, nullable=True)
    area = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(40), default='available', nullable=False)
    agent_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    property_type = db.relationship('PropertyType', backref='properties')

    def __repr__(self):
        return f"<Property {self.title} price={self.price}>"
    
class PropertyType(db.Model):
    __tablename__ = 'property_type'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<PropertyType {self.name}>"

class PropertyImage(db.Model):
    __tablename__ = 'property_image'

    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_main = db.Column(db.Boolean, default=False)
    sort_order = db.Column(db.Integer, default=0)
    caption = db.Column(db.String(255), nullable=True)

    property = db.relationship('Property', backref='images')

    def __repr__(self):
        return f"<PropertyImage property_id={self.property_id} path={self.image_path}>"
    

class PropertyFeature(db.Model):
    __tablename__ = 'property_feature'

    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    category = db.Column(Enum('interior', 'exterior', 'amenity', name='feature_category'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<PropertyFeature property_id={self.property_id} name={self.name}>"
    

class Favorite(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Favorite user_id={self.user_id} property_id={self.property_id}>"
    
class ContactMessage(db.Model):
    __tablename__ = 'contact_message'
    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(30), nullable=True)
    subject = db.Column(db.String(255), nullable=True)
    message = db.Column(db.Text, nullable=False)
    message_type = db.Column(Enum('general', 'property_inquiry', 'agent_inquiry', name='message_type'), default='general', nullable=False)
    status = db.Column(Enum('new', 'read', 'closed', name='message_status'), default='new', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ContactMessage agent_id={self.agent_id} property_id={self.property_id} name={self.name}>"

