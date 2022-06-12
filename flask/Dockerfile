FROM  python:3.8
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY src .

RUN pip install -r requirements.txt
RUN pip install gunicorn
RUN echo "launch=docker" > config.config

EXPOSE 5000

CMD gunicorn --bind 0.0.0.0:5000 --log-level DEBUG wsgi:app

#CMD ["gunicorn", "-w", "4", "--bind", "0.0.0.0:5000", "--log-level", "DEBUG", "wsgi:app"]