import numpy as np
from folio_service import *

load_all_css = """
<style>

body {
  background-color: #10212e !important; 
}

section{
  width: 100%;
  -webkit-box-sizing: border-box;
          box-sizing: border-box;
}
.card{
  position: relative;
  height: auto;
  background: linear-gradient(-45deg,#fe0847,#feae3f);
  border-radius: 15px !important;
  border: unset !important;
  margin: 15px !important;
  padding: 40px 20px;
  -webkit-box-shadow: 0 10px 15px rgba(0,0,0,.1) ;
          box-shadow: 0 10px 15px rgba(0,0,0,.1) ;
-webkit-transition: .5s;
}


.col-sm-12 {
    padding-right: 0px !important;;
    padding-left: 0px !important;;
    padding-bottom: 20px;
}

.col-sm-12:nth-child(n) .card,
.col-sm-12:nth-child(n) .card .title .fa{
  background: linear-gradient(-45deg,#0f3a5d, #153044);

}

.col-md-12 {
    padding-right: 0px !important;;
    padding-left: 0px !important;;
    padding-bottom: 20px;
}

.col-md-12:nth-child(n) .card,
.col-md-12:nth-child(n) .card .title .fa{
  background: linear-gradient(-45deg,#0f3a5d, #153044);

}

.title .fa{
  color:#fff;
  font-size: 60px;
  width: 100px;
  height: 100px;
  border-radius:  50%;
  text-align: center;
  line-height: 100px;
  -webkit-box-shadow: 0 10px 10px rgba(0,0,0,.1) ;
          box-shadow: 0 10px 10px rgba(0,0,0,.1) ;

}
.title h2 {
  position: relative;
  margin: 20px  0 0;
  padding: 0;
  color: #fff;
  font-size: 28px;
 z-index: 2;
}

.price {
    color: #fff;
}

.card a {
  position: relative;
  z-index: 2;
  background: #fff;
  color : black;
  width: 150px;
  height: 40px;
  line-height: 40px;
  border-radius: 40px;
  display: block;
  text-align: center;
  margin: 20px auto 0 ;
  font-size: 16px;
  cursor: pointer;
  -webkit-box-shadow: 0 5px 10px rgba(0, 0, 0, .1);
          box-shadow: 0 5px 10px rgba(0, 0, 0, .1);

}

.avatar {
    width: 50px; /* Adjust size as needed */
    height: 50px;
    border-radius: 50%; /* Makes it circular */
    object-fit: cover; /* Ensures the image fits the circle */
    border: 2px solid #ddd; 
  }

.btn-dark {
  color: #fff !important;
  background-color: #212529 !important;
  border-color: #212529 !important;
}

.table-dark-border {
      border: 2px solid #343A40 !important;
    }
    .table-dark-border th,
    .table-dark-border td {
      border: 1px solid #343A40 !important; 
    }

.table-main td:first-child {
      background-color: #065984;
    }
.table-main td {
      border: 2px solid #065984 !important;
    }
  
.table-ticker td {
      border: 2px solid #065984 !important;
    }

.container-fluid {
    padding: 0 !important;
}

.container {
    padding: 0 !important;
}

#main-folio-tab {
    height: 100%;
    width: 100%;
    overflow-x:hidden !important;
    border: unset;
}

.html-container {
    overflow: hidden;
}

:root { 
  font-family: 'Inter', sans-serif !important; 
}

:root .dark {
  --background-fill-primary: #10212e !important; 
}

@supports (font-variation-settings: normal) {
  :root { font-family: 'Inter var', sans-serif !important; }
}

.icon-button-wrapper {
  visibility: hidden !important;
}

</style>
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.2/css/all.min.css" rel="stylesheet" >
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
<link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css" rel="stylesheet">


<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap" rel="stylesheet">

"""


def folio_overview(
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
):
    return f"""
    <small class="text-warning mb-1 mt-4 fw-bold">Portfolio Overview</small>
    <div class="table-responsive mb-4">
        <table class="table text-center table-main">
          <tbody>
            <tr>
              <td class="px-2"><i class="fa-solid fa-piggy-bank me-2 fw-bold" style="color: #ea8dad !important;"></i></i>Total Value</td>
              <td class="px-2">
                <span class="p-1 px2 w-100 rounded text-dark d-inline-block mb-2 fw-bold" style="background: #13ff01 !important;"><sup class="text-dark">$</sup>{total_folio_value_w_cash}</span>
              </td>
            </tr>

            <tr>
              <td class="px-2"><i class="fa-solid fa-cart-shopping me-2" style="color: #8aebfe !important;"></i>Principal Invested</td>
              <td class="px-2">
                <span class="bg-info p-1 px2 w-100 rounded text-dark d-inline-block mb-2"><sup class="text-dark">$</sup>{principal_invested}</span>
              </td>
            </tr>
            
            <tr>
              <td class="px-2"><i class="fa-solid fa-chart-line me-2" style="color: #8aebfe !important;"></i>Equities Value</td>
              <td class="px-2">
                <span class="bg-info p-1 px2 w-100 rounded text-dark d-inline-block mb-2"><sup class="text-dark">$</sup>{total_folio_value}</span>
              </td>
            </tr>

            <tr>
              <td class="px-2"><i class="fa-solid fa-house-flag me-2" style="color: #8aebfe !important;"></i>Equities Cost</td>
              <td class="px-2">
                <span class="bg-info p-1 px2 w-100 rounded text-dark d-inline-block mb-2"><sup class="text-dark">$</sup>{equities_cost}</span>
              </td>
            </tr>
            
            <tr>
              <td class="px-2"><i class="fa-solid fa-money-check-dollar me-2" style="color: #4fcb41 !important;"></i>Available Cash</td>
              <td class="px-2">
                <span class="bg-success p-1 px2 w-100 rounded text-white d-inline-block mb-2"><sup>$</sup>{available_cash}</span>
              </td>
            </tr>
            
            <tr>
              <td class="px-2"><i class="fa-solid fa-arrow-trend-up me-2" style="color: #4fcb41 !important;"></i>Realised PnL</td>
              <td class="px-2">
                <span class="bg-success p-1 px2 w-100 rounded text-white d-inline-block mb-2"><sup class="text-white">$</sup>{total_r_pnl}</span>
              </td>
            </tr>
            <tr>
              <td class="px-2"><i class="fa-solid fa-face-surprise me-2" style="color: #e1d400 !important;"></i>Unrealised PnL</td>
              <td class="px-2">
                <span class="bg-warning p-1 px2 w-100 rounded text-dark d-inline-block mb-2"><sup class="text-dark">$</sup>{total_u_pnl}</span>
              </td>
            </tr>

            <tr>
              <td class="px-2"><i class="fa-solid fa-money-bill-trend-up me-2" style="color: #e1d400 !important;"></i>Total PnL</td>
              <td class="px-2">
                <span class="bg-warning p-1 px2 w-100 rounded text-dark d-inline-block mb-2"><sup class="text-dark">$</sup>{total_pnl}</span>
              </td>
            </tr>
            
            <tr>
              <td class="px-2"><i class="fa-regular fa-trash-can me-2" style="color: #ff5353 !important;"></i>Interest Gained</td>
              <td class="px-2">
                <span class="bg-danger p-1 px2 w-100 rounded text-white d-inline-block mb-2"><sup class="text-white">$</sup>{interest_recieved}</span>
              </td>
            </tr>
            
            <tr>
              <td class="px-2"><i class="fa-solid fa-poo me-2" style="color: #000000 !important;"></i>Fees Paid</td>
              <td class="px-2">
                <span class="bg-dark p-1 px2 w-100 rounded text-white d-inline-block mb-2"><sup class="text-white">$</sup>{fees_paid}</span>
              </td>
            </tr>
            
          </tbody>
        </table>
    </div>
"""


def folio_ticker_table(portfolio):
    folio_ticker_table_html = """
    <small class="text-warning mb-1 mt-4 fw-bold">Portfolio Tracker</small>
    <div class="table-responsive mb-4">
      <table class="table text-center table-ticker">
          <thead class="fw-bold text-center">
              <tr>
                  <td class="bg-dark text-white text-center">
                      <i class="fa-solid fa-circle-dollar-to-slot fa-2x"></i>
                  </td>
                  <td class="bg-dark text-white text-center px-2">TODAY</td>
                  <td class="bg-dark text-white text-center px-2">

                    <div class="d-flex flex-column flex-md-row align-items-center justify-content-center text-center">
                      <span class="text-white d-inline-block mx-md-2">
                          MY FOLIO
                      </span>
                      <div class="d-flex flex-row align-items-center justify-content-center">
                          <span class="d-inline-block fw-normal" style="color: #13ff01 !important; font-size: 12px !important;">
                              Count
                          </span>
                          <span class="d-inline-block text-warning fw-normal" style="font-size: 12px !important;">
                              (%)
                          </span>
                          <span class="d-inline-block text-white fw-normal" style="font-size: 12px !important;">
                              Price
                          </span>
                      </div>
                    </div>
                    
                    
                  </td>
                  <td class="bg-dark text-white text-center px-2">52W H/L</td>
              </tr>
          </thead>  
          <tbody>
    """

    for index, row in portfolio.iterrows():
        ticker_row = create_ticker_table_row(
            row["SYMBOL"],
            row["UnitPrice"],
            row["Current"],
            row["52High"],
            row["52Low"],
            row["Quantity"],
            row["FolioPercent"],
        )
        folio_ticker_table_html += ticker_row

    folio_ticker_table_html += """
          </tbody>
        </table>
      </div>
    """

    return folio_ticker_table_html


def create_ticker_table_row(
    symbol, unit_cost, current_price, fiftytwohigh, fiftytwolow, quantity, folio_percent
):
    return f"""
  <tr>
      <!-- First Column -->
      <td class="text-dark py-md-4 fw-bold text-center">
          <div class="d-flex flex-column flex-md-row align-items-center justify-content-center">
              <img src="{get_logo(symbol)}" width="20" class="mb-2 mb-md-0 me-0 me-md-3">
              <span>{symbol}</span>
          </div>
      </td>
      
      <td class="px-1 pb-2 py-md-4 text-center">
          <div class="d-flex flex-column flex-md-row align-items-center justify-content-center">
              <i class="fa-solid {arrow(current_price, unit_cost)} text-{color(current_price, unit_cost)} fa-lg mb-1 mb-md-0 me-0 me-md-1 mt-2 mt-md-0"></i>
              <span class="text-white d-inline-block mt-2">
                  <sup>$</sup>{current_price}
              </span>
          </div>
      </td>
      <td class="px-1 pb-1 py-md-4 text-center">
        <div class="d-flex flex-column flex-md-row align-items-center justify-content-center text-center">
          <div class="d-flex flex-row align-items-center justify-content-center mb-2 mb-md-0 me-0 me-md-2">
              <span class="d-inline-block me-2" style="color: #13ff01 !important; font-size: 14px !important;">
                  {quantity}
              </span>
              <span class="d-inline-block text-warning" style="font-size: 14px !important;">
                  ({folio_percent}%)
              </span>
          </div>
          <span class="text-white d-inline-block">
              <sup>$</sup>{unit_cost}
          </span>
        </div>
      </td>
      
      <td class="px-1 py-1 py-md-4 text-center">
          <div class="d-flex flex-column flex-md-row align-items-center justify-content-center h-100">
              <small class="bg-success p-1 px-2 rounded text-white d-inline-block mb-2 mb-md-0 me-0 me-md-2">
                  <sup class="text-white">$</sup>{fiftytwohigh}
              </small>
              <small class="bg-danger p-1 px-2 rounded text-white d-inline-block">
                  <sup class="text-white">$</sup>{fiftytwolow}
              </small>
          </div>
      </td>

  </tr>
"""


def create_exited_asset_table_row(symbol, buy, description, pnl):
    return f"""
  <tr>
      <!-- First Column -->
      <td class="text-dark py-md-4 fw-bold text-center">
          <div class="d-flex flex-column flex-md-row align-items-center justify-content-center">
              <img src="{get_logo(symbol)}" width="20" class="mb-2 mb-md-0 me-0 me-md-3">
              <span>{symbol}</span>
          </div>
      </td>
      
      <td class="px-1 pb-2 py-md-4 text-center">
          <div class="d-flex flex-column flex-md-row align-items-center justify-content-center">
              <span class="text-white d-inline-block mt-2">
                  {description}
              </span>
          </div>
      </td>
      <td class="px-1 pb-2 py-md-4 text-center">
          <div class="d-flex flex-column flex-md-row align-items-center justify-content-center">
              <span>{buy}</span>
          </div>
      </td>
      
      <td class="px-1 pb-2 py-md-4 text-center">
          <div class="d-flex flex-column flex-md-row align-items-center justify-content-center">
              <span class="text-white rounded mt-2 d-inline-block px-2 py-1 {'bg-danger' if pnl < 0 else 'bg-success'}">
                  <sup>$</sup>{pnl}
              </span>
          </div>
      </td>

  </tr>
"""


def folio_exited_assets(exited_assets):
    exited_assets_table_html = """
    <hr style="border-top: 4px #065984; margin: 20px 0;">
    <small class="text-warning mb-1 mt-4 fw-bold">Exited Assets</small>
    <div class="table-responsive mb-4">
      <table class="table text-center table-ticker">
          <thead class="fw-bold text-center">
              <tr>
                  <td class="bg-dark text-white text-center">
                      <i class="fa-solid fa-circle-dollar-to-slot fa-2x"></i>
                  </td>
                  <td class="bg-dark text-white text-center px-2">Description</td>
                  <td class="bg-dark text-white text-center px-2">Trade Quantity</td>
                  <td class="bg-dark text-white text-center px-2">PnL</td>
              </tr>
          </thead>  
          <tbody>
    """

    for index, row in exited_assets.iterrows():
        ticker_row = create_exited_asset_table_row(
            row["SYMBOL"],
            row["Total Buy"],
            row["Description"],
            row["PnL"],
        )
        exited_assets_table_html += ticker_row

    exited_assets_table_html += """
          </tbody>
        </table>
      </div>
    """

    return exited_assets_table_html


def color(price_a, price_b):
    return np.where(price_a > price_b, "success", "danger")


def caret(price_a, price_b):
    return np.where(price_a > price_b, "fa-caret-up", "fa-caret-down")


def arrow(price_a, price_b):
    return np.where(price_a > price_b, "fa-arrow-trend-up", "fa-arrow-trend-down")


def red_green_bg(price_a, price_b):
    return np.where(
        price_a > price_b,
        f"""
            <span class="bg-success p-1 w-100 rounded text-white d-inline-block mb-2"><sup>$</sup>{price_a}</span>
          """,
        f"""
            <span class="bg-danger p-1 w-100 rounded text-white d-inline-block mb-2"><sup>$</sup>{price_a}</span>
          """,
    )


def red_yellow_bg(price_a, price_b):
    return np.where(
        price_a > price_b,
        f"""
            <span class="bg-warning p-1 w-100 rounded text-dark d-inline-block mb-2"><sup class="text-dark">$</sup>{price_a}</span>
          """,
        f"""
            <span class="bg-danger p-1 w-100 rounded text-white d-inline-block mb-2"><sup>$</sup>{price_a}</span>
          """,
    )


def create_ticker_card(ticker):
    unit_price = ticker["UnitPrice"]
    folio_percent = ticker["FolioPercent"]
    symbol = ticker["SYMBOL"]
    description = ticker["Description"]
    exchange = ticker["Exchange"]
    quantity = ticker["Quantity"]
    cost_basis = ticker["CostBasis"]
    r_pnl = ticker["PnL"]
    u_pnl = ticker["UPnL"]
    t_pnl = ticker["TPnL"]

    fifty_two_high = ticker["52High"]
    fifty_two_low = ticker["52Low"]
    day_high = ticker["DayHigh"]
    day_low = ticker["DayLow"]
    current = ticker["Current"]
    market_value = ticker["MarketValue"]

    ticker_logo = ticker["Logo"]

    ticker_card_html = f"""
    <div class="col-sm-12 col-md-12">
        <div class="card text-center p-3">
            <div class="d-flex align-items-center justify-content-center mb-3">
                <div class="col-4 d-flex align-items-start">  
                  <span class="text-white d-inline-block mx-1">
                    <i class="fa-solid {caret(current, unit_price)} text-{color(current, unit_price)} fa-lg"></i>
                    <sup> $</sup>{current}
                  </span>
                </div>
                <div class="col-8">
                    <span class="d-inline-block mb-2" style="color: #13ff01 !important; font-size: 18px !important;">
                      {quantity}  Owned
                    </span>
                </div>
            </div>

            <div class="d-flex align-items-center justify-content-center mb-5">
                <div class="col-4">                  
                  <img src="{ticker_logo}" width="100" class="me-3">
                </div>
                <div class="col-8">
                    <h2 class="mb-0 mt-1">{symbol}</h3>
                    <p class="m-0 px-2">{description}</p>
                    <small class="text-warning mb-1 fw-bold">{exchange}</small>
                </div>
            </div>
            <div class="d-flex align-items-center mb-3">
                <span class="text-warning mx-2 fw-bold">TIME</span>
                <span class="text-warning mx-2 fw-bold px-1">|</span>
                <span class="text-white mx-2 fw-bold">LOW</span>
                <span class="text-warning mx-2 fw-bold px-1">|</span>
                <span class="text-white mx-2 fw-bold">HIGH</span>
            </div>
            <div class="d-flex align-items-center mb-3">
                <span class="text-warning mx-2">52W</span>
                <span class="text-white d-inline-block mx-1 px-2">
                  <i class="fa-solid {arrow(fifty_two_low, current)} text-{color(fifty_two_low, current)} fa-lg"></i>
                  <sup> $</sup>{fifty_two_low}
                </span>
                <span class="text-white d-inline-block mx-1 px-2">
                  <i class="fa-solid {arrow(fifty_two_high, current)} text-{color(fifty_two_high, current)} fa-lg"></i>
                  <sup> $</sup>{fifty_two_high}
                </span>
            </div>
            <div class="d-flex align-items-center mb-3">
                <span class="text-warning mx-2">DAY</span>
                <span class="text-white d-inline-block mx-1 px-2">
                  <i class="fa-solid {arrow(day_low, current)} text-{color(day_low, current)} fa-lg"></i>
                  <sup> $</sup>{day_low}
                </span>
                <span class="text-white d-inline-block mx-1 px-2">
                  <i class="fa-solid {arrow(day_high, current)} text-{color(day_high, current)} fa-lg"></i>
                  <sup> $</sup>{day_high}
                </span>

            </div>
            <div class="table-responsive">
                <table class="table table-striped table-hover table-dark-border">
                  <tbody>
                    <tr>
                        <td class="table-dark">Folio %</td>
                        <td class="text-light fw-bold">
                           <span class="bg-info p-1 w-100 rounded text-dark d-inline-block mb-2" style="background: #13ff01 !important;"><sup class="text-dark">%</sup>{folio_percent}</span>
                        </td>   
                    </tr>
                    <tr>
                        <td class="table-dark">Market Value</td>
                        <td class="text-light fw-bold">{red_green_bg(market_value, cost_basis)}</td>
                    </tr>

                    <tr>
                        <td class="table-dark">Cost Basis</td>
                        <td class="text-light fw-bold">
                           <span class="bg-info p-1 w-100 rounded text-dark d-inline-block mb-2"><sup class="text-dark">$</sup>{cost_basis}</span>
                        </td>                       
                    </tr>
                    
                    <tr>
                        <td class="table-dark">Average Price</td>
                        <td class="text-light fw-bold">
                           <span class="bg-white p-1 w-100 rounded text-dark d-inline-block mb-2"><sup class="text-dark">$</sup>{unit_price}</span>
                        </td>                       
                    </tr>
                    
                    
                    <tr>
                        <td class="table-dark">Realised PnL</td>
                        <td class="text-light fw-bold">
                           {red_green_bg(r_pnl,0)}
                        </td> 
                    </tr>
                    
                    <tr>
                        <td class="table-dark">Unrealised PnL</td>
                        <td class="text-light fw-bold">
                          {red_yellow_bg(u_pnl,0)}
                        </td> 
                    </tr>
                      
                    <tr>
                        <td class="table-dark">Total PnL</td>
                        <td class="text-light fw-bold">
                           {red_yellow_bg(t_pnl,0)}
                        </td> 
                    </tr>
                  </tbody>
                </table>
            </div>
        </div>
    </div>
    """
    return ticker_card_html


def ticker_cards(portfolio):
    html = """
    <small class="text-warning mb-1 mt-2 fw-bold">Individual Stock Cards</small>
    <section>
      <div class="container-fluid">
        <div class="container">
          <div class="row">
    """

    for index, row in portfolio.iterrows():
        card_html = create_ticker_card(row)
        html += card_html

    html += """
          </div>
        </div>
      </div>
    </section>
    """

    return html
