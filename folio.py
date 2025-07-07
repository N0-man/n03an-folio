import gradio as gr
from folio_service import *
from style_components import *
import os
from ticker_info import *
import pandas as pd

import os

IB = "IB"
GROWTH = "Growth"
EMERGING = "Emerging"
DIVIDENT = "Divident"
MARKET_DATA_REFRESH = (
    3600  # refresh every 60 mins - total refresh time is 50-60 seconds
)
# TICKER_DATA_REFRESH = 2  # additional 2 seconds to allow market data refresh
passkey = os.getenv("PASSCODE")

(
    portfolio,
    growth_portfolio,
    emerging_portfolio,
    divident_portfolio,
    exited_assets,
    total_r_pnl,
    fees_paid,
    equities_cost,
) = get_folios()

available_cash, principal_invested, interest_recieved = get_cash_details()
# Compute portfolio with market data
portfolio, total_folio_value, total_folio_value_w_cash, total_u_pnl, total_pnl = (
    get_market_data(portfolio, total_r_pnl, principal_invested, available_cash)
)


def handle_passcode(passcode):
    if passcode == passkey:
        return (
            gr.Textbox(visible=False),
            gr.Button(visible=False),
            gr.Tabs(visible=True),
        )
    else:
        raise gr.Error(
            "That looks like a fart 💨. Are you who you are?",
            duration=10,
        )
        # return gr.Textbox(visible=True), gr.Button(visible=True), gr.Tabs(visible=False)


def sync_market_data():
    global portfolio, total_folio_value, total_folio_value_w_cash, total_u_pnl, total_pnl
    portfolio, total_folio_value, total_folio_value_w_cash, total_u_pnl, total_pnl = (
        get_market_data(portfolio, total_r_pnl, principal_invested, available_cash)
    )


def render_data():
    sync_market_data()
    return (
        folio_overview(
            total_folio_value_w_cash,
            principal_invested,
            total_folio_value,
            available_cash,
            equities_cost,
            total_r_pnl,
            total_u_pnl,
            total_pnl,
            interest_recieved,
            fees_paid,
        )
        + folio_ticker_table(portfolio)
        + ticker_cards(portfolio)
        + folio_exited_assets(exited_assets)
    )


def render_ticker_tab(ticker):
    return ticker_cards(pd.DataFrame([ticker]))


# def render_ticker_info(symbol):
#     with open(f"static/{symbol}.md", "rb") as file:
#         raw = file.read()
#     raw_str = raw.decode("utf-8")
#     return raw_str


# def render_ticker_info(symbol):
#     file_path = f"static/ticker_info/{symbol}.md"
#     try:
#         logo = f"![{symbol}](https://n0-man.github.io/n03an-folio/static/ticker_icons/{symbol}.png)"
#         with open(file_path, "rb") as file:
#             raw_str = file.read()
#     except FileNotFoundError:
#         logo = f"![{symbol}](https://raw.githubusercontent.com/nvstly/icons/main/ticker_icons/{symbol}.png)"
#         raw_str = f"## {symbol}"
#         with open(file_path, "w", encoding="utf-8") as file:
#             file.write(raw_str)
#     return logo + "<br><br>" + raw_str


def render_ticker_info(symbol):
    file_path = f"static/ticker_info/{symbol}.md"
    logo = f"![{symbol}]({get_logo(symbol)})"

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
    except FileNotFoundError:
        content = f"## {symbol}"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)

    # Return formatted markdown
    return f"\n{logo}\n\n{content}"


def main():
    theme = gr.themes.Soft(
        primary_hue="rose",
        secondary_hue="yellow",
        neutral_hue="sky",
        text_size="lg",
        font=[gr.themes.GoogleFont("Inter"), "sans-serif"],
    )

    with gr.Blocks(theme=theme, fill_height=True) as folio:
        gr.HTML(load_all_css)
        with gr.Row(equal_height=False) as folio_header:
            with gr.Column(scale=1, min_width=100):
                gr.Image(
                    "logo.png",
                    height=100,
                    width=100,
                    show_label=False,
                    show_download_button=False,
                    container=False,
                    show_fullscreen_button=False,
                )
            with gr.Column(scale=4, min_width=200):
                gr.Markdown(
                    """
                # n03an's folio
                #### رَبَّنَا أَفْرِغْ عَلَيْنَا صَبْرًا وَتَوَفَّنَا مُسْلِمِينَ
                """
                )

        with gr.Tabs(visible=False, selected=IB) as folio_tabs:
            with gr.Tab(IB, id=IB, elem_id="main-folio-tab"):
                gr.HTML(value=render_data, every=MARKET_DATA_REFRESH, padding=False)
            for _, row in portfolio.iterrows():
                symbol = row["SYMBOL"]
                with gr.Tab(symbol):
                    # gr.HTML(
                    #     value=render_ticker_tab,
                    #     every=TICKER_DATA_REFRESH,
                    #     padding=False,
                    # )
                    gr.Markdown(
                        f"""
                        {render_ticker_info(symbol)}
                        """
                    )

        with gr.Row():
            with gr.Column(scale=2):
                passcode = gr.Textbox(
                    placeholder="enter your passcode", show_label=False, type="password"
                )
            with gr.Column():
                submit = gr.Button("Submit", interactive=True)

        submit.click(
            fn=handle_passcode,
            inputs=[passcode],
            outputs=[passcode, submit, folio_tabs],
        )

    folio.launch()


if __name__ == "__main__":
    main()
