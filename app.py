from flask import Flask, render_template, request, redirect
import Quandl
import numpy as np
from bokeh.plotting import figure, output_notebook, show
from bokeh.embed import components

app = Flask(__name__)

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index')
def index():
  return render_template('index.html')

@app.route('/', methods=['POST'])
def post_ticker():
  text = request.form['ticker']
  df = Quandl.get("WIKI/"+text.upper(),returns="pandas", authtoken="qCQkVD-2dfsdr6Sx4e2b")
  # prepare some data
  stock_close = np.array(df[df.index >= '2016-02-20']['Close']) #np.random.random(50)#
  stock_dates = np.array(df[df.index >= '2016-02-20'].index, dtype=np.datetime64) #np.arange(50) #
  window_size = 30
  window = np.ones(window_size)/float(window_size)
  # create a new plot with a a datetime axis type
  p = figure(width=800, height=350, x_axis_type="datetime")
  # add renderers
  p.line(stock_dates, stock_close, color='navy', legend='Close Price')
  # customize
  p.title = stock + " One-Month Average"
  p.grid.grid_line_alpha=0
  p.xaxis.axis_label = 'Date'
  p.yaxis.axis_label = 'Price'
  p.ygrid.band_fill_color="olive"
  p.ygrid.band_fill_alpha = 0.1
  script, div = components(p)
  return render_template('graph.html', script=script, div=div)

if __name__ == '__main__':
  app.run(port=33507)
