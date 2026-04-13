# SQL Injection Demo — Security Awareness Project

> A hands-on educational web app demonstrating how SQL injection attacks work and how parameterised queries prevent them.

Built by **Gargi Kharat** | Diploma IT, Vidyalankar Polytechnic, Mumbai  
🔐 Aspiring Cybersecurity Professional

---

## What this project does

This project simulates a login system in two modes:

| Mode | Description |
|------|-------------|
| **Vulnerable** | Login query directly concatenates user input — SQL injection is possible |
| **Secure** | Login uses parameterised queries — injection attempts are completely blocked |

You can switch between modes in real time and see exactly what SQL query gets executed — making the attack and the defence both visible and understandable.

---

## The attack explained

In the vulnerable mode, the SQL query looks like this:

```sql
SELECT * FROM users WHERE username = 'INPUT' AND password = 'INPUT'
```

An attacker can type `' OR '1'='1` as the username. The query becomes:

```sql
SELECT * FROM users WHERE username = '' OR '1'='1' AND password = ''
```

Since `'1'='1'` is always true, the attacker bypasses authentication entirely — **without knowing any password**.

---

## The fix — parameterised queries

```python
# VULNERABLE ❌
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"

# SECURE ✅
query = "SELECT * FROM users WHERE username = ? AND password = ?"
cursor.execute(query, (username, password))
```

With parameterised queries, user input is treated as **data only** — never as executable SQL code.

---

## Tech stack

- **Backend:** Python, Flask
- **Database:** SQLite3
- **Frontend:** HTML, CSS (vanilla — no frameworks)
- **Concept:** OWASP Top 10 — A03: Injection

---

## How to run locally

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/sql-injection-demo.git
cd sql-injection-demo

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python app.py

# 4. Open in browser
# http://127.0.0.1:5000
```

---

## Test credentials

| Username | Password | Role |
|----------|----------|------|
| admin | admin@123 | Administrator |
| gargi | pass123 | Student |
| teacher | teach@456 | Teacher |

---

## Attack payloads to try (vulnerable mode only)

| Payload (username field) | Effect |
|--------------------------|--------|
| `' OR '1'='1` | Bypasses password check |
| `admin'--` | Comments out password condition |
| `' OR 1=1--` | Always-true injection |

---

## What I learned

- How SQL injection exploits unsanitised input
- Why string concatenation in queries is dangerous
- How parameterised queries are the industry-standard fix
- OWASP Top 10 — Injection vulnerabilities
- Flask routing, SQLite3, and session management

---

## Disclaimer

This project is built **strictly for educational and security awareness purposes**. It demonstrates a known vulnerability in a controlled, local environment. Never use vulnerable patterns in real applications.

---

## Connect with me

- LinkedIn: [linkedin.com/in/gargi-kharat](https://linkedin.com/in/gargi-kharat)
- Email: gargikharat712b@gmail.com

---

*If this helped you understand SQL injection — drop a ⭐ on the repo!*
