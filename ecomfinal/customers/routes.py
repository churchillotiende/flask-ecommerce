import email

from click import confirm
from .forms import Customer, CustomerLoginForm , UpdateAccountForm
from .models import CustomerOrder, CustomerRegister
from ecomfinal import app , db , bcrypt , photos
from flask import render_template , flash ,redirect , url_for, request, session
from flask_login import current_user, login_user
import secrets
import os
from flask_login import login_required

@app.route('/customer/reg' , methods = ['GET' , 'POST'])
def customer_reg():
    form = Customer(request.form)
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data)
        register = CustomerRegister(name = form.name.data ,city = form.city.data , country = form.country.data , zip_code = form.zip_code.data , address = form.address.data ,email = form.email.data , password = hashed_pw , confirm = hashed_pw)
        db.session.add(register)
        flash(f'Welcome{form.name.data}' , 'success')
        db.session.commit()
        return redirect(url_for('customer'))
    return render_template('customer/register.html' , form = form)

@app.route('/customer' , methods = ['GET'])
def customer():
    return render_template('customer/index.html')

@app.route('/customer/account' , methods = ['POST' , 'GET'])
@login_required
def custom_account():
    form=UpdateAccountForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.city = form.city.data
        current_user.country = form.country.data
        current_user.date_created = form.date_created.data
        current_user.zip_code = form.zip_code.data
        current_user.profile = form.profile.data
        current_user.address = form.address.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f'Your Account has been updated', 'success')
        return redirect(url_for('custom_account'))
    elif request.method == 'GET':
            form.name.data= current_user.name
            form.city.data =current_user.city
            form.country.data =current_user.country
            form.date_created.data =current_user.date_created
            form.zip_code.data =current_user.zip_code
            form.profile.data =  current_user.profile
            form.address.data = current_user.address
            form.email.data= current_user.email
    # image_file = url_for('static' , filename = 'images/' + current_user.profile)
    return render_template('customer/account.html' , title = 'Account', form=form)

@app.route('/customer_login', methods = ['GET','POST'])
def customer_login():
        form =CustomerLoginForm()
        if form.validate_on_submit():
            user=CustomerRegister.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password , form.password.data):
                login_user(user , form.remember_me.data) 
                next_page=request.args.get('next')               
                flash('You have logged in successfully' , 'success')
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash("Login unsuccessful please check email and Password" , 'danger')
        return render_template('customer/login.html' , title = 'customer Login' , form = form)


@app.route('/getorder')
@login_required
def get_order():
	if current_user.is_authenticated:
		customer_id = current_user.id
		invoice = secrets.token_hex(4)
		try:
			order = CustomerOrder(invoice = invoice , customer_id = customer_id , orders = session['Shoppingcart'])
			db.session.add(order)
			db.session.commit()
			session.pop('Shoppingcart')
			flash(f'Your order has been sent successfully' , 'success')
			return redirect(url_for('orders' , invoice = invoice))
		except Exception as e:
			print(e)
			flash('Something went wrong' , 'danger')
			return redirect(url_for('getCart'))
			

@app.route('/orders/<invoice>')
@login_required

def orders(invoice):
    if current_user.is_authenticated:
        grandTotal = 0
        subTotal = 0
        customer_id = current_user.id
        customer = CustomerRegister.query.filter_by(id = customer_id).first()
        orders = CustomerOrder.query.filter_by(customer_id = customer_id).order_by(CustomerOrder.id.desc()).first()
        for _key , product in orders.orders.items():
            discount = (product['Discount']/100) * float(product['Cost'])
            subTotal += float(product['Cost']) * int(product['Quantity'])
            subTotal -= discount
            tax = ("%.2f" % (.006 * float(subTotal)))
            grandTotal = float("%.2f" % (1.006 * subTotal))
    else:
        return redirect(url_for('customer_login'))
    return render_template('customer/order.html' , invoice= invoice , tax = tax , subTotal = subTotal , grandTotal = grandTotal , orders = orders , customer = customer)
