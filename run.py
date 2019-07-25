from flask import Flask, session, render_template, request, redirect, url_for, Response, json, g, flash
from flask_sqlalchemy import SQLAlchemy
import os
import random
import subprocess
import csv
import socket

app = Flask(__name__)
app.secret_key = os.urandom(67)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stock.db'

try:
	win_cmd = 'ipconfig'
	process = subprocess.check_output(win_cmd).decode()
	try:
		index = process.index('192')
	except:
		index = process.index('169')
        
	IP = ""
	
	for i in range(16):
                v = process[index+i]
                if not v.isdigit():
                        if v != '.':
                                break
                
                IP = IP + v
                
	
	print(IP)
	
except:
	unix_cmd = 'ifconfig'
	process = subprocess.check_output(unix_cmd).decode()
	try:
		index = process.index('192')
	except:
		index = process.index('10')
	IP = ""
	for i in range(15):
		IP = IP+process[index+i]
	IP = IP.strip()
	print(IP)
	os.system('rm ~/Documents/Flask_Apps/ShareMarket/stocks.db')

db = SQLAlchemy(app)

# Models start here
#
#

class Investors(db.Model):
	__tablename__ = 'investors'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(100), nullable=False)
	password = db.Column(db.String)
	stocks1 = db.Column(db.Integer, nullable=False, default=0)
	stocks2 = db.Column(db.Integer, nullable=False, default=0)
	stocks3 = db.Column(db.Integer, nullable=False, default=0)
	stocks4 = db.Column(db.Integer, nullable=False, default=0)
	stocks5 = db.Column(db.Integer, nullable=False, default=0)
	stocks6 = db.Column(db.Integer, nullable=False, default=0)
	stocks7 = db.Column(db.Integer, nullable=False, default=0)
	stocks8 = db.Column(db.Integer, nullable=False, default=0)
	stocks9 = db.Column(db.Integer, nullable=False, default=0)
	stocks10 = db.Column(db.Integer, nullable=False, default=0)
	stocks11 = db.Column(db.Integer, nullable=False, default=0)
	stocks12 = db.Column(db.Integer, nullable=False, default=0)
	stocks13 = db.Column(db.Integer, nullable=False, default=0)
	stocks14 = db.Column(db.Integer, nullable=False, default=0)
	stocks15 = db.Column(db.Integer, nullable=False, default=0)
	sales = db.relationship('Sales',backref='investors', lazy='dynamic')
	purchases = db.relationship('Purchases', primaryjoin="and_(Investors.id)==Purchases.recipient_id")
	amount_left = db.Column(db.Float, nullable=False, default=0)

class Sales(db.Model):
	__tablename__ = 'sales'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	sender_id = db.Column(db.Integer, db.ForeignKey('investors.id'))
	stock_id = db.Column(db.Integer,db.ForeignKey('companies.id'))
	amount = db.Column(db.Integer, nullable=False)
	number_of_stocks = db.Column(db.Integer, nullable=False)

class Purchases(db.Model):
	__tablename__ = 'purchases'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	recipient_id = db.Column(db.Integer, db.ForeignKey('investors.id'))
	stock_id = db.Column(db.Integer,db.ForeignKey('companies.id'))
	amount = db.Column(db.Integer, nullable=False)
	number_of_stocks = db.Column(db.Integer, nullable=False)

class Companies(db.Model):
	__tablename__ = 'companies'
	
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(100), nullable=False)
	current_price = db.Column(db.Float, nullable=False, default=100)
	recent_trend = db.Column(db.String)
	shares_left = db.Column(db.Integer, nullable=False, default=100)

class Room(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), unique=True)

	def __init__(self, name):
		self.name = name
	

	def __repr__(self):
		return '<Room {}>'.format(self.name)	


### CHECK SELL AND BUY CONDITIONS
###
###
def checksell(stockid,nos,investor):
	stockid = int(stockid)
	# investor = Investors.query.filter_by(name=session['name']).first()
	if( stockid == 1 and investor.stocks1 >= nos ):
		investor.stocks1 -= nos
		return True
	if( stockid == 2 and investor.stocks2 >= nos ):
		investor.stocks2 -= nos
		return True
	if( stockid == 3 and investor.stocks3 >= nos ):
		investor.stocks3 -= nos
		return True
	if( stockid == 4 and investor.stocks4 >= nos ):
			investor.stocks4 -= nos
			return True
	if( stockid == 5 and investor.stocks5 >= nos ):
			investor.stocks5 -= nos
			return True
	if( stockid == 6 and investor.stocks6 >= nos ):
			investor.stocks6 -= nos
			return True
	if( stockid == 7 and investor.stocks7 >= nos ):
			investor.stocks7 -= nos
			return True
	if( stockid == 8 and investor.stocks8 >= nos ):
			investor.stocks8 -= nos
			return True
	if( stockid == 9 and investor.stocks9 >= nos ):
			investor.stocks9 -= nos
			return True
	if( stockid == 10 and investor.stocks10 >= nos ):
			investor.stocks10 -= nos
			return True
	if( stockid == 11 and investor.stocks11 >= nos ):
			investor.stocks11 -= nos
			return True
	if( stockid == 12 and investor.stocks12 >= nos ):
			investor.stocks12 -= nos
			return True
	if( stockid == 13 and investor.stocks13 >= nos ):
			investor.stocks13 -= nos
			return True
	if( stockid == 14 and investor.stocks14 >= nos ):
			investor.stocks14 -= nos
			return True
	if( stockid == 15 and investor.stocks15 >= nos ):
			investor.stocks15 -= nos
			return True
	return False

def checkbuy(stockid,nos,investor,stock):
	# investor = Investors.query.filter_by(name = session['name']).first()
	# stock = Stock.query.filter_by(id = stockid).first()
	print("nos=")
	print(nos)
	nos=int(nos)

	print(stock.current_price)
	
	stockid = int(stockid)
	print(type(stockid))
	print(stockid)


	if investor.amount_left >= stock.current_price * nos and stock.shares_left >= nos :
		if stockid == 1 :
			investor.stocks1 += nos
		if stockid == 2 :
			investor.stocks2 += nos
		if stockid == 3 :
			investor.stocks3 += nos
		if stockid == 4 :
			investor.stocks4 += nos
		if stockid == 5 :
			investor.stocks5 += nos
		if stockid == 6 :
			investor.stocks6 += nos
		if stockid == 7 :
			investor.stocks7 += nos
		if stockid == 8 :
			investor.stocks8 += nos
		if stockid == 9 :
			investor.stocks9 += nos
		if stockid == 10 :
			investor.stocks10 += nos
		if stockid == 11 :
			investor.stocks11 += nos
		if stockid == 12 :
			investor.stocks12 += nos
		if stockid == 13 :
			investor.stocks13 += nos
		if stockid == 14 :
			investor.stocks14 += nos
		if stockid == 15 :
			investor.stocks15 += nos
		
		db.session.commit()
		return True
	return False

#### Views start here
###
###
@app.before_first_request
def initialize():
    db.create_all()
#     with open('companies.csv', mode='r') as csv_file:
#     	csv_reader = csv.DictReader(csv_file)
#     	for row in csv_reader:
#     		company = Companies(id=row['id'],name=row['name'],current_price=row['current_price'],recent_trend=row['recent_trend'],shares_left=row['shares_left'])
#     		db.session.add(company)
#     with open('investors.csv', mode='r') as csv_file:
#     	csv_reader = csv.DictReader(csv_file)
#     	for row in csv_reader:
#     		investor = Investors()
#     		investor.id = row['id']
#     		investor.name = row['name']
#     		investor.password = row['password']
#     		investor.stocks1 = row['stocks1']
#     		investor.stocks2 = row['stocks2']
#     		investor.stocks3 = row['stocks3']
#     		investor.stocks4 = row['stocks4']
#     		investor.stocks5 = row['stocks5']
#     		investor.stocks6 = row['stocks6']
#     		investor.stocks7 = row['stocks7']
#     		investor.stocks8 = row['stocks8']
#     		investor.stocks9 = row['stocks9']
#     		investor.stocks10 = row['stocks10']
#     		investor.stocks11 = row['stocks11']
#     		investor.stocks12 = row['stocks12']
#     		investor.stocks13 = row['stocks13']
#     		investor.stocks14 = row['stocks14']
#     		investor.stocks1 = row['stocks15']
#     		investor.amount_left = row['amount_left']
#     		db.session.add(investor)
#     db.session.commit()		


@app.route('/')
@app.route('/login')
def login():
	return render_template('login.html')
@app.route('/enter', methods=['POST'])
def enter():
	session.pop('name', None)
	name = request.form['name']
	password = request.form['password']
	try:
		if name == 'admin':
			if password == 'admin123' :
				session['name'] = name
				return redirect(url_for('admin_home'))
			else:
				return render_template('unauth.html')

		investor = Investors.query.filter_by(name=name).first()
		print(investor.password)
		if(password == investor.password):
			session['name'] = name
			return redirect('/home')
		else:
			return render_template('unauth.html')
	except:
		return render_template('unauth.html')

@app.route('/price', methods=['PUT'])
def price():
	data = request.get_json()
	stock = Companies.query.filter_by(id=data['id']).first()
	return Response(
		json.dumps({'price':stock.current_price, 'trend':stock.recent_trend, 'shares':stock.shares_left }),
		status = 200,
		mimetype = 'application/json'
		)

@app.route('/home')
def home():
	return render_template('alt_home.html', name=session['name'],stocks=Companies.query.all(),investor=Investors.query.filter_by(name=session['name']).first())


@app.route('/admin_home')
def admin_home():
	investors=Investors.query.all()
	return render_template('admin_home.html', investors=investors,stocks=Companies.query.all())

@app.route('/sell')
def sell():
	if session['name']:
		return render_template('sell.html',companies=Companies.query.all())
	else:
		return redirect(url_for('login'))

@app.route('/decrease',methods=['POST'])
def decrease():
	number_of_stocks = int(request.form['number'])
	stock_id = int(request.form['stock_id'])
	
	investor = Investors.query.filter_by(name=session['name']).first()
	stock = Companies.query.filter_by(id=stock_id).first()

	if checksell(stock_id,number_of_stocks,investor):
		investor.amount_left += stock.current_price * number_of_stocks
		sale = Sales(sender_id=investor.id,stock_id=stock_id,amount=stock.current_price,number_of_stocks=number_of_stocks)
		stock.shares_left += number_of_stocks
		stock.current_price -= 0.1* number_of_stocks 
		stock.recent_trend = 'down'	
		db.session.add(sale)
		db.session.commit()
		return redirect(url_for('home'))
	else:
		return render_template('funderror.html')

@app.route('/buy')
def buy():
	if session['name']:
		return render_template('buy.html',companies=Companies.query.all())
	else:
		return redirect(url_for('login'))

@app.route('/increase',methods=['POST'])
def increase():
	number_of_stocks = int(request.form['number'])
	stock_id = int(request.form['stock_id'])
	
	investor = Investors.query.filter_by(name=session['name']).first()
	stock = Companies.query.filter_by(id=stock_id).first()

	if checkbuy(stock_id,number_of_stocks,investor,stock):
		investor.amount_left -= stock.current_price * number_of_stocks
		purchase = Purchases(recipient_id=investor.id,stock_id=stock_id,amount=stock.current_price,number_of_stocks=number_of_stocks)
		stock.shares_left -= number_of_stocks
		stock.current_price += 0.12 * number_of_stocks
		stock.recent_trend = 'up'
		db.session.add(purchase)
		db.session.commit()
		return redirect(url_for('home'))
	else:
		return render_template('funderror.html')

@app.route('/logout')
def logout():
	session.pop('name',None)
	return redirect('/login')

@app.route('/admin_change')
def admin_change():
	if(session['name']=='admin'):
		return render_template('admin_change.html', companies=Companies.query.all())
	else:
		return redirect(url_for('home'))

@app.route('/admin_increase', methods=['POST'])
def admin_increase():
	stock_id = request.form['stock_id']
	inc_in_price = int(request.form['number'])
	print(inc_in_price)
	company = Companies.query.filter_by(id=stock_id).first()
	company.current_price += inc_in_price
	company.recent_trend = 'up'
	db.session.commit()
	return redirect('/admin_change')

@app.route('/admin_decrease', methods=['POST'])
def admin_decrease():
	stock_id = request.form['stock_id']
	inc_in_price = int(request.form['number'])
	company = Companies.query.filter_by(id=stock_id).first()
	company.current_price -= inc_in_price
	company.recent_trend = 'down'
	db.session.commit()
	return redirect('/admin_change')

@app.route('/change', methods=['POST'])
def change():
	current_price = request.form['number']
	stock_id = request.form['stock_id']

	stock = Companies.query.filter_by(id=stock_id).first()
	if stock.current_price > int(current_price):
		stock.recent_trend = 'down'
	else:
		stock.recent_trend = 'up'
	stock.current_price = current_price
	db.session.commit()
	return redirect(url_for('admin_home'))

@app.route('/sales')
def sales():
	return render_template('sales.html',investors=Investors.query.all())


@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

if __name__ == "__main__":
        
        print(IP)
        
        app.run(host=IP,port=5000,debug=True)

