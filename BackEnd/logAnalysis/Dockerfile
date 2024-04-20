FROM python:3.10

# Copiez les fichiers nécessaires dans l'image
COPY listener.py /app/listener.py
COPY ml.py /app/ml.py
COPY mail.py /app/mail.py
COPY requirements.txt /app/requirements.txt

RUN mkdir /app/logs; mkdir /app/models; mkdir /app/tmp; pip install -r /app/requirements.txt

WORKDIR /app/

# Définissez le point d'entrée de l'image
CMD ["python", "listener.py"]
