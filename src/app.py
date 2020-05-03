from flask import Flask
from src.run import get_covid_plot


app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World!"

@app.route('/covid_map')
def get_covid_map():
    return get_covid_plot()


if __name__ == '__main__':
    app.run()