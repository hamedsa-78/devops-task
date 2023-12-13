FROM python:3.9-slim

RUN pip install -U pip
RUN pip install pipenv 

WORKDIR /app

COPY [ "Pipfile", "Pipfile.lock", "./" ]

RUN pipenv install --system --deploy

COPY [ "*.py" , "./" ]

EXPOSE 8000

ENTRYPOINT [ "uvicorn", "gateway:app", "--host", "0.0.0.0", "--port", "8000" ]
