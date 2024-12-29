import numpy as np

load_all_css = """
<style>

body{

}
section{
  width: 100%;
  -webkit-box-sizing: border-box;
          box-sizing: border-box;
          padding: 40px 0;
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
  background: linear-gradient(-45deg,#049fd8,#343839);

}

.col-md-12 {
    padding-right: 0px !important;;
    padding-left: 0px !important;;
    padding-bottom: 20px;
}

.col-md-12:nth-child(n) .card,
.col-md-12:nth-child(n) .card .title .fa{
  background: linear-gradient(-45deg,#049fd8,#343839);

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
.price,.option{
  position: relative;
  z-index: 2;
}
.price {
    color: #fff;
}
.option ul {
  margin: 0;
  padding: 0;

}
.option ul li {
    margin: 0 0 10px;
    padding: 0;
    list-style: none;
    color: #fff;
    font-size: 16px;
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
    border: 2px solid #ddd; /* Optional: adds a border */
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

:root { font-family: 'Inter', sans-serif; }
@supports (font-variation-settings: normal) {
  :root { font-family: 'Inter var', sans-serif; }
}

</style>
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.2/css/all.min.css" rel="stylesheet" >
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
<link rel="preconnect" href="https://rsms.me/">
<link rel="stylesheet" href="https://rsms.me/inter/inter.css">

"""


def folio_overview(
    self_contribution, market_value, cash, equities, r_pnl, u_pnl, interest, fees
):
    return f"""
    <div class="table-responsive">
        <table class="table text-center table-main">
          <tbody>
            <tr>
              <td>Self Contribution</td>
              <td>
                <i class="fa-solid fa-cart-shopping me-2"></i>
                <p class="badge rounded-pill bg-info m-0 text-dark text-center"><sup class="text-dark">$</sup>{self_contribution}</p>
              </td>
                
            </tr>
            
            <tr>
              <td>Market Value</td>
              <td>
                <i class="fa-solid fa-earth-americas me-2"></i>
                <p class="badge rounded-pill bg-warning m-0 text-dark text-center"><sup class="text-dark">$</sup>{market_value}</p>
              </td>
            </tr>
            
            <tr>
              <td>Available Cash</td>
              <td>
                <i class="fa-solid fa-hand-holding-dollar me-2"></i>
                <p class="badge rounded-pill bg-success m-0 text-light text-center"><sup class="text-light">$</sup>{cash}</p>
              </td>
            </tr>
            
            <tr>
              <td>Equities</td>
              <td>
                <i class="fa-solid fa-city me-2"></i>
                <p class="badge rounded-pill bg-info m-0 text-dark text-center"><sup class="text-dark">$</sup>{equities}</p>
              </td>
            </tr>
            
            <tr>
              <td>Realised PnL</td>
              <td>
                <i class="fa-solid fa-thumbs-up me-2"></i>
                <p class="badge rounded-pill bg-success m-0 text-light text-center"><sup class="text-light">$</sup>{r_pnl}</p>
              </td>
            </tr>
            <tr>
              <td>Unrealised PnL</td>
              <td>
                <i class="fa-solid fa-face-surprise me-2"></i>
                <p class="badge rounded-pill bg-warning m-0 text-dark text-center"><sup class="text-dark">$</sup>{u_pnl}</p>
              </td>
            </tr>
            
            <tr>
              <td>Interest</td>
              <td>
                <i class="fa-regular fa-trash-can me-2"></i>
                <p class="badge rounded-pill bg-danger m-0 text-light text-center"><sup class="text-light">$</sup>{interest}</p>
              </td>
            </tr>
            
            <tr>
              <td>Fees</td>
              <td>
                <i class="fa-solid fa-poo me-2"></i>
                <p class="badge rounded-pill bg-secondary m-0 text-light text-center"><sup class="text-light">$</sup>{fees}</p>
              </td>
            </tr>
            
          </tbody>
        </table>
    </div>
"""


def create_stock_card(
    symbol, description, exchange, quantity, cost_basis, r_pnl, total_cost_basis
):
    try:
        unit_cost = np.round(cost_basis / quantity, 2)
        folio_percent = np.round((cost_basis / total_cost_basis) * 100, 2)
    except ZeroDivisionError:
        unit_cost = 0
        folio_percent = 0

    ticker_icon = f"https://n0-man.github.io/n03an-folio/static/ticker_icons/{symbol}.png"
    card_html = f"""
    <div class="col-sm-12 col-md-12">
        <div class="card text-center p-3">
            <div class="d-flex align-items-center justify-content-center mb-3">
                <div class="col-4 align-items-center text-center">
                  <img src="{ticker_icon}" width="100" class="me-3">
                </div>
                <div class="col-8">
                    <span class="bg-dark p-1 px-4 rounded text-white d-inline-block mb-2">{quantity}  Owned</span>
                    <h2 class="mb-0 mt-1">{symbol}</h3>
                    <p class="m-0">{description}</p>
                    <small class="text-warning mb-1">{exchange}</small>
                    <div class="price mb-2 mt-2">
                        <h4 class="badge rounded-pill bg-danger m-0 w-50 text-center"><sup>$</sup>450.45</h4>
                    </div>
                </div>
            </div>

            <div class="table-responsive">
                <table class="table table-striped table-hover table-dark-border">
                  <tbody>
                    <tr>
                        <td class="table-dark">Market Value</td>
                        <td class="text-light fw-bold"><sup>$</sup>10,900.00</td>
                    </tr>

                    <tr>
                        <td class="table-dark">Cost Basis</td>
                        <td class="text-light fw-bold"><sup>$</sup>{cost_basis}</td>
                    </tr>
                    
                    <tr>
                        <td class="table-dark">Average Price</td>
                        <td class="text-light fw-bold"><sup>$</sup>{unit_cost}</td>
                    </tr>
                    
                    <tr>
                        <td class="table-dark">Folio %</td>
                        <td class="text-light fw-bold">{folio_percent}<sup>%</sup></td>
                    </tr>
                    
                    <tr>
                        <td class="table-dark">Realised PnL</td>
                        <td class="text-light fw-bold"><sup>$</sup>{r_pnl}</td>
                    </tr>
                    
                    <tr>
                        <td class="table-dark">Unrealised PnL</td>
                        <td class="text-light fw-bold"><sup>$</sup>10,900.00</td>
                    </tr>
                      
                    <tr>
                        <td class="table-dark">Total PnL</td>
                        <td class="text-light fw-bold"><sup>$</sup>10,900.00</td>
                    </tr>
                  </tbody>
                </table>
            </div>

            <button class="btn btn-dark text-light border-dark m-3">
                <i class="fa-solid fa-binoculars"></i> {symbol} Details
            </button>
        </div>
    </div>
    """
    return card_html


def stock_cards(folio, total_cost_basis):
    """
    Generates HTML cards for each stock in the folio DataFrame.
    """
    cards_html = """
    <section>
      <div class="container-fluid">
        <div class="container">
          <div class="row">
    """

    for index, row in folio.iterrows():
        card_html = create_stock_card(
            row["SYMBOL"],
            row["Description"],
            row["Exchange"],
            row["Quantity"],
            row["CostBasis"],
            row["PnL"],
            total_cost_basis,
        )
        cards_html += card_html

    cards_html += """
          </div>
        </div>
      </div>
    </section>
    """

    return cards_html


data_cards = """
<section>
  <div class="container-fluid">
    <div class="container">
      <div class="row">
        <div class="col-sm-12 col-md-12">
            <div class="card text-center p-3">
                <div class="d-flex align-items-center justify-content-center mb-3">
                    <img src="https://assets.parqet.com/logos/symbol/TSLA?format=png" width="100" class="rounded-circle me-3">
                    <div>
                        <span class="bg-dark p-1 px-4 rounded text-white d-inline-block mb-2">71 Owned</span>
                        <h2 class="m-0">TSLA</h2>
                        <p class="m-0">Tesla Inc Company Name</p>
                    </div>
                </div>

                <div class="price mb-2">
                    <h4 class="badge rounded-pill bg-danger m-0 w-50 text-center"><sup>$</sup>450.45</h4>
                </div>

                <div class="table-responsive">
                    <table class="table table-striped table-hover table-dark-border">
                        <tbody>
                            <tr>
                                <td class="table-dark">Market Value</td>
                                <td>$10,900.00</td>
                            </tr>

                            <tr>
                                <td class="table-dark">Cost Basis</td>
                                <td>$10,900.00</td>
                            </tr>
                            
                            <tr>
                                <td class="table-dark">Average Price</td>
                                <td>$10,900.00</td>
                            </tr>
                            
                            <tr>
                                <td class="table-dark">Folio %</td>
                                <td>$10,900.00</td>
                            </tr>
                            
                            <tr>
                                <td class="table-dark">Realised PnL</td>
                                <td>$10,900.00</td>
                            </tr>
                            
                            <tr>
                                <td class="table-dark">Unrealised PnL</td>
                                <td>$10,900.00</td>
                            </tr>
                             
                            <tr>
                                <td class="table-dark">Total PnL</td>
                                <td>$10,900.00</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <button class="btn btn-dark text-light border-dark m-3">
                    <i class="fa-solid fa-binoculars"></i> Details
                </button>
            </div>
        </div>

        <!-- END Col one -->
        <div class="col-sm-12 col-md-12">
            <div class="card text-center p-3">
                <div class="d-flex align-items-center justify-content-center mb-3">
                    <img src="https://assets.parqet.com/logos/symbol/TSLA?format=png" width="100" class="rounded-circle me-3">
                    <div>
                        <span class="bg-dark p-1 px-4 rounded text-white d-inline-block mb-2">71 Owned</span>
                        <h2 class="m-0">TSLA</h2>
                        <p class="m-0">Tesla Inc Company Name</p>
                    </div>
                </div>

                <div class="price mb-2">
                    <h4 class="badge rounded-pill bg-danger m-0 w-50 text-center"><sup>$</sup>450.45</h4>
                </div>

                <div class="table-responsive">
                    <table class="table table-striped table-hover table-dark-border">
                        <tbody>
                            <tr>
                                <td class="table-dark">Market Value</td>
                                <td>$10,900.00</td>
                            </tr>

                            <tr>
                                <td class="table-dark">Cost Basis</td>
                                <td>$10,900.00</td>
                            </tr>
                            
                            <tr>
                                <td class="table-dark">Average Price</td>
                                <td>$10,900.00</td>
                            </tr>
                            
                            <tr>
                                <td class="table-dark">Folio %</td>
                                <td>$10,900.00</td>
                            </tr>
                            
                            <tr>
                                <td class="table-dark">Realised PnL</td>
                                <td>$10,900.00</td>
                            </tr>
                            
                            <tr>
                                <td class="table-dark">Unrealised PnL</td>
                                <td>$10,900.00</td>
                            </tr>
                             
                            <tr>
                                <td class="table-dark">Total PnL</td>
                                <td>$10,900.00</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <button class="btn btn-dark text-light border-dark m-3">
                    <i class="fa-solid fa-binoculars"></i> Details
                </button>
            </div>
        </div>
        <!-- END Col two -->
      </div>
    </div>
  </div>
</section>

"""