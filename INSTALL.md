# Installation & Deployment Guide

## Local Setup (Your Machine)

### Python Dependencies
```bash
pip install -r requirements.txt
```

**Already Included:**
- allure-pytest 2.13.2 ✓ (this is the Python plugin)
- Do NOT add: allure-commandline (use brew instead)

### System Tools (macOS)
```bash
brew install allure jmeter
```

### Browser
```bash
playwright install chromium
```

---

## Important: allure-commandline vs allure-pytest

### ❌ DO NOT DO THIS:
```bash
pip install allure-commandline  # ← This will fail!
pip install jmeter              # ← This will fail!
```

### ✅ DO THIS INSTEAD:
```bash
# Python packages (in requirements.txt)
pip install -r requirements.txt

# System tools (via package manager)
brew install allure jmeter
```

### Why?
- **allure-pytest** = Python plugin (goes in requirements.txt)
- **allure-commandline** = System tool (installed via brew/apt)
- **jmeter** = System tool (installed via brew/apt)

They serve different purposes and install differently!

---

## GitHub Actions (CI/CD)

### Current Workflow: `.github/workflows/tests.yml`

The workflow is already configured to:
1. Install Python dependencies from requirements.txt ✓
2. Run all tests with Allure integration ✓
3. Generate Allure reports ✓

### What's Already Handled:
```yaml
# Python dependencies
pip install -r requirements.txt

# Tests with Allure
pytest tests/ -v --alluredir=reports/allure-results

# Generate report
allure generate reports/allure-results -o reports/allure-report
```

### What Needs Pre-Installation in Runner:
For GitHub Actions to work fully, the runner might need:
```bash
brew install allure jmeter
```

**OR** use a pre-built Actions runner that has them.

### Alternative for GitHub Actions:
If macOS runner doesn't have tools pre-installed, update `.github/workflows/tests.yml`:

```yaml
- name: Install system tools
  run: |
    brew install allure jmeter
```

---

## Testing Locally Before Push

```bash
# 1. Install everything
pip install -r requirements.txt
playwright install chromium
brew install allure jmeter

# 2. Run all tests
pytest tests/ -v --alluredir=reports/allure-results

# 3. Generate report
allure generate reports/allure-results -o reports/allure-report --clean

# 4. View report
allure open reports/allure-report

# 5. Verify load tests appear
# Look for "Load Test:" tests in dashboard
```

---

## Push to Repository

### Before Pushing:
```bash
# Make sure tests pass locally
pytest tests/ --alluredir=reports/allure-results -q

# Generate report one more time
allure generate reports/allure-results -o reports/allure-report --clean
```

### Push:
```bash
git add .
git commit -m "Add Allure reporting + 50-user load test framework"
git push origin main
```

### After Push:
1. GitHub Actions will automatically run tests
2. Check Actions tab for results
3. View generated Allure reports (if configured for artifacts)

---

## Project Files Reference

### Python Test Code:
- `tests/api/` - 28 API tests
- `tests/ui/` - 24 UI tests  
- `tests/loadtest/test_loadtest_results.py` - Load test Allure integration
- `tests/loadtest/orangehrm_login_loadtest.jmx` - JMeter test plan

### Configuration:
- `requirements.txt` - Python packages (install with pip)
- `pytest.ini` - Pytest settings + markers
- `conftest.py` - Pytest fixtures & Allure setup

### Reports:
- `reports/allure-report/` - HTML dashboard
- `reports/allure-results/` - Raw test data
- `reports/report.html` - Pytest HTML report

### Tools & Scripts:
- `analyze_loadtest.sh` - Load test analyzer
- `.github/workflows/tests.yml` - CI/CD pipeline

### Documentation:
- `SETUP.md` - This setup guide
- `docs/ENHANCEMENTS_GUIDE.md` - Allure + JMeter guide
- `docs/LOAD_TEST_UNDERSTANDING.md` - Load test explanation
- `docs/LOADTEST_QUICK_REFERENCE.md` - Quick reference

---

## Troubleshooting

### "command not found: allure"
```bash
brew install allure
```

### "command not found: jmeter"
```bash
brew install jmeter
```

### "ModuleNotFoundError: pytest"
```bash
pip install -r requirements.txt
```

### Tests fail in GitHub Actions
1. Check if system tools are installed in runner
2. Update workflow to install them if needed:
```yaml
- run: brew install allure jmeter
```

### Allure report not generating
Make sure Allure CLI is installed:
```bash
which allure
allure --version
```

---

## Summary Checklist

### Local Machine Setup:
- [ ] `pip install -r requirements.txt`
- [ ] `playwright install chromium`
- [ ] `brew install allure`
- [ ] `brew install jmeter`
- [ ] Tests run successfully locally
- [ ] Allure reports generate

### Before Pushing:
- [ ] All tests pass
- [ ] Load tests in Allure
- [ ] Report generates without errors
- [ ] No warnings during test runs

### After Pushing:
- [ ] GitHub Actions workflow runs
- [ ] Tests pass in CI/CD
- [ ] Review Actions logs if fails
- [ ] Verify Allure reports generated

---

## Final Notes

✅ **This project is production-ready:**
- All dependencies specified in requirements.txt
- System tools installation documented
- Load tests integrated in Allure
- CI/CD pipeline configured
- Documentation complete

🚀 **You can push and deploy with confidence!**
