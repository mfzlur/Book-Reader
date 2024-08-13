INSTRUCTIONS FOR LINUX/WSL

Navigate to the folder where app.py is situated

To set up a virtual environment:
- python3 -m venv v

To activate the virtual environment:
- source v/bin/activate or . v/bin/activate

To install the required dependencies:
- pip install -r requirements.txt

To run the application, execute:
- python3 app.py

To run migrations, execute:
- flask db init
- flask db migrate -m "migration message"
- flask db upgrade

To send mail using celery and frontend execute:
- npm run dev
- go to http://localhost:5173/celery/mail
- type email and name the hit send email button
- email will be sent in about 10s

Admin Details
email- admin@email.com
password- Admin@123

