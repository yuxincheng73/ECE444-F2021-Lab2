from flask import Flask, render_template, session, redirect, url_for, flash
from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms import validators
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email
from flask_bootstrap import Bootstrap
from flask_moment import Moment

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
bootstrap = Bootstrap(app)
moment = Moment(app)

class NameForm(Form):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = EmailField('What is your UofT Email address', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        session.permanent = False
        old_name = session.get('name')
        old_email = session.get('email')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        if old_email is not None and old_email != form.email.data:
            flash('Looks like you have changed your email!')
        session['name'] = form.name.data
        session['email'] = form.email.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), email=session.get('email'))
    
@app.route('/user/<name>')
def user(name):
    print(datetime.utcnow())
    return render_template('user.html', name=name, current_time=datetime.utcnow())

if __name__ == '__main__':
    app.run(debug=True)