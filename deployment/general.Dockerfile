FROM python:3.10

WORKDIR /app/src

COPY requirements.txt .
RUN /usr/local/bin/python -m pip install --upgrade pip

ENV PATH=$PATH:/app/vendor/bin
ENV PYTHONPATH=$PYTHONPATH:/app/vendor/lib/python3.10/site-packages
ENV PYTHONUNBUFFERED=1

COPY . /app