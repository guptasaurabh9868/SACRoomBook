# SACRoom Booking Portal.
Portal for creating Accounts for independent bodies of IITB for booking SACRooms.

## Installations Instructions
```
git clone https://github.com/guptasaurabh9868/SACRoomBook.git
cd SACRoomBook
pip3 install -r requirements.txt
cd SACBooking
vim email_info.py            ### Add Details of Email, as described below.
python3 manage.py makemigrations main bookings
python3 manage.py migrate
python3 manage.py runserver
```
Note:- For Normal Execution, need to add a file "email_info.py" to SACBooking Folder, with following details:

```
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp-auth.iitb.ac.in'   ###Email SMTP server
EMAIL_HOST_USER = 'LDAPID@iitb.ac.in'   ###Email ID
EMAIL_HOST_PASSWORD = '[yourpassword]'  ###Password for EMAIL ID.
EMAIL_PORT = 25               ###Email server Port.
```

These Details will be used to send emails for notifications in the app for various purpose.
