import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import plotly.express as px


csv_file = '../output.csv'
data = pd.read_csv(csv_file, header=None, names=['Название файла', 'Ссылка на файл', 'Заголовок'], encoding='utf-16')

# TFidf по заголовку -- возможно надо по ссылке/названию/файлу целиком
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(data['Заголовок'])

# Кластеризация K-соседей
num_clusters = 5
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
kmeans.fit(X)

# Переводим в 2D через tsne 
# (пока не очень хорошо то, что объекты 1го кластера лежат вообще где угодно, визульно непонятно)
tsne = TSNE(n_components=2, random_state=42)
X_tsne = tsne.fit_transform(X.toarray())


df = pd.DataFrame(X_tsne, columns=['Component 1', 'Component 2'])
df['Cluster'] = kmeans.labels_
df['Title'] = data['Заголовок']
df['PDF Link'] = data['Ссылка на файл']

fig = px.scatter(df, x='Component 1', y='Component 2', color='Cluster', hover_name='Title',
                 title='Кластеризация документов')

# Строим ссылки на файлы -- подумать можно ли как-то улучшить
# Сейчас отображается все время, хочется только при наведении
for i in range(len(df)):
    fig.add_annotation(
        x=df['Component 1'][i],
        y=df['Component 2'][i],
        text=f'<a href="{df["PDF Link"][i]}" target="_blank">Скачать {df["Title"][i]}</a>',
        #showarrow=True,
        #arrowhead=1,
        ax=10,
        ay=-20,
        font=dict(color="black"),
    )

fig.write_html('tsne_interactive_plot.html')
