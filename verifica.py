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

@app.route('/elimina_cliente', methods=['GET', 'POST'])
def elimina_cliente():
    global df
    msg = ''
    if request.method == 'POST':
        customer_id = int(request.form['customer_id'])
        if customer_id in df['CustomerID'].values:
            df = df[df['CustomerID'] != customer_id]
            df.to_csv('/workspace/Verifica22-05/data/vendite.csv', index=False)
            msg = 'Cliente eliminato.'
        else:
            msg = 'Cliente inesistente.'
    
    return render_template('elimina_cliente.html', msg=msg) 

@app.route('/aggiungi_cliente', methods=['GET', 'POST'])
def aggiungi_cliente():
    global df
    msg = ''
    if request.method == 'POST':
        new_row = {
            'CustomerID': int(request.form['customer_id']),
            'CustomerName': request.form['customer_name'],
            'ContactName': request.form['contact_name'],
            'Address': request.form['address'],
            'City': request.form['city'],
            'PostalCode': request.form['postal_code'],
            'Country': request.form['country']
        }
        new_df = pd.DataFrame([new_row])
        df = pd.concat([df, new_df], ignore_index=True)
        df.to_csv('/workspace/Verifica22-05/data/vendite.csv', index=False)
        msg = 'Cliente aggiunto con successo!'
    
    return render_template('aggiungi_cliente.html', msg=msg)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)