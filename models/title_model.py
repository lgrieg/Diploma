import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

csv_file = '../output.csv'
data = pd.read_csv(csv_file, header=None, names=['Название файла', 'Ссылка на файл', 'Заголовок'], encoding='utf-16')

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(data['Заголовок'])

num_clusters = 3
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
kmeans.fit(X)

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X.toarray())

print(X_pca)
print(X_pca[:, 0])
print(X_pca[:, 1])

plt.figure(figsize=(10, 8))
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=kmeans.labels_, cmap='viridis', marker='o', s = 10, alpha=0.6)

#for i, txt in enumerate(data['Заголовок']):
    #plt.annotate(txt, (X_pca[i, 0], X_pca[i, 1]), fontsize=3)
    #plt.annotate(txt, (X_pca[i, 0], X_pca[i, 1]), fontsize=5)

plt.title('Кластеризация по названию ')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.colorbar()
plt.show()