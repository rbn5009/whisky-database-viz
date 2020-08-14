import os
from flask import Flask, request, url_for, redirect, render_template
import numpy as np

app = Flask(__name__, static_url_path='/static')

@app.route("/")
def index():
    return render_template("index.html");   

@app.route("/index")
def index2():
    return render_template("index.html");

@app.route("/about")
def about():
    return render_template("about.html");

@app.route("/motivation")
def motivation():
    return render_template("motivation.html");

@app.route("/terms")
def terms():
    return render_template("terms.html");

@app.route('/tsne_description', methods=['GET', 'POST'])
def tsne_description():
    return render_template('tsne_description.html')

@app.route('/tsne_scatter', methods=['GET', 'POST'])
def tsne_scatter():
	labels = ['A', 'B', 'C']
	data = {'labels': labels}
	datasets = []
	for ped in labels:
		X = np.random.normal(0,1,100)
		Y = np.random.normal(0,1,100)
		X = X.tolist()
		Y = Y.tolist()

		r,g,b = np.random.randint(0,255),np.random.randint(0,255),np.random.randint(0,255)

		unit = {
	          'label': ped,
	          'backgroundColor': "rgba(0,0,0,0)",
	          'borderColor': "rgba({},{},{},0.8)".format(r,g,b), #// The main line color
	          'borderCapStyle': 'circle',
	          'borderDash': [],# // try [5, 15] for instance
	          'borderDashOffset': 0.0,
	          'borderJoinStyle': 'miter',
	          'pointBorderColor': "black",
	          'pointBackgroundColor': "rgba({},{},{},0.8)".format(r,g,b),
	          'pointBorderWidth': 1,
	          'pointHoverRadius': 8,
	          'pointHoverBackgroundColor': "rgba({},{},{},1.0)".format(r,g,b),
	          'pointHoverBorderColor': "black",
	          'pointHoverBorderWidth': 1,
	          'pointRadius': 6,
	          'pointHitRadius': 10,
	          'lineTension': 0.1,
	          'showLine': False,          

	          # 'data': list(df[df.ID==ped]['Mean'].values),
	          'data': [{'x': x, 'y':y} for x,y in zip(X, Y)]
	        }
        datasets.append(unit)
	data['datasets'] = datasets
	axes = ['Chart Title', 'X label', 'Y label']

	return render_template('scatter.html',**locals())
    #return render_template('scatter.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7000, debug=True)