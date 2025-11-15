from flask import Flask, render_template, redirect, url_for, flash, request, abort
from config import Config
from models import db, User, Job, Application
from forms import LoginForm, RegisterForm, JobForm, ApplyForm
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from functools import wraps
from datetime import datetime, timedelta

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# role-based decorator
def roles_required(*roles):
    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            if current_user.role not in roles:
                flash("Unauthorized access", "danger")
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_first_request
def create_tables():
    db.create_all()
    # create default admin if not exists
    if not User.query.filter_by(email='admin@portal.com').first():
        admin = User(email='admin@portal.com', password='adminpass', name='Admin', role='admin')
        db.session.add(admin)
        db.session.commit()

@app.route('/')
def index():
    latest_jobs = Job.query.order_by(Job.created_at.desc()).limit(6).all()
    return render_template('index.html', jobs=latest_jobs)

# AUTH
@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            flash('Logged in successfully','success')
            return redirect(request.args.get('next') or url_for('index'))
        flash('Invalid credentials','danger')
    return render_template('auth/login.html', form=form)

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered', 'danger')
        else:
            user = User(email=form.email.data, password=form.password.data,
                        name=form.name.data, role=form.role.data,
                        company=form.company.data if form.role.data=='employer' else None)
            db.session.add(user)
            db.session.commit()
            flash('Registered! Please login.', 'success')
            return redirect(url_for('login'))
    return render_template('auth/register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out','info')
    return redirect(url_for('index'))

# Jobs browsing
@app.route('/jobs')
def job_list():
    jobs = Job.query.order_by(Job.created_at.desc()).all()
    return render_template('jobs/list.html', jobs=jobs)

@app.route('/jobs/<int:job_id>', methods=['GET','POST'])
def job_detail(job_id):
    job = Job.query.get_or_404(job_id)
    form = ApplyForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated or current_user.role != 'jobseeker':
            flash('You must be logged in as a jobseeker to apply.', 'warning')
            return redirect(url_for('login'))
        appn = Application(job_id=job.id, user_id=current_user.id, cover_letter=form.cover_letter.data)
        db.session.add(appn)
        db.session.commit()
        flash('Application submitted', 'success')
        return render_template('apply_success.html', job=job)
    return render_template('jobs/detail.html', job=job, form=form)

# Employer routes
@app.route('/employer/dashboard')
@roles_required('employer')
def employer_dashboard():
    jobs = Job.query.filter_by(employer_id=current_user.id).order_by(Job.created_at.desc()).all()
    return render_template('employer/dashboard.html', jobs=jobs)

@app.route('/employer/post_job', methods=['GET','POST'])
@roles_required('employer')
def post_job():
    form = JobForm()
    if form.validate_on_submit():
        job = Job(title=form.title.data, description=form.description.data,
                  location=form.location.data, employer_id=current_user.id)
        db.session.add(job)
        db.session.commit()
        flash('Job posted', 'success')
        return redirect(url_for('employer_dashboard'))
    return render_template('employer/post_job.html', form=form)

@app.route('/employer/job/<int:job_id>/applications')
@roles_required('employer')
def view_applications(job_id):
    job = Job.query.get_or_404(job_id)
    if job.employer_id != current_user.id:
        abort(403)
    applications = job.apps = job.applications
    return render_template('jobs/list.html', jobs=[], applications=applications)  # reuse simple view

# Jobseeker routes
@app.route('/jobseeker/dashboard')
@roles_required('jobseeker')
def jobseeker_dashboard():
    apps = Application.query.filter_by(user_id=current_user.id).order_by(Application.applied_at.desc()).all()
    return render_template('jobseeker/dashboard.html', applications=apps)

@app.route('/jobseeker/profile', methods=['GET','POST'])
@roles_required('jobseeker')
def profile():
    # simple profile edit (name only demo)
    if request.method == 'POST':
        current_user.name = request.form.get('name')
        db.session.commit()
        flash('Profile updated','success')
    return render_template('jobseeker/profile.html')

# Admin routes
@app.route('/admin/dashboard')
@roles_required('admin')
def admin_dashboard():
    # compute simple stats
    total_jobs = Job.query.count()
    total_employers = User.query.filter_by(role='employer').count()
    total_jobseekers = User.query.filter_by(role='jobseeker').count()

    # time filtered counts (examples)
    now = datetime.utcnow()
    day_ago = now - timedelta(days=1)
    week_ago = now - timedelta(days=7)
    month_ago = now - timedelta(days=30)
    year_ago = now - timedelta(days=365)

    jobs_day = Job.query.filter(Job.created_at >= day_ago).count()
    jobs_week = Job.query.filter(Job.created_at >= week_ago).count()
    jobs_month = Job.query.filter(Job.created_at >= month_ago).count()
    jobs_year = Job.query.filter(Job.created_at >= year_ago).count()

    return render_template('admin/dashboard.html',
                           total_jobs=total_jobs,
                           total_employers=total_employers,
                           total_jobseekers=total_jobseekers,
                           jobs_day=jobs_day, jobs_week=jobs_week, jobs_month=jobs_month, jobs_year=jobs_year)

# simple route to create sample data (for testing) - remove or protect in production
@app.route('/create-sample')
def create_sample():
    if User.query.filter_by(email='emp@company.com').first():
        flash('Sample already created', 'info')
        return redirect(url_for('index'))
    emp = User(email='emp@company.com', password='emppass', name='Employer Inc', role='employer', company='Employer Inc')
    seeker = User(email='js@user.com', password='jspass', name='Job Seeker', role='jobseeker')
    db.session.add_all([emp,seeker])
    db.session.commit()
    j1 = Job(title='Frontend Developer', description='Work with React/HTML/CSS', location='Remote', employer_id=emp.id)
    j2 = Job(title='Backend Python Developer', description='Flask / Django experience', location='Bengaluru', employer_id=emp.id)
    db.session.add_all([j1,j2])
    db.session.commit()
    flash('Sample data created', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
