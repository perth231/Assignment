# -*- coding: utf-8 -*-
"""4250Solution.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Iqim6i9HB2_ozrTktScxIpnPX4-aYfK2
"""



# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from ast import literal_eval
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet
from surprise import SVD
from surprise import Dataset
from surprise.model_selection import cross_validate
import warnings; warnings.simplefilter('ignore')

mdf = pd. read_csv('/content/movies_metadata.csv')
mdf.head()

!pip install scikit-surprise

mdf['genres'] = mdf['genres'].fillna('[]').apply(literal_eval).apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])

vote_counts = mdf[mdf['vote_count'].notnull()]['vote_count'].astype('int')
vote_averages = mdf[mdf['vote_average'].notnull()]['vote_average'].astype('int')
C = vote_averages.mean()
C

min_req = vote_counts.quantile(0.95)
min_req

mdf['year'] = pd.to_datetime(mdf['release_date'], errors='coerce').apply(lambda x: str(x).split('-')[0] if x != np.nan else np.nan)

qlfd_mov = mdf[(mdf['vote_count'] >= min_req ) & (mdf['vote_count'].notnull()) & (mdf['vote_average'].notnull())][['title', 'year', 'vote_count', 'vote_average', 'popularity', 'genres']]
qlfd_mov['vote_count'] = qlfd_mov['vote_count'].astype('int')
qlfd_mov['vote_average'] = qlfd_mov['vote_average'].astype('int')
qlfd_mov.shape

def weighted_rating(x):
    v = x['vote_count']
    R = x['vote_average']
    return (v/(v+min_req) * R) + (min_req/(min_req+v) * C)

qlfd_mov['wr'] = qlfd_mov.apply(weighted_rating, axis=1)

qlfd_mov = qlfd_mov.sort_values('wr', ascending=False).head(250)

qlfd_mov.head(15)

schart = mdf.apply(lambda x: pd.Series(x['genres']),axis=1).stack().reset_index(level=1, drop=True)
schart.name = 'genre'
gen_mdf = mdf.drop('genres', axis=1).join(schart)

def build_chart(genre, percentile=0.85):
    df = gen_mdf[gen_mdf['genre'] == genre]
    vote_counts = df[df['vote_count'].notnull()]['vote_count'].astype('int')
    vote_averages = df[df['vote_average'].notnull()]['vote_average'].astype('int')
    C = vote_averages.mean()
    m = vote_counts.quantile(percentile)
    
    qlfd = df[(df['vote_count'] >= m) & (df['vote_count'].notnull()) & (df['vote_average'].notnull())][['title', 'year', 'vote_count', 'vote_average', 'popularity']]
    qlfd['vote_count'] = qlfd['vote_count'].astype('int')
    qlfd['vote_average'] = qlfd['vote_average'].astype('int')
    
    qlfd['wr'] = qlfd.apply(lambda x: (x['vote_count']/(x['vote_count']+m) * x['vote_average']) + (m/(m+x['vote_count']) * C), axis=1)
    qlfd = qlfd.sort_values('wr', ascending=False).head(250)
    
    return qlfd

build_chart('Romance').head(15)

links_small = pd.read_csv('/content/links_small.csv')
links_small = links_small[links_small['tmdbId'].notnull()]['tmdbId'].astype('int')

mdf = mdf.drop([19730, 29503, 35587])

mdf['id'] = mdf['id'].astype('int')

smd = mdf[mdf['id'].isin(links_small)]
smd.shape

smd['tagline'] = smd['tagline'].fillna('')
smd['description'] = smd['overview'] + smd['tagline']
smd['description'] = smd['description'].fillna('')

tf = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
tfidf_matrix = tf.fit_transform(smd['description'])

tfidf_matrix.shape

cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

cosine_sim[0]

smd = smd.reset_index()
titles = smd['title']
indices = pd.Series(smd.index, index=smd['title'])

def recomend_movie(title):
    idx = indices[title]
    mov_similarity_scr = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:31]
    movie_indices = [i[0] for i in sim_scores]
    return titles.iloc[movie_indices]

get_recommendations('The Godfather').head(10)

get_recommendations('The Godfather: Part III').head(10)

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(16, 6))
heatmap = sns.heatmap(mdf.corr(), vmin=-1, vmax=1, annot=True)
heatmap.set_title('Correlation Heatmap', fontdict={'fontsize':12}, pad=12);

mdf.columns

sns.countplot(x ='adult', data = mdf)
 
# Show the plot
plt.show()

sns.countplot(x ='year', data = mdf)
 
# Show the plot
plt.show()

df = mdf.groupby(['original_language', 'year']).count()['status']
print(df) 
  
# plot the result 
df.plot() 
plt.xticks(rotation=30) 
plt.show()

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

plt.figure(figsize=(15,10))
country.size().sort_values(ascending=False).plot.bar()
plt.xticks(rotation=50)
plt.xlabel("Country of Origin")
plt.ylabel("Number of Wines")
plt.show()