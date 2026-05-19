from tester.client import get

def run_all_tests():
    results = []

    # TEST 1 : /latest répond HTTP 200
    r = get("/latest?from=EUR")
    results.append({
        "name": "GET /latest - HTTP 200",
        "status": "PASS" if r["status"] == 200 else "FAIL",
        "latency_ms": r["latency_ms"],
        "details": r["error"] or ""
    })

    # TEST 2 : /latest contient les champs obligatoires
    r = get("/latest?from=EUR")
    data = r["json"] or {}
    champs = ["amount", "base", "date", "rates"]
    manquants = [c for c in champs if c not in data]
    results.append({
        "name": "GET /latest - champs obligatoires",
        "status": "PASS" if not manquants else "FAIL",
        "latency_ms": r["latency_ms"],
        "details": f"Manquants: {manquants}" if manquants else ""
    })

    # TEST 3 : /latest - types corrects
    r = get("/latest?from=EUR")
    data = r["json"] or {}
    types_ok = (
        isinstance(data.get("amount"), (int, float)) and
        isinstance(data.get("base"), str) and
        isinstance(data.get("rates"), dict)
    )
    results.append({
        "name": "GET /latest - types corrects",
        "status": "PASS" if types_ok else "FAIL",
        "latency_ms": r["latency_ms"],
        "details": "" if types_ok else "Types incorrects"
    })

    # TEST 4 : /currencies répond HTTP 200
    r = get("/currencies")
    results.append({
        "name": "GET /currencies - HTTP 200",
        "status": "PASS" if r["status"] == 200 else "FAIL",
        "latency_ms": r["latency_ms"],
        "details": r["error"] or ""
    })

    # TEST 5 : /currencies contient EUR et USD
    r = get("/currencies")
    data = r["json"] or {}
    results.append({
        "name": "GET /currencies - EUR et USD présents",
        "status": "PASS" if "EUR" in data and "USD" in data else "FAIL",
        "latency_ms": r["latency_ms"],
        "details": "" if "EUR" in data else "EUR ou USD manquant"
    })

    # TEST 6 : date valide retourne HTTP 200
    r = get("/2024-01-01?from=EUR&to=USD")
    results.append({
        "name": "GET /2024-01-01 - HTTP 200",
        "status": "PASS" if r["status"] == 200 else "FAIL",
        "latency_ms": r["latency_ms"],
        "details": r["error"] or ""
    })

    # TEST 7 : date invalide retourne une erreur (pas 200)
    r = get("/invalid-date")
    results.append({
        "name": "GET /invalid-date - erreur attendue",
        "status": "PASS" if r["status"] != 200 else "FAIL",
        "latency_ms": r["latency_ms"],
        "details": f"Code reçu: {r['status']}"
    })

    return results
