from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path
from model import train_model, screen_sample

app = Flask(__name__)
app.secret_key = "change-this-secret-key"
DB_PATH = Path(__file__).with_name("medicine.db")
MODEL = train_model()  # Trained on illustrative synthetic data for demonstration only.

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                medicine_name TEXT NOT NULL,
                batch_number TEXT NOT NULL,
                manufacturer TEXT NOT NULL,
                ph REAL NOT NULL,
                assay_pct REAL NOT NULL,
                dissolution_pct REAL NOT NULL,
                moisture_pct REAL NOT NULL,
                result TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

@app.route("/")
def index():
    with get_db() as conn:
        total = conn.execute("SELECT COUNT(*) FROM tests").fetchone()[0]
        flagged = conn.execute(
            "SELECT COUNT(*) FROM tests WHERE result = 'Flag for laboratory review'"
        ).fetchone()[0]
        recent = conn.execute("SELECT * FROM tests ORDER BY id DESC LIMIT 5").fetchall()
    return render_template("index.html", total=total, flagged=flagged, recent=recent)

@app.route("/test", methods=["GET", "POST"])
def test_medicine():
    if request.method == "POST":
        try:
            name = request.form["medicine_name"].strip()
            batch = request.form["batch_number"].strip()
            manufacturer = request.form["manufacturer"].strip()
            ph = float(request.form["ph"])
            assay = float(request.form["assay_pct"])
            dissolution = float(request.form["dissolution_pct"])
            moisture = float(request.form["moisture_pct"])

            if not all([name, batch, manufacturer]):
                raise ValueError("Please complete all medicine details.")
            if not (0 <= ph <= 14 and 0 <= assay <= 150 and
                    0 <= dissolution <= 100 and 0 <= moisture <= 100):
                raise ValueError("One or more test values are outside the allowed input range.")

            result = screen_sample(MODEL, [ph, assay, dissolution, moisture])

            with get_db() as conn:
                cursor = conn.execute("""
                    INSERT INTO tests
                    (medicine_name, batch_number, manufacturer, ph, assay_pct,
                     dissolution_pct, moisture_pct, result)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (name, batch, manufacturer, ph, assay, dissolution, moisture, result))
                test_id = cursor.lastrowid

            return redirect(url_for("result", test_id=test_id))
        except (ValueError, KeyError) as error:
            flash(str(error), "error")
    return render_template("test.html")

@app.route("/result/<int:test_id>")
def result(test_id):
    with get_db() as conn:
        record = conn.execute("SELECT * FROM tests WHERE id = ?", (test_id,)).fetchone()
    if record is None:
        flash("Test record not found.", "error")
        return redirect(url_for("index"))
    return render_template("result.html", record=record)

@app.route("/history")
def history():
    with get_db() as conn:
        records = conn.execute("SELECT * FROM tests ORDER BY id DESC").fetchall()
    return render_template("history.html", records=records)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
