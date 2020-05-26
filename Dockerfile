#FROM publysher/alpine-scipy:1.0.0-numpy1.14.0-python3.6-alpine3.7
FROM python:3

#RUN apk --no-cache add --virtual .builddeps g++ musl-dev \
RUN pip install --upgrade pip \
    && pip install --upgrade setuptools \
    && pip install grpcio==1.29.0 \
    && pip install firebase-admin==4.3.0 \
    && pip install numpy==1.18.4 \
    && pip install scipy==1.4.1 \
    && pip install joblib==0.15.1 \
    && pip install threadpoolctl==2.0.0 \
    && pip install scikit-learn==0.23.1 \
    #&& apk del .builddeps \
    && rm -rf /root/.cache

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

CMD ["python", "src/app.py"]