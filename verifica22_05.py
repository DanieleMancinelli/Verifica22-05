from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

df = pd.read_csv('/workspace/Verifica22-05/data/vendite.csv')

@app.route('/')
def homepage():
    risultato = sorted(list(set(df['Country'])))
    return render_template('nazioni.html', lista=risultato)

@app.route('/elencocitta/<nazione>', methods=['GET'])
def citta(nazione):
    info = df[df['Country'] == nazione]
    city_counts = info['City'].value_counts().sort_values(ascending=False)
    return render_template('radiobutton.html', tabella=city_counts)

@app.route('/elencoclienti', methods=['GET'])
def clienti():
    citta = request.args.get('citta')
    info = df[df['City'] == citta]
    return render_template('table.html', tabella=info.to_html())

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)