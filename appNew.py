import io
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from flask import Flask, render_template, request, Response
app = Flask(__name__)

import pandas as pd
df = pd.read_excel("https://github.com/wtitze/3E/blob/main/BikeStores.xls?raw=true", sheet_name='products')
nomiCategorie = pd.read_excel("https://github.com/wtitze/3E/blob/main/BikeStores.xls?raw=true", sheet_name='categories')

@app.route('/', methods=['GET'])
def form():
    return render_template('home.html')

@app.route('/categoria', methods=['GET'])
def categoria():  
    categorie = nomiCategorie['category_name'].tolist() 
    return render_template('input.html', categorie = categorie)

@app.route('/risultatocategoria', methods=['GET'])
def risultatocategoria():
    categoria = request.args.get('categoria')
    idCategoria = nomiCategorie[nomiCategorie['category_name'].str.contains(categoria)]['category_id'].tolist()
    table = df[df['category_id'] == idCategoria[0]].sort_values(by='product_name')
    return render_template('risultato.html', table = table.to_html())

@app.route('/prezzo', methods=['GET'])
def prezzo():
    return render_template('input2.html')

@app.route('/risultatoprezzo', methods=['GET'])
def risultatoprezzo():
    minimo, massimo = request.args.get('minimo'), request.args.get('massimo')
    table = df[(df['list_price'] > float(minimo)) & (df['list_price'] < float(massimo))].sort_values(by='list_price', ascending=False)
    return render_template('risultato.html', table = table.to_html())

@app.route('/nome', methods=['GET'])
def nome():  
    return render_template('input3.html')

@app.route('/risultatonome', methods=['GET'])
def risultatonome():
    prodotto = request.args.get('nome')
    table = df[df['product_name'].str.contains(prodotto)].sort_values(by='product_name')
    return render_template('risultato.html', table = table.to_html())

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
categorie = df.groupby('category_id').count().sort_values(by='model_year', ascending = False)[['product_id']]
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

@app.route('/numero', methods=['GET'])
def numero():
    return render_template('risultato.html',  table = categorie.to_html() )

@app.route('/grafico', methods=['GET'])
def grafico():
    
    dati = categorie['product_id']
    labels = categorie.index.map(str)
    fig, ax = plt.subplots()
    plt.bar(labels, dati)
    plt.title('Numero di prodotti per categoria')
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=32245, debug=True)