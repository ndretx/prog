import os
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import datetime
import spotipy
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurar cliente Spotipy
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET")
))

# Carregar a planilha
planilha = pd.read_excel("artistas_albuns_ano.xlsx")

# Função para buscar o gênero do artista no Spotify
def buscar_genero(artista, album):
    # Buscar o álbum e o artista
    resultados = sp.search(q=f"album:{album} artist:{artista}", type='album', limit=1)
    if resultados['albums']['items']:
        album_info = resultados['albums']['items'][0]
        artista_id = album_info['artists'][0]['id']
        
        # Buscar o gênero do artista se não estiver disponível no álbum
        artista_info = sp.artist(artista_id)
        generos = artista_info.get('genres', [])
        generos_maiusculo = [genero.upper() for genero in generos]
        
        return ', '.join(generos_maiusculo) if generos_maiusculo else "GÊNERO NÃO ENCONTRADO"
    else:
        return "ÁLBUM NÃO ENCONTRADO"

# Criar colunas na planilha com gêneros formatados em maiúsculas
planilha['Gênero'] = planilha.apply(lambda row: buscar_genero(row['Nome do Artista'], row['Álbum']), axis=1)

# Obter a data e hora atual no formato DDMMYYYYHHMM
data_hora = datetime.now().strftime("%d%m%Y%H%M")
nome_arquivo = f"planilha_atualizada_{data_hora}.xlsx"

# Salvar a planilha atualizada
planilha.to_excel(nome_arquivo, index=False)
print(f"Planilha atualizada salva como {nome_arquivo}")
