FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

# ENVS RECOMENDATIONS
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# COPY DEPENDENCIES
COPY requirements.txt ./

# COPY PROJECT
COPY ./app /app/app

# INSTALL DEPENDENCIES
RUN pip install -r requirements.txt

EXPOSE 80
