import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--start", required=True, type=lambda s: datetime.strptime(s, '%d/%m/%Y'))
    parser.add_argument("-e", "--end", required=True, type=lambda s: datetime.strptime(s, '%d/%m/%Y'))
    args = parser.parse_args()
    return args


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

def get_exchange_rates(start_date, end_date):
    exchange_rates = []
    for date in daterange(start_date, end_date):
        date_str = date.strftime("%-d/%-m/%Y")

        url = f"https://www.bna.com.ar/Cotizador/HistoricoPrincipales?id=monedas&fecha={date_str}&filtroEuro=1&filtroDolar=1"

        response = requests.get(url)
        html = response.text

        soup = BeautifulSoup(html, "html.parser")
        table_usd = soup.find("div", attrs={"id": "tablaDolar"})
        table = table_usd.find("table", attrs={"class":"table table-bordered cotizador"})
        rows = [[td.get_text() for td in tr.find_all("td")] for tr in table.find("tbody").find_all("tr")]

        for moneda, compra, venta, fecha in rows:
            if date_str == fecha:
                exchange_rates.append([moneda, float(compra), float(venta), fecha])


        table_usd = soup.find("div", attrs={"id": "tablaEuro"})
        table = table_usd.find("table", attrs={"class":"table table-bordered cotizador"})
        rows = [[td.get_text() for td in tr.find_all("td")] for tr in table.find("tbody").find_all("tr")]

        for moneda, compra, venta, fecha in rows:
            if date_str == fecha:
                exchange_rates.append([moneda, float(compra), float(venta), fecha])
    return exchange_rates


if __name__ == "__main__":
    args = parse_arguments()
    start_date = args.start
    end_date = args.end
    header = ["Fecha", "Moneda", "Compra", "Venta"]
    exchange_rates = get_exchange_rates(start_date, end_date)

    with open("exchange_rates.csv", "w") as f:
        f.write(";".join(header))
        for moneda, compra, venta, fecha in exchange_rates:
            compra_str = f"{compra:.2f}".replace(".", ",")
            venta_str = f"{venta:.2f}".replace(".", ",")
            f.write(f"\n{fecha};{moneda};{compra_str};{venta_str}")
