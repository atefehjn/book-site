from flask import render_template, redirect, url_for, flash,Blueprint,abort, session
# from forms import RegistrationForm,SignInForm
from .forms import RegistrationForm, SignInForm
from .books import books
bp = Blueprint('main', __name__)

user_data = {}

@bp.route('/')
def index():
    return redirect(url_for('main.home'))

@bp.route('/registration')
def signup():
    return render_template('index.html')
@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        
        # Store user data in the dictionary
        if username not in user_data:
            user_data[username] = {'email': email, 'password': password}
            flash('You have successfully signed up!', 'success')
            return redirect(url_for('main.signin'))
        else:
            flash('Username already exists. Please choose a different one.', 'danger')
    return render_template('register.html', form=form)

@bp.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SignInForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        print(username," ",password)
        # Check if the user exists and the password is correct
        if username in user_data and user_data[username]['password'] == password:
            session['user'] = username  # Store the username in the session
            flash('You have successfully signed in!', 'success')
            return redirect(url_for('main.home'))  # Assuming you have a home route
        else:
            flash('Invalid username or password.', 'danger')
    
    return render_template('signin.html', form=form)

@bp.route('/home')
def home():
    book_list = books.values()
    is_logged_in = 'user' in session
    return render_template('home.html',books = book_list,is_logged_in=is_logged_in)

@bp.route('/home/<book_id>')
def book_details(book_id):
    if 'user' not in session:  # Check if the user is not signed in
        flash('Please sign in to view book details.', 'warning')
        return redirect(url_for('main.signup'))  # Redirect to registration page if not signed in
    book = books.get(book_id)
    if book is None:
        abort(404)
    return render_template('book_detail.html', book=book)

@bp.route('/logout')
def logout():
    session.pop('user', None)  # Remove the user from the session
    flash('You have successfully logged out.', 'info')
    return redirect(url_for('main.home'))
