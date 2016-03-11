from flask import Flask, render_template, request, redirect
import Quandl
import numpy as np
from bokeh.plotting import figure, output_notebook, show
from bokeh.embed import components

app = Flask(__name__)

@app.route('/')
def main():
  print "MADE IT HERE 1"
  return redirect('/index')

@app.route('/index', methods=['GET','POST'])
def index():
  if request.method == 'POST':
    print "GOT TO POST"
    stock = request.form['ticker']
    print stock
    return redirect('/graph')
  else:
    print "GOT TO ELSE"
    return render_template('index.html')

@app.route('/graph')
def graph():
  print "MADE IT HERE 4"
  #df = Quandl.get("WIKI/"+text.upper(),returns="pandas", authtoken="qCQkVD-2dfsdr6Sx4e2b")
  #stock_close = np.array(df[df.index >= '2016-02-20']['Close']) 
  #stock_dates = np.array(df[df.index >= '2016-02-20'].index, dtype=np.datetime64)
  stock_close = np.random.random(50)
  stock_dates = np.arange(50)
  window_size = 30
  window = np.ones(window_size)/float(window_size)
  print "MADE IT HERE 5"
  # create a new plot with a a datetime axis type
  p = figure(width=800, height=350, x_axis_type="datetime")
  # add renderers
  p.line(stock_dates, stock_close, color='navy', legend='Close Price')
  # customize
  print "MADE IT HERE 6"
  p.title = stock + " One-Month Average"
  p.grid.grid_line_alpha=0
  p.xaxis.axis_label = 'Date'
  p.yaxis.axis_label = 'Price'
  p.ygrid.band_fill_color="olive"
  p.ygrid.band_fill_alpha = 0.1
  print "MADE IT HERE 7"
  script, div = components(p)
  print "MADE IT HERE 8"
  return render_template('graph.html', script=script, div=div)
  print "MADE IT HERE 9"

if __name__ == '__main__':
  #app.debug = True
  app.run(port=33507)
