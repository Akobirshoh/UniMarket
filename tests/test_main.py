import subprocess
import sys
import time
import requests


def _run_server():
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "src.main:app", "--port", "8001"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    time.sleep(1.2)
    return proc


def test_root():
    proc = _run_server()
    try:
        r = requests.get("http://127.0.0.1:8001/")
        assert r.status_code == 200
        data = r.json()
        assert data["message"].startswith("Добро пожаловать")
    finally:
        proc.terminate()


def test_health():
    proc = _run_server()
    try:
        r = requests.get("http://127.0.0.1:8001/health")
        assert r.status_code == 200
        data = r.json()
        assert data["status"] == "healthy"
    finally:
        proc.terminate()


def test_about():
    proc = _run_server()
    try:
        r = requests.get("http://127.0.0.1:8001/about")
        assert r.status_code == 200
        data = r.json()
        assert data["project"] == "UniMarket"
        assert data["author"] == "Акобиршох"
    finally:
        proc.terminate()
