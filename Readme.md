# BNA Exchange rates script

## Description

This project contains a script that receives two dates and returns in a CSV the exchange rates for US Dollar and Euro provided by the BNA (Banco de la Nacion Argentina).

## Usage

1. Install the required dependecies in python:

```
pip install -r requirements.txt
```

2. Execute the bna.py script provided as arguments the start and end date in the following format `dd/mm/yyyy`:

```
python3 bna.py -s 01/07/2023 -e 31/12/2023
```

3. The output will be provided in the file named `exchange_rates.csv`