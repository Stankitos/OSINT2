# Antigravity - OSINT Dashboard

Um painel de Inteligência de Fontes Abertas (OSINT) focado em organização, velocidade e conformidade com privacidade.

## 🏗 Arquitetura
O sistema é projetado para ser hospedado gratuitamente no **GitHub Pages**. 
A arquitetura é dividida em:
1. **Frontend**: Interface estática (HTML/CSS/JS) com design premium, dark mode e responsividade. Responsável pela interação do usuário.
2. **Backend (Automação)**: Scripts em Python (`osint_backend.py`) para consumir APIs externas que não suportam CORS ou que precisam ocultar chaves de acesso. 

## 🛡 Privacidade e Legalidade
Este projeto foi construído respeitando as melhores práticas:
* **Conformidade LGPD/GDPR**: Os dados não são persistidos em bancos de dados relacionais públicos, servindo apenas para visualização e cruzamento temporário de informações.
* **Segurança de API**: As chaves de API não devem ser inseridas no código fonte. O Frontend permite salvar as chaves diretamente no `localStorage` do seu navegador. Para o backend, utilize **GitHub Secrets**.
* **Tratamento de Homônimos**: Filtros adicionais de profissão e localidade ajudam a identificar alvos corretamente, evitando exposição de pessoas erradas.
* **Respeito aos ToS (Termos de Serviço)**: Intervalos de requests (`sleep`) no backend Python garantem que a ferramenta não faça scraping agressivo ou DDoS nas fontes.

## 🚀 Fluxo de Trabalho (GitHub Desktop + Pages)

### 1. Clonar e Modificar Localmente
1. Abra o **GitHub Desktop**.
2. Clone o repositório para o seu computador.
3. Edite os arquivos (`index.html`, `script.js`, `styles.css`) usando seu editor preferido (ex: VS Code).
4. No GitHub Desktop, preencha o resumo das alterações (ex: "Atualização de CSS") e clique em **Commit to main**.
5. Clique em **Push origin** para enviar as alterações.

### 2. Ativar o GitHub Pages
1. No repositório no GitHub, acesse **Settings** > **Pages**.
2. Em **Build and deployment**, selecione a branch `main` e a pasta `/ (root)`.
3. O GitHub fornecerá uma URL pública (ex: `https://seu-usuario.github.io/OSINT/`). O site estará online em alguns minutos.

## 🔌 APIs Sugeridas
Para alimentar o banco de dados do projeto, recomenda-se o uso oficial das seguintes APIs:
* **Google Custom Search API**: Para realizar dorks (`site:linkedin.com`, etc).
* **Have I Been Pwned API**: Para checar vazamento de emails e senhas.
* **WHOIS / Registro.br**: Para validar propriedades de domínio.
* **Portais da Transparência**: Através de dados abertos governamentais.
