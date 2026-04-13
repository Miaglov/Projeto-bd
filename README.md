# 🐾 PataVerde — Sistema de Gerenciamento de Petshop

Sistema web de gerenciamento de petshop desenvolvido com **Python + Flask + MySQL**, empacotado com **Docker** para rodar em qualquer máquina.

---

## ✅ Pré-requisito

Você só precisa ter o **Docker** instalado:

- **Windows / Mac:** https://www.docker.com/products/docker-desktop
- **Arch Linux:** `sudo pacman -S docker docker-compose`
- **Ubuntu/Debian:** `sudo apt install docker.io docker-compose`

> Não é necessário instalar Python, MySQL ou qualquer outra dependência.

---

## 🚀 Como rodar

### 1. Clone o repositório ou copie a pasta do projeto

```bash
git clone https://github.com/Miaglov/Projeto-bd.git
cd Projeto-bd
```

### 2. Suba o sistema com Docker

```bash
docker-compose up --build
```

> Na primeira vez pode demorar alguns minutos — o Docker vai baixar as imagens e configurar tudo automaticamente.

### 3. Acesse no navegador

```
http://127.0.0.1:5000
```

### 4. Para encerrar

```bash
# Ctrl+C no terminal, depois:
docker-compose down
```

---

## 🔄 Próximas vezes

Não precisa do --build novamente:

```bash
docker-compose up
```

---

## 📁 Estrutura do projeto

```
petshop/
├── app.py                # Rotas Flask (lógica principal)
├── db.py                 # Conexão com o banco MySQL
├── database.sql          # Script de criação do banco + dados de exemplo
├── requirements.txt      # Dependências Python
├── Dockerfile            # Configuração do container Python/Flask
├── docker-compose.yml    # Orquestração dos containers (Flask + MySQL)
└── templates/            # Templates HTML
    ├── base.html
    ├── index.html        # Dashboard
    ├── clientes/
    ├── pets/
    ├── servicos/
    ├── funcionarios/
    └── agendamentos/
```

---

## ✅ Funcionalidades (CRUD completo)

| Módulo        | Cadastrar | Listar | Editar | Excluir |
|---------------|-----------|--------|--------|---------|
| Clientes      | ✅        | ✅     | ✅     | ✅      |
| Pets          | ✅        | ✅     | ✅     | ✅      |
| Serviços      | ✅        | ✅     | ✅     | ✅      |
| Funcionários  | ✅        | ✅     | ✅     | ✅      |
| Agendamentos  | ✅        | ✅     | ✅     | ✅      |

---

## 🗄️ Diagrama ER

```
clientes (1) ──< pets (N)
pets     (N) ──< agendamentos (N) >── servicos
                 agendamentos (N) >── funcionarios
```

---

## 🛠️ Tecnologias

- Python 3.12 + Flask 3.0
- MySQL 8.0
- Docker + Docker Compose