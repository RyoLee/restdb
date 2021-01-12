FROM python:3.7.9-alpine
ADD ./restdb.cfg.sample /
ADD ./restdb.py /
ADD ./entrypoint.sh /
RUN pip install pymysql flask \
&& chmod +x /entrypoint.sh
WORKDIR /
ENTRYPOINT ["/entrypoint.sh"]