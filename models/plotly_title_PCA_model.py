import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import plotly.express as px
##старая модель с методом главных компонент и названием
#есть визуализация в плотли

csv_file = '../output.csv'
data = pd.read_csv(csv_file, header=None, names=['Название файла', 'Ссылка на файл', 'Заголовок'], encoding='utf-16')

# TFidf по заголовку -- возможно надо по ссылке/названию/файлу целиком
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(data['Заголовок'])

# Кластеризация к соседей 
# может нужно подумать над другим
num_clusters = 5
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
kmeans.fit(X)

# Переводим в 2D через PCA 
# работает плохо -- все в одном месте возможно из-за того что отнормировать не получается 
# можно попробовать нормально отнормировать или применить что-то другое
pca = PCA(n_components=2, power_iteration_normalizer='LU', svd_solver='full')
X_pca = pca.fit_transform(X.toarray())


df = pd.DataFrame(X_pca, columns=['Component 1', 'Component 2'])
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
        showarrow=True,
        arrowhead=1,
        ax=20,
        ay=-30,
        font=dict(color="black"),
    )

fig.write_html('PCA_interactive_plot.html')
