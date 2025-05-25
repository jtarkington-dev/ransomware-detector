# Ransomware Detector

**Tagline:** Cross-platform, open-source tool for detecting and isolating ransomware in real time.

---

## 🎯 Purpose & Goals

- Detect suspicious file behavior:

  - Mass file modifications
  - Unusual file extensions
  - High entropy content (encrypted data)

- Alert users and log events in both JSON and human-readable formats
- Isolate offending processes:

  - Suspend or kill
  - Disable network access

- Protect the filesystem:

  - Remount critical directories as read-only

- Cross-platform support:

  - Works on both Linux and Windows via abstraction layers

---

## 🧱 Architecture Diagram

_(To be added in a separate diagram file)_

---

## 🚀 Quickstart

### 1. Initialize Repository & Install Dependencies

```bash
git init
cp .env.example .env
./setup.sh
```

### 2. Start the Detector

```bash
rdetector start
```

### 3. Status / Stop

```bash
rdetector status
rdetector stop
```

### 4. Usage

```bash
rdetector [start|stop|status|watch]
```

See `docs/cli.md` for full CLI reference.

---

## 🧪 Testing

### Run Unit Tests

```bash
pytest
```

### Simulate Ransomware in Sandbox

Follow the guide in `docs/testing.md`.

---

## 🤝 Contributing

- Follow `PEP8` standards and lint with `flake8`
- Write unit tests for any new functionality
- Document all design decisions in `docs/`

---

## 📄 License

This project is licensed under the MIT License. See `LICENSE` for full details.

---

## 📦 `requirements.txt`

```txt
watchdog
psutil
netifaces
python-dotenv
cryptography
structlog
pytest
flake8
```

---

## ⚙️ `setup.sh`

```bash
#!/usr/bin/env bash
set -e

# 1. Check Python
if ! command -v python3 &> /dev/null; then
  echo "Python3 not found. Please install Python 3.8+." >&2
  exit 1
fi

# 2. Check pip
if ! command -v pip3 &> /dev/null; then
  echo "pip3 not found. Please install pip." >&2
  exit 1
fi

# 3. Create & activate venv
python3 -m venv venv
source venv/bin/activate

# 4. Install requirements
pip install --upgrade pip
pip install -r requirements.txt

# 5. Verify auditd on Linux
if [[ "$(uname)" == "Linux" ]]; then
  if ! command -v auditctl &> /dev/null; then
    echo "⚠️  auditd not found. Install via your package manager (e.g. apt install auditd)." >&2
  fi
fi

echo "Setup complete. Activate with 'source venv/bin/activate'."
```

### Make Executable

```bash
chmod +x setup.sh
```

---

## 🔧 `.env.example`

```ini
# ========== Logging ==========
LOG_LEVEL=INFO
LOG_FILE=logs/detector.log

# ========== Alerting ==========
ALERT_EMAIL=security@example.com

# ========== Sandbox ==========
SANDBOX_DIR=/absolute/path/to/sandbox

# ========== Detection ==========
ENTROPY_THRESHOLD=7.5
FILE_CHANGE_RATE=100  # file events per minute

# ========== Isolation ==========
# Comma-separated options: suspend_process, kill_process, disable_network, remount_readonly
ISOLATION_ACTIONS=suspend_process,disable_network

# Optional OS override
# OS_OVERRIDE=linux
# OS_OVERRIDE=windows
```
