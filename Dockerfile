FROM python:3.9-alpine
WORKDIR /code
ENV FLASK_APP=db_create.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1
RUN apk add --no-cache gcc g++ musl-dev linux-headers libffi-dev openssl-dev python3-dev curl
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run"]