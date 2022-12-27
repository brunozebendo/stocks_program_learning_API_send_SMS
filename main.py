"""o objetivo do código é usar uma API para conseguir os dados de uma determinada ação na bolsa de valores
compará-las em valores a do final de uma dia com a do final do dia anterior, além disso, mandar um sms
com as notícias de uma determinada empresa se a diferença das ações for maior que cinco por cento"""

import requests
from twilio.rest import Client

VIRTUAL_TWILIO_NUMBER = "your virtual twilio number"
VERIFIED_NUMBER = "your own phone number verified with Twilio"
"""o stock name e o nome da companhia são requisitos obrigatórios para conseguir a informação"""
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
"""a API_KEY é uma chave que é gerada no site acima e exigida para o acesso"""
STOCK_API_KEY = "YOUR OWN API KEY FROM ALPHAVANTAGE"
NEWS_API_KEY = "YOUR OWN API KEY FROM NEWSAPI"
TWILIO_SID = "YOUR TWILIO ACCOUNT SID"
TWILIO_AUTH_TOKEN = "YOUR TWILIO AUTH TOKEN"

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}
"""o response vai receber as informações obtida no endpoint, lembrando que a sintaxe é request.get, passando
como parâmetros o endpointo que é o endereço do site e os parêmetros obrigatórios e opcionais, nesse caso
o function com a hora do dia que se quer a ação, o nome da ação e a chave de quem está consultando"""
response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
"""aqui foi usado o list compreenhension pois se simplesmente pegássemos o dado do dicionário json, 
ele poderia estar alterado no dia seguinte, assim, o dicionário foi transformado conforme o código abaixo
de onde foi aproveitado somente o valor. Depois, foi obtido o primeiro item da lista que eram os valores
da ação para o dia anterior, isso acontece porque o dicionário traz uma série de valores dos últimos
 dias, assim, ontem será o item [0] e antes de ontem [1] e depois foi obtido o valor do fechamento
  através da cha 4. close., atentar que o nome da chave tem que ser exatamente igual, com espaço, ponto, 
  tudo.. Lembrando que há um site para ver as informações do dicionário json de forma mais visual"""
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)

#the day before yesterday's closing stock price
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
print(day_before_yesterday_closing_price)
"""essa parte do código serve para apurar se a diferença foi positiva ou negativa e mandar uma mensagem com emoji"""
difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

#Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
"""aqui foi achada a diferença entre as ações de um dia para outro simplesmente diminuindo ambas e multiplicando
por 100, lembrando que a string tem que ser transformada em float antes do cálculo"""
diff_percent = round((difference / float(yesterday_closing_price)) * 100)
print(diff_percent)


    ## STEP 2: Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

"""abaixo o código para mais um API, aqui, se o percentual das ações tiver uma diferença maior que cinco por 
cento, a API busca informações em sites de notícias, cria uma dicionário Json de onde guarda os três primeiros
artigos acessando a chave ["articles"} e usando a função slide -1. Reparar q essa chave qInTitle é um dos
parâmetros que está no site para que o programa a palavra em todo o artigo"""
if abs(diff_percent) > 5:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]

    #Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
    three_articles = articles[:3]
    print(three_articles)

    ## STEP 3: Use Twilio to send a seperate message with each article's title and description to your phone number.

    #Create a new list of the first 3 article's headline and description using list comprehension.
"""as próximas linhas formatam a mensagem que será enviada por sms, pra isso, novamente é usado o list
compreehension com a primeira parte sendo todas as informações que serão obtidas na descrição do artigo"""
    formatted_articles = [f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
    print(formatted_articles)
    #Send each article as a separate message via Twilio.
"""essa é a sintaxe do twilio, mas com um for loop para pegar cada um dos 3 artigos"""
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    #TODO 8. - Send each article as a separate message via Twilio.
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=VIRTUAL_TWILIO_NUMBER,
            to=VERIFIED_NUMBER
        )
