# Hospital Management System (HMS)

A full-stack Hospital Management System built using Django, PostgreSQL, Google Calendar API, and a Serverless Email Notification Service.

This project was developed as a locally runnable healthcare appointment management platform supporting:
- Role-based authentication
- Doctor and patient dashboards
- Appointment slot creation
- Appointment request and approval workflow
- Email notifications
- Google Calendar integration
- Notification system
- Booking history tracking

The system follows a realistic hospital workflow where patients request appointments and doctors approve or reject them.

Because letting random people directly occupy medical schedules with one click is apparently considered “bad architecture” in healthcare. Humanity occasionally surprises me.

---

# Features

## Authentication
- User signup/login/logout
- Doctor and patient role separation
- Protected dashboards using Django authentication

## Doctor Features
- Create appointment slots
- Edit slots
- Delete slots
- View booking requests
- Accept/reject appointments
- View booking history
- Receive notifications

## Patient Features
- View available slots
- Request appointments
- View booking status
- Receive approval/rejection notifications
- Email notifications

## Notifications
- Dashboard notifications
- Email notifications via serverless service
- Appointment confirmation alerts

## Google Calendar Integration
- OAuth login with Google
- Event creation after booking confirmation
- Doctor calendar updates
- Patient calendar updates

---

# Tech Stack

| Technology | Purpose |
|---|---|
| Django | Backend framework |
| PostgreSQL | Database |
| HTML/CSS | Frontend |
| Google Calendar API | Calendar integration |
| Node.js | Serverless email service |
| Serverless Framework | Local serverless execution |
| Gmail SMTP | Email delivery |

---

# Folder Structure

```text
hms/
│
├── core/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── calendar_service.py
│   └── templates/
│
├── email-service/
│   ├── handler.js
│   ├── serverless.yml
│   └── package.json
│
├── ai-tool-usage-log/
│
├── manage.py
├── requirements.txt
└── README.md