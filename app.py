from flask import Flask, render_template, request, redirect
import Quandl
import numpy as np
from bokeh.plotting import figure, output_notebook, show
from bokeh.embed import components
from bokeh.resources import CDN

app = Flask(__name__)
app.vars={}

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index', methods=['GET','POST'])
def index():
  if request.method == 'POST':
    ticker = request.form['ticker'].upper()
    #print ticker
    app.vars['stock'] = ticker
    return redirect('/graph')
    # return redirect(url_for('graph',stock=ticker))
  else:
    return render_template('index.html')

@app.route('/graph', methods=['GET','POST'])
def graph():
  stock = app.vars['stock']
  df = Quandl.get("WIKI/"+stock,returns="pandas", authtoken="qCQkVD-2dfsdr6Sx4e2b")
  stock_close = np.array(df[df.index >= '2016-02-20']['Close']) 
  stock_dates = np.array(df[df.index >= '2016-02-20'].index, dtype=np.datetime64)
  #stock_close = np.random.random(50)
  #stock_dates = np.arange(50)
  # create a new plot with a a datetime axis type
  p = figure(width=800, height=350, x_axis_type="datetime")
  # add renderers
  p.line(stock_dates, stock_close, color='navy', legend='Close Price')
  # customize more
  p.title = stock + " Month Closing Prices"
  p.grid.grid_line_alpha=0
  p.xaxis.axis_label = 'Date'
  p.yaxis.axis_label = 'Price'
  p.ygrid.band_fill_color="olive"
  p.ygrid.band_fill_alpha = 0.1
  script, div = components(p)
  return render_template('graph.html', script=script, div=div)

if __name__ == '__main__':
  #app.debug = True
  app.run(port=33507)
