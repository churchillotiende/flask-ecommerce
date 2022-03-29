from ecomfinal import app , db
from flask import render_template , flash ,redirect , url_for, request , session , current_app

from ecomfinal.products.models import AddProduct

def MagerDicts(dict1 , dict2):
	if isinstance(dict1 , list) and isinstance(dict2 , list):
		return dict1 + dict2
	elif isinstance(dict1 , dict) and isinstance(dict2 , dict):
		return dict(list(dict1.items()) + list(dict2.items()))
	return False


@app.route('/addcart' , methods = ['POST'])
def AddCart():
    try:
        product_id = request.form.get('product_id')
        colors = request.form.get('colors')
        quantity = request.form.get('quantity')
        product = AddProduct.query.filter_by(id = product_id).first()

        if product_id and colors and quantity and request.method == 'POST':
            DictItems = {product_id:{"Name":product.name , "Cost":product.price , "Discount":product.discount , 'stock':product.stock,"Colors":colors , "Quantity":quantity , "Image": product.image_1 , 'color':product.color}}
            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
                if product_id in session['Shoppingcart']:
                    for key , item in session['Shoppingcart'].items():
                        if int(key) == int(product_id):
                            session.modified = True
                            item['Quantity'] +=1
                else:
                    session['Shoppingcart'] = MagerDicts(session['Shoppingcart'] , DictItems)
                    return redirect(request.referrer)
            else:
                session['Shoppingcart']= DictItems
                return redirect(request.referrer)
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)

@app.route('/carts')
def getCart():
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <=0:
        return redirect(url_for('home'))
    subtotal = 0
    grandtotal = 0
    for key, product in session['Shoppingcart'].items():
        product_cost = float(product['Cost'])
        product_quantity = int(product['Quantity'])
        discount = (product['Discount'] / 100 * float(product['Cost']))
        subtotal += product_cost * product_quantity
        subtotal -= discount
        tax = ('%.2f' % (0.006 * float(subtotal)))
        grandtotal = float('%.2f' % (1.006 * subtotal))
	
    return render_template('products/carts.html' , tax = tax , grandtotal = grandtotal)

@app.route('/empty')
def empty_cart():
    try:
         session.pop('Shoppingcart' , None)
         return redirect(url_for('home'))
    except Exception as e:
        print(e)

@app.route('/updatecart/<int:code>' , methods = ['POST'])
def update_cart(code):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    if request.method == 'POST':
        quantity = request.form.get('quantity')
        color = request.form.get('color')
    try:
        for key , item in session['Shoppingcart'].items():
            if int(key) == code:
                item['Quantity'] = quantity
                item['Colors'] = color
                flash(f'Your item has been updated' , 'success')
                return redirect(url_for('getCart'))
    except Exception as e:
        print(e)
        return redirect(url_for('getCart'))

@app.route('/deleteitem/<int:id>')
def deleteitem(id):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <=0:
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key , item in session['Shoppingcart'].items():
            if int(key) == id:
                session['Shoppingcart'].pop(key , None)
                return redirect(url_for('getCart'))
        pass
    except Exception as e:
        print(e)
        return redirect(url_for('getCart'))