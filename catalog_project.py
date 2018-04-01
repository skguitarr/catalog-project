from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine, desc, text
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Items

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#API Endpoint 1
@app.route('/categories/JSON')
def categoryJSON():
    categories = session.query(Category).all()
    return jsonify(Category=[i.serialize for i in categories])

#API Endpoint 2
@app.route('/category/<int:category_id>/items/JSON')
def itemsJSON(category_id):
    items = session.query(Items).filter_by(category_id = category_id).all()
    return jsonify(Catalog=[i.serialize for i in items])

# Show all categories
@app.route('/')
@app.route('/categories/')
def showCategories():
    #sqlStatement = text('select i.name, i.creation_date, c.name as category_name from Items i, Category c where i.category_id = c.id order by i.creation_date desc limit 10')
    sqlStatement = 'select i.name, i.creation_date, c.name as category_name from Items i, Category c where i.category_id = c.id order by i.creation_date desc limit 10'
    mostRecent = session.execute(sqlStatement).fetchall()
    categories = session.query(Category).all()
    #mostRecent = session.query(Items).order_by(desc(Items.creation_date)).limit(10)
    return render_template('categories.html', categories=categories, mostRecent=mostRecent)

# Show item details
@app.route('/categories/<int:category_id>/')
@app.route('/categories/<int:category_id>/item/')
def showItems(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    categories = session.query(Category).all()
    items = session.query(Items).filter_by(category_id=category_id).all()
    count = session.query(Items).filter_by(category_id=category_id).count()
    return render_template('items.html', items=items, category=category, categories=categories, count = count)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
