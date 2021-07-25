FROM python:3.8.10-alpine3.14

RUN pip install pipenv

RUN mkdir -p /backend
WORKDIR /backend

COPY Pipfile Pipfile.lock ./
RUN pipenv install --deploy --ignore-pipfile

COPY . .

EXPOSE 8000

CMD ["pipenv", "run", "python", "deploy.py"]
