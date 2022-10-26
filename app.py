from flask import Flask
import git
from src.business_logic.process_query import create_business_logic
from src.IO.get_data_from_yahoo import get_last_stock_price


app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello():
    return f'Hello dear humans and zombies, you should use a better route:!\nEX: get_stock_val/<ticker>\n'


@app.route('/get_stock_val/<ticker>', methods=['GET'])
def get_stock_value(ticker):
    bl = create_business_logic()
    prediction = bl.do_predictions_for(ticker)
    df = get_last_stock_price(ticker) 
    print(df)
    pred_sma30 = df['close'].rolling(30).mean()
    pred_sma30 = pred_sma30[29]
    price= df['close'][29]

    return f'Linear regression for {ticker} : {prediction}\n SMA30 for {ticker} : {pred_sma30}\n D-1 price: {price}'


@app.route('/getversion/')
def getversion():
    repo = git.Repo(search_parent_directories=True)
    sha = repo.head.object.hexsha

    return f'{sha}\n'


if __name__ == '__main__':
    # Used when running locally only. When deploying to Cloud Run,
    # a webserver process such as Gunicorn will serve the app.
    app.run(host='localhost', port=8080, debug=True)
