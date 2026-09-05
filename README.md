# Quantum Neural Network PQC

> **Domain:** Post-Quantum Cryptography & Quantum Machine Learning  
> **Standards:** NIST FIPS 203/204/205, ISO/IEC 17825, QML Parameter-Shift Rule Standard

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB.svg?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688.svg?logo=fastapi&logoColor=white)
![Audit Trail](https://img.shields.io/badge/Audit-HMAC--SHA256_Tamper--Evident-brightgreen.svg)

</div>

---

## 📖 What It Does

Quantum Neural Network PQC is a multi-agent evaluation framework that processes task payloads through specialized worker agents to produce consensus dossiers with cryptographic audit trails. It provides:

- **Multi-Agent Task Evaluation**: Distributed worker agents (InvariantQC, SafetyEscalation, ProtocolConformance) evaluate payloads against domain thresholds
- **Consensus Dossier Generation**: Aggregated results with urgency classification and integrity status
- **Cryptographic Audit Trail**: HMAC-SHA256 tamper-evident logging of all operations
- **PHI Outbound Guard**: Prevents sensitive data leakage via regex pattern detection
- **FastAPI REST API**: HTTP endpoints for task processing and system monitoring
- **Batch CSV Processing**: High-throughput batch evaluation of task records

---

## ⚙️ Architecture

### Agent Framework (`agents/`)
- **SystemSupervisor**: Master orchestrator coordinating worker evaluations
- **InvariantQCWorker**: Primary metric boundary auditor (threshold: 25.0)
- **SafetyEscalationWorker**: Critical safety interlock (threshold: 12.0 secondary)
- **ProtocolConformanceWorker**: Specification conformance checker
- **PHIGuard**: Zero-PHI outbound interceptor with regex pattern detection
- **AuditLogger**: HMAC-SHA256 chained cryptographic audit trail
- **FastAPI Server**: REST endpoints at `/api/audit`, `/api/chat`, `/metrics`, `/health`

### QNN PQC Agent (`qnn_pqc_agent/`)
- **QNNCoordinator**: Executive coordinator for quantum ML evaluations
- **FrontierDomainEngine**: Core algorithmic engine with parameter-shift rule
- **DataReuploadingEncoderAgent**: Primary parameter auditor
- **VariationalLayerAgent**: Critical kinetics safeguard
- **ParameterShiftGradientAgent**: Protocol conformance triager

### Enrichment Suite (`enrichment.py`)
- Parameter-Shift Rule with Gradient Variance Reduction
- Hardware-Efficient PQC with Entangling Layer Optimization
- Composite enrichment suite for domain-specific evaluations

---

## 💻 Installation

```bash
pip install fastapi uvicorn pydantic pytest
```

---

## 🚀 CLI Usage

### 1. Single Task Evaluation
```bash
python cli.py audit --task-id TASK-001 --target KEY-01 --primary 28.5 --secondary 14.2 --critical --status DISCORDANT
```

### 2. Supervisor Chat Query
```bash
python cli.py chat "What is the system status?"
```

### 3. Batch CSV Processing
```bash
python cli.py batch -i sample.csv -o results.csv
```

### 4. Verify Audit Trail Integrity
```bash
python cli.py verify-audit
```

### 5. Launch REST API Server
```bash
python cli.py serve --host 127.0.0.1 --port 8000
```

### 6. Run Simulation Benchmark
```bash
python simulator.py 1000
```

---

## 🛡️ Security Features

- **Zero-PHI Outbound Interceptor**: Active regex inspection blocking SSNs, MRNs, phone numbers, emails, and patient identifiers
- **Tamper-Evident HMAC-SHA256 Audit Trail**: Chained, cryptographically signed logs for every evaluation
- **Cryptographic Key Management**: Secure random key generation when `AUDIT_SECRET_KEY` environment variable is not set
- **Input Validation**: Pydantic models with strict type checking and bounds validation

### Environment Variables
| Variable | Description | Default |
|:---------|:------------|:--------|
| `AUDIT_SECRET_KEY` | HMAC-SHA256 signing key | Random (generated per session) |
| `MODEL_PROVIDER` | LLM provider selection | `mock` |

---

## 🧪 Testing

Run the automated test suite:

```bash
pytest -v
```

Test coverage includes:
- PHI guard enforcement
- Specialized worker evaluations
- Supervisor consensus and audit integrity
- CLI command validation
- Enrichment suite execution

---

## 🐳 Docker Deployment

```bash
docker build -t quantum-neural-network-pqc .
docker run -p 8000:8000 -e AUDIT_SECRET_KEY=$(openssl rand -hex 32) quantum-neural-network-pqc
```

Or using Docker Compose:

```bash
AUDIT_SECRET_KEY=$(openssl rand -hex 32) docker compose up
```

---

## 📊 Prometheus Metrics

Access operational metrics at `http://localhost:8000/metrics`:

- `system_tasks_total`: Total tasks processed
- `alerts_triggered_total`: Alerts by urgency tier
- `phi_outbound_blocks_total`: PHI interception count
- `audit_chain_blocks_total`: Audit blocks signed
- `task_processing_duration_avg_seconds`: Average evaluation latency

---

## 📁 Project Structure

```
quantum-neural-network-pqc/
├── agents/               # Enterprise agent framework
│   ├── api.py           # FastAPI REST server
│   ├── base.py          # Security, PHI guard, audit trail
│   ├── models.py        # Pydantic data models
│   ├── supervisor.py    # Master orchestrator
│   ├── workers.py       # Specialized worker agents
│   ├── llm_factory.py   # LLM provider factory
│   ├── learning.py      # Bayesian calibration engine
│   ├── metrics.py       # Prometheus metrics collector
│   └── streamer.py      # WebSocket telemetry broadcaster
├── qnn_pqc_agent/        # QNN PQC agent framework
│   ├── agents.py        # Sub-agents and coordinator
│   ├── engine.py        # Core algorithmic engine
│   ├── models.py        # Data models
│   ├── cli.py           # CLI interface
│   └── server.py        # FastAPI server factory
├── tests/               # Pytest test suite
├── web/                 # Web operations console
├── cli.py               # Main CLI entry point
├── simulator.py         # High-throughput simulation
├── enrichment.py        # Domain enrichment suite
├── sample.csv           # Sample batch input
├── sample_payload.json  # Sample API payload
├── benchmark_dataset.json # Golden benchmark test cases
├── Dockerfile           # Container build
├── docker-compose.yml   # Container orchestration
└── pyproject.toml       # Project metadata
```
