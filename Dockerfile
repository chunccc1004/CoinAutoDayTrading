FROM python:3.11

WORKDIR /home/

RUN git clone https://github.com/chunccc1004/CoinAutoDayTrading.git

WORKDIR /home/CoinAutoDayTrading/

RUN git checkout feature/docker_test

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["bash", "-c", "python -u main.py"]