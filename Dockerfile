FROM publysher/alpine-scipy:1.0.0-numpy1.14.0-python3.6-alpine3.7

RUN apk --no-cache add --virtual .builddeps g++ musl-dev \
    && pip install --upgrade pip \
    && pip install scikit-learn==0.19.1 \
    && apk del .builddeps \
    && rm -rf /root/.cache

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

CMD ["python", "src/app.py"]
