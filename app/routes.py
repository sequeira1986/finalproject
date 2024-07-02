from flask import Blueprint, render_template, url_for, flash, redirect, request
from app import db, bcrypt
from app.models import User, Lesson, Registration
from app.forms import RegistrationForm, LoginForm, LessonForm
from flask_login import login_user, current_user, logout_user, login_required

bp = Blueprint('routes', __name__)


@bp.route('/')
@bp.route('/index')
def index():
    lessons = Lesson.query.all()
    return render_template('index.html', lessons=lessons)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('routes.login'))
    return render_template('register.html', title='Register', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('routes.index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('routes.index'))


@bp.route('/lesson/new', methods=['GET', 'POST'])
@login_required
def new_lesson():
    form = LessonForm()
    if form.validate_on_submit():
        lesson = Lesson(title=form.title.data, subject=form.subject.data, level=form.level.data,
                        content=form.content.data, author=current_user)
        db.session.add(lesson)
        db.session.commit()
        flash('Your lesson has been created!', 'success')
        return redirect(url_for('routes.index'))
    return render_template('create_lesson.html', title='New Lesson', form=form)


@bp.route('/lesson/<int:lesson_id>')
def lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    return render_template('lesson_detail.html', title=lesson.title, lesson=lesson)


@bp.route('/about')
def about():
    return render_template('about.html', title='About')


@bp.route('/lesson/<int:lesson_id>/register')
@login_required
def register_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    registration = Registration(student=current_user, lesson=lesson)
    db.session.add(registration)
    db.session.commit()
    flash('You have successfully registered for the lesson!', 'success')
    return redirect(url_for('routes.lesson', lesson_id=lesson_id))


@bp.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        keyword = request.form['keyword']
        lessons = Lesson.query.filter(Lesson.title.contains(keyword) | Lesson.subject.contains(keyword)).all()
        return render_template('search_results.html', lessons=lessons, keyword=keyword)
    return redirect(url_for('routes.index'))
