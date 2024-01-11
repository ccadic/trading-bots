import asyncio
from binance import AsyncClient
from tabulate import tabulate
import datetime
import telegram

# Paramètres de votre bot Telegram
TELEGRAM_TOKEN = "6739910430:xxxxxxxxxxxxxxxxxxxx"
TELEGRAM_CHAT_ID = "-408786357632"

# Couleurs pour l'affichage dans le terminal
RED = "\033[91m"
RESET = "\033[0m"

async def calculate_ma(client, symbol, interval, period):
    """ Calcule la moyenne mobile pour une période donnée. """
    candles = await client.get_klines(symbol=symbol, interval=interval, limit=period)
    closes = [float(candle[4]) for candle in candles]
    return sum(closes) / len(closes)

async def calculate_slope(client, symbol, interval, period):
    """ Calcule la pente de la moyenne mobile. """
    current_ma = await calculate_ma(client, symbol, interval, period)
    previous_ma = await calculate_ma(client, symbol, interval, period + 1)
    slope = current_ma - previous_ma
    return slope

async def send_telegram_message(bot, message):
    """ Envoie un message à votre chat Telegram. """
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

async def main():
    # Initialisation des clients Binance et Telegram
    binance_client = await AsyncClient.create()
    telegram_bot = telegram.Bot(token=TELEGRAM_TOKEN)

    condition_was_true = False
    message_sent = False

    await send_telegram_message(telegram_bot, "BTC USD Signals Re-Started *** Sends ALERT when MA(7) > MA(25) > MA(99) ")

    while True:
        try:
            # Calcul des moyennes mobiles
            ma7 = await calculate_ma(binance_client, "BTCUSDT", AsyncClient.KLINE_INTERVAL_15MINUTE, 7)
            ma25 = await calculate_ma(binance_client, "BTCUSDT", AsyncClient.KLINE_INTERVAL_15MINUTE, 25)
            ma99 = await calculate_ma(binance_client, "BTCUSDT", AsyncClient.KLINE_INTERVAL_15MINUTE, 99)

            # Calcul des pentes
            slope_ma7 = await calculate_slope(binance_client, "BTCUSDT", AsyncClient.KLINE_INTERVAL_15MINUTE, 7)
            slope_ma25 = await calculate_slope(binance_client, "BTCUSDT", AsyncClient.KLINE_INTERVAL_15MINUTE, 25)
            slope_ma99 = await calculate_slope(binance_client, "BTCUSDT", AsyncClient.KLINE_INTERVAL_15MINUTE, 99)

            btc_price = await binance_client.get_symbol_ticker(symbol="BTCUSDT")
            btc_price = btc_price["price"]

            data = [
                ["Date/Heure", datetime.datetime.now()],
                ["MA(7)", ma7, "Slope MA(7)", slope_ma7],
                ["MA(25)", ma25, "Slope MA(25)", slope_ma25],
                ["MA(99)", ma99, "Slope MA(99)", slope_ma99],
                ["BTC Price", btc_price]
            ]

            table = tabulate(data, headers="firstrow", tablefmt="grid")
            print(table)

            # Vérification des conditions
            if ma7 > ma25 > ma99 and all(slope > 0 for slope in [slope_ma7, slope_ma25, slope_ma99]):
                if not condition_was_true:
                    alert_message = RED + "BTC RED Alert: MA(7) > MA(25) > MA(99) with Positive Slopes" + RESET
                    print(alert_message)
                    await send_telegram_message(telegram_bot, "BTC/USDT ALERT: MA(7) > MA(25) > MA(99) with Positive Slopes\n\n" + table)
                    condition_was_true = True
                    message_sent = False
            else:
                if condition_was_true and not message_sent:
                    await send_telegram_message(telegram_bot, "MA(7) MA(25) MA(99) not aligned anymore or Slopes not Positive\n\n" + table)
                    message_sent = True
                condition_was_true = False

            await asyncio.sleep(900)  # Attendre 15 minutes
        except Exception as e:
            print("Erreur:", e)
            await asyncio.sleep(60)  # Attendre 1 minute en cas d'erreur

    await binance_client.close_connection()

if __name__ == "__main__":
    asyncio.run(main())
