FROM python:3.6

EXPOSE 5000
RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY app/requirements.txt /usr/src/app
#COPY app /app/
RUN pip install -r /usr/src/app/requirements.txt

#COPY app/app.py /app

#ENTRYPOINT ["python", "/src/app.py"]
#CMD python app.py
CMD ["gunicorn", "--bind=0.0.0.0:5000", "--workers=8", "manage:app"]