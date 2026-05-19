import requests
import time

BASE_URL = "https://api.frankfurter.app"
TIMEOUT = 3  # secondes
MAX_RETRIES = 1

def get(endpoint):
    """
    Effectue un GET sur l'endpoint donné.
    Retourne un dict avec : status, json, latency_ms, error
    """
    url = f"{BASE_URL}{endpoint}"
    attempt = 0

    while attempt <= MAX_RETRIES:
        try:
            start = time.time()
            response = requests.get(url, timeout=TIMEOUT)
            latency_ms = round((time.time() - start) * 1000)

            # Gestion rate limit
            if response.status_code == 429:
                print("Rate limit atteint, attente 2s...")
                time.sleep(2)
                attempt += 1
                continue

            return {
                "status": response.status_code,
                "json": response.json() if response.headers.get("Content-Type", "").startswith("application/json") else None,
                "latency_ms": latency_ms,
                "error": None
            }

        except requests.exceptions.Timeout:
            attempt += 1
            if attempt > MAX_RETRIES:
                return {"status": None, "json": None, "latency_ms": None, "error": "Timeout"}

        except Exception as e:
            return {"status": None, "json": None, "latency_ms": None, "error": str(e)}

    return {"status": None, "json": None, "latency_ms": None, "error": "Max retries atteint"}
