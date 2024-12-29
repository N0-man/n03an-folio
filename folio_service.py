import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pandas as pd
from cryptography.fernet import Fernet
import os
from io import StringIO

from datetime import datetime

data = "current_data"
folio_key = os.getenv("FOLIO_KEY")
f = Fernet(folio_key)

def decrypt(file_path):
    with open(file_path, "rb") as file:
        file_data = file.read()
    raw = f.decrypt(file_data)
    raw_str = raw.decode('utf-8')
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
    print(available_cash)
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


def total_profits(portfolio):
    total = portfolio["PnL"].sum()


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
    total_fees = portfolio["Fees"].sum()
    equities = portfolio["CostBasis"].sum()

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
        total_fees,
        equities,
    )


# def table(folio):
#     # table
#     html_table = folio.to_html(index=False)
#     display_html(html_table, raw=True)

# def render(cat_folio, title):
#     table(cat_folio)
