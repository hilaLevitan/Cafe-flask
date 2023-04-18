from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,URLField,SelectField
from wtforms.validators import DataRequired,URL
import csv
import os
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRETE_KEY')
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location=URLField('location (link)',validators=[DataRequired(),URL(require_tld=True,message='url is not valid')])
    openT=StringField('open time',validators=[DataRequired()])
    close=StringField('closeing time',validators=[DataRequired()])
    coffeeRating=SelectField(label='coffee rating',choices=['☕️','☕️☕️','☕️☕️☕️','☕️☕️☕️☕️'])
    wifi=SelectField(label='wifi power',choices=['💪','💪💪','💪💪💪','✘'])
    power=SelectField(label='power outlet rating fields',choices=['🔌','🔌🔌','🔌🔌'])
    submit = SubmitField('Submit')
    
# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add',methods=['GET','POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_data = form.data
        new_row = [value for (key,value) in new_data.items() if not key in ['submit','csrf_token']]
        with open('cafe-data.csv',mode='a', newline='',encoding="utf8") as csv_file:
            wr = csv.writer(csv_file)
            wr.writerow(new_row)
        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='',encoding="utf8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
