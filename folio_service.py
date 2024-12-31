import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pandas as pd
from cryptography.fernet import Fernet
import os
from io import StringIO
import yfinance as yf

from datetime import datetime

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
    return trades


trades = get_trades()


def calculate(symbol):
    orders = trades[
        (trades["Symbol"] == symbol) & (trades["LevelOfDetail"] == "EXECUTION")
    ]
    cost_basis = orders["CostBasis"].sum()
    fees = abs(orders["Taxes"].sum()) + abs(orders["IBCommission"].sum())
    pnl = orders[(orders["Buy/Sell"] == "SELL")]["FifoPnlRealized"].sum()

    return np.round(cost_basis, 2), np.round(pnl, 2), np.round(fees, 2)


def get_info(symbol):
    row = trades[
        (trades["Symbol"] == symbol) & (trades["LevelOfDetail"] == "EXECUTION")
    ].iloc[0]
    return row["Description"], row["ListingExchange"]


def buy_sell_trades(symbol):
    orders = trades[
        (trades["Symbol"] == symbol) & (trades["LevelOfDetail"] == "EXECUTION")
    ]
    total_sell = abs(orders[(orders["Buy/Sell"] == "SELL")]["Quantity"].sum())
    total_buy = orders[(orders["Buy/Sell"] == "BUY")]["Quantity"].sum()
    current_quantity = orders["Quantity"].sum()
    return (
        int(np.round(current_quantity, 0)),
        np.round(total_buy, 1),
        np.round(total_sell, 1),
    )


def squash(portfolio, new_symbol, old_symbol):
    # Select rows to merge
    new_asset = portfolio[portfolio["SYMBOL"] == new_symbol].iloc[0]
    old_asset = portfolio[portfolio["SYMBOL"] == old_symbol].iloc[0]

    # Sum numerical values
    squash_asset = (
        new_asset[["CostBasis", "Quantity", "Total Buy", "Total Sell", "PnL", "Fees"]]
        + old_asset[["CostBasis", "Quantity", "Total Buy", "Total Sell", "PnL", "Fees"]]
    )

    # Combine non-numerical values (take from new_symbol)
    squash_asset["SYMBOL"] = new_symbol
    squash_asset["Description"] = new_asset["Description"]
    squash_asset["Exchange"] = new_asset["Exchange"]

    # Drop the row of old and new asset reocrds. Concat the squashed asset
    portfolio = portfolio[~portfolio["SYMBOL"].isin([new_symbol, old_symbol])]
    portfolio = pd.concat([portfolio, pd.DataFrame([squash_asset])])

    return portfolio


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
    growth_symbols = ["VIR", "TSLA", "PLL", "MU", "IREN", "CLSK", "AMD"]
    emerging_symbols = ["BTDR", "IRD"]
    divident_symbols = ["MRK"]
    data = []

    for symbol in symbols:
        cost, pnl, fees = calculate(symbol)
        description, exchange = get_info(symbol)
        current_quantity, total_buy, total_sell = buy_sell_trades(symbol)
        data.append(
            [
                symbol,
                description,
                exchange,
                cost,
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
            "Quantity",
            "Total Buy",
            "Total Sell",
            "PnL",
            "Fees",
        ],
    )
    # Merge equities that has gone through an aquisition
    portfolio = squash(portfolio, "IRD", "OCUP")
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
        fees_paid,
        equities_cost,
    )


def get_ticker_info(symbol):
    data = yf.Ticker(symbol).info
    return (
        np.round(data["fiftyTwoWeekHigh"], 2),
        np.round(data["fiftyTwoWeekLow"], 2),
        np.round(data["dayHigh"], 2),
        np.round(data["dayLow"], 2),
        np.round(data["currentPrice"], 2),
    )


def get_ticker_logo(symbol):
    return f"https://n0-man.github.io/n03an-folio/static/ticker_icons/{symbol}.png"


def get_market_data(portfolio, total_r_pnl, principal_invested, available_cash):
    total_folio_value = 0
    total_u_pnl = 0
    for index, row in portfolio.iterrows():
        symbol = row["SYMBOL"]
        quantity = row["Quantity"]
        cost_basis = row["CostBasis"]
        fifty_two_high, fifty_two_low, day_high, day_low, current = get_ticker_info(
            symbol
        )
        folio_percent = np.round((cost_basis / principal_invested) * 100, 2)
        market_value = np.round((quantity * current), 2)
        u_pnl = np.round((market_value - cost_basis), 2)

        portfolio.at[index, "UPnL"] = u_pnl
        portfolio.at[index, "TPnL"] = np.round((u_pnl + row["PnL"]), 2)
        portfolio.at[index, "MarketValue"] = market_value
        portfolio.at[index, "Logo"] = get_ticker_logo(symbol)
        portfolio.at[index, "UnitCost"] = get_unit_cost(cost_basis, quantity)
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


# def table(folio):
#     # table
#     html_table = folio.to_html(index=False)
#     display_html(html_table, raw=True)

# def render(cat_folio, title):
#     table(cat_folio)
