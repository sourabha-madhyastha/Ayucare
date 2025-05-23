CREATE DATABASE IF NOT EXISTS "ayucare";
USE "ayucare";


CREATE TABLE IF NOT EXISTS "user" (
    'id' INT PRIMARY KEY,
    'email' VARCHAR(50) NOT NULL,
    'password' VARCHAR(255) NOT NULL,
    'role' ENUM('doctor', 'patient') NOT NULL
)

CREATE TABLE IF NOT EXISTS "doctor" (
    'id'INT PRIMARY KEY,
    'user_id' INT NOT NULL,
    'name' VARCHAR(100) NOT NULL,
    'email' VARCHAR(50) NOT NULL,
    'contact' VARCHAR(15) NOT NULL,
    'specialization' VARCHAR(100) NOT NULL,
    'availability' JSON NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE 
)

CREATE TABLE IF NOT EXISTS "patient" (
    'id' INT PRIMARY KEY,
    'user_id' INT NOT NULL,
    'name' VARCHAR(100) NOT NULL,
    'email' VARCHAR(50) NOT NULL,
    'age' INT NOT NULL,
    'gender' VARCHAR(10) NOT NULL,
    'contact' VARCHAR(15) NOT NULL,
    'address' VARCHAR(255) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id) 
    ON DELETE CASCADE 
    ON UPDATE CASCADE 
)
CREATE TABLE IF NOT EXISTS "appointment" (
    'id' INT PRIMARY KEY,
    'doctor_id' INT NOT NULL,
    'patient_id' INT NOT NULL,
    'date' DATE NOT NULL,
    'time' TIME NOT NULL,
    FOREIGN KEY (doctor_id) REFERENCES doctor(id) 
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    FOREIGN KEY (patient_id) REFERENCES patient(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
)

CREATE TABLE IF NOT EXISTS "prescription" (
    'id' INT PRIMARY KEY,
    'appointment_id' INT NOT NULL,
    'notes' VARCHAR(255) NOT NULL,
    FOREIGN KEY (appointment_id) REFERENCES appointment(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
)
