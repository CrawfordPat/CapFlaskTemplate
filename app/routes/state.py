from flask.app import Flask
from app import app
import datetime as dt
from flask import flash
from flask_wtf import FlaskForm
from mongoengine.fields import EmailField
import mongoengine.errors
from wtforms.validators import URL, NumberRange, Email, Optional, InputRequired, ValidationError, DataRequired, EqualTo
from wtforms import PasswordField, StringField, SubmitField, TextAreaField, HiddenField, IntegerField, SelectField, FileField, BooleanField
from app.classes.data import User
from app.classes.data import State
from app.classes.forms import StateForm

@app.route('/state/new', methods=['GET', 'POST'])
def new_state():
    state = StateForm()

    if state.validate_on_submit():
        newState = State(
            stateName = state.stateName.data,
            totalBudget = state.totalBudget.data,
            perCapitaBudget = state.perCapitaBudget.data,
            budgetGrowth = state.budgetGrowth.data,

            modifydate = dt.datetime.utcnow()
        )

    newState.save()