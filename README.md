# Shop Counter

This desktop application aims to provide a minimal and flexible resource management platform for medium businesses to a local shopkeeper.
Currently it supports ledger entries like credit and debit amount in any transaction.
Plan is to add options for taking orders and product sell entries.

# Instructions To Use

- Install MongoDB as per you system configuration from [here](https://www.mongodb.com/download-center#community).
- Start the MongoDB server, for Windows - follow [this](https://docs.mongodb.com/tutorials/install-mongodb-on-windows/).
- Change database configuration in `configs/connect_db.json`.
- Make sure you have Python 3.x installed ([download](https://www.python.org/downloads/)).
- Install the requirements by:
```bash
pip install -r requirements.txt
```
- Launch application by changing to this directory and running:
```bash
python home.py
```

# Project Architecture

- `shop-counter` is designed to be highly flexible to meet different
requirements in the most simplistic way. Most of the elements can be change by
just changing the corresponding properties in `configs/elements.json`.
- Each feature like Customer Entry, Ledger, Order Entry, Sells Entry, etc are
defined as `tabs` and can be added and removed from the `json` file itself without modifying the code.
- Application is even database agnostic meaning you can swich to SQL based database just by changing the corresponding functions in `db_ops.py` module.
- `home.py` is the main module that uses the `elements.py` module to populate the
GUI elements. These elements are defined in the `configs/elements.json`

# Contributing / Modifying

You can modify it if the current form doesn't suits you requirements, keeping
following points in mind:
- `id` field of buttons defined in `json` files is used as function name which
must be defined in `Table` class.
- If `value` field is defined in `columns` field, then there must be a function
with this name in the `Table` class
- If you need any help, feel free to [contact](http://nikhilsoni.me/contact).

# License

[MIT License](https://nks.mit-license.org/)
