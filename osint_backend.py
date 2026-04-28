import os
import json
import time
import requests
from datetime import datetime

# ==========================================
# ANTIGRAVITY - OSINT DATA COLLECTOR
# ==========================================
# Este script pode ser rodado via GitHub Actions para 
# coletar dados e gerar um relatório estático (.json)
# que o Frontend irá consumir via GitHub Pages.

# Carrega tokens do ambiente (GitHub Secrets)
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
GOOGLE_CSE_ID = os.environ.get('GOOGLE_CSE_ID')
HIBP_API_KEY = os.environ.get('HIBP_API_KEY')

def buscar_google(query):
    """Busca no Google Custom Search"""
    if not GOOGLE_API_KEY or not GOOGLE_CSE_ID:
        return {"error": "Chaves do Google não configuradas."}
    
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={GOOGLE_API_KEY}&cx={GOOGLE_CSE_ID}"
    try:
        response = requests.get(url)
        # Rate Limiting: Pausa para evitar bloqueios
        time.sleep(2)
        if response.status_code == 200:
            return response.json().get('items', [])
        return []
    except Exception as e:
        return {"error": str(e)}

def verificar_vazamentos(email):
    """Verifica e-mail na API do Have I Been Pwned"""
    if not HIBP_API_KEY:
        return {"error": "Chave do HIBP não configurada."}
    
    headers = {
        'hibp-api-key': HIBP_API_KEY,
        'user-agent': 'Antigravity-OSINT-Tool'
    }
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
    try:
        response = requests.get(url, headers=headers)
        time.sleep(2) # Respeitando ToS e Rate Limits
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return [] # Nenhum vazamento
        return {"error": f"Erro HTTP {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def consultar_whois(dominio):
    """Placeholder para consulta WHOIS de domínios (ex: Registro.br)"""
    # Aqui pode ser implementada uma chamada para uma API WHOIS real ou biblioteca python-whois
    print(f"Consultando WHOIS para: {dominio}")
    return {"status": "Não implementado", "mensagem": "Integração WHOIS necessária"}

def consultar_portal_transparencia(nome):
    """Placeholder para busca em dados abertos / Portal da Transparência"""
    # Integração com APIs governamentais (requer chave de API específica em muitos casos)
    print(f"Consultando Portal da Transparência para: {nome}")
    return {"status": "Não implementado", "mensagem": "Integração Portal da Transparência necessária"}

def gerar_relatorio_estatico(alvos):
    """Gera o arquivo JSON que será lido pelo frontend (GitHub Pages)"""
    resultados = {}
    
    for alvo in alvos:
        print(f"Investigando alvo: {alvo['nome']}")
        
        dados = {
            "timestamp": datetime.now().isoformat(),
            "google_results": buscar_google(f'"{alvo["nome"]}" {alvo.get("profissao", "")}'),
            "vazamentos": verificar_vazamentos(alvo.get("email", "")) if alvo.get("email") else [],
            "portal_transparencia": consultar_portal_transparencia(alvo["nome"]),
            "whois": consultar_whois(alvo.get("dominio", "")) if alvo.get("dominio") else {}
        }
        resultados[alvo['id']] = dados
        
    # Salvar em arquivo para o frontend consumir
    os.makedirs('data', exist_ok=True)
    with open('data/relatorio_osint.json', 'w', encoding='utf-8') as f:
        json.dump(resultados, f, ensure_ascii=False, indent=4)
    print("Relatório gerado em data/relatorio_osint.json")

if __name__ == "__main__":
    # Exemplo de configuração de alvos (pode vir de um arquivo config.json no repositório)
    lista_alvos = [
        {"id": "alvo_01", "nome": "João Silva Exemplo", "email": "joao.exemplo@email.com", "profissao": "Engenheiro"}
    ]
    
    print("Iniciando varredura OSINT. Respeite os Termos de Serviço e Leis de Privacidade.")
    gerar_relatorio_estatico(lista_alvos)
    print("Script pronto para uso em automação (GitHub Actions).")
