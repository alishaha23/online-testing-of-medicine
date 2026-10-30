# Online Testing and Monitoring of Medicine (Educational Prototype)

A Flask web application for recording medicine sample measurements, running an illustrative ML screening model, and reviewing test history.

## Features
- Medicine and batch record entry
- Demonstration screening using pH, assay, dissolution, and moisture values
- SQLite test-history database
- Dashboard and result pages

## Technology
Python, Flask, SQLite, NumPy, scikit-learn, HTML, Bootstrap, CSS.

## Run locally
1. Install Python 3.10 or newer.
2. Create and activate a virtual environment:
   - Windows: `py -m venv .venv` then `.venv\\Scripts\\activate`
   - macOS/Linux: `python3 -m venv .venv` then `source .venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Start the app: `python app.py`
5. Open `http://127.0.0.1:5000` in your browser.

## Important limitation
The classifier is trained on synthetic illustrative data and its ranges are not official pharmaceutical specifications. This project is for software/ML learning only. It cannot authenticate medicines or determine whether they are safe or fit for use. Real medicine quality assessment requires validated methods, product-specific standards, and authorized laboratory testing. Do not use this demo to make medical or purchasing decisions.
