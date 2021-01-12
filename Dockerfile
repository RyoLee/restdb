FROM python:3.7.9-alpine
ADD ./res/* /
RUN pip install pymysql flask \
&& chmod +x /entrypoint.sh
WORKDIR /
ENTRYPOINT ["/entrypoint.sh"]