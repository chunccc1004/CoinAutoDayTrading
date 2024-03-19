FROM python:3.11

WORKDIR /home/

RUN git clone https://github.com/chunccc1004/CoinAutoDayTrading.git

WORKDIR /home/CoinAutoDayTrading/

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["bash", "-c", "python main.py"]