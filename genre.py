import os
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

# Carregar as variáveis de ambiente
load_dotenv()

# Configurar o cliente Spotipy
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET")
))

# Carregar a planilha
planilha = pd.read_excel("artistas_albuns_ano.xlsx")  # Substitua pelo nome da sua planilha

# Função para buscar o gênero de um álbum no Spotify
def buscar_genero(artista, album):
    resultados = sp.search(q=f"album:{album} artist:{artista}", type='album', limit=1)
    if resultados['albums']['items']:
        album_info = resultados['albums']['items'][0]
        genero = album_info['genres']
        return genero[0] if genero else "Gênero não encontrado"
    else:
        return "Álbum não encontrado"

# Função para carregar gêneros de um CSV local
def carregar_generos_csv(caminho):
    try:
        generos_df = pd.read_csv(caminho)
        return generos_df.set_index(['Nome do Artista', 'Título do Álbum']).to_dict()['Gênero']
    except Exception as e:
        print(f"Erro ao carregar o arquivo CSV: {e}")
        return {}

# Função para buscar o gênero no CSV
def buscar_genero_csv(artista, album, generos_csv):
    key = (artista, album)
    return generos_csv.get(key, "Gênero não encontrado")

# Carregar gêneros do CSV
generos_csv = carregar_generos_csv('generos_albuns.csv')

# Criar colunas na planilha
planilha['Gênero'] = planilha.apply(lambda row: buscar_genero(row['Nome do Artista'], row['Álbum']), axis=1)

# Atualizar gêneros não encontrados com dados do CSV
for i, row in planilha.iterrows():
    if row['Gênero'] == "Gênero não encontrado":
        planilha.at[i, 'Gênero'] = buscar_genero_csv(row['Nome do Artista'], row['Álbum'], generos_csv)

# Salvar a planilha atualizada
planilha.to_excel("planilha_atualizada.xlsx", index=False)
print("Planilha atualizada com os gêneros dos álbuns.")
