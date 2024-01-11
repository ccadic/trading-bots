This Python script implements a cryptocurrency trading strategy for the BTC/USDT pair on the Binance exchange. It periodically calculates moving averages (MAs) and their slopes to determine the trend and sends alerts through Telegram.

Key Features:

Moving Average Calculation: The script calculates three moving averages for BTC/USDT - MA(7), MA(25), and MA(99), using 15-minute intervals.

Slope Calculation: It computes the slope of each moving average. The slope is determined by the difference between the current value and the previous value of the MA.

Condition Checking: The script checks two conditions:

If all three MAs are in ascending order (MA(7) > MA(25) > MA(99)).
If the slopes of all three MAs are positive, indicating an upward trend.
Telegram Alerts: When both conditions are met, and it wasn't true in the previous check, an alert with detailed information is sent to a specified Telegram chat. If the conditions change (either MAs are not aligned or slopes turn negative), a different alert is sent.

Continuous Monitoring: The script runs continuously, checking the conditions every 15 minutes.

This strategy is useful for users interested in monitoring the BTC/USDT pair for potential bullish trends based on moving averages and their slopes.

Contact: @sulfuroid
BTC wallet address if you want to help: bc1qpzu36plm902ja7kxqkrrrryu32tg3zaknm2wsk
