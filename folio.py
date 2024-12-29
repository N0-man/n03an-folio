import gradio as gr
from folio_service import *
from style_components import *
import os

IB = "IB"
GROWTH = "Growth"
EMERGING = "Emerging"
DIVIDENT = "Divident"
passkey = os.getenv("PASSCODE")


def handle_passcode(passcode):
    if passcode == passkey:
        return gr.Textbox(visible=False), gr.Button(visible=False), gr.Tabs(visible=True)
    else:
        raise gr.Error(
                "That looks like a fart 💨. Are you who you are?",
                duration=10,
            )
        # return gr.Textbox(visible=True), gr.Button(visible=True), gr.Tabs(visible=False)

def main():
    theme = gr.themes.Soft(
        primary_hue="rose",
        secondary_hue="yellow",
        neutral_hue="sky",
        text_size="lg",
    )

    (
        portfolio,
        growth_portfolio,
        emerging_portfolio,
        divident_portfolio,
        exited_assets,
        total_pnl,
        total_fees,
        equities,
    ) = get_folios()

    available_cash, self_contribution, interest_recieved = get_cash_details()

    with gr.Blocks(theme=theme, fill_height=True) as folio:
        gr.HTML(load_all_css)
        with gr.Row(equal_height=False):
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
                gr.HTML(
                    folio_overview(
                        self_contribution,
                        "115200.32",
                        available_cash,
                        equities,
                        total_pnl,
                        total_pnl + 1000,
                        interest_recieved,
                        total_fees,
                    ),
                    padding=False,
                )
                gr.HTML(stock_cards(portfolio, self_contribution), padding=False)

            with gr.Tab(GROWTH):
                gr.Markdown(
                """
                # n03an's folio
                """)
            with gr.Tab(EMERGING):
                gr.Label("Hello World", elem_classes="dancing")
            with gr.Tab(DIVIDENT):
                gr.Markdown(
                """
                # n03an's folio
                """)

        with gr.Row():
            with gr.Column(scale=2):
                passcode = gr.Textbox(
                    placeholder="enter your passcode",
                    show_label = False,
                    type="password"
                )
            with gr.Column():
                submit = gr.Button("Submit", interactive=True)

        submit.click(fn = handle_passcode, inputs=[passcode], outputs=[passcode, submit, folio_tabs])

    folio.launch()


if __name__ == "__main__":
    main()
