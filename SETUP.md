# Setup Guide - QA Test Framework

## Installation

### 1. Python Dependencies (pip)
```bash
pip install -r requirements.txt
```

**Python Packages Include:**
- pytest (9.0.3) - Test framework
- pytest-html (4.2.0) - HTML reports
- allure-pytest (2.13.2) - Allure plugin for pytest
- playwright (1.60.0) - Browser automation
- requests (2.34.2) - HTTP client
- Faker (40.19.1) - Data generation

### 2. System Tools (NOT via pip)

#### Allure Command-Line Tool
`allure-commandline` is a **system tool**, NOT a Python package. Install via package manager:

**macOS:**
```bash
brew install allure
```

**Verify Installation:**
```bash
allure --version
```

Expected output: `allure version 2.42.0`

#### JMeter
Also install via package manager:

**macOS:**
```bash
brew install jmeter
```

**Verify Installation:**
```bash
jmeter --version
```

### 3. Browser Installation (Playwright)
```bash
playwright install chromium
```

---

## What's Installed

| Component | Type | Install Method | Version |
|-----------|------|-----------------|---------|
| pytest | Python | pip | 9.0.3 |
| allure-pytest | Python | pip | 2.13.2 |
| playwright | Python | pip | 1.60.0 |
| requests | Python | pip | 2.34.2 |
| **allure** | System Tool | brew | 2.42.0 |
| **jmeter** | System Tool | brew | 5.6.3 |
| chromium | Browser | playwright | Latest |

---

## Running Tests

### Run All Tests with Allure
```bash
pytest tests/ -v --alluredir=reports/allure-results
```

### Generate Allure Report
```bash
allure generate reports/allure-results -o reports/allure-report --clean
```

### View Allure Dashboard
```bash
allure open reports/allure-report
```

### Run Specific Test Categories

**API Tests:**
```bash
pytest tests/api/ -v --alluredir=reports/allure-results
```

**UI Tests:**
```bash
pytest tests/ui/ -v --alluredir=reports/allure-results
```

**Load Tests (Allure Integration):**
```bash
pytest tests/loadtest/test_loadtest_results.py -v --alluredir=reports/allure-results
```

**JMeter Load Test (50 concurrent users):**
```bash
jmeter -n -t tests/loadtest/orangehrm_login_loadtest.jmx \
  -l results/loadtest_complete.jtl \
  -Jthreads=50 -Jrampup=60 -Jloops=2
```

---

## Project Structure

```
qa-takehome/
├── tests/
│   ├── api/ .......................... REST API tests (28 tests)
│   ├── ui/ ........................... UI/E2E tests (24 tests)
│   └── loadtest/ ..................... Load testing
│       ├── orangehrm_login_loadtest.jmx .... JMeter test plan
│       └── test_loadtest_results.py ........ Allure integration
├── reports/
│   ├── allure-report/ ................ HTML dashboard
│   ├── allure-results/ ............... Test data files
│   └── report.html ................... Pytest HTML report
├── results/
│   └── loadtest_complete.jtl ......... JMeter results
├── logs/
│   ├── jmeter_complete.log ........... JMeter logs
│   ├── api_tests.log ................. API test logs
│   └── ui_test_sample.log ............ UI test logs
├── docs/
│   ├── ENHANCEMENTS_GUIDE.md ......... Framework documentation
│   ├── LOAD_TEST_UNDERSTANDING.md .... Load test explanation
│   └── LOADTEST_QUICK_REFERENCE.md ... Quick reference
├── conftest.py ....................... Pytest configuration
├── pytest.ini ........................ Pytest settings
├── requirements.txt .................. Python dependencies
└── analyze_loadtest.sh ............... Load test analyzer

```

---

## Important Notes

### Why `allure-commandline` Not in requirements.txt?

The `allure-commandline` tool:
- Is a **system command-line application**, not a Python package
- Must be installed via your OS package manager (brew, apt, etc.)
- Cannot be installed via `pip`
- Is NOT needed for running tests, only for generating/viewing reports

The Python integration is via `allure-pytest` (already in requirements.txt).

### CI/CD Integration

GitHub Actions will automatically:
1. Install Python dependencies from `requirements.txt`
2. Use system tools (allure, jmeter) if pre-installed
3. Run all tests with Allure integration
4. Generate and upload reports

See `.github/workflows/tests.yml` for automation configuration.

---

## Troubleshooting

### "command not found: allure"
**Solution:** Install Allure via Homebrew
```bash
brew install allure
```

### "command not found: jmeter"
**Solution:** Install JMeter via Homebrew
```bash
brew install jmeter
```

### "ModuleNotFoundError: No module named 'pytest'"
**Solution:** Install Python dependencies
```bash
pip install -r requirements.txt
```

### "Playwright browsers not found"
**Solution:** Install Chromium browser
```bash
playwright install chromium
```

---

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt
playwright install chromium

# 2. Ensure system tools are installed
brew install allure jmeter

# 3. Run all tests with Allure
pytest tests/ -v --alluredir=reports/allure-results

# 4. Generate and view report
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report

# 5. (Optional) Run load test separately
jmeter -n -t tests/loadtest/orangehrm_login_loadtest.jmx \
  -l results/loadtest.jtl -Jthreads=50
```

Done! Your test framework is ready to use. 🚀
