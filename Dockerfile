FROM python:3.7-alpine
ADD . /code
COPY . /code 
WORKDIR /code
ENV FLASK_RUN_HOST 0.0.0.0
EXPOSE 5000
ENV FLASK_APP app.py
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt                                                   

COPY . .
CMD ["flask", "run"]

