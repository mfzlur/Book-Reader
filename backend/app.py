#<------------------------------IMPORTS-------------------------------------->

from flask import Flask, jsonify, request, make_response, send_file, url_for
from flask.views import MethodView
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, unset_jwt_cookies, get_jwt
from flask_restful import Api, Resource
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta
from flask_cors import CORS
from flask_migrate import Migrate
import os
from werkzeug.utils import secure_filename

from flask_caching import Cache

from worker import celery_init_app
from tasks import auto_book_return, send_email_using_celery, send_monthly_report
from celery.result import AsyncResult
from celery.schedules import crontab
import pandas as pd

#<---------------------------------INIT-------------------------------------->

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Secret key for JWT
db = SQLAlchemy(app)
jwt = JWTManager(app)
api = Api(app)
app.app_context().push()

UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Enable CORS
CORS(app, origins='http://localhost:5173')
migrate = Migrate(app,db) # database migration setup 


# Add CORS headers to every response
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET, PUT, POST, DELETE, OPTIONS'
    return response


# Configuration for Flask-Caching
app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_HOST'] = 'localhost'
app.config['CACHE_REDIS_PORT'] = 6379 
app.config['CACHE_REDIS_DB'] = 0
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'

# Initialize the cache
cache = Cache(app)

celery_app = celery_init_app(app)

#<-------------------------------MODELS--------------------------------------->


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    admin = db.Column(db.Boolean, default=False)

    requests_by_user = db.relationship('Request', backref='user', lazy=True, cascade="all,delete")
    ratings = db.relationship('Rating', backref='user', lazy=True, cascade="all,delete")

    bought_books = db.relationship('BoughtBook', backref='user', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "admin": self.admin
        }
    

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    author = db.Column(db.String(255))
    description = db.Column(db.Text)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'))
    total_copy = db.Column(db.Integer)
    issued_copy = db.Column(db.Integer)
    present_copy = db.Column(db.Integer)
    filename = db.Column(db.String(255))

    requests_for_book = db.relationship('Request', backref='book', cascade="all,delete")
    ratings = db.relationship('Rating', backref='book', lazy=True, cascade="all,delete")

    bought_books = db.relationship('BoughtBook', backref='book', lazy=True)

    def average_rating(self):
        total_ratings = sum([rating.rating for rating in self.ratings])
        if total_ratings:
            return total_ratings / len(self.ratings)
        

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "author": self.author,
            "description": self.description,
            "section_id": self.section_id,
            "section": Section.query.get(self.section_id).name,
            "filename": self.filename,
            "total_copy": self.total_copy,
            "issued_copy": self.issued_copy,
            "present_copy": self.present_copy,
            "average_rating": self.average_rating(),
            
        }

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    description = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.now())

    books = db.relationship('Book', backref='section', lazy=True, cascade="all,delete")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "date_created": self.date_created.isoformat(),
            "books": [book.to_dict() for book in self.books]
        }

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    date_requested = db.Column(db.DateTime())
    status = db.Column(db.Enum('pending', 'bought', 'rejected', 'approved', 'revoked', 'returned', name='request_status'))
    date_return = db.Column(db.DateTime())

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "book_id": self.book_id,
            "date_requested": self.date_requested,
            "status": self.status,
            "date_return": self.date_return.isoformat() if self.date_return else None
        }
class BoughtBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    date_bought = db.Column(db.DateTime())
    quantity = db.Column(db.Integer)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "book_id": self.book_id,
            "date_bought": self.date_bought.isoformat(),
            "quantity": self.quantity,
            "book_name": Book.query.get(self.book_id).name,
            "book_author": Book.query.get(self.book_id).author,
            "filename": Book.query.get(self.book_id).filename,
            "average_rating": Book.query.get(self.book_id).average_rating()


        }

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    rating = db.Column(db.Integer)

#<----------------------------CELERY REDIS TASKS------------------------------->

@app.route('/cache')
@cache.cached(timeout=30)
def index():
    return  str(datetime.now())

# celery


@celery_app.task
def generate_csv_task(data):
    df = pd.DataFrame(data)
    csv_path = './export.csv'
    df.to_csv(csv_path, index=False)
    return csv_path

@app.route('/export-csv', methods=['POST'])
def export_csv():
    data = request.json  # The data you want to export
    task = generate_csv_task.apply_async(args=[data])
    return jsonify({"task_id": task.id, "status_url": url_for('task_status', task_id=task.id)})

@app.route('/status/<task_id>')
def task_status(task_id):
    task = generate_csv_task.AsyncResult(task_id)
    print(task.state)
    if task.state == 'SUCCESS':
        return send_file(task.result, as_attachment=True)
    else:
        return jsonify({"state": task.state})

#celery beat
@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Executes every 20 seconds
    sender.add_periodic_task(20.0, auto_book_return.s(), name='add every 20', expires=100)

    # Executes tasks every day at 6:16 (UTC).
    sender.add_periodic_task(
        crontab(minute=00, hour=12),
        auto_book_return.s(),
    )
    sender.add_periodic_task(
        crontab(0, 0, day_of_month='1'),
        send_monthly_report.s()
    )

    sender.add_periodic_task(10.0, send_monthly_report.s(), name=' email add every 10 ', expires=100)
    return "Task Executed Successfully"

@app.route('/api/celery/email/<name>/<email>', methods=['POST'])
def celery_test_endpoint(name, email):
    result = send_email_using_celery.delay(name, email)

    return jsonify({'task_id': str(result)})

@app.route('/api/celery/email/status/<task_id>', methods=['GET', 'POST'])
def celery_status_endpoint(task_id):
    result = AsyncResult(task_id)
    return jsonify({'status': result.state, 'result': result.result})

#<----------------------------HELPER FUNCTIONS-------------------------------->




def create_admin():
    """Create an admin user if one doesn't exist."""
    if not db.session.query(User).filter(User.admin==True).first():
        user = User(name='Admin User', email='admin@email.com', password=generate_password_hash('Admin@123'), admin=True)
        db.session.add(user)
        db.session.commit()

#<-------------------------------ROUTES--------------------------------------->

@app.route('/api/login', methods=['POST'])
def login():
    """Login route to authenticate users and provide a JWT token."""
    email = request.json.get('email')
    password = request.json.get('password')

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id, additional_claims={"is_admin": user.admin}, expires_delta=timedelta(days=1))
        return make_response(jsonify({
            'access_token': access_token,
            'user_id': user.id,
            'is_admin': user.admin,
            'name': user.name
        }), 200)
    
    return make_response(jsonify({'msg': 'Invalid credentials'}), 401)


@app.route('/api/logout', methods=['POST'])
@jwt_required()
def logout():
    response = jsonify({'message':'Logged out successfully'})
    unset_jwt_cookies(response)
    return response, 200

@app.route('/api/register', methods=['POST'])
def register():
    """Register route to create a new user."""
    name = request.json.get('name')
    email = request.json.get('email')
    password = request.json.get('password')
    
    if User.query.filter_by(email=email).first():
        return make_response(jsonify({'msg': 'Email already exists'}), 400)

    new_user = User(name=name, email=email, password=generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()
    
    return make_response(jsonify({'msg': 'User registered successfully'}), 201)

@app.route('/api/user/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get the profile of the current user."""
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    issued_books = Request.query.filter_by(user_id=user_id, status='approved').count()
    pending_books = Request.query.filter_by(user_id=user_id, status='pending').count()
    bought_books = BoughtBook.query.filter_by(user_id=user_id).count()
 
    return jsonify({'total_bought_books': bought_books, 'total_pending_books': pending_books, 'total_issued_books': issued_books, 'name': user.name, 'email': user.email})

@app.route('/api/search', methods=['GET'])
@jwt_required()
def search():
    query = request.args.get('q', '')
    query = query.lower()
    """Search for books and sections by query string."""
    
    books = Book.query.filter(Book.name.ilike(f'%{query}%') | Book.author.ilike(f'%{query}%')).all()
    sections = Section.query.filter(Section.name.ilike(f'%{query}%')).all()

    response = {
        "books": [book.to_dict() for book in books],
        "sections": [section.to_dict() for section in sections]
    }
    return jsonify(response)

@app.route('/api/add/book/rating/<int:book_id>', methods=['POST'])
@jwt_required()
def add_rating(book_id):
    """Add a rating for a book."""
    user_id = get_jwt_identity()
    rating = request.json.get('rating')

    existing_rating = Rating.query.filter_by(user_id=user_id, book_id=book_id).first()
    if existing_rating:
        existing_rating.rating = rating
        return jsonify({'msg': 'You have already Rated this book'})

    new_rating = Rating(user_id=user_id, book_id=book_id, rating=rating)
    db.session.add(new_rating)
    db.session.commit()

    return jsonify({'msg': 'Rating submitted successfully'})

@app.route('/api/add/book/<int:book_id>/<int:section_id>', methods=['POST'])
def add_book_to_section(book_id, section_id):
    """Add a book to a section."""
    book = Book.query.filter_by(id=book_id).first()
    if not book:
        return jsonify({'msg': 'Book not found'})

    section = Section.query.get(section_id)
    if not section:
        return jsonify({'msg': 'Section not found'})

    section.books.append(book)
    book.section_id = section_id
    db.session.commit()
    return jsonify({'msg': 'Book added to section'})

@app.route('/api/remove/book/<int:book_id>/<int:section_id>', methods=['POST'])
def remove_book_from_section(book_id, section_id):
    """Remove a book from a section."""
    book = Book.query.filter_by(id=book_id).first()
    if not book:
        return jsonify({'msg': 'Book not found'})

    section = Section.query.filter_by(id=section_id).first()
    if not section:
        return jsonify({'msg': 'Section not found'})

    if book in section.books:
        section.books.remove(book)
        db.session.commit()
    return jsonify({'msg': 'Book removed from section'})

@app.route('/api/book/request/<int:book_id>', methods=['POST'])
@jwt_required()
def request_book(book_id):
    """Request a book."""
    user_id = get_jwt_identity()
    existing_request = Request.query.filter_by(user_id=user_id, book_id=book_id, status='approved').first()
    if existing_request:
        return jsonify({'msg': 'You have already requested this  Go to My Books to check the status'})
    
    requests_count = Request.query.filter(
        Request.user_id == user_id,
        ~Request.status.in_(('revoked', 'rejected', 'returned'))
    ).count()
    if requests_count >= 5:
        return jsonify({'msg': 'You have already made 5 book requests. You can only make 5 book requests at a time.'})

    request_obj = Request(user_id=user_id, book_id=book_id, status='pending')
    db.session.add(request_obj)
    db.session.commit()
    return jsonify({'msg': 'Request submitted successfully'})

@app.route('/api/requests', methods=['GET'])
@jwt_required()
def get_book_requests():
    claims = get_jwt()
    if not claims['is_admin']:
        return make_response(jsonify({'msg': 'Admins only!'}), 403)
    """Get all requests for the current user."""
    requests = Request.query.all()
    return make_response(jsonify([req.to_dict() for req in requests]), 200)

@app.route('/api/accept/book/request/<int:request_id>', methods=['POST'])
def accept_request(request_id):
    """Accept a book request."""
    request_obj = Request.query.filter_by(id=request_id).first()
    request_obj.status = 'approved'
    request_obj.date_requested = datetime.now()
    book = Book.query.filter_by(id=request_obj.book_id).first()
    book.issued_copy += 1
    book.present_copy -= 1
    db.session.commit()
    return make_response(jsonify({'msg': 'Request accepted successfully'}), 200)

@app.route('/api/reject/book/request/<int:request_id>', methods=['POST'])
def reject_request(request_id):
    """Reject a book request."""
    request_obj = Request.query.filter_by(id=request_id).first()
    request_obj.status = 'rejected'
    db.session.commit()
    return make_response(jsonify({'msg': 'Request rejected successfully'}), 200)

@app.route('/api/revoke/book/request/<int:request_id>', methods=['POST'])
def revoke_request(request_id):
    """Revoke a book request."""
    request_obj = Request.query.filter_by(id=request_id).first()
    request_obj.status = 'revoked'
    db.session.commit()
    return make_response(jsonify({'msg': 'Request revoked successfully'}), 200)

@app.route('/api/user/books', methods=['GET'])
@jwt_required()
def get_user_books():
    """Get all books issued to the current user."""
    user_id = get_jwt_identity()
    requests = Request.query.filter_by(user_id=user_id, status='approved').all()
    books = [req.book.to_dict() for req in requests]
    return make_response(jsonify(books), 200)

@app.route('/api/return/book/<int:book_id>', methods=['POST'])
@jwt_required()
def return_book(book_id):
    """Return a book issued by the current user."""
    user_id = get_jwt_identity()
    
    request_obj = Request.query.filter_by(user_id=user_id, book_id=book_id, status='approved').first()
    if not request_obj:
        return make_response(jsonify({'msg': 'No active request found for this book.'}), 404)
    
    request_obj.status = 'returned'
    request_obj.date_return = datetime.now()
    book = request_obj.book
    book.present_copy += 1
    book.issued_copy -= 1
    db.session.commit()
    return make_response(jsonify({'msg': 'Book returned successfully.'}), 200)

@app.route('/api/book/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """Get a book by ID."""
    book = Book.query.filter_by(id=book_id).first()
    json_book = {
        'name': book.name,
        'author': book.author,
        'description': book.description,
        'total_copy': book.total_copy,
        'section_id': book.section_id
    }
    if not book:
        return make_response(jsonify({'msg': 'Book not found'}), 404)
    
    print(json_book)
    return make_response(jsonify(json_book), 200)

@app.route('/api/section/<int:section_id>', methods=['GET'])
def get_section(section_id):
    """Get a section by ID."""
    section = Section.query.filter_by(id=section_id).first()
    if not section:
        return make_response(jsonify({'msg': 'Section not found'}), 404)
    return make_response(jsonify(section.to_dict()), 200)



class BoughtBooksResource(Resource):
    @jwt_required()
    def get(self):
        """Get all books bought by the current user."""
        user_id = get_jwt_identity()
        requests = Request.query.filter_by(user_id=user_id, status='bought').all()
        books = [req.book.to_dict() for req in requests]
        return jsonify({'books': books})

api.add_resource(BoughtBooksResource, '/api/user/bought_books')

class BuyBookResource(Resource):
    @jwt_required()
    def post(self):
        """Buy a book for the current user."""
        user_id = get_jwt_identity()
        book_id = request.json.get('book_id')

        book = Book.query.get(book_id)
        if not book:
            return jsonify({'msg': 'Book not found'}), 404

        existing_request = Request.query.filter_by(user_id=user_id, book_id=book_id, status='bought').first()
        if existing_request:
            return make_response(jsonify({'msg': 'You have already bought this book.'}), 400)

        if book.present_copy <= 0:
            return make_response(jsonify({'msg': 'The book is not available.'}), 400)

        existing_request = Request.query.filter_by(user_id=user_id, book_id=book_id).first()
        if existing_request:
            existing_request.status = 'bought'
        else:
            new_request = Request(user_id=user_id, book_id=book_id, date_requested=datetime.now(), status='bought')
            db.session.add(new_request)

        book.present_copy -= 1
        book.issued_copy += 1
        db.session.commit()

        return make_response(jsonify({'msg': 'Book bought successfully.'}), 200)

api.add_resource(BuyBookResource, '/api/user/buy_book')

class BookDetailsResource(Resource):
    @jwt_required()
    def get(self, book_id):
        """Get details of a specific book."""
        book = Book.query.get(book_id)
        if not book:
            return make_response(jsonify({'msg': 'Book not found'}), 404)
        
        return make_response(jsonify({'book': book.to_dict()}), 200)

api.add_resource(BookDetailsResource, '/api/books/<int:book_id>')

class UserRequestStatusResource(Resource):
    @jwt_required()
    def get(self):
        """Get all requests made by the current user."""
        user_id = get_jwt_identity()
        requests = Request.query.filter_by(user_id=user_id).all()
        request_list = [req.to_dict() for req in requests]
        return jsonify({'requests': request_list})

    @jwt_required()
    def delete(self, request_id):
        """Delete a specific request made by the current user."""
        user_id = get_jwt_identity()
        request_obj = Request.query.filter_by(id=request_id, user_id=user_id).first()
        if not request_obj:
            return make_response(jsonify({'msg': 'Request not found.'}), 404)

        db.session.delete(request_obj)
        db.session.commit()
        return make_response(jsonify({'msg': 'Request deleted successfully.'}), 200)

api.add_resource(UserRequestStatusResource, '/api/user/requests', '/api/user/requests/<int:request_id>')

class UserRequestResource(Resource):
    @jwt_required()
    def post(self):
        """Make a request for a book."""
        user_id = get_jwt_identity()
        book_id = request.json.get('book_id')

        book = Book.query.filter_by(id=book_id).first()

        existing_request = Request.query.filter_by(user_id=user_id, book_id=book_id).first()
        if existing_request:
            if existing_request.status == 'bought':
                return make_response(jsonify({'msg': 'You have already bought this book'}), 400)
            return make_response(jsonify({'msg': 'You have already requested this book'}), 400)

        issued_books_count = Request.query.filter_by(user_id=user_id, status='approved').count()
        pending_books_count = Request.query.filter_by(user_id=user_id, status='pending').count()
        if (issued_books_count + pending_books_count) >= 5:
            return make_response(jsonify({'msg': 'You have already Requested the maximum number of books'}), 400)

        if book.present_copy <= 0:
            return make_response(jsonify({'msg': 'The book is not available'}), 400)

        new_request = Request(user_id=user_id, book_id=book_id, date_requested=datetime.now(), status='pending')
        db.session.add(new_request)
        db.session.commit()

        return make_response(jsonify({'msg': 'Request submitted successfully'}), 201)

api.add_resource(UserRequestResource, '/api/user/request_book')

class AdminRequestsResource(Resource):
    @jwt_required()
    def get(self):
        """Get all requests for admin review."""
        claims = get_jwt()
        if not claims['is_admin']:
            return make_response(jsonify({'msg': 'Admins only!'}), 403)

        requests = Request.query.all()
        return jsonify([request.to_dict() for request in requests])

    @jwt_required()
    def post(self):
        """Approve, reject, or revoke requests."""
        claims = get_jwt()
        if not claims['is_admin']:
            return make_response(jsonify({'msg': 'Admins only!'}), 403)

        request_id = request.json.get('request_id')
        action = request.json.get('action')

        request_obj = Request.query.filter_by(id=request_id).first()

        if action == 'approve':
            if request_obj.status == 'pending' and request_obj.book.present_copy > 0:
                request_obj.book.present_copy -= 1
                request_obj.book.issued_copy += 1
                request_obj.status = 'approved'
            else:
                return make_response(jsonify({'msg': 'Request cannot be approved'}), 400)
        elif action == 'reject':
            if request_obj.status == 'pending':
                request_obj.status = 'rejected'
            else:
                return make_response(jsonify({'msg': 'Request cannot be rejected'}), 400)
        elif action == 'revoke':
            if request_obj.status == 'approved':
                request_obj.book.present_copy += 1
                request_obj.book.issued_copy -= 1
                request_obj.status = 'revoked'
            else:
                return make_response(jsonify({'msg': 'Request cannot be revoked'}), 400)
        else:
            return make_response(jsonify({'msg': 'Invalid action'}), 400)

        db.session.commit()
        return make_response(request_obj.to_dict(), 200)

api.add_resource(AdminRequestsResource, '/api/admin/requests')

@app.route('/api/my/books', methods=['GET'])
@jwt_required()
def my_books():
    """Get all books issued to the current user."""
    user_id = get_jwt_identity()
    requests = Request.query.filter_by(user_id=user_id).all()
    books = []
    for req in requests:
        if req.status != 'revoked':
            books.append(req.book.to_dict())
            books[-1]['request_status'] = req.status
    return make_response(jsonify(books), 200)

@app.route('/api/buy/book/<int:book_id>', methods=['POST'])
@jwt_required()
def buy_book(book_id):
    """Buy a book."""
    user_id = get_jwt_identity()

    bought_book = BoughtBook.query.filter_by(user_id=user_id, book_id=book_id).first()
    if bought_book:
        book = Book.query.filter_by(id=book_id).first()
        if book.present_copy <= 0:
            return make_response(jsonify({'msg': 'The book is not available'}), 200)
        bought_book.quantity += 1
        
        book.total_copy -= 1
        book.present_copy -= 1
        db.session.commit()
        return make_response(jsonify({'msg': 'Book is bought again'}), 200)

    book = Book.query.filter_by(id=book_id).first()
    user = User.query.filter_by(id=user_id).first()


    if book.present_copy <= 0:
        return make_response(jsonify({'msg': 'The book is not available'}), 200)


    bought_book = BoughtBook(user_id=user_id, book_id=book_id, date_bought=datetime.now(), quantity = 1)
    book.total_copy -= 1
    book.present_copy -= 1
    user.bought_books.append(bought_book)
    book.bought_books.append(bought_book)

    db.session.add(bought_book)
    db.session.commit()

    return make_response(jsonify({'msg': 'Book bought successfully'}), 200)

@app.route('/api/bought/books', methods=['GET'])
@jwt_required()
def bought_books():
    """Get all books bought by the current user."""
    user_id = get_jwt_identity()
    books = BoughtBook.query.filter_by(user_id=user_id).all()
    for b in books:
        print(b.to_dict())
    return make_response(jsonify([book.to_dict() for book in books]), 200)



class BookResource(Resource):
    @jwt_required(optional=True)
    def get(self, book_id=None):
        """Get book details or a list of all books."""
        if book_id:
            book = Book.query.filter_by(id=book_id).first()
            response_data = book.to_dict()

            if get_jwt_identity():
                user_id = get_jwt_identity()
                request = Request.query.filter_by(user_id=user_id, book_id=book_id).first()
                response_data['request_status'] = request.status if request else None
            else:
                response_data['request_status'] = None

            return jsonify(response_data)
        else:
            books = Book.query.all()
            return jsonify([book.to_dict() for book in books])

    @jwt_required()
    def post(self):
        """Add a new book (admin only)."""
        claims = get_jwt()
        if not claims['is_admin']:
            return make_response(jsonify({'msg': 'Admins only!'}), 403)
        

        section = Section.query.filter_by(name=request.form.get('section')).first()
        if not section:
            section = Section(name=request.form.get('section'))
            db.session.add(section)
            db.session.commit()


        
        new_book = Book(
            name=request.form.get('name'),
            author=request.form.get('author'),
            description=request.form.get('description'),
            section_id=section.id,
            total_copy=request.form.get('total_copies'),
            present_copy=request.form.get('total_copies'),
            issued_copy=0,
        )

        
        file = request.files['file']
    
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file_path2 = os.path.join('../frontend/public', filename)
            file.save(file_path)
            file.save(file_path2)
            new_book.filename = filename

        db.session.add(new_book)
        db.session.commit()
        return make_response(jsonify(new_book.to_dict()), 201)

    @jwt_required()
    def put(self, book_id):
        """Edit a book's details (admin only)."""
        claims = get_jwt()
        if not claims['is_admin']:
            return jsonify({'msg': 'Admins only!'}), 403

        book = Book.query.filter_by(id=book_id).first()
        data = request.json
        book.name = data['name']
        book.author = data['author']
        book.description = data['description']
        book.total_copy = data['total_copy']
        db.session.commit()
        return make_response(jsonify({'msg': 'Book updated successfully'}), 200)

    @jwt_required()
    def delete(self, book_id):
        """Delete a book (admin only)."""
        claims = get_jwt()
        if not claims['is_admin']:
            return make_response(jsonify({'msg': 'Admins only!'}), 403)

        book = Book.query.filter_by(id=book_id).first()
        db.session.delete(book)
        db.session.commit()
        return make_response(jsonify({'msg': 'Book deleted successfully'}), 201)

api.add_resource(BookResource, '/api/add/book', '/api/edit/book/<int:book_id>', '/api/delete/book/<int:book_id>')

class SectionResource(Resource):
    @jwt_required()
    def get(self, section_id=None):
        """Get section details or a list of all sections."""
        if section_id:
            section = Section.query.filter_by(id=section_id).first()
            books = Book.query.filter_by(section_id=section_id).all()
            book_list = [book.to_dict() for book in books]
            return jsonify({'section': section.to_dict(), 'books': book_list})
        else:
            sections = Section.query.all()
            return jsonify([section.to_dict() for section in sections])

    @jwt_required()
    def post(self):
        """Add a new section (admin only)."""
        claims = get_jwt()
        if not claims['is_admin']:
            return make_response(jsonify({'msg': 'Admins only!'}), 403)

        data = request.json
        new_section = Section(
            name=data['name'],
            description=data['description']
        )
        db.session.add(new_section)
        db.session.commit()
        return make_response(jsonify(new_section.to_dict()), 201)

    @jwt_required()
    def put(self, section_id):
        """Edit a section's details (admin only)."""
        claims = get_jwt()
        if not claims['is_admin']:
            return make_response(jsonify({'msg': 'Admins only!'}), 403)

        section = Section.query.filter_by(id=section_id).first()
        data = request.json
        section.name = data['name']
        section.description = data['description']
        db.session.commit()
        return make_response(jsonify(section.to_dict()), 200)

    @jwt_required()
    def delete(self, section_id):
        """Delete a section (admin only)."""
        claims = get_jwt()
        if not claims['is_admin']:
            return make_response(jsonify({'msg': 'Admins only!'}), 403)

        section = Section.query.filter_by(id=section_id).first()
        db.session.delete(section)
        db.session.commit()
        return make_response(jsonify({'msg': 'Section deleted.'}), 201)

api.add_resource(SectionResource, '/api/add/section', '/api/edit/section/<int:section_id>', '/api/delete/section/<int:section_id>')

@app.route('/api/other/books/<int:section_id>', methods=['GET'])
def get_other_books(section_id):
    books = Book.query.all()
    other_boooks = []
    for book in books:
        if not book.section_id:
            new_book = {
            "id": book.id,
            "name": book.name,
            "author": book.author,
            "description": book.description,
            "section_id": None,
            "section": 'Undefined',
            "total_copy": book.total_copy,
            "issued_copy": book.issued_copy,
            "present_copy": book.present_copy,
            # "link": self.link,
            "average_rating": book.average_rating()}

            other_boooks.append(new_book)
        elif book.section_id != section_id:
            other_boooks.append(book.to_dict())

    return jsonify(other_boooks)

@app.route('/api/librarian/stats', methods=['GET'])
def get_librarian_stats():
    books = Book.query.all()
    total_books = len(books)
    total_books_issued = sum(book.issued_copy for book in books)

    total_books_bought = BoughtBook.query.count()
    total_sections = Section.query.count()
    total_users = User.query.count()

    res = 0
    count = 0
    avg_book_rating = '-'
    for book in books:
        if book.average_rating() is not None:
            res += float(book.average_rating())
            count += 1
    if count > 0:
        avg_book_rating = round(res/count, 2)
    return jsonify({'total_books': total_books, 'total_books_issued': total_books_issued, 'total_books_bought': total_books_bought, 'total_sections': total_sections, 'total_users': total_users, 'average_book_rating': avg_book_rating}), 200

@app.route('/api/chartdata', methods=['GET'])
def get_chart_data():
    """Get chart data."""
    sections = Section.query.all()
    chart_data = {
        'labels': [section.name for section in sections],
        'data': [len(section.books) for section in sections]
    }
    return jsonify(chart_data)

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({"error": "File not found"}), 404

#<---------------------------------------RUN--------------------------------------->
if __name__ == '__main__':
    db.create_all()
    create_admin()
    app.run(debug=True)
