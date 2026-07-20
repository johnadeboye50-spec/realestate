from flask import render_template,redirect, request, session, url_for, flash
from app import app
from app.form import RegisterForm, LoginForm
from app.models import User, db, AgentProfile
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if session.get('user_id') is not None:
        return redirect(url_for('home'))

    if form.validate_on_submit():
        email = (form.email.data or '').strip().lower()
        password = form.password.data
        user = User.query.filter(func.lower(func.trim(User.email)) == email).first()

        if not user:
            flash('No account found with that email.', 'error')
            return render_template('public/login.html', form=form)

        if not user.is_active:
            flash('Your account is inactive. Please contact support.', 'error')
            return render_template('public/login.html', form=form)

        if not check_password_hash(user.password_hash, password):
            flash('Incorrect password. Please try again.', 'error')
            return render_template('public/login.html', form=form)

        session['user_id'] = user.id
        session['user_role'] = user.role
        session['user_name'] = user.username
        session.permanent = bool(form.remember_me.data)

        flash('Login successful!', 'success')

        if user.role == 'agent':
            return redirect(url_for('home'))
        if user.role == 'admin':
            flash('Invalid role. Admins should log in through the admin panel.', category='error')
            return redirect(url_for('login'))
        if user.role == 'client':
            return redirect(url_for('home'))

    return render_template('public/login.html', form=form)

@app.route('/register',methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if session.get('user_id') is not None:
        return redirect(url_for('home'))
    if request.method == 'GET':
        return render_template('public/register.html', form=form)
    else:
        if form.validate_on_submit():
            email = form.email.data
            
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash('This Email has already been registerd. please login or use another email')
                return render_template('public/register.html', form=form)
            
            role = form.role.data
            full_name = form.full_name.data
            password = generate_password_hash(form.password.data)
            new_user = User(username=full_name, email=email, role=role, password_hash=password)
            try:
                db.session.add(new_user)
                db.session.commit()
                if role == 'agent':
                    agent_profile = AgentProfile(user_id=new_user.id)
                    db.session.add(agent_profile)
                    db.session.commit()
                flash('Account created successfully! Please log in.')
                return redirect(url_for('login'))
            except Exception as e:
                db.session.rollback()
                flash('An error occurred while creating your account. Please try again.')
                return render_template('public/register.html', form=form)
        else:
            return render_template('public/register.html', form=form)
        

@app.post('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/client-dashboard')
def client_dashboard():
    return None

@app.route('/agent-dashboard')
def agent_dashboard():
    return None


@app.route('/terms')
def terms():
    return render_template('public/terms.html')

@app.route('/privacy')
def privacy():
    return render_template('public/privacy.html')

