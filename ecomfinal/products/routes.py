from ecomfinal.admin.routes import category
from .models import Brand , Category , AddProduct
from .forms import AddProducts
from ecomfinal import app , db , bcrypt , photos , search
from flask import render_template , flash ,redirect , url_for, request , session , current_app
import secrets
import os

@app.route('/')
@app.route('/home' , methods = ['GET' , 'POST'])
def home():
    page = request.args.get('page',1 ,type = int)
    products = AddProduct.query.filter(AddProduct.stock > 0).paginate(page = page , per_page = 4)
    brands = Brand.query.join(AddProduct , Brand.id == AddProduct.brand_id).all()
    categories = Category.query.join(AddProduct , (Category.id == AddProduct.brand_id)).all()
    return render_template('products/index.html' , title = 'Candleglows' , products = products , brands = brands  , categories = categories)

@app.route('/result')
def result():
    searchword = request.args.get('query')
    products = AddProduct.query.msearch(searchword, fields=['name','description'] , limit=6)
    return render_template('products/result.html',products=products)

@app.route('/product/:<int:id>' , methods = ['GET'])
def single_page(id):
    product = AddProduct.query.get_or_404(id)
    brands = Brand.query.join(AddProduct , Brand.id == AddProduct.brand_id).all()
    categories = Category.query.join(AddProduct , (Category.id == AddProduct.brand_id)).all()
    return render_template('/products/single_page.html' , product = product , brands = brands , categories = categories)

@app.route('/brand/:<int:id>' , methods = ['GET'])
def get_brand(id):
    brand = AddProduct.query.filter_by(brand_id = id)
    brands = Brand.query.join(AddProduct , Brand.id == AddProduct.brand_id).all()
    categories = Category.query.join(AddProduct , (Category.id == AddProduct.brand_id)).all()
    return render_template('products/index.html' , title = 'Candleglows' , brand = brand , brands = brands , categories = categories)

@app.route('/category:<int:id>', methods = ['GET'])
def get_prod_cat(id):
    get_prod_cats = AddProduct.query.filter_by(category_id = id)
    categories = Category.query.join(AddProduct , Category.id == AddProduct.category_id).all()
    brands = Brand.query.join(AddProduct , Brand.id == AddProduct.brand_id).all()
    return render_template('products/index.html' , title = 'Candleglows', categories = categories, brands = brands , get_prod_cats=get_prod_cats)

@app.route('/addbrand' , methods = ['GET' , 'POST'])
def addbrand():
    if request.method == 'POST':
        getBrand = request.form.get('brand')
        brand = Brand(name=getBrand)
        db.session.add(brand)
        flash(f'The brand {getBrand} was added to your database' , 'success')
        db.session.commit()
        return redirect(url_for('addbrand'))
    return render_template('products/addbrand.html' , title = 'Brand' , brands = 'brands')

@app.route('/updatebrand:<int:id>', methods =['GET','POST'])
def updatebrand(id):
    if 'email' not in session:
        flash(f'Please login first' , 'danger')
    updatebrand =Brand.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method == 'POST':
        updatebrand.name = brand
        flash(f'Your brand has been updated' , 'success')
        db.session.commit()
        return redirect(url_for('brands'))
    return render_template('products/updatebrand.html' , title = 'updatebrand page' , updatebrand = updatebrand)

@app.route('/deletebrand/<int:id>', methods=['POST'])
def deletebrand(id):
    brand = Brand.query.get_or_404(id)
    if request.method=="POST":
        db.session.delete(brand)
        db.session.commit()
        flash(f"The brand {brand.name} was deleted from your database","success")
        return redirect(url_for('admin'))
    flash(f"The brand {brand.name} can't be  deleted from your database","warning")
    return redirect(url_for('admin'))

@app.route('/addcat' , methods = ['GET' , 'POST'])
def addcat():
    if request.method == 'POST':
        getCat = request.form.get('category')
        category = Category(name=getCat)
        db.session.add(category)
        flash(f'The category {getCat} was added to your database' , 'success')
        db.session.commit()
        return redirect(url_for('addcat'))
    return render_template('products/addbrand.html' , title = 'Category')

@app.route('/updatecat:<int:id>', methods =['GET','POST'])
def updatecat(id):
    if 'email' not in session:
        flash(f'Please login first' , 'danger')
    updatecat =Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method == 'POST':
        updatecat.name = category
        flash(f'Your category has been updated' , 'success')
        db.session.commit()
        return redirect(url_for('category'))
    return render_template('products/updatebrand.html' , title = 'updatecategory page' ,updatecat = updatecat)

@app.route('/deletecategory/<int:id>' , methods = ['POST'])
def deletecategory(id):
    category = Category.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(category)
        db.session.commit()
        flash(f'The category { category.name } was deleted' , 'success')
        return redirect(url_for('admin'))
    flash(f'The category { category.name } cant be deleted' , 'success')
    return redirect(url_for('admin'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _ , f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path , 'static/images' , picture_fn)
    form_picture.save(picture_path)

    return picture_fn


@app.route('/addproduct' , methods = ['GET' , 'POST'])
def addproduct():
    brands = Brand.query.all()
    categories = Category.query.all()
    form = AddProducts()

    if request.method == 'POST':
        image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
        image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
        image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")

        # These are the names selected in the various brand and categories fields
        brand = request.form.get('brand')
        category = request.form.get('category')

        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        description = form.description.data
        color = form.color.data       
        product = AddProduct(name = name ,price = price, discount = discount, stock = stock , description = description , 
                                color = color , image_1 = image_1 , image_2 = image_2 , image_3 = image_3 , brand_id = brand , category_id = category)
        db.session.add(product)
        db.session.commit()
        flash(f'The product {form.name.data} is added to the database')
        return redirect(url_for('home'))
    return render_template('products/addproduct.html' , title = 'Add Product' , form = form , brands = brands , categories = categories)

@app.route('/updateproduct/<int:id>' , methods = ['GET' , 'POST'])
def updateproduct(id):
    form = AddProducts(request.form)
    categories = Category.query.all()
    brands = Brand.query.all()
    product = AddProduct.query.get_or_404(id)
    brand = request.form.get('brand')
    category = request.form.get('category')
    if request.method == 'POST' and 'image_1' in request.files:
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.stock = form.stock.data
        product.description = form.description.data
        product.color = form.color.data
        product.brand_id = brand
        product.category_id = category

        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
            except:
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
                product.image_1 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
            except:
                product.image_1 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
                product.image_1 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
            except:
                product.image_1 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")

        flash('The product was updated','success')
        db.session.commit()
        return redirect(url_for('admin'))
    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.description.data = product.description
    form.color.data = product.color
    form.image_1.data = product.image_1
    form.image_2.data = product.image_2
    form.image_3.data = product.image_3
    return render_template('products/updateproduct.html' , form = form , categories = categories , brands = brands , product = product)

@app.route('/deleteproduct:<int:id>' , methods = ['POST'])
def deleteproduct(id):
    product = AddProduct.query.get_or_404(id)
    if request.method == 'POST':
        try:
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
        except Exception as e:
            print(e)
        db.session.delete(product)
        db.session.commit()
        flash('The product was deleted','success')
        return redirect(url_for('admin'))
    flash(f'Cant delete the product' , 'danger')
    return redirect(url_for('admin'))