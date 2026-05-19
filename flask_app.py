from flask import Flask, jsonify, render_template
from tester.runner import run
from storage import init_db, save_run, list_runs

app = Flask(__name__)
init_db()

@app.route("/")
def index():
    return render_template("dashboard.html", runs=list_runs())

@app.route("/run")
def run_tests():
    result = run()
    save_run(result)
    return jsonify(result)

@app.route("/dashboard")
def dashboard():
    runs = list_runs()
    return render_template("dashboard.html", runs=runs)

@app.route("/health")
def health():
    runs = list_runs(limit=1)
    if not runs:
        return jsonify({"status": "UNKNOWN", "message": "Aucun run effectué"})
    dernier = runs[0]
    return jsonify({
        "status": dernier["summary"]["disponibilite"],
        "timestamp": dernier["timestamp"],
        "error_rate": dernier["summary"]["error_rate"],
        "latency_ms_avg": dernier["summary"]["latency_ms_avg"]
    })

@app.route("/export")
def export():
    runs = list_runs()
    return jsonify(runs)

if __name__ == "__main__":
    app.run(debug=True)
