FROM python:3.8.10-alpine3.14

RUN pip install pipenv

RUN mkdir -p /backend
WORKDIR /backend

COPY Pipfile Pipfile.lock ./
RUN pipenv install --deploy --ignore-pipfile

COPY . .

CMD ["pipenv", "run", "python", "deploy.py"]