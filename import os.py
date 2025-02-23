import os
import time
import asyncio
import requests
import numpy as np
import pandas as pd
from pybit.unified_trading import HTTP
from telegram import Bot

class BybitAutoTrader:
    def __init__(self, api_key, api_secret, telegram_token, telegram_chat_id, investment_amount=100, leverage=5, spread_threshold=0.5):
        self.api_key = api_key
        self.api_secret = api_secret
        self.telegram_token = telegram_token
        self.telegram_chat_id = telegram_chat_id
        self.investment_amount = investment_amount
        self.leverage = leverage
        self.spread_threshold = spread_threshold
        self.session = HTTP(api_key=self.api_key, api_secret=self.api_secret)
        self.trade_history = []
        self.data_log = []
        self.bot = Bot(token=self.telegram_token)

    def get_price(self, symbol):
        try:
            spot_price = self.session.get_ticker(category="spot", symbol=symbol)['result']['lastPrice']
            futures_price = self.session.get_ticker(category="linear", symbol=symbol + "USDT")['result']['lastPrice']
            return float(spot_price), float(futures_price)
        except Exception as e:
            print(f"Error fetching price for {symbol}: {e}")
            return None, None

    def find_best_spread(self):
        symbols = ["BTCUSDT", "ETHUSDT", "XRPUSDT", "SOLUSDT"]
        best_symbol = None
        max_spread = 0

        for symbol in symbols:
            spot, futures = self.get_price(symbol)
            if spot is None or futures is None:
                continue
            
            spread = abs((futures - spot) / spot * 100)
            self.data_log.append({"symbol": symbol, "spread": spread, "timestamp": time.time()})
            
            if spread > max_spread:
                max_spread = spread
                best_symbol = symbol
        
        return best_symbol, max_spread

    def send_telegram_alert(self, message):
        try:
            self.bot.send_message(chat_id=self.telegram_chat_id, text=message)
        except Exception as e:
            print(f"Error sending Telegram alert: {e}")

    def execute_trade(self):
        symbol, spread = self.find_best_spread()
        if spread < self.spread_threshold:
            print("No suitable trade found.")
            return
        
        spot_price, futures_price = self.get_price(symbol)
        position_size = self.investment_amount * self.leverage / spot_price
        
        print(f"Executing trade for {symbol}: Spread = {spread:.2f}%")
        
        try:
            self.session.place_order(category="spot", symbol=symbol, side="Buy", orderType="Market", qty=position_size)
            self.session.place_order(category="linear", symbol=symbol + "USDT", side="Sell", orderType="Market", qty=position_size, leverage=self.leverage)
            self.trade_history.append({"symbol": symbol, "spread": spread, "timestamp": time.time()})
            message = f"Trade executed!\nSymbol: {symbol}\nSpread: {spread:.2f}%"
            self.send_telegram_alert(message)
            print("Trade executed!")
        except Exception as e:
            print(f"Trade execution failed: {e}")
    
    def save_trade_history(self):
        df = pd.DataFrame(self.trade_history)
        df.to_csv("trade_history.csv", index=False)
        print("Trade history saved to CSV")
    
    def backtest_spread_strategy(self, historical_data):
        print("Running backtest...")
        profits = []
        for data in historical_data:
            spread = abs((data['futures'] - data['spot']) / data['spot'] * 100)
            if spread > self.spread_threshold:
                profits.append(spread)
        avg_profit = np.mean(profits) if profits else 0
        print(f"Backtest completed. Average profit potential: {avg_profit:.2f}%")

    def run(self):
        while True:
            self.execute_trade()
            self.save_trade_history()
            time.sleep(60)

if __name__ == "__main__":
    api_key = os.getenv("BYBIT_API_KEY")
    api_secret = os.getenv("BYBIT_API_SECRET")
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
    trader = BybitAutoTrader(api_key, api_secret, telegram_token, telegram_chat_id)
    trader.run()


900줄 규모의 코드를 단계적으로 추가하려면 다음과 같이 요청하면 됩니다:  

### **예제 명령어**  
1. **"이어서 기능 추가해줘"** → 이전 코드 유지하면서 새로운 기능만 추가  
2. **"기능을 나눠서 하나씩 추가해줘"** → 한 번에 하나의 기능씩 추가  
3. **"1단계: 리스크 관리 기능 추가해줘"** → 특정 기능을 단계적으로 구현 요청  
4. **"2단계: GUI 인터페이스 추가해줘"** → 명확한 순서 지정  

다음으로 어떤 기능을 추가할까요? 🚀