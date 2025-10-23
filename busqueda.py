from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, parse_qs
import os

def listar_txt(carpeta):
    if not os.path.exists(carpeta):
        return []
    
    return [f for f in os.listdir(carpeta) if f.endswith('.txt')]

def leer_lineas(carpeta, archivo):
    ruta = os.path.join(carpeta, archivo)
    if not os.path.exists(ruta):
        return []
    with open(ruta, 'r', encoding='utf-8') as f:
        return [linea.strip() for linea in f.readlines() if linea.strip()]

def leer_archivo(carpeta, archivo):
    ruta = os.path.join(carpeta, archivo)
    if not os.path.exists(ruta):
        return "Archivo no encontrado."
    with open(ruta, 'r', encoding='utf-8') as f:
        return f.read()


def buscar(query):
    url = f"https://html.duckduckgo.com/html/?q={query}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/115.0 Safari/537.36",
        "Referer": "https://duckduckgo.com/",
    }

    try:
        # timeout=10 significa que esperará 10 segundos máximo
        res = requests.post(url, headers=headers, data={"q": query}, timeout=10)
        res.raise_for_status()  # lanza error si el servidor responde con 4xx o 5xx

        soup = BeautifulSoup(res.text, "html.parser")
        results = soup.select("a.result__a")

        if not results:
            print("⚠️ No se encontraron resultados. Puede haber un bloqueo o cambio en el HTML.")
        else:
            for link in results[:10]:
                procesar_link(link, query)

    except requests.Timeout:
        print("⏰ La solicitud tardó demasiado y fue cancelada (timeout).")
    except requests.RequestException as e:
        print(f"❌ Error en la solicitud: {e}")


def procesar_link(link, query):
    href = link["href"]

    # Si es un enlace de DuckDuckGo, extraemos el dominio final
    if href.startswith("https://duckduckgo.com/"):
        params = parse_qs(urlparse(href).query)
        dominio = params.get("ad_domain", [None])[0]  # Ej: 'ninomanuel.es'
        if dominio:
            agregar_entrada(query, dominio)
        else:
            agregar_entrada(query, href)  # por si acaso no tiene ad_domain
    else:
        # Si no es de DuckDuckGo, usamos la URL tal cual o su dominio
        dominio = urlparse(href).netloc
        agregar_entrada(query, dominio or href)


def agregar_entrada(nombre_archivo, texto):
    with open('webs/' + nombre_archivo + '.txt' , 'a', encoding='utf-8') as archivo:
        archivo.write(texto + '\n')
    print(f"Entrada agregada al archivo '{nombre_archivo}' con éxito.")

