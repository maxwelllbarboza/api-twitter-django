# 🐦 Twitter Clone API

Este projeto é uma **API RESTful** desenvolvida com **Django e Django REST Framework (DRF)** que simula as funcionalidades básicas do Twitter.

🔹 **Principais Recursos:**  
✅ Autenticação de usuários com JWT  
✅ Postagem de tweets  
✅ Curtidas e respostas nos tweets  
✅ Sistema de seguidores  
✅ Busca de tweets e usuários  

---

## 🚀 Tecnologias Utilizadas

- **Python 3.9+**
- **Django**
- **Django REST Framework (DRF)**
- **PostgreSQL**
- **JWT (SimpleJWT)**
- **Django ORM**
- **Cloudinary (opcional)** → Para armazenar imagens (avatares, mídia nos tweets)
- **Docker (opcional)** → Para rodar o banco de dados em container

---

## ⚙️ Instalação e Configuração  

### 🔧 **Pré-requisitos**
Antes de iniciar, certifique-se de ter instalado:
- [Python 3.9+](https://www.python.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Docker](https://www.docker.com/) (Opcional)

### 📥 **Clonando o repositório**
```sh
git clone https://github.com/seu-usuario/twitter-clone-api.git
cd twitter-clone-api
```

### 📦 **Criando e ativando o ambiente virtual**
```sh
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 📦 **Instalando dependências**
```sh
pip install -r requirements.txt
```

### 🛠️ **Configurando variáveis de ambiente**
Crie um arquivo `.env` e adicione:
```
SECRET_KEY=sua-chave-secreta
DEBUG=True
ALLOWED_HOSTS=*

DATABASE_NAME=twitter_clone
DATABASE_USER=seu_usuario
DATABASE_PASSWORD=sua_senha
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

### 🔄 **Rodando as migrações do banco**
```sh
python manage.py migrate
```

### ▶️ **Iniciando o servidor**
```sh
python manage.py runserver
```
A API estará disponível em `http://localhost:8000`.

---

# 📌 **Endpoints e Exemplos de JSON**

## 🔹 **Autenticação**
### 🔑 Criar conta
`POST /api/auth/register/`
```json
{
  "username": "maxwell",
  "email": "maxwell@email.com",
  "password": "12345678"
}
```
🔹 **Resposta**
```json
{
  "id": 1,
  "username": "maxwell",
  "email": "maxwell@email.com"
}
```

### 🔑 Login
`POST /api/auth/login/`
```json
{
  "email": "maxwell@email.com",
  "password": "12345678"
}
```
🔹 **Resposta**
```json
{
  "access": "JWT_ACCESS_TOKEN",
  "refresh": "JWT_REFRESH_TOKEN"
}
```

### 🔑 Obter dados do usuário autenticado
`GET /api/auth/me/`
🔹 **Cabeçalho:**  
`Authorization: Bearer JWT_ACCESS_TOKEN`
🔹 **Resposta**
```json
{
  "id": 1,
  "username": "maxwell",
  "email": "maxwell@email.com",
  "followers": 10,
  "following": 5
}
```

---

## 🔹 **Usuários**
### 🔎 Buscar um usuário
`GET /api/users/1/`
🔹 **Resposta**
```json
{
  "id": 1,
  "username": "maxwell",
  "bio": "Desenvolvedor apaixonado por código!",
  "followers_count": 10,
  "following_count": 5
}
```

### 🤝 Seguir um usuário
`POST /api/users/1/follow/`
🔹 **Cabeçalho:**  
`Authorization: Bearer JWT_ACCESS_TOKEN`
🔹 **Resposta**
```json
{
  "message": "Agora você está seguindo maxwell"
}
```

---

## 🔹 **Tweets**
### ✍️ Criar um tweet
`POST /api/tweets/`
🔹 **Cabeçalho:**  
`Authorization: Bearer JWT_ACCESS_TOKEN`
```json
{
  "content": "Meu primeiro tweet!"
}
```
🔹 **Resposta**
```json
{
  "id": 1,
  "content": "Meu primeiro tweet!",
  "author": "maxwell",
  "likes_count": 0,
  "replies_count": 0,
  "created_at": "2024-02-21T12:00:00Z"
}
```

### 🔍 Buscar um tweet específico
`GET /api/tweets/1/`
🔹 **Resposta**
```json
{
  "id": 1,
  "content": "Meu primeiro tweet!",
  "author": "maxwell",
  "likes_count": 5,
  "replies_count": 2
}
```

### ❤️ Curtir um tweet
`POST /api/tweets/1/like/`
🔹 **Cabeçalho:**  
`Authorization: Bearer JWT_ACCESS_TOKEN`
🔹 **Resposta**
```json
{
  "message": "Tweet curtido com sucesso!"
}
```

### 💬 Responder um tweet
`POST /api/tweets/1/reply/`
🔹 **Cabeçalho:**  
`Authorization: Bearer JWT_ACCESS_TOKEN`
```json
{
  "content": "Ótimo tweet!"
}
```
🔹 **Resposta**
```json
{
  "id": 2,
  "content": "Ótimo tweet!",
  "author": "user123",
  "parent_tweet": 1,
  "created_at": "2024-02-21T12:10:00Z"
}
```

---

## 📝 **Licença**
Este projeto está sob a licença **MIT**.

---

👨‍💻 **Desenvolvido por [Seu Nome](https://github.com/seu-usuario)**



