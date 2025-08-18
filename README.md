# 🎓 EdVenture

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.x-green.svg?logo=flask)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-DB-lightblue.svg?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-em%20desenvolvimento-orange)]()

Plataforma interativa de **gamificação para professores**.  
O **EdVenture** permite que educadores compartilhem projetos, recebam comentários e colaborem em uma jornada de aprendizagem inovadora, unindo **educação + tecnologia + engajamento**.

---

## 🚀 Funcionalidades

- 📂 **Projetos**  
  - Criação de projetos completos com título, descrição, autor, categoria e ano escolar.  
  - Upload de múltiplas mídias (imagens, vídeos, documentos).  
  - Edição e visualização em página individual.

- 🖼️ **Feed**  
  - Exibição de todos os projetos publicados.  
  - Filtros por **tags**, **categoria** e **ano escolar**.  
  - Ranking de termos mais usados em cada campo.

- 💬 **Comentários**  
  - Interação em cada projeto (perfil e página individual).  
  - Espaço para feedback construtivo e discussões.

- 🏆 **Gamificação**  
  - Ranking de pontuações.  
  - Tasks quinzenais e flash tasks (pontos extras).  
  - Premiações e conquistas para engajar professores.

- 📱 **Responsividade**  
  - Layout adaptável para desktop, tablets e celulares.

---

## 🛠️ Tecnologias Utilizadas

- [Python](https://www.python.org/) + [Flask](https://flask.palletsprojects.com/)  
- [SQLite](https://www.sqlite.org/) (banco de dados local)  
- [HTML5](https://developer.mozilla.org/pt-BR/docs/Web/HTML), [CSS3](https://developer.mozilla.org/pt-BR/docs/Web/CSS), [JavaScript](https://developer.mozilla.org/pt-BR/docs/Web/JavaScript)  
- [Bootstrap](https://getbootstrap.com/) ou [TailwindCSS](https://tailwindcss.com/)  
- [FontAwesome](https://fontawesome.com/) (ícones)  

---

## 📂 Estrutura do Projeto



- EdVenture/
- ├── app.py # Aplicação Flask principal
- ├── models.py # Modelos do banco de dados
- ├── forms.py # Formulários (WTForms)
- ├── routes.py # Rotas principais
- ├── comunidade.db # Banco de dados SQLite
- ├── static/ # Arquivos estáticos (CSS, JS, imagens)
- │ └── avatares/
- ├── templates/ # Templates HTML
- │ ├── base.html
- │ ├── perfil.html
- │ ├── feed.html
- │ ├── missoes.html
- │ ├── taverna.html
- │ └── visualizar_projeto.html
- └── README.md


---

## ⚡ Instalação e Execução

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/seuusuario/edventure.git
   cd edventure

2. **Crie e ative um ambiente virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows

3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt

4. **Execute a aplicação**:
   ```bash
   flask run

5. **Acesse no navegador**:
👉 http://127.0.0.1:5000


👥 Contribuição

Quer contribuir? Siga os passos:

Faça um fork do projeto.

Crie uma branch para sua feature (git checkout -b minha-feature).

Faça commit das alterações (git commit -m 'Adicionei nova feature').

Faça push para a branch (git push origin minha-feature).

Abra um Pull Request.

📜 Licença

Este projeto está licenciado sob a MIT License.

✨ Créditos

Projeto desenvolvido por Gustavo Oliveira e colaboradores.
Inspirado na ideia de unir educação, gamificação e tecnologia para transformar a jornada dos professores.