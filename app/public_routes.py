from datetime import timedelta
from datetime import datetime
from flask import render_template,redirect, request, session, url_for, flash
from functools import wraps
from app import app
from app.form import RegisterForm, LoginForm, EmailVerificationCodeForm
from app.models import User, db, AgentProfile
from app.auth_utils import generate_verification_code, send_verification_code_message
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func


@app.after_request
def after_request(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_id') is None:
            flash('You need to be logged in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function



def send_verification_email(user):
    """Send a verification email to the user."""
    code = generate_verification_code()
    user.email_verification_code = code
    user.email_verification_expiry_at = datetime.utcnow() + timedelta(minutes=30)
    user.email_verification_attempts = 0
    db.session.commit()

    return send_verification_code_message(user.email, code, expiry_minutes=30)


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

@app.route('/agent_page')
def agent_page():
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

        chk = check_password_hash(user.password_hash, password)
        if chk:
            if not user.email_verified:
                session['pending_email'] = user.email
                send_ok = send_verification_email(user)
                if send_ok:
                    flash('Please verify your email before logging in. A verification code has been sent to your inbox.', 'warning')
                else:
                    flash('Please verify your email before logging in. We could not send a new code, please try again.', 'error')
                return redirect(url_for('verify_email', email=user.email))
            
            session['user_id'] = user.id
            session['user_role'] = user.role
            session['user_name'] = user.username
            session.permanent = bool(form.remember_me.data)

            flash('Login successful!', 'success')

            if user.role == 'agent':
                return redirect(url_for('agent_dashboard'))
            if user.role == 'admin':
                flash('Invalid role. Admins should log in through the admin panel.', category='error')
                return redirect(url_for('login'))
            if user.role == 'client':
                return redirect(url_for('home'))
        else:
            flash('Incorrect password please try again', category='error')
            return redirect(url_for('login'))

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
                flash('This email is already registered. Please log in or use a different email address.', 'error')
                return render_template('public/register.html', form=form)
            
            role = form.role.data
            full_name = form.full_name.data
            password = generate_password_hash(form.password.data)
            new_user = User(username=full_name, email=email, role=role, password_hash=password)
            try:
                db.session.add(new_user)
                db.session.commit()
                send_ok = send_verification_email(new_user)
                if send_ok:
                    session['pending_email'] = new_user.email
                    flash('Registration was successful. Please check your email for the verification code.', 'success')
                    return redirect(url_for('verify_email', email=new_user.email))
                else:
                    flash('Registration was successful, but your verification code could not be sent. Please contact support.', 'warning')
                    return redirect(url_for('login'))
            except Exception as e:
                db.session.rollback()
                flash('An error occurred while creating your account. Please try again.')
                return render_template('public/register.html', form=form)
        else:
            return render_template('public/register.html', form=form)
        

@app.route('/verify-email', methods=['GET', 'POST'])
def verify_email():
    form = EmailVerificationCodeForm()

    email = (request.args.get('email') or request.form.get('email') or session.get('pending_email') or '').strip().lower()
    if not email:
        flash('Please provide your email address to continue verification.', 'info')
        return redirect(url_for('login'))

    session['pending_email'] = email

    user = User.query.filter(func.lower(func.trim(User.email)) == email).first()
    if not user:
        flash('We could not find an account with that email address.', 'error')
        return redirect(url_for('login'))

    if user.email_verified:
        flash('This email is already verified. Please log in.', 'info')
        return redirect(url_for('login'))

    if form.validate_on_submit():
        code = form.code.data.strip()

        if user.email_verification_expiry_at and user.email_verification_expiry_at < datetime.utcnow():
            flash('Your verification code has expired. Please request a new one.', 'warning')
            return redirect(url_for('resend_email_verification_code', email=email))

        if (user.email_verification_attempts or 0) >= 5:
            flash('Too many failed attempts. Please request a new code.', 'error')
            return redirect(url_for('resend_email_verification_code', email=email))

        if code != user.email_verification_code:
            user.email_verification_attempts = (user.email_verification_attempts or 0) + 1
            db.session.commit()
            flash('The verification code is incorrect. Please try again.', 'error')
            return render_template('public/verify_email_code.html', form=form, email=email)

        user.email_verified = True
        user.email_verified_at = datetime.utcnow()
        user.email_verification_code = None
        user.email_verification_expiry_at = None
        user.email_verification_attempts = 0
        db.session.commit()
        session.pop('pending_email', None)
        flash('Your email has been verified successfully. You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('public/verify_email_code.html', form=form, email=email)

@app.route('/resend-email_verification_code',methods=['GET','POST'])
def resend_email_verification_code():
    email = (request.args.get('email') or request.form.get('email') or '').strip().lower()

    if not email:
        flash('Please provide your email address.', 'error')
        return redirect(url_for('login'))
    
    user = User.query.filter(func.lower(func.trim(User.email)) == email).first()
    if not user:
        flash('We could not find an account with that email address.', 'error')
        return redirect(url_for('login'))

    if user.email_verified:
        flash('This email is already verified. Please log in.', 'info')
        return redirect(url_for('login'))
    
    send_ok = send_verification_email(user)

    if send_ok:
        session['pending_email'] = email
        flash('A new verification code has been sent. Please check your inbox.', 'success')
        return redirect(url_for('verify_email', email=email))
    else:
        flash('Your verification code could not be sent. Please contact support.', 'warning')
        return redirect(url_for('login'))
    

@app.post('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/client-dashboard')
def client_dashboard():
    return None


@app.route('/terms')
def terms():
    return render_template('public/terms.html')

@app.route('/privacy')
def privacy():
    return render_template('public/privacy.html')

