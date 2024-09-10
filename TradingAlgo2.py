
from AlgorithmImports import *

#main
class MeasuredMagentaHornet(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2021, 1, 1)
        self.set_end_date(2024, 1, 1)
        self.set_cash(100000)
        self.symbol=self.AddEquity("SPY",Resolution.MINUTE).symbol
        self.rollingWindow = RollingWindow[TradeBar](2)
        self.consolidate(self.symbol, Resolution.DAILY,self.customBarHandler)
        
        self.schedule.on(self.date_rules.every_day(self.symbol),
                    self.time_rules.before_market_close(self.symbol, 15),
                    self.ExitPositions)
    def on_data(self, data: Slice):
        if not self.rollingWindow.is_ready:
            return

        if not (self.time.hour == 9 and self.time.minute == 31):
            return

        if data[self.symbol].open >= 1.01*self.rollingWindow[0].Close:
            self.set_holdings(self.symbol, -1)
        elif data[self.symbol].open <= 0.99* self.rollingWindow[0].Close:
            self.set_holdings(self.symbol, 1)



    def customBarHandler(self, bar):
        self.rollingWindow.Add(bar)
    
    def ExitPositions(self):
        self.liquidate(self.symbol)
