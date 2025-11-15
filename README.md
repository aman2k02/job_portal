# Job Portal - Flask + SQLite + Bootstrap 

## Features
- Flask backend with SQLAlchemy (SQLite)
- Role-based users: admin, employer, jobseeker
- Employers can post jobs and view applications
- Jobseekers can apply and view applications
- Admin dashboard with simple stats
- Responsive UI with header/footer and left slide-out menu

## Setup

1. Clone or copy files into a folder, e.g. `job_portal/`.
   Open CMD / PowerShell / VS Code terminal, then run:
   
     git clone https://github.com/aman2k02/job_portal.git

   Move inside the project folder

    cd job_portal
   
2. Create a virtual environment:

   python -m venv venv

   Now Activate virtual Environment

    venv\Scripts\activate

3. Install dependencies:

   pip install -r requirements.txt

4. Run the project:

    python app.py

5. A default admin user is created automatically the first time the app runs:

--------------Email: admin@portal.com-------------

--------------Password: adminpass-----------------

You can create test data via the browser:

Visit: http://127.0.0.1:5000/create-sample

That creates:

Employer: emp@company.com / emppass

Jobseeker: js@user.com / jspass


----------------Important URLs------------------

Home: http://127.0.0.1:5000/

Login: http://127.0.0.1:5000/login

Register: http://127.0.0.1:5000/register

Admin dashboard: http://127.0.0.1:5000/admin/dashboard

Employer dashboard: http://127.0.0.1:5000/employer/dashboard

Jobseeker dashboard: http://127.0.0.1:5000/jobseeker/dashboard

Create sample data: http://127.0.0.1:5000/create-sample

