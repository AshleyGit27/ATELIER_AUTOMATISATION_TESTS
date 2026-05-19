from tester.tests import run_all_tests
import datetime

def run():
    tests = run_all_tests()
    
    # Calcul des métriques
    passed = sum(1 for t in tests if t["status"] == "PASS")
    failed = sum(1 for t in tests if t["status"] == "FAIL")
    total = len(tests)
    
    # Latences (on ignore les None)
    latences = [t["latency_ms"] for t in tests if t["latency_ms"] is not None]
    
    if latences:
        avg = round(sum(latences) / len(latences))
        latences_triees = sorted(latences)
        index_p95 = max(0, int(len(latences_triees) * 0.95) - 1)
        p95 = latences_triees[index_p95]
    else:
        avg = None
        p95 = None

    return {
        "api": "Frankfurter",
        "timestamp": datetime.datetime.now().isoformat(),
        "summary": {
            "passed": passed,
            "failed": failed,
            "total": total,
            "error_rate": round(failed / total, 3) if total > 0 else 0,
            "latency_ms_avg": avg,
            "latency_ms_p95": p95,
            "disponibilite": "UP" if failed == 0 else "DEGRADED" if failed < total else "DOWN"
        },
        "tests": tests
    }
