FROM python:3.10
ENV PYTHONUNBUFFERED 1

WORKDIR /workspace

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
RUN chmod +x /workspace/scripts/init-local.sh


EXPOSE 8000-8080
