import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pandas as pd
from cryptography.fernet import Fernet
import os
from io import StringIO
from yahooquery import Ticker
from datetime import datetime
import requests

# Manually update this based on your portfolio
growth_symbols = ["VIR", "TSLA", "PLL", "MU", "IREN", "CLSK", "AMD", "BITB", "ALAB"]
emerging_symbols = ["BTDR", "IRD", "CRMD", "LFMD"]
divident_symbols = ["MRK", "TSM"]

# Manually update this based future acquisitions
acquisitions = [["IRD", "OCUP"]]
acquisitions = {
    "OCUP": {
        "new_symbol": "IRD",
        "description": "OPUS GENETICS INC",
        "exchange": "NASDAQ",
    },
    "PLL": {
        "new_symbol": "ELVR",
        "description": "ELEVRA LITHIUM LTD",
        "exchange": "NASDAQ",
    },
}

data = "current_data"
folio_key = os.getenv("FOLIO_KEY")
f = Fernet(folio_key)


def decrypt(file_path):
    with open(file_path, "rb") as file:
        file_data = file.read()
    raw = f.decrypt(file_data)
    raw_str = raw.decode("utf-8")
    return pd.read_csv(StringIO(raw_str))


def get_account_info():
    raw = decrypt(f"{data}/account.csv")
    columns = [
        "ClientAccountID",
        "CurrencyPrimary",
        "Name",
        "AccountType",
        "CustomerType",
        "AccountCapabilities",
        "TradingPermissions",
        "DateOpened",
        "DateFunded",
        "Street",
        "Street2",
        "City",
        "State",
        "Country",
        "PostalCode",
        "IBEntity",
        "PrimaryEmail",
    ]
    account = raw[columns].copy()
    return account


def get_cash_report():
    crtt = decrypt(f"{data}/CRTT.csv")
    available_cash = np.round(
        crtt[crtt["CurrencyPrimary"] == "BASE_SUMMARY"]["NetCashBalanceSLB"].iloc[0], 2
    )
    return crtt, available_cash


def get_cash_transactions():
    ctrn = decrypt(f"{data}/CTRN.csv")
    return ctrn


def get_positions():
    positions = decrypt(f"{data}/POST.csv")
    return positions


def get_trades():
    trades = decrypt(f"{data}/TRNT.csv")

    # squash aquisition
    for old_symbol, acquisition_info in acquisitions.items():
        new_symbol = acquisition_info["new_symbol"]
        description = acquisition_info["description"]
        exchange = acquisition_info["exchange"]

        trades.loc[trades["Symbol"] == old_symbol, "Description"] = description
        trades.loc[trades["Symbol"] == old_symbol, "ListingExchange"] = exchange
        trades.loc[trades["Symbol"] == old_symbol, "Symbol"] = new_symbol

    return trades


trades = get_trades()


def get_info(symbol):
    row = trades[
        (trades["Symbol"] == symbol) & (trades["LevelOfDetail"] == "EXECUTION")
    ].iloc[0]
    return row["Description"], row["ListingExchange"]


def calculate_portfolio_from_trades(symbol):
    orders = trades[
        (trades["Symbol"] == symbol) & (trades["LevelOfDetail"] == "EXECUTION")
    ]

    orders_sorted = orders.sort_values(by="OrderTime")

    total_quantity = 0.0
    total_cost_basis = 0.0
    total_pnl = 0.0

    for index, row in orders_sorted.iterrows():
        if row["Buy/Sell"] == "BUY":
            total_quantity += row["Quantity"]
            total_cost_basis += row["CostBasis"]
        elif row["Buy/Sell"] == "SELL":
            qty_sold = abs(row["Quantity"])
            # net_cash = row['NetCash']
            fifopnl = row["FifoPnlRealized"]
            sale_cost_basis = abs(row["CostBasis"])

            total_cost_basis -= sale_cost_basis
            total_quantity -= qty_sold
            total_pnl += fifopnl

    average_unit_price = (
        total_cost_basis / total_quantity if total_quantity > 0 else 0.0
    )

    fees = abs(orders["Taxes"].sum()) + abs(orders["IBCommission"].sum())
    total_sell = abs(orders[(orders["Buy/Sell"] == "SELL")]["Quantity"].sum())
    total_buy = orders[(orders["Buy/Sell"] == "BUY")]["Quantity"].sum()

    return (
        int(np.round(total_quantity, 0)),
        np.round(average_unit_price, 2),
        np.round(fees, 2),
        np.round(total_cost_basis, 2),
        np.round(total_pnl, 2),
        np.round(total_buy, 1),
        np.round(total_sell, 1),
    )


def categorised_portfolio(portfolio, category_symbols):
    cat_folio = portfolio[portfolio["SYMBOL"].isin(category_symbols)]
    cat_folio.reset_index(drop=True, inplace=True)
    return cat_folio


def get_cash_details():
    crtt, available_cash = get_cash_report()
    ctrn = get_cash_transactions()
    bank_transfers = ctrn.query(
        'CurrencyPrimary == "USD" and Type == "Deposits/Withdrawals"'
    )["Amount"].sum()
    interest_recieved = ctrn.query(
        'CurrencyPrimary == "USD" and Type == "Broker Interest Received"'
    )["Amount"].sum()

    return (
        np.round(available_cash, 2),
        np.round(bank_transfers, 2),
        np.round(interest_recieved, 2),
    )


def get_folios():
    symbols = trades[trades["AssetClass"] == "STK"].Symbol.unique()
    data = []

    for symbol in symbols:
        description, exchange = get_info(symbol)
        current_quantity, unit_price, fees, cost_basis, pnl, total_buy, total_sell = (
            calculate_portfolio_from_trades(symbol)
        )

        data.append(
            [
                symbol,
                description,
                exchange,
                cost_basis,
                unit_price,
                current_quantity,
                total_buy,
                total_sell,
                pnl,
                fees,
            ]
        )

    portfolio = pd.DataFrame(
        data,
        columns=[
            "SYMBOL",
            "Description",
            "Exchange",
            "CostBasis",
            "UnitPrice",
            "Quantity",
            "Total Buy",
            "Total Sell",
            "PnL",
            "Fees",
        ],
    )
    portfolio = portfolio.sort_values(by="SYMBOL")

    total_pnl = portfolio["PnL"].sum()
    fees_paid = portfolio["Fees"].sum()
    equities_cost = portfolio["CostBasis"].sum()

    growth_portfolio = categorised_portfolio(portfolio, growth_symbols)
    emerging_portfolio = categorised_portfolio(portfolio, emerging_symbols)
    divident_portfolio = categorised_portfolio(portfolio, divident_symbols)
    exited_assets = portfolio[portfolio["Quantity"] == 0.0]

    # remove exited positions
    portfolio = portfolio[portfolio["Quantity"] != 0.0]

    return (
        portfolio,
        growth_portfolio,
        emerging_portfolio,
        divident_portfolio,
        exited_assets,
        np.round(total_pnl, 2),
        np.round(fees_paid, 2),
        np.round(equities_cost, 2),
    )


def get_ticker_info(symbol, tickers):
    tickers_price = tickers.price
    tickers_summary = tickers.summary_detail
    return (
        np.round(tickers_summary[symbol]["fiftyTwoWeekHigh"], 2),
        np.round(tickers_summary[symbol]["fiftyTwoWeekLow"], 2),
        np.round(tickers_summary[symbol]["dayHigh"], 2),
        np.round(tickers_summary[symbol]["dayLow"], 2),
        np.round(tickers_price[symbol]["regularMarketPrice"], 2),
    )


def get_logo(symbol):
    primary_url = (
        f"https://raw.githubusercontent.com/nvstly/icons/main/ticker_icons/{symbol}.png"
    )
    fallback_url = f"https://raw.githubusercontent.com/N0-man/n03an-folio/gh-pages/static/ticker_icons/{symbol}.png"  # use this for logo's not maintained by nvstly
    default_url = "https://raw.githubusercontent.com/N0-man/n03an-folio/main/logo.png"

    try:
        response = requests.head(primary_url)
        if response.status_code == 200:
            return primary_url
        else:
            return fallback_url
    except requests.RequestException:
        return default_url


def get_market_data(portfolio, total_r_pnl, principal_invested, available_cash):
    total_folio_value = 0
    total_u_pnl = 0

    symbols = portfolio["SYMBOL"].tolist()
    tickers = Ticker(symbols)

    for index, row in portfolio.iterrows():
        symbol = row["SYMBOL"]
        quantity = row["Quantity"]
        cost_basis = row["CostBasis"]

        fifty_two_high, fifty_two_low, day_high, day_low, current = get_ticker_info(
            symbol, tickers
        )
        folio_percent = np.round((cost_basis / principal_invested) * 100, 2)
        market_value = np.round((quantity * current), 2)
        u_pnl = np.round((market_value - cost_basis), 2)

        portfolio.at[index, "UPnL"] = u_pnl
        portfolio.at[index, "TPnL"] = np.round((u_pnl + row["PnL"]), 2)
        portfolio.at[index, "MarketValue"] = market_value
        portfolio.at[index, "Logo"] = get_logo(symbol)
        portfolio.at[index, "UnitPrice"] = row["UnitPrice"]
        portfolio.at[index, "Current"] = current
        portfolio.at[index, "52High"] = fifty_two_high
        portfolio.at[index, "52Low"] = fifty_two_low
        portfolio.at[index, "DayHigh"] = day_high
        portfolio.at[index, "DayLow"] = day_low

        total_folio_value += market_value
        total_u_pnl += u_pnl

    total_pnl = total_u_pnl + total_r_pnl
    total_folio_value_w_cash = total_folio_value + available_cash

    for index, row in portfolio.iterrows():
        folio_percent = np.round(
            (row["MarketValue"] / total_folio_value_w_cash) * 100, 2
        )
        portfolio.at[index, "FolioPercent"] = folio_percent

    return (
        portfolio,
        np.round(total_folio_value, 2),
        np.round(total_folio_value_w_cash, 2),
        np.round(total_u_pnl, 2),
        np.round(total_pnl, 2),
    )


def get_unit_cost(cost_basis, quantity):
    return np.round(cost_basis / quantity, 2)
