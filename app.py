from flask import Flask, render_template, request, url_for, flash
from werkzeug.utils import redirect
from flask_mysqldb import MySQL
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, DateField
from wtforms.validators import DataRequired, NumberRange
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secure random secret key

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'inventory'

mysql = MySQL(app)

# Form for adding drinks
class DrinkForm(FlaskForm):
    name_of_drink = StringField('Name of Drink', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0)])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=0)])
    expiry_date = DateField('Expiry Date', validators=[DataRequired()])
    batch_number = IntegerField('Batch Number', validators=[DataRequired()])
    drink_subtype = StringField('Drink Subtype', validators=[DataRequired()])

@app.route('/')
def Index():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM soft_drinks_tbl")
        data = cursor.fetchall()
        cursor.close()
        return render_template('index.html', drinks=data)
    except Exception as e:
        flash(f"Error fetching drinks: {str(e)}", 'error')
        return render_template('index.html', drinks=[])

@app.route('/insert', methods=['POST'])
def insert():
    form = DrinkForm()
    if form.validate_on_submit():
        try:
            cursor = mysql.connection.cursor()
            cursor.execute(
                "INSERT INTO soft_drinks_tbl (name_of_drink, price, quantity, expiry_date, batch_number, drink_subtype) VALUES (%s, %s, %s, %s, %s, %s)",
                (form.name_of_drink.data, form.price.data, form.quantity.data, form.expiry_date.data, form.batch_number.data, form.drink_subtype.data)
            )
            mysql.connection.commit()
            cursor.close()
            flash("Successfully Added Drink", 'success')
            return redirect(url_for('Index'))
        except Exception as e:
            flash(f"Error adding drink: {str(e)}", 'error')
            return redirect(url_for('Index'))
    else:
        flash("Invalid input. Please check the form data.", 'error')
        return redirect(url_for('Index'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM soft_drinks_tbl WHERE id = %s", (id,))
        mysql.connection.commit()
        cursor.close()
        flash("Successfully Deleted Drink", 'success')
        return redirect(url_for('Index'))
    except Exception as e:
        flash(f"Error deleting drink: {str(e)}", 'error')
        return redirect(url_for('Index'))

if __name__ == '__main__':
    app.run(debug=True)