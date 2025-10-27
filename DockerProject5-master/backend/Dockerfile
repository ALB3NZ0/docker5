FROM python:3.11

WORKDIR /docker-project

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . . 

EXPOSE 8000

CMD [ "python", "main.py" ]