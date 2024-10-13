FROM python:3.11

RUN pip install --upgrade pip setuptools

RUN apt update

RUN useradd -rms /bin/bash bro && chmod 777 /opt /run

WORKDIR /lil_bro

COPY --chown=bro:lil_bro req.txt /lil_bro/req.txt

RUN pip install -r req.txt

RUN mkdir /lil_bro/static && mkdir /lil_bro/media && chown -R bro:bro /lil_bro && chmod 755 /lil_bro

COPY --chown=bro:lil_bro . .

USER bro

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
