from flask import Flask, render_template,url_for
from forms import InputForm
import pickle
from recommender_module import recommend

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_KEY'

recommender = pickle.load(open('recommend.pkl','rb'))

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')

@app.route('/popular_hotels')
def popular():
    return render_template('popular.html', title='Popular')

@app.route('/recommend', methods=["GET", "POST"])
def recommended_hotels():
    form = InputForm()
    recommendations = None  # Initialize to an empty list or None
    if form.validate_on_submit():
        country = form.country.data 
        city = form.city.data 
        property = form.property.data
        room = form.room.data 
        recommendations = recommender(str(room),str(country),str(city),str(property))
    return render_template('recommend.html', title='Recommend', form=form, recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)
