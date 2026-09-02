from app import app, db
from app.models import AgentProfile, User, db
from flask import render_template, redirect, request, session, url_for, flash
from app.public_routes import login_required
from functools import wraps
from datetime import datetime

def agent_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_role') != 'agent':
            flash('You need to be an agent to access this page.', 'error')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/agent-dashboard')
@login_required
@agent_required
def agent_dashboard():
   if session.get('user_id') is not None:
        current_time = datetime.utcnow()
        return render_template('agent/dashboard.html',current_time=current_time)
   return url_for('home')

@app.route('/agent_profile')
@login_required
@agent_required
def agent_profile():
    return render_template('agent/my-profile.html')

@app.route('/agent-add-property')
@login_required
@agent_required
def agent_add_property():
    return render_template('agent/add-property.html')

@app.route('/agent-inquiries')
@login_required
@agent_required
def agent_inquiries():
    return render_template('agent/inquiries.html')

@app.route('/agent-settings')
@login_required
@agent_required
def agent_settings():
    return render_template('agent/settings.html')

@app.route('/agent-my-properties')
@login_required
@agent_required
def agent_properties():
    return render_template('agent/my-properties.html')
