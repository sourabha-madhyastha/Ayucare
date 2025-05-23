import datetime
import json
from flask import Flask, render_template, request
from login import LoginForm, RegisterFormPatient, RegisterFormDoctor, AppointmentForm
from flask_mysqldb import MySQL
import mysql.connector
import bcrypt
from flask import session
from datetime import datetime  # Update this import
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


app=Flask(__name__)
# Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'samarth@123'
app.config['MYSQL_DB'] = 'ayucare'

mysql = MySQL(app)

app.config['SECRET_KEY'] = 'sourabha'
# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
#login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, email, role):
        self.id = id
        self.email = email
        self.role = role

@login_manager.user_loader
def load_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, email, role FROM user WHERE id = %s", [user_id])
    user_data = cur.fetchone()
    cur.close()
    if user_data:
        return User(id=user_data[0], email=user_data[1], role=user_data[2])
    return None



#register = RegisterForm()


@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method =="POST":
        email= form['email'].data
        password= form['password'].data
        form_role=form['role'].data
        cur = mysql.connection.cursor()
        result= cur.execute("SELECT * FROM user WHERE email=%s", [email])
        if result > 0:
            a=cur.fetchone()
            print(a)
            stored_hashed_password = a[2]
           
            if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
                role = a[3]
                user_id = a[0]
                session['user_id'] = user_id  # Store user_id in the session
                session['role'] = role  # Store role in the session
               
                if form_role == role:
                    user=User(id=user_id,email=email,role=role)
                    # Load the user object
                    login_user(user)
                    if role == 'doctor':
                        cur.execute("SELECT id FROM doctor WHERE user_id=%s", [user_id])
                        doctor = cur.fetchone()
                        if doctor:
                            session['doctor_id'] = doctor[0]
                        return render_template('doctor_dashboard.html', name=a[1])
                    elif role == 'patient':
                        cur.execute("SELECT id FROM patient WHERE user_id=%s", [user_id])
                        patient = cur.fetchone()
                        if patient:
                            session['patient_id'] = patient[0]
                        return render_template('patient_dashboard.html')
                else:
                    return render_template('login.html', error="Invalid role",form=form)
                    
        return render_template('login.html', form=form, error="Invalid email or password")
    else:
        return render_template('login.html', form=form)

@app.route('/patientregister',methods=['GET','POST'])
def patientregister():
    form=RegisterFormPatient()
    if request.method == "POST":
        name = form['name'].data
        email = form['email'].data
        contact_number = form['contact_number'].data
        age = form['age'].data
        gender = form['gender'].data
        role = form['role'].data
        password = form['password'].data

         # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        password_final = hashed_password.decode('utf-8')
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM user WHERE email=%s", [email])
        if result > 0:
            return render_template('patientregister.html', form=form, error="Email already exists")
        else:
            cur.execute("INSERT INTO user ( email, password, role) VALUES (%s, %s, %s)", (email, password_final, role))
            mysql.connection.commit()
            cur.execute("SELECT id FROM user WHERE email=%s", [email])
            user_id = cur.fetchone()[0]
            # Insert into patient table with user_id
            cur.execute("INSERT INTO patient (user_id,name, contact, age,gender) VALUES (%s,%s, %s, %s, %s)", (user_id,name, contact_number, age,gender))
            mysql.connection.commit()
            cur.close()
        return render_template('patient_dashboard.html', appointmentForm=AppointmentForm())
    else:
        return render_template('patientregister.html', form=form)

@app.route('/doctorregister',methods=['GET','POST'])
def doctorregister():
    form=RegisterFormDoctor()
    if request.method == "POST":
        name = form['name'].data
        email = form['email'].data
        contact_number = form['contact_number'].data
        specialisation = form['specialisation'].data
        role = form['role'].data
        password = form['password'].data
        availability = {
            "monday": "9:00 AM - 5:00 PM",
            "tuesday": "9:00 AM - 5:00 PM",
            "wednesday": "9:00 AM - 5:00 PM",
            "thursday": "9:00 AM - 5:00 PM",
            "friday": "9:00 AM - 5:00 PM"
        }
        # Convert availability to JSON string
        availability_json = json.dumps(availability)

         # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        password_final = hashed_password.decode('utf-8')
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM user WHERE email=%s", [email])
        if result > 0:
            return render_template('doctorregister.html', form=form, error="Email already exists")
        else:
            cur.execute("INSERT INTO user ( email, password, role) VALUES (%s, %s, %s)", (email, password_final, role))
            mysql.connection.commit()
            cur.execute("SELECT id FROM user WHERE email=%s", [email])
            user_id = cur.fetchone()[0]
            # Insert into doctor table with user_id
            cur.execute("INSERT INTO doctor (user_id, name, contact, specialization,availability) VALUES (%s,%s, %s, %s, %s)", (user_id,name, contact_number,specialisation,availability_json))
            mysql.connection.commit()
            cur.close()
        print("Rendering template: doctor_dashboard.html")
        return render_template('doctor_dashboard.html', name=name, email=email, contact_number=contact_number,specialisation=specialisation, role=role, password=password)
    return render_template('doctorregister.html', form=form)

@app.route('/success',methods=['GET','POST'])
def success():
    form=RegisterFormPatient()
    if request.method == "POST":
        name = form['name'].data
        email = form['email'].data
        contact_number = form['contact_number'].data
        age = form['age'].data
        role = form['role'].data
        password = form['password'].data
    return render_template('display.html', name=name, email=email, contact_number=contact_number,age=age, role=role, password=password)


@app.route('/bookappointment',methods=['GET','POST'])
@login_required
def bookappointment():
    if 'patient_id' not in session:
        return "Unauthorized access", 403 
    form=AppointmentForm()
    cur = mysql.connection.cursor()
    cur.execute("SELECT id,name FROM doctor")
    doctors = cur.fetchall()
    print(doctors)
    form.doctor.choices = [(doctor[0], doctor[1]) for doctor in doctors]
    if request.method=="POST":
        doctor_id = form['doctor'].data
        patient_id = session['patient_id']  # Get the patient ID from the session
        date = form['date'].data
        time = form['time'].data

        # Retrieve the doctor's availability
        cur.execute("SELECT availability FROM doctor WHERE id = %s", [doctor_id])
        availability_json = cur.fetchone()[0]
        availability = json.loads(availability_json)  # Convert JSON string to Python dictionary

        # Validate the appointment date and time
        appointment_date = datetime.strptime(date, "%Y-%m-%d")
        appointment_time = datetime.strptime(time, "%H:%M:%S").time()
        day_of_week = appointment_date.strftime("%A").lower()  # Get the day of the week (e.g., "monday")

        if day_of_week not in availability:
            return render_template('book_appointment.html', form=form, error="Doctor is not available on this day")

        # Parse the doctor's available hours for the selected day
        available_hours = availability[day_of_week]
        start_time_str, end_time_str = available_hours.split(" - ")
        start_time = datetime.strptime(start_time_str, "%I:%M %p").time()
        end_time = datetime.strptime(end_time_str, "%I:%M %p").time()
        
        # Check if the appointment time falls within the available hours
        if not (start_time <= appointment_time <= end_time):
            return render_template('book_appointment.html', form=form, error="Doctor is not available at this time")

        cur.execute("INSERT INTO appointment (doctor_id, patient_id, date, time) VALUES (%s, %s, %s, %s)", (doctor_id, patient_id, date, time))
        mysql.connection.commit()
        cur.close()
        return render_template('display.html')
    
    return render_template('book_appointment.html', form=form)

@app.route('/patient_history',methods=['GET','POST'])
@login_required
def patient_history():
    if 'patient_id' not in session:
        return "Unauthorized access", 403
    patient_id = session['patient_id']  # Get the logged-in patient's ID
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT a.date, a.time, d.name AS doctor_name, d.specialization
        FROM appointment a
        JOIN doctor d ON a.doctor_id = d.id
        WHERE a.patient_id = %s
        ORDER BY a.date DESC, a.time DESC
    """, [patient_id])
    history = cur.fetchall()
    cur.close()
    return render_template('history.html', history=history)

@app.route('/logout',methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    # session.pop('user_id', None)
    # session.pop('role', None)
    # session.pop('patient_id', None)
    session.clear()  # Clear all session data
    return render_template('home.html')
    
if __name__ == '__main__':
    app.run(debug=True)