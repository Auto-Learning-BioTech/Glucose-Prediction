FROM python:3

RUN pip install --upgrade pip \
    && pip install --upgrade setuptools \
    && pip install grpcio==1.29.0 \
    && pip install firebase-admin==4.3.0 \
    && pip install numpy==1.18.4 \
    && pip install scipy==1.4.1 \
    && pip install joblib==0.15.1 \
    && pip install threadpoolctl==2.0.0 \
    && pip install scikit-learn==0.23.1 \
    && pip install tzlocal==2.1 \
    && rm -rf /root/.cache

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

CMD ["python", "src/app.py"]