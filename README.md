# Shop Counter

This desktop application aims to provide a minimal and flexible resource management platform for medium businesses to a local shopkeeper.
Currently it supports ledger entries like credit and debit amount in any transaction.
Plan is to add options for taking orders and product sell entries.

# Instructions To Use

- Install MongoDB as per you system configuration from [here](https://www.mongodb.com/download-center#community).
- Start the MongoDB server, for Windows - follow [this](https://docs.mongodb.com/tutorials/install-mongodb-on-windows/).
- Download and extract the [Windows package](https://github.com/krsoninikhil/shop-counter/releases/download/v1.0/ShopCounter.zip).
- Change database configuration in `configs/connect_db.json`.
- Start application by executing `ShopCounter.exe`.

# Upgrading

- If you've using v1.0, there are some changes in the way data is stored. To 
make your presaved data work with new version, run this script:
```bash
mongo utils/upgrade_from_v1.js
```

# Project Architecture

- `shop-counter` is designed to be highly flexible to meet different
requirements in the most simplistic way. Most of the elements can be change by
just changing the corresponding properties in `configs/elements.json`.
- It uses Python 3 and is based on awesome open source [kivy](https://kivy.org) framework.
- Each feature like Customer Entry, Ledger, Order Entry, Sells Entry, etc are
defined as `tabs` and can be added and removed from the `json` file itself without modifying the code.
- Codebase is mostly database agnostic meaning you can swich to SQL based database just by changing the corresponding functions in `db_ops.py` module.
- `home.py` is the main module that uses the `elements.py` module to populate the
GUI elements. These elements are defined in the `configs/elements.json`

# Contributing / Modifying

You can modify it if the current form doesn't suits you requirements, following
information might be handy:
- Make sure you have ([Python 3.x](https://www.python.org/downloads/)) installed.
- Install the requirements by:
```bash
pip install -r requirements.txt
```
- To make `kivy` work, you might need to follow [this](https://kivy.org/docs/gettingstarted/installation.html).
- Launch application by changing to this directory and running:
```bash
python home.py
```

###### Code Related Assumptions:
- `id` field of buttons defined in `json` files is used as function name which
must be defined in `Table` class.
- If `value` field is defined in `columns` field, then there must be a function
with this name in the `Table` class
- To package the app for Windows, follow [this](https://kivy.org/docs/guide/packaging-windows.html).
- While packaging if you get error like [`Unable to find any valuable Window provider`](https://groups.google.com/forum/#!topic/kivy-users/W3dS534BqQI),
copy the `libpng16-16.dll` from your system to `dist` folder of the package,
which mostly can be found at `C:\Users\<username>\AppData\Local\Programs\Python\Python35\share\sdl2\bin`
- If you need any help, feel free to [contact](http://nikhilsoni.me/contact).

# License

[MIT License](https://nks.mit-license.org/)
