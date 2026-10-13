# Quantum Neural Network PQC

A Python rule-evaluation and audit demonstration with a standalone browser interface. Despite the repository name, the current implementation **does not implement quantum circuits, quantum-neural-network training, parameter-shift gradients, or post-quantum cryptographic primitives**. Its existing rule engines use configurable-in-code numeric thresholds and keyword matching.

## Browser demo

Open [the local web application](web/) in a browser after downloading the repository. It runs entirely in JavaScript and does not require Python, a server, Pyodide, or any external API. The root `index.html` redirects to `web/` for static hosting.

The demo evaluates these same rules from `agents/workers.py`:

| Rule | Trigger | Result |
| --- | --- | --- |
| Primary metric | Greater than 25 | Elevated |
| Secondary metric | Greater than 12 | Elevated |
| Critical flag | Enabled | Critical |
| Status descriptor | Contains DISCORDANT, ANOMALY, MUTANT, VIOLATION, FAIL or REJECT (case-insensitive) | Elevated |

The browser can export its unsigned result as JSON. It **does not** produce a server dossier or a cryptographically signed audit entry. No form input is transmitted or saved by the demo.

## Python CLI and API

Requires Python 3.9 or later.

```bash
python -m pip install -e ".[server,test]"
python cli.py audit --task-id TASK-001 --target KEY-01 --primary 28.5 --secondary 14.2 --critical --status DISCORDANT
python cli.py batch -i sample.csv -o results.csv
python cli.py verify-audit
python cli.py serve --host 127.0.0.1 --port 8000
```

The main CLI uses the `agents/` supervisor and Pydantic-validated payloads. Its REST API provides `GET /health`, `GET /metrics`, `POST /api/audit`, `POST /api/chat` and `GET /api/audit/logs`. The metrics endpoint returns JSON, **not** Prometheus exposition text.

A separate legacy coordinator is available through the installed `quantum-neural-network-pqc` command or `python -m qnn_pqc_agent.cli`. It has different thresholds and does not use the HMAC audit ledger. The `enrichment.py` module reports threshold classifications and is not an implementation of parameter-shift differentiation or entangling-gate optimization.

## Tests

```bash
python -m pytest -q
python -m compileall -q agents qnn_pqc_agent cli.py enrichment.py simulator.py tests
node --test tests/test_browser.cjs
```

Node.js is only needed to run the browser unit tests, not to use the static application. CI runs Python checks on versions 3.10, 3.11 and 3.12, as well as the Node.js evaluation tests.

## Security and privacy limitations

- Audit entries are HMAC-SHA256 authenticated and chained, but their key and records live **only in memory**. Restarting the process loses the records; integrity checks are not a persistent audit archive.
- Set `AUDIT_SECRET_KEY` to a strong, private random value when running the server. Do not put it in the repository or browser code.
- The regular-expression identifier checks are incomplete and do **not** certify de-identification or HIPAA compliance. Do not submit real patient data, secrets or sensitive identifiers.
- The API has **no authentication** and should only be exposed on a trusted network. The Docker Compose example binds the service to localhost by default.
- The deterministic mock chat service does not call third-party LLM providers.

For local container development:

```bash
export AUDIT_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
docker compose up --build
```

The server is available at `http://127.0.0.1:8000`. This is a development setup, not a hardened public service.

## Technology and compatibility

Python, Pydantic, FastAPI (optional server), plain HTML/CSS/JavaScript, and GitHub Actions. The browser demo uses standard web APIs and works in current desktop and mobile browsers with JavaScript enabled. No browser-Python runtime is necessary for its limited threshold-evaluation functionality.

## License

[MIT](LICENSE).
