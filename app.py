from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a secure key
db = SQLAlchemy(app)

# Import the database models
from models import Product,ProductMovement,Location

# Routes and views

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/products', methods=['GET', 'POST'])
def products():
    if request.method == 'POST':
        product_id = request.form['product_id']
        if product_id:
            new_product = Product(product_id=product_id)
            db.session.add(new_product)
            db.session.commit()
    products = Product.query.all()
    return render_template('products.html', products=products)

@app.route('/locations', methods=['GET', 'POST'])
def locations():
    if request.method == 'POST':
        location_id = request.form['location_id']
        if location_id:
            new_location = Location(location_id=location_id)
            db.session.add(new_location)
            db.session.commit()
    locations = Location.query.all()
    return render_template('locations.html', locations=locations)

@app.route('/movements', methods=['GET', 'POST'])
def movements():
    if request.method == 'POST':
        movement_id = request.form['movement_id']
        from_location = request.form['from_location']
        to_location = request.form['to_location']
        product_id = request.form['product_id']
        qty = int(request.form['qty'])
        if movement_id and (from_location or to_location) and product_id and qty:
            new_movement = ProductMovement(
                movement_id=movement_id,
                from_location=from_location,
                to_location=to_location,
                product_id=product_id,
                qty=qty
            )
            db.session.add(new_movement)
            db.session.commit()
    movements = ProductMovement.query.all()
    return render_template('movements.html', movements=movements)

if __name__ == '__main__':
    app.run(debug=True)