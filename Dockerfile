FROM python:2.7

ADD ./main.py /main.py

CMD ["python", "/main.py"]
