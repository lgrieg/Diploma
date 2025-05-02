import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import plotly.express as px
from transformers import BertTokenizer, BertModel
import torch
from sklearn.manifold import TSNE
from matplotlib.patches import Ellipse
import plotly.graph_objects as go

csv_file = '../output.csv'
data = pd.read_csv(csv_file, header=None, names=['Название файла', 'Ссылка на файл', 'Заголовок'], encoding='utf-16')
data['Текст'] = ''

for index, row in data.iterrows():
    name = row['Название файла']
    if name == 'Название файла':
        continue
    try:
        with open(f'../txt_files/{name}', 'r', encoding='utf-16') as file:
            data.at[index, 'Текст'] = file.read()
    except FileNotFoundError:
        print(f"Файл {name} не найден.")
    except Exception as e:
        print(f"Ошибка при чтении файла {name}: {e}")

print(data)

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

def get_embeddings(texts):
    inputs = tokenizer(texts.tolist(), return_tensors='pt', padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).numpy()

embeddings = get_embeddings(data['Текст'])

num_clusters = 5
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
data['cluster'] = kmeans.fit_predict(embeddings)

#pca = PCA(n_components=2)
#reduced_embeddings = pca.fit_transform(embeddings)

tsne = TSNE(n_components=2, random_state=42)
reduced_embeddings = tsne.fit_transform(embeddings)

data['x'] = reduced_embeddings[:, 0]
data['y'] = reduced_embeddings[:, 1]

# fig = px.scatter(data, x='x', y='y', color='cluster', hover_name='Заголовок', 
#                  hover_data={'Ссылка на файл': True}, title="Кластеризация документов")

fig = go.Figure()

# Добавили овалычтобы визуализировать кластеры лучше
for i in range(num_clusters):
    cluster_data = reduced_embeddings[data['cluster'] == i]
    mean = cluster_data.mean(axis=0)
    cov = np.cov(cluster_data.T)
    eigenvalues, eigenvectors = np.linalg.eig(cov)

    width = 2 * np.sqrt(eigenvalues[0])
    height = 2 * np.sqrt(eigenvalues[1])
    
    ellipse_x = mean[0] + width * np.cos(np.linspace(0, 2 * np.pi, 100))
    ellipse_y = mean[1] + height * np.sin(np.linspace(0, 2 * np.pi, 100))
    
    fig.add_trace(go.Scatter(
        x=ellipse_x,
        y=ellipse_y,
        mode='lines',
        name=f'Ellipse {i}',
        line=dict(width=2),
        showlegend=False,
        fill='toself',
        opacity=0.5,
        fillcolor='rgba(0, 100, 80, 0.2)'
    ))

fig.update_layout(
    title='кластеризация с использованием BERT и TSNE',
    xaxis_title='',
    yaxis_title='',
    showlegend=True
)

for i in range(num_clusters):
    cluster_data = reduced_embeddings[data['cluster'] == i]
    fig.add_trace(go.Scatter(
        x=cluster_data[:, 0],
        y=cluster_data[:, 1],
        mode='markers',
        name=f'Cluster {i}',
        text=data.loc[data['cluster'] == i, 'Заголовок'],
        customdata=data['Ссылка на файл'],
        hovertemplate='<b>Description:</b> %{text}<br><b>Link:</b> <a href="%{customdata}" target="_blank">Open</a>',
        marker=dict(size=10),
        hoverinfo='text'
    ))

for i in range(len(data)):
    fig.add_annotation(
        x=data["x"][i],
        y=data["y"][i],
        text=f'<a href="{data["Ссылка на файл"][i]}" target="_blank">   </a>',
        ax=0,
        ay=0,
        font=dict(color="black"),
    )


fig.write_html('fulltext_BERT_tsne.html')
