from flask import Flask, render_template, request, Response
app = Flask(__name__)

import pandas as pd
df = pd.read_excel("https://github.com/wtitze/3E/blob/main/BikeStores.xls?raw=true", sheet_name='products')

@app.route('/', methods=['GET'])
def form():
    return render_template('home.html')

@app.route('/categoria', methods=['GET'])
def categoria():
    categoria = request.args.get('categoria')
    table = df[df['category_id'] == categoria].sort_values(by='product_name').to_html()  
    return render_template('input.html', table = table, categorie = df['category_id'].tolist())

@app.route('/prezzo', methods=['GET'])
def prezzo():
    return render_template('input.html')

@app.route('/nome', methods=['GET'])
def nome():
    return render_template('input.html')

@app.route('/numero', methods=['GET'])
def numero():
    return render_template('input.html')

@app.route('/grafico', methods=['GET'])
def grafico():
    return render_template('input.html')



if __name__ == '__main__':
  app.run(host='0.0.0.0', port=32245, debug=True)