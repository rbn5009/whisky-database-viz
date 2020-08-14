import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.preprocessing import LabelEncoder
from sklearn.manifold import TSNE

def load_database():
	with open("whisky-database.json", "r") as f:
		db = json.load(f)
	return db

def plot_flavor(db):
	styles = []
	for entry in db: 
		styles.extend(entry['Characteristics'])

	n, counts = np.unique(styles, return_counts=True)
	df = pd.DataFrame(n, columns=['Flavor'])
	df['Counts'] = counts
	df = df.sort_values('Counts', ascending=False)
	df.set_index("Flavor", inplace=True)
	df.plot(kind='bar')
	plt.title("Pareto Chart of Whisky Flavors in Database (%d unique)" %len(n))
	plt.pause(0.1)

def plot_pca(X, y=None):
	plt.close('all')

	pca = PCA(n_components=30)
	Xt = pca.fit_transform(X)

	if isinstance(y, np.ndarray):
		le = LabelEncoder()
		colors = le.fit_transform(y)
	else: 
		colors = [1 for n in range(len(X))]

	plt.scatter(Xt[:,0], Xt[:,1], s=50, alpha=0.5, c=colors, cmap='jet')

	plt.xlabel("PCA 1")
	plt.ylabel("PCA 2")
	plt.title("2D PCA Plot of Representing {} Variables".format(X.shape[1]))
	plt.pause(0.1)

	plt.figure()
	plt.plot(pca.explained_variance_.cumsum(), marker='o')
	plt.xlabel("No. PCA Components")
	plt.ylabel("Explained Variance")
	plt.title("PCA Scree Plot")
	plt.pause(0.1)

def plot_tsne(X,y=None):
	tsne = TSNE(n_components=2, learning_rate = 100, n_iter=5000, perplexity=20, verbose=True)
	Xt = tsne.fit_transform(X)

	try:
		y = y.astype('float32')
		ytype = 'numeric'
	except:
		ytype = 'categorical'

	if isinstance(y, np.ndarray):
		if ytype == 'numeric':
			colors = y
		else:
			le = LabelEncoder()
			colors = le.fit_transform(y)
	else: 
		colors = [1 for n in range(len(X))]

	plt.scatter(Xt[:,0], Xt[:,1], s=50, alpha=0.5, c=colors, cmap='jet')

	plt.xlabel("tSNE 1")
	plt.ylabel("tSNE 2")
	plt.title("2D tSNE Plot of Representing {} Variables".format(X.shape[1]))
	if isinstance(y, np.ndarray): 
		plt.colorbar()

	plt.pause(0.1)


