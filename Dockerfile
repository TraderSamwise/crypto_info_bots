FROM python:3.7

# Creating working directory
#WORKDIR /var/www/html

# Copying requirements
COPY . .

RUN apt-get update ##[edited]
RUN apt-get install ffmpeg libsm6 libxext6  -y
#    && apk add gcc \
#    && apk add musl-dev \
#    && apk add linux-headers \
#    && apk add jpeg-dev \
#    && apk add zlib-dev \
#    && apk add mariadb-dev \
#    && apk add libffi-dev

# install pypi packages
COPY requirements.txt /requirements.txt

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

CMD ["python","-u","src/scanner.py"]