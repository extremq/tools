# Tools
A collection of independent tools for various purposes.

# Contents
- [Requirements](#requirements)
- [Money Lost](#money-lost)

# Requirements
- `config.env`: Copy `example_config.env` and fill in the values.
- `requirements.txt`: Install the required packages with `pip install -r requirements.txt`.

# Money Lost
A tool to calculate how much money you lost in the exchange rate when you bought something in a foreign currency.

Requires Open Exchange Rates API key. You can get one for free [here](https://openexchangerates.org/signup/free).

## Usage
You can use the tool by running the `main.py` file with the `money_lost` command.
It will print the help message if you don't provide any arguments.
```commandline
> py .\main.py money_lost -f RON -t EUR -s 4200 -b 845.05
Success: Environment variables loaded successfully.
 Your rate:      4.970 RON / per EUR
 Real rate:      4.939 RON / per EUR

Your value:    845.050 EUR
Real value:    850.460 EUR
------------------------------
Difference:      5.410 EUR
```