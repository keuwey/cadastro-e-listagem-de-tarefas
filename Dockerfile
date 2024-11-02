# Usar uma imagem oficial do Python como base
FROM python:3.13

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar os arquivos de requisitos para instalar as dependências
COPY requirements.txt requirements.txt

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todos os arquivos do projeto para o diretório de trabalho
COPY . .

# Define a variável de ambiente para o Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# Expor a porta que a aplicação Flask vai utilizar
EXPOSE 5000

# Definir o comando para iniciar a aplicação
CMD ["flask", "run", "--host=0.0.0.0"]
