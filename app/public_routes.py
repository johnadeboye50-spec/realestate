from flask import render_template,redirect, url_for, flash
from app import app

@app.route('/')
def home():
    return render_template('public/index.html')

@app.route('/about')
def about():
    return render_template('public/about.html')

@app.route('/properties')
def properties():
    return render_template('public/properties.html')

@app.route('/property-details')
def property_details():
    return render_template('public/property-details.html')

@app.route('/services')
def services():
    return render_template('public/services.html')

@app.route('/agents')
def agents():
    return render_template('public/agents.html')

@app.route('/agent-profile')
def agent_profile():
    return render_template('public/agent-profile.html')

@app.route('/blog')
def blog():
    return render_template('public/blog.html')

@app.route('/blog-details')
def blog_details():
    return render_template('public/blog-details.html')

@app.route('/contact')
def contact():
    return render_template('public/contact.html')

# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('public/404.html'), 404

@app.route('/terms')
def terms():
    return render_template('public/terms.html')

@app.route('/privacy')
def privacy():
    return render_template('public/privacy.html')