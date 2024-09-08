#clear the default template
from AlgorithmImports import *


class UpgradedTanDogfish(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2024, 1, 1)
        self.set_end_date(2025, 1, 1)
        self.set_cash(100000)
        spy = self.add_equity("SPY", Resolution.Daily)
        
        spy.set_data_normalization_mode(DataNormalizationMode.RAW)

        self.spy = spy.symbol
        self.set_benchmark("SPY")
        self.set_brokerage_model(brokerage_name.InteractiveBrokerBrokerage, account_type.Margin)
        
        self.EntryPrice = 0
        self.period = timedelta(31)
        self.nextEntryTime = self.time

    def on_data(self, data):
        if not self.spy in data:
            return 
        
        price = data[self.spy].Close

        if not self.portfolio.invested:
         if self.nextEntryTime <= self.time:
            self.set_holdings(self.spy, 1)
          #  self.market_order(self.spy, int(self.portfolio.cash / price))
            self.log("BUY SPY @" + str(price))
            self.EntryPrice = price

        elif self.EntryPrice*1.1 < price or self.EntryPrice * 0.9 > price :
            self.liquidate()
            self.log("SELL SPY @" + str(price))
            self.nextEntryTime = self.time + self.period