from flask_wtf import FlaskForm
from wtforms import SelectField,SubmitField,StringField
from wtforms.validators import DataRequired
import joblib
import pickle
import pandas

df = pickle.load(open('df_final.pkl', 'rb'))

class InputForm(FlaskForm):
    country = SelectField(
        'Country',
        validators=[DataRequired()],
        choices= df['country'].unique().tolist()
    )

    city = SelectField(
        'City',
        validators=[DataRequired()],
        choices = df['city'].unique().tolist()
    )

    property = SelectField(
        'Property',
        validators=[DataRequired()],
        choices=df['propertytype'].unique().tolist()
    )

    room = SelectField(
        'Rooms',
        validators=[DataRequired()],
        choices=df['roomtype'].unique().tolist()
    )

    submit = SubmitField(
        'Search',
    )

