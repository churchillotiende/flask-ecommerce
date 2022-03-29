from turtle import title
from flask import render_template , flash , redirect , url_for , request , session
from ecomfinal import app , db , bcrypt
from .forms import AdminRegForm , AdminLoginForm , UpdateAccountForm
from .models import Admin
from ecomfinal.products.models import AddProduct , Brand , Category
from flask_login import login_user , logout_user , current_user , login_required

@app.route('/admin')
def admin():
    products = AddProduct.query.all()
    return render_template('admin/index.html' , title = 'Admin Page'  ,products = products)


@app.route('/brands')
def brands():
	brands = Brand.query.order_by(Brand.id.desc()).all()
	return render_template('admin/brand.html' ,title = 'Brand Page' , brands = brands)

@app.route('/category')
def category():
	categories = Category.query.order_by(Category.id.desc()).all()
	return render_template('admin/brand.html' ,title = 'Category Page' , categories = categories)

@app.route("/admin/register" , methods = ['GET', 'POST'])
def register():
    form = AdminRegForm()
    if form.validate_on_submit():
        password=bcrypt.generate_password_hash(form.password_hash.data).decode('utf-8')
        admin = Admin(username = form.username.data ,password_hash = password, confirm_pwd = password, email = form.email.data) 
        db.session.add(admin)
        db.session.commit()
        flash(f'Welcome {form.username.data} you are now able to login')
        return redirect(url_for('admin_login'))
    return render_template("admin/register.html" , title ='AdminRegister' , form = form)

@app.route('/admin_login', methods = ['GET','POST'])
def admin_login():
        if current_user.is_authenticated:
            return redirect(url_for('admin'))
        form =AdminLoginForm()
        if form.validate_on_submit():
            admin=Admin.query.filter_by(email=form.email.data).first()
            if admin and bcrypt.check_password_hash(admin.password_hash , form.password_hash.data):
                login_user(admin , form.remember_me.data) 
                next_page=request.args.get('next')               
                flash('You have logged in successfully' , 'success')
                return redirect(next_page) if next_page else redirect(url_for('admin'))
            else:
                flash("Login unsuccessful please check email and Password" , 'danger')
        return render_template('admin/login.html' , title = 'Admin Login' , form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('admin'))

@app.route('/account' , methods = ['POST' , 'GET'])
@login_required
def account():
    form=UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your Account has been updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
            form.username.data= current_user.username
            form.email.data= current_user.email
    image_file = url_for('static' , filename = 'images/' + current_user.image_file)
    return render_template('account.html' , title = 'Account' , image_file=image_file , form=form)