import os
from flask import Flask, request, url_for, redirect, render_template
import numpy as np
import json
from matplotlib import cm


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
	with open('./database/umap_coordinates.json', 'r') as f:
		coord = json.load(f)
		coord_npy = np.array(coord['dice'])
	with open('./database/attribute_data.json', 'r') as f:
		attrs = json.load(f)
	with open('./database/whisky_names.json', 'r') as f:
		names = json.load(f)

	labels = np.unique(attrs['Country']).tolist()
	data = {'labels': labels}

	viridis = cm.get_cmap('tab20c', len(labels))

	datasets = []
	for ix, lab in enumerate(labels):
		ind = [n for n,i in enumerate(attrs['Country']) if i == lab]
		X = coord_npy[ind,0]
		Y = coord_npy[ind,1]
		X = X.tolist()
		Y = Y.tolist()

		attr_dict = {}
		for key in list(attrs.keys()):
			attr_dict[key] = list(np.array(attrs[key])[ind])

		#r,g,b = np.random.randint(0,255),np.random.randint(0,255),np.random.randint(0,255)
		r,g,b,_ = viridis(ix)
		r = (r*255).astype('uint8')
		g = (g*255).astype('uint8')
		b = (b*255).astype('uint8')
		#import pdb; pdb.set_trace()
		unit = {
	          'label': lab,
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
	          'data': [{'x': x, 'y':y} for x,y in zip(X, Y)],
	          'idx': ind,
	          'names': list(np.array(names)[ind]),
	          'attrs': attr_dict
	        }
		datasets.append(unit)
	data['datasets'] = datasets
	axes = ['2D Scatter Plot of UMAP Whisky Latent Space', 'Component #1', 'Component #2']

	return render_template('scatter.html',**locals())
    #return render_template('scatter.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7000, debug=True)