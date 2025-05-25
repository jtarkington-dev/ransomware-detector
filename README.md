# Ransomware Detector

**Tagline:** Cross-platform, open-source tool for detecting and isolating ransomware in real time.

---

## 🎯 Purpose & Goals

- Detect suspicious file behavior (mass changes, odd extensions, high entropy)
- Alert users and log events in both JSON and human-readable formats
- Isolate offending processes (suspend/kill, disable network)
- Protect file systems (remount as read-only)
- Support Linux & Windows via abstraction layers

---

## 🚀 Quickstart

### 1. Clone & Enter Repo

```bash
git clone git@github.com:<you>/ransomware-detector.git
cd ransomware-detector
```

### 2. Copy Environment Template

```bash
cp .env.example .env
```

### 3. Install Dependencies

```bash
chmod +x setup.sh
./setup.sh
```

### 4. Run the Detector

```bash
rdetector start
```

### 5. Check Status or Stop

```bash
rdetector status
rdetector stop
```

---

## 📁 File Overview

- `setup.sh` – Bootstrap script to install Python dependencies
- `.env.example` – Environment variable template
- `requirements.txt` – Python package list
- `src/`, `docs/`, `tests/`, `sandbox/`, `utils/` – Code, docs, tests, simulators, helpers

---

## 🧪 Testing

- **Unit tests:**

```bash
pytest
```

- **Ransomware simulation:**
  See `sandbox/` and `docs/testing.md`

---

## 🤝 Contributing

- Follow PEP8 and lint with `flake8`
- Write tests for new features
- Document design decisions in `docs/`

---

## 📄 License

MIT License – see `LICENSE`
