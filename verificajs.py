from flask import Flask, jsonify, request, render_template
import pandas as pd

app = Flask(__name__)

# Load the data
df = pd.read_csv('/workspace/Verifica22-05/data/vendite.csv')

@app.route('/')
def homepage():
    return render_template('indexjs.html')

@app.route('/get_countries', methods=['GET'])
def get_countries():
    countries = sorted(list(set(df['Country'])))
    return jsonify(countries)

@app.route('/get_cities/<country>', methods=['GET'])
def get_cities(country):
    cities_info = df[df['Country'] == country]
    city_counts = cities_info['City'].value_counts().sort_values(ascending=False).to_dict()
    return jsonify(city_counts)

@app.route('/get_customers', methods=['GET'])
def get_customers():
    city = request.args.get('city')
    customers_info = df[df['City'] == city]
    return jsonify(customers_info.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=32457, debug=True)