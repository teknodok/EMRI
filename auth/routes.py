from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user, UserMixin
from itsdangerous import URLSafeTimedSerializer
from extensions import login_manager, mail
from flask_mail import Message
import pyodbc
import random
from config import Config

auth_bp = Blueprint('auth', __name__, template_folder='templates/auth')

# User class for flask_login
class User(UserMixin):
    def __init__(self, id, email, name, department):
        self.id = id
        self.email = email
        self.name = name
        self.department = department

@login_manager.user_loader
def load_user(user_id):
    # load user from DB by id
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT employee_id, email, name, department FROM Employees WHERE employee_id = ?", user_id)
    row = cursor.fetchone()
    conn.close()
    if row:
        emp_id, email, name, dept = row
        user = User(emp_id, email, name, dept)
        return user
    else:
        return None

def get_db_conn():

    cfg = Config

    server = cfg.DB_SERVER
    database = cfg.DB_DATABASE
    username = cfg.DB_USERNAME
    password = cfg.DB_PASSWORD
    driver = cfg.DB_DRIVER
    conn_str = (
        f"DRIVER={{{driver}}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
    )
    conn = pyodbc.connect(conn_str)
    return conn

# Step 1: login form to take email
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        if not email.endswith('@emri.in'):
            flash('Please use an @emri.in email address.', 'danger')
            return render_template('login.html')
        session['email_for_otp'] = email
        otp = str(random.randint(100000, 999999))
        session['otp'] = otp
        # Send OTP via email
        msg = Message("Your OTP", recipients=[email])
        msg.body = f"Your login OTP is: {otp}"
        mail.send(msg)
        return redirect(url_for('auth.verify_otp'))
    return render_template('login.html')

# Step 2: verify OTP
@auth_bp.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        submitted = request.form.get('otp', '').strip()
        if submitted == session.get('otp'):
            email = session.get('email_for_otp')
            # check if user already registered
            conn = get_db_conn()
            cursor = conn.cursor()
            cursor.execute("SELECT employee_id, name, department FROM Employees WHERE email = ?", email)
            row = cursor.fetchone()
            if row:
                emp_id, name, dept = row
                user = User(emp_id, email, name, dept)
                login_user(user)
                conn.close()
                # redirect based on department
                if dept.lower() == 'operations':
                    return redirect(url_for('operations.dashboard'))
                elif dept.lower() == 'technology':
                    return redirect(url_for('technology.dashboard'))
                elif dept.lower() == 'quality':
                    return redirect(url_for('quality.dashboard'))
                else:
                    # default landing
                    return "Department not recognized", 400
            else:
                conn.close()
                # not registered => go to registration
                return redirect(url_for('auth.register'))
        else:
            flash('Invalid OTP. Please try again.', 'danger')
            return render_template('verify_otp.html')
    return render_template('verify_otp.html')

# Step 3: registration
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = session.get('email_for_otp')
        employee_id = request.form.get('employee_id').strip()
        name = request.form.get('name').strip()
        department = request.form.get('department').strip()
        district = request.form.get('district').strip()
        role = request.form.get('role').strip()
        designation = request.form.get('designation').strip()

        conn = get_db_conn()
        cursor = conn.cursor()
        # insert into Employees table
        cursor.execute(
            """INSERT INTO Employees (employee_id, name, email, department, district, role, designation)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            employee_id, name, email, department, district, role, designation
        )
        conn.commit()
        conn.close()

        # log user in
        user = User(employee_id, email, name, department)
        login_user(user)
        # redirect to department landing
        if department.lower() == 'operations':
            return redirect(url_for('operations.dashboard'))
        elif department.lower() == 'technology':
            return redirect(url_for('technology.dashboard'))
        elif department.lower() == 'quality':
            return redirect(url_for('quality.dashboard'))
        else:
            return "Department not recognized", 400

    # methods GET
    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
