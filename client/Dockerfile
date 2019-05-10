FROM python:3.6

EXPOSE 80



WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY client.py /app
#CMD python admin.py

