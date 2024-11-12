# Cadastro e listagem de tarefas

Projetinho feito como instrumento avaliativo em um processo seletivo.

## Deploy

A aplicação está hospedada na plataforma [Render](https://render.com/) e está acessível no seguinte link:

- [Aplicação de Tarefas - Deploy Render](https://cadastro-e-listagem-de-tarefas.onrender.com/)

### Executando Localmente

Se preferir, você pode rodar a aplicação localmente. Siga os passos:

Clone o repositório e entre na pasta do projeto:

```bash
git clone https://github.com/keuwey/cadastro-e-listagem-de-tarefas
cd cadastro-e-listagem-de-tarefas
```

Faça o build da imagem Docker e rode

```bash
docker-compose up --build
```

Por fim, acesse a aplicação pelo navegador em <http://localhost:5000>

## Funcionalidades

- Cadastrar tarefas
- Editar Tarefas
- Reordenar Tarefas
- Excluir Tarefas

## Stack utilizada

**Frontend:** HTML & CSS

**Backend:** Flask, SQLAlchemy, SQLite
