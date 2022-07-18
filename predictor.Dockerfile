FROM python:3.8

COPY predictor predictor
COPY sklearnserver sklearnserver

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r ./predictor/requirements.txt

RUN pip install --no-cache-dir -e ./sklearnserver

EXPOSE 8080

RUN useradd kserve -m -u 1000 -d /home/kserve
USER 1000
ENTRYPOINT ["python", "-m", "sklearnserver", "--model_dir", "./predictor",  "--model_name", "income", "--protocol", "seldon.http"]
