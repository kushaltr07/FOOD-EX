from flask import Flask, render_template, redirect, url_for, session, request
from datetime import datetime
app = Flask(__name__)
app.secret_key = "foodex123"

menu_items = [
    {"id":1,"name":"BURGER","price":120,"image":"BURGER.jpg"},
    {"id":2,"name":"Pizza","price":250,"image":"Pizza.jpg"},
    {"id":3,"name":"Pasta","price":180,"image":"Pasta.jpg"},
    {"id":4,"name":"Sandwich","price":150,"image":"Sandwich.jpg"},
    {"id":5,"name":"Fries","price":100,"image":"Fries.jpg"},
    {"id":6,"name":"Noodles","price":170,"image":"Noodles.jpg"},
    {"id":7,"name":"Biryani","price":220,"image":"Biryani.jpg"},
    {"id":8,"name":"Drink","price":60,"image":"Drink.jpg"},
    {"id":9,"name":"Ice Cream","price":90,"image":"Icecream.jpg"},
]
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/menu')
def menu():
    return render_template('menu.html', items=menu_items)

@app.route('/add/<int:item_id>')
def add(item_id):
    cart = session.get('cart', [])

    for item in menu_items:
        if item["id"] == item_id:
            cart.append(item)

    session['cart'] = cart
    return redirect(url_for('menu'))

@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    total = sum(item["price"] for item in cart_items)
    return render_template('cart.html', cart=cart_items, total=total)

@app.route('/checkout')
def checkout():
    cart_items = session.get('cart', [])
    total = sum(item["price"] for item in cart_items)

    return render_template("checkout.html", total=total)

@app.route('/place_order', methods=['POST'])
def place_order():
    name = request.form['name']
    phone = request.form['phone']
    address = request.form['address']
    payment = request.form['payment']

    cart_items = session.get('cart', [])
    total = sum(item["price"] for item in cart_items)

    order_time = datetime.now().strftime("%d-%m-%Y %I:%M %p")

    response = render_template(
        'order_success.html',
        name=name,
        phone=phone,
        address=address,
        payment=payment,
        total=total,
        cart=cart_items,
        order_time=order_time
    )

    # Clear cart after creating the response
    session['cart'] = []

    return response

@app.route('/remove/<int:index>')
def remove(index):
    cart = session.get('cart', [])

    if 0 <= index < len(cart):
        cart.pop(index)

    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/clear')
def clear():
    session['cart'] = []
    return redirect(url_for('cart'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)