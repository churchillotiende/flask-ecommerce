from ecomfinal import db
class AddProduct(db.Model):
	__tablename__ = 'products'
	id = db.Column(db.Integer , primary_key=True)
	name = db.Column(db.String(30) , nullable = False , unique = True)
	price = db.Column(db.Float(30) , nullable = False)
	discount = db.Column(db.Float(30) , nullable = False , default= 0)
	stock = db.Column(db.Integer , nullable = False)
	color = db.Column(db.String(30) , nullable = False)
	description = db.Column(db.Text(130) , nullable = False)

	brand_id = db.Column(db.Integer , db.ForeignKey('brand.id') , nullable = False)
	brand = db.relationship('Brand' , backref =db.backref('brands') , lazy = True)
	category_id = db.Column(db.Integer , db.ForeignKey('category.id') , nullable = False)
	category = db.relationship('Category' , backref =db.backref('posts') , lazy = True)

	image_1 = db.Column(db.String(125) , nullable = False , default = 'default.jpg')
	image_2 = db.Column(db.String(125) , nullable = False , default = 'default.jpg')
	image_3 = db.Column(db.String(125) , nullable = False , default = 'default.jpg')


class Brand(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(30) , nullable = False , unique = True)

class Category(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(30) , nullable = False , unique = True)
db.create_all()