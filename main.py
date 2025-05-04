#!/usr/bin/env python3
"""
Bug Bounty Companion with Anthropic AI Integration
A CLI-based tool for security researchers to organize their workflow
"""

import os
import sys
import logging
from typing import Optional
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime
import email_validator

# This is needed to make the package importable
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Create Flask app
flask_app = Flask(__name__)
flask_app.secret_key = os.environ.get("SESSION_SECRET", "dev_key_for_bug_bounty_companion")

# Configure database
flask_app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
flask_app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Setup database
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
db.init_app(flask_app)

# Define models
class EmailSignup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255))
    organization = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Create tables
with flask_app.app_context():
    db.create_all()

# Configuration
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "bug_bounty_admin")

# Helper functions
def is_authenticated():
    """Check if user is authenticated"""
    return session.get('authenticated', False)

# Routes
@flask_app.route('/')
def index():
    """Landing page"""
    return render_template('index.html')

@flask_app.route('/signup', methods=['POST'])
def signup():
    """Handle email signup"""
    email = request.form.get('email')
    name = request.form.get('name', '')
    organization = request.form.get('organization', '')
    
    if not email:
        flash('Email address is required', 'error')
        return redirect(url_for('index'))
    
    try:
        # Validate email
        from email_validator import validate_email, EmailNotValidError
        valid = validate_email(email)
        email = valid.email
        
        # Check if email already exists
        existing_signup = EmailSignup.query.filter_by(email=email).first()
        if existing_signup:
            flash('You are already registered for our Alpha Phase!', 'info')
            return redirect(url_for('index'))
        
        # Add new signup
        signup = EmailSignup(
            email=email,
            name=name,
            organization=organization
        )
        db.session.add(signup)
        db.session.commit()
        
        flash('Thanks for joining our Alpha Phase!', 'success')
        return redirect(url_for('thank_you'))
    
    except Exception as e:
        logging.error(f"Error in signup: {str(e)}")
        db.session.rollback()
        flash('An error occurred. Please try again.', 'error')
        return redirect(url_for('index'))

@flask_app.route('/thank-you')
def thank_you():
    """Thank you page after signup"""
    return render_template('thank_you.html')

# Admin routes
@flask_app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    if request.method == 'POST':
        password = request.form.get('password')
        
        if password == ADMIN_PASSWORD:
            session['authenticated'] = True
            return redirect(url_for('admin_emails'))
        else:
            flash('Invalid password', 'error')
    
    return render_template('admin_login.html')

@flask_app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.pop('authenticated', None)
    return redirect(url_for('admin_login'))

@flask_app.route('/admin/emails')
def admin_emails():
    """Admin page to list all email signups"""
    if not is_authenticated():
        return redirect(url_for('admin_login'))
    
    # Get all email signups
    signups = EmailSignup.query.order_by(EmailSignup.created_at.desc()).all()
    
    return render_template('admin_emails.html', signups=signups)

# Make this file callable as a Flask app for gunicorn
app = flask_app

# When run directly, start the Flask app
if __name__ == "__main__":
    # Check if being run in CLI mode
    if len(sys.argv) > 1 and sys.argv[1] == "cli":
        # Run the CLI app
        from audit_companion.cli import app as cli_app
        cli_app()
    else:
        # Run the Flask app
        flask_app.run(host="0.0.0.0", port=5000, debug=True)
