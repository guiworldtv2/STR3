import subprocess
import time
import os
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import yt_dlp


from pytube import YouTube

# Configuring Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")

# Instanciando o driver do Chrome
driver = webdriver.Chrome(options=chrome_options)

# Ler os links do arquivo LINKSYOUTUBE.txt
try:
    with open('YOUTUBEALL.txt', 'r') as f:
        links = [line.strip() for line in f.readlines()]
except Exception as e:
    print(f"Erro ao ler o arquivo LINKSYOUTUBE.txt: {e}")
    links = []


banner = r'''
#EXTM3U x-tvg-url="https://iptv-org.github.io/epg/guides/ar/mi.tv.epg.xml"
#EXTM3U x-tvg-url="https://raw.githubusercontent.com/mudstein/XML/main/TIZENsiptv.xml"
#EXTM3U x-tvg-url="https://raw.githubusercontent.com/K-vanc/Tempest-EPG-Generator/main/Siteconfigs/Argentina/%5BENC%5D%5BEX%5Delcuatro.com_0.channel.xml"
#EXTM3U x-tvg-url="https://raw.githubusercontent.com/Nicolas0919/Guia-EPG/master/GuiaEPG.xml"
'''

# Instalando streamlink

subprocess.run(['pip', 'install', 'pytube'])
subprocess.run(['pip', 'install', '--upgrade', 'yt dlp'])

time.sleep(5)
from pytube import YouTube

# Define as opções para o youtube-dl
ydl_opts = {
    'format': 'best',  # Obtém a melhor qualidade

    'write_all_thumbnails': False,  # Não faz download das thumbnails
    'skip_download': True,  # Não faz download do vídeo
}

# Get the playlist and write to file
try:
    with open('./LISTA5YTALL.m3u', 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        f.write(banner)
        for i, link in enumerate(links):
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(link, download=False)
                if 'url' not in info:
                    print(f"Erro ao gravar informações do vídeo {link}: 'url'")
                    continue
                url = info['url']
                thumbnail_url = info['thumbnail']
                description = info.get('description', '')[:10]
                title = info.get('title', '')
                f.write(f"#EXTINF:-1 group-title=\"YOUTUBE\" tvg-logo=\"{thumbnail_url}\",{title} - {description}...\n")
                f.write(f"{url}\n")
                f.write("\n")
            except Exception as e:
                print(f"Erro ao processar o link {link}: {e}")
                continue
except Exception as e:
    print(f"Erro ao criar o arquivo .m3u8: {e}")
