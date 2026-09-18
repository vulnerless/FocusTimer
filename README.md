# FocusTimer

Pomodoro timer web app with a task list (Flask).

Caner Bora Göktaş

## Installation
Requires Python 3.10+.

```bash
git clone https://github.com/vulnerless/FocusTimer.git
cd FocusTimer
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Usage
```bash
python app.py
```
Open http://127.0.0.1:5000

## Tests
```bash
pytest -v                                                    # 20 tests
pytest --cov=app --cov=timer_core --cov-branch               # coverage
flake8 --exclude .venv .                                     # static analysis
```
