# Limpia los datos y genera un archivo con todos los artículos
print('Loading libraries')
import pandas as pd

dfs = []

for i in range(3):
    print('Reading file', i+1)
    df = pd.read_csv('articles{}.csv'.format(i+1))
    print('Processing file', i+1)
    df = df[['id', 'title', 'content']]
    df.title = df.title.str.strip()
    df.content = df.content.str.strip()
    dfs.append(df)

df_all = pd.concat(dfs)
print('Writing output file')
df_all.to_csv('articles_all.csv'.format(i+1), encoding='utf-8', index=False)