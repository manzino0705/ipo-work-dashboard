from flask import Flask, render_template
from IPO_date import IPO_date 
from kospi_data import get_kospi_kosdaq_data, get_exchange_rate
from weather import get_weather
from news import get_news
from merge import get_merge

app = Flask(__name__)

@app.route('/')
def home():
   IPO_data = IPO_date()
   k_data = get_kospi_kosdaq_data()
   exchange_data = get_exchange_rate()
   weather_data = get_weather()
   today_news = get_news()
   merge = get_merge()
   return render_template('index.html', IPO_data=IPO_data , k_data=k_data, e_data= exchange_data, w_data=weather_data, news=today_news, m=merge)

@app.route('/work')
def work():
   IPO_data = IPO_date()
   return render_template('work.html',IPO_data=IPO_data )

@app.route('/news')
def news():
   today_news = get_news()
   return render_template('news.html',news=today_news)

if __name__ == '__main__':
   app.run('0.0.0.0', port=5050, debug=True)

