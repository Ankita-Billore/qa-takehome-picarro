# QA Automation Enhancements Guide

This guide covers two major enhancements to the QA automation framework:
1. **Allure Report Integration** - Professional test reporting with detailed analytics
2. **OrangeHRM Load Testing** - Concurrent login testing for 50+ users

---

## Table of Contents

1. [Allure Reports Setup & Usage](#allure-reports-setup--usage)
2. [OrangeHRM Load Testing (50 Users)](#orangehrm-load-testing-50-users)
3. [Troubleshooting](#troubleshooting)
4. [CI/CD Integration](#cicd-integration)

---

## Allure Reports Setup & Usage

### What is Allure?

Allure is a professional test reporting framework that provides:
- **Beautiful HTML Reports** with interactive dashboards
- **Test History** tracking test trends over time
- **Detailed Failure Analysis** with screenshots, logs, and attachments
- **Categorization** by severity, feature, story, and more
- **Flaky Test Detection** for identifying unstable tests
- **Performance Metrics** showing response times and throughput

### Installation

#### 1. Install Python Package
```bash
pip install -r requirements.txt
```
This installs `allure-pytest==2.13.2` which is required for pytest integration.

#### 2. Install Allure Command-Line Tool

**macOS (Homebrew):**
```bash
brew install allure
```

**Ubuntu/Debian:**
```bash
sudo apt-add-repository ppa:qameta/allure
sudo apt-get update
sudo apt-get install allure
```

**Windows (Chocolatey):**
```powershell
choco install allure
```

**Manual Installation:**
1. Download from: https://github.com/allure-framework/allure2/releases
2. Extract and add to PATH

### Running Tests with Allure

#### Local Execution with HTML Report

**Step 1: Run tests with Allure results collection:**
```bash
# Run all tests
pytest tests/ -v --alluredir=reports/allure-results

# Run specific test suite
pytest tests/ui/ -v --alluredir=reports/allure-results

# Run only API tests
pytest tests/api/ -v --alluredir=reports/allure-results

# Run smoke tests
pytest -m smoke -v --alluredir=reports/allure-results
```

**Step 2: Generate HTML report:**
```bash
allure generate reports/allure-results -o reports/allure-report --clean
```

**Step 3: View report (auto-opens in browser):**
```bash
allure open reports/allure-report
```

#### One-Command Execution

Create a convenience script:
```bash
# Save as: run_tests_with_allure.sh
#!/bin/bash
pytest tests/ -v --alluredir=reports/allure-results && \
allure generate reports/allure-results -o reports/allure-report --clean && \
allure open reports/allure-report
```

Run with:
```bash
chmod +x run_tests_with_allure.sh
./run_tests_with_allure.sh
```

### Allure Report Features

#### 1. Dashboard Overview
- **Pass/Fail Rate** pie chart
- **Test Execution Timeline** showing duration
- **Flaky Tests** percentage
- **Test Breakdown** by category

#### 2. Behaviors View
Shows tests organized by:
- **Epic** (major feature)
- **Feature** (sub-component)
- **Story** (specific requirement)

#### 3. Categories
- **By Severity**: Critical, Major, Minor, Trivial
- **By Status**: Passed, Failed, Skipped, Broken
- **By Duration**: Slow, Normal, Fast

#### 4. Failures & Errors
Detailed analysis including:
- Stack traces
- Attached screenshots
- Log files
- Execution duration

#### 5. Timeline
Shows execution order and duration of each test

#### 6. Retries
Displays retried tests and their history

### Adding Allure Decorators to Tests

Enhance test reports with descriptive metadata:

```python
import allure

@allure.feature("Authentication")
@allure.story("User Login")
@allure.title("Successful login with valid credentials")
@allure.description("Verify user can login with valid admin credentials")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.login
def test_login_successful_navigation(login_page):
    """Test successful login and navigation to dashboard."""
    login_page.login()
    assert login_page.is_user_logged_in()
```

#### Allure Decorator Reference

| Decorator | Purpose | Example |
|-----------|---------|---------|
| `@allure.feature()` | Group tests by feature | `@allure.feature("Employee Management")` |
| `@allure.story()` | Group tests by user story | `@allure.story("Add New Employee")` |
| `@allure.title()` | Custom test name in report | `@allure.title("Verify employee creation")` |
| `@allure.description()` | Test description | `@allure.description("Test adds new employee...")` |
| `@allure.severity()` | Test priority level | `@allure.severity(allure.severity_level.CRITICAL)` |
| `@allure.step()` | Document test steps | `@allure.step("Fill employee form")` |

#### Severity Levels

```python
import allure

@allure.severity(allure.severity_level.CRITICAL)    # Must pass
@allure.severity(allure.severity_level.MAJOR)       # Important
@allure.severity(allure.severity_level.NORMAL)      # Regular
@allure.severity(allure.severity_level.MINOR)       # Nice to have
@allure.severity(allure.severity_level.TRIVIAL)     # Low priority
```

### Attaching Data to Allure Reports

```python
import allure

def test_with_attachments(page):
    # ... test code ...
    
    # Attach screenshot
    screenshot = page.screenshot()
    allure.attach(
        screenshot,
        name="page_screenshot",
        attachment_type=allure.attachment_type.PNG
    )
    
    # Attach JSON
    allure.attach(
        '{"key": "value"}',
        name="response_json",
        attachment_type=allure.attachment_type.JSON
    )
    
    # Attach HTML
    allure.attach(
        "<h1>Test Report</h1>",
        name="report_html",
        attachment_type=allure.attachment_type.HTML
    )
```

### Generating Allure Reports in CI/CD

See [CI/CD Integration](#cicd-integration) section below.

---

## OrangeHRM Load Testing (50 Users)

### What is This Test Plan?

A JMeter load test that simulates **50 concurrent users** logging into OrangeHRM simultaneously and performing login/logout cycles. This validates:
- System stability under concurrent logins
- Response times at peak load
- Error handling with high concurrent user count
- Server resource utilization

### Test Scenarios Covered

1. **GET Login Page** - Retrieve login form (check: page loads)
2. **POST Login Credentials** - Submit username/password (check: 200/302 status)
3. **GET Dashboard** - Access user dashboard (check: dashboard content loads)
4. **GET Logout** - Perform logout (check: 200/302 status)

Each user cycles through all 4 steps, repeated 3 times.

### Load Test Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| **THREADS** | 50 | Number of concurrent users |
| **RAMPUP** | 60 | Time in seconds to ramp up to 50 users (1 user/second) |
| **LOOPS** | 3 | Number of times each user repeats the scenario |
| **USERNAME** | Admin | OrangeHRM login username |
| **PASSWORD** | admin123 | OrangeHRM login password |
| **DURATION** | 600s | Maximum test execution time (10 minutes) |

**Total Expected Requests**: 50 users × 3 loops × 4 endpoints = 600 requests

### Installation & Setup

#### 1. Install Apache JMeter

**macOS (Homebrew):**
```bash
brew install jmeter
```

**Ubuntu/Debian:**
```bash
sudo apt-get install jmeter
```

**Windows:**
1. Download: https://jmeter.apache.org/download_jmeter.cgi
2. Extract and run `bin/jmeter.bat`

**Manual (All Platforms):**
1. Download: https://jmeter.apache.org/download_jmeter.cgi
2. Extract to preferred location
3. Add `bin/` directory to PATH

#### 2. Verify Installation
```bash
jmeter --version
```

Expected output: `Apache JMeter 5.5` (or newer)

### Running the Load Test

#### Method 1: GUI Mode (Visual, Recommended for First Run)

```bash
# Start JMeter GUI
jmeter

# In GUI:
# 1. File → Open → tests/loadtest/orangehrm_login_loadtest.jmx
# 2. Review threads, rampup, loops settings
# 3. Click green "Start" button (top toolbar)
# 4. Watch real-time execution in results viewers
# 5. Stop when complete (red stop button)
```

**Results Viewers Available:**
- **View Results Table** - Detailed pass/fail per request
- **Graph Results** - Response time trends over time
- **Summary Report** - Aggregated metrics

#### Method 2: CLI Mode (Recommended for CI/CD)

**Light Load (5 users, validation run):**
```bash
jmeter -n \
  -t tests/loadtest/orangehrm_login_loadtest.jmx \
  -l results/loadtest_light.jtl \
  -j logs/jmeter_light.log \
  -Jthreads=5 \
  -Jrampup=10 \
  -Jloops=2
```

**Standard Load (50 users, full test):**
```bash
jmeter -n \
  -t tests/loadtest/orangehrm_login_loadtest.jmx \
  -l results/loadtest_standard.jtl \
  -j logs/jmeter_standard.log \
  -Jthreads=50 \
  -Jrampup=60 \
  -Jloops=3
```

**Heavy Load (100 users, stress test):**
```bash
jmeter -n \
  -t tests/loadtest/orangehrm_login_loadtest.jmx \
  -l results/loadtest_heavy.jtl \
  -j logs/jmeter_heavy.log \
  -Jthreads=100 \
  -Jrampup=60 \
  -Jloops=2
```

**Endurance Test (30 users, long-running):**
```bash
jmeter -n \
  -t tests/loadtest/orangehrm_login_loadtest.jmx \
  -l results/loadtest_endurance.jtl \
  -j logs/jmeter_endurance.log \
  -Jthreads=30 \
  -Jrampup=30 \
  -Jloops=50 \
  -Jduration=1800
```

### Analyzing Load Test Results

#### 1. Basic Console Output
```
Summary:
    Samples: 600
    Average: 1245 ms
    Min: 234 ms
    Max: 8932 ms
    Errors: 2 (0.33%)
    Throughput: 1.2/sec
```

#### 2. JTL File Analysis
```bash
# View summary of results
grep "Latency" results/loadtest_standard.jtl | head -10

# Count successful requests
grep "success=\"true\"" results/loadtest_standard.jtl | wc -l

# Count failed requests
grep "success=\"false\"" results/loadtest_standard.jtl | wc -l
```

#### 3. Convert JTL to CSV
```bash
# Generate CSV report
jmeter -l results/loadtest_standard.jtl \
  -o reports/jmeter_report \
  -g results/loadtest_standard.jtl
```

#### 4. Key Metrics to Monitor

| Metric | Good | Warning | Critical |
|--------|------|---------|----------|
| **Average Response Time** | < 500ms | 500-2000ms | > 2000ms |
| **95th Percentile** | < 1000ms | 1-3000ms | > 3000ms |
| **99th Percentile** | < 2000ms | 2-5000ms | > 5000ms |
| **Error Rate** | 0% | 0.1-1% | > 1% |
| **Throughput** | > 50/sec | 20-50/sec | < 20/sec |

### Expected Results (50 Users, 3 Loops)

```
ThreadGroup Results: 600 samples
  Successful: 594 (99%)
  Failed: 6 (1%)
  
Endpoints:
  GET /auth/login: Avg 450ms, Min 200ms, Max 3500ms
  POST /auth/validate: Avg 1200ms, Min 400ms, Max 8932ms
  GET /dashboard: Avg 650ms, Min 300ms, Max 4200ms
  GET /auth/logout: Avg 380ms, Min 150ms, Max 2100ms
  
Overall:
  Average Response Time: 1020ms
  95th Percentile: 3200ms
  Throughput: 0.98 req/sec
```

### Troubleshooting Load Tests

#### Issue: "Connection Refused"
**Cause**: OrangeHRM server unreachable
```bash
# Verify server is running
curl -I https://opensource-demo.orangehrmlive.com/web/index.php/auth/login

# Check JMeter settings
# Base URL should be: https://opensource-demo.orangehrmlive.com
```

#### Issue: Many Failures (> 5%)
**Cause**: Server overloaded or rate-limiting
```bash
# Increase rampup time to reduce concurrent spike
jmeter -n -t tests/loadtest/orangehrm_login_loadtest.jmx \
  -Jthreads=50 \
  -Jrampup=120  # Increased from 60

# Reduce number of users
jmeter -n -t tests/loadtest/orangehrm_login_loadtest.jmx \
  -Jthreads=30  # Reduced from 50
```

#### Issue: "Out of Memory"
**Cause**: JMeter running out of heap space
```bash
# Increase JMeter heap size
export JVM_ARGS="-Xms2g -Xmx4g"
jmeter -n -t tests/loadtest/orangehrm_login_loadtest.jmx
```

#### Issue: Slow Response Times
**Cause**: Server under stress or network latency
```bash
# Check server logs for errors
# Monitor server CPU/Memory during test
# Try running test during off-peak hours
# Consider reducing concurrent users
```

### Creating Custom Load Tests

To modify the load test for different scenarios:

**In JMeter GUI:**
1. Open the test plan file
2. Modify ThreadGroup settings:
   - Right-click ThreadGroup → Edit
   - Adjust "Number of Threads", "Ramp-Up Period", "Loop Count"
3. Modify User Defined Variables:
   - Edit THREADS, RAMPUP, LOOPS, USERNAME, PASSWORD
4. Add/remove HTTP Samplers as needed
5. Save the file

**Example: Create test for employee creation (advanced):**
1. Duplicate login flow (GET /auth/login, POST /auth/validate)
2. Add HTTP sampler for GET /web/index.php/pim/addEmployee
3. Add HTTP sampler for POST /web/index.php/pim/addEmployee with employee data
4. Configure assertions for 200 response and success message

---

## CI/CD Integration

### GitHub Actions Integration

The GitHub Actions workflow automatically:
1. Installs allure-pytest
2. Runs tests with `--alluredir` flag
3. Generates Allure HTML reports
4. Uploads reports as artifacts

**View Reports:**
1. Go to GitHub Actions workflow run
2. Scroll to "Artifacts" section
3. Download `api-test-reports`, `ui-test-reports`, or `smoke-test-reports`
4. Extract and open `allure-report/index.html` in browser

### Manual Allure Commandline Installation in CI

If not using package manager:
```yaml
- name: Install Allure CLI
  run: |
    curl -o allure-2.25.0.zip https://github.com/allure-framework/allure2/releases/download/2.25.0/allure-2.25.0.zip
    unzip allure-2.25.0.zip
    export PATH=$PATH:$(pwd)/allure-2.25.0/bin
```

### Load Test Results Archival

To store load test results:
```yaml
- name: Archive Load Test Results
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: loadtest-results
    path: |
      results/
      logs/jmeter*.log
```

---

## Best Practices

### Allure Report Best Practices

1. **Use Meaningful Test Names**
   ```python
   @allure.title("Verify employee creation with valid data")
   def test_add_employee_with_valid_data(employee_page):
   ```

2. **Add Detailed Descriptions**
   ```python
   @allure.description("""
   Verify that a new employee can be created with valid data:
   - First Name: John
   - Last Name: Doe
   - Employee ID: Unique 8-digit number
   Assertions: Success message displayed
   """)
   ```

3. **Use Severity Levels Appropriately**
   - CRITICAL: Login, core workflows
   - MAJOR: Important features
   - NORMAL: Standard functionality
   - MINOR: UI enhancements
   - TRIVIAL: Nice-to-have

4. **Attach Relevant Data**
   - Screenshots on failure (already done in conftest.py)
   - Request/response bodies for API tests
   - Log snippets for error context

5. **Create Test Suites with Features**
   ```python
   @allure.feature("Employee Management")
   @allure.story("Create Employee")
   ```

### Load Test Best Practices

1. **Start Small, Scale Gradually**
   - Run with 5 users first
   - Increase to 50 users
   - Then stress test with 100+ users

2. **Run During Off-Peak Hours**
   - Reduces impact on actual users
   - Provides more stable baseline metrics

3. **Monitor Server Resources**
   - CPU usage should stay < 80%
   - Memory usage should stay < 80%
   - Disk I/O should remain normal

4. **Document Test Results**
   - Screenshot graphs before/after
   - Save JTL files with timestamp
   - Track trends over time

5. **Test Real Scenarios**
   - Use actual usernames/passwords
   - Simulate realistic think time between actions
   - Test during expected peak usage times

---

## Quick Reference Commands

### Allure
```bash
# Run tests with Allure
pytest tests/ -v --alluredir=reports/allure-results

# Generate report
allure generate reports/allure-results -o reports/allure-report --clean

# Open report
allure open reports/allure-report

# All in one
pytest tests/ -v --alluredir=r && allure generate r -o report && allure open report
```

### JMeter
```bash
# Light load test
jmeter -n -t tests/loadtest/orangehrm_login_loadtest.jmx -Jthreads=5 -Jloops=2

# Standard load test (50 users)
jmeter -n -t tests/loadtest/orangehrm_login_loadtest.jmx

# GUI mode
jmeter

# Generate report from JTL
jmeter -l results/loadtest.jtl -o reports/jmeter_report -g results/loadtest.jtl
```

---

## Support & Troubleshooting

### Common Issues

**Q: Allure report not generating?**
A: Ensure `allure-commandline` is installed: `brew install allure` (macOS)

**Q: JMeter shows "Connection Refused"?**
A: Verify OrangeHRM is accessible: `curl https://opensource-demo.orangehrmlive.com`

**Q: Load test results show 100% failure?**
A: Check that username/password are correct in test variables (Admin/admin123)

**Q: GitHub Actions taking too long?**
A: Allure generation adds ~2 minutes. Disable if not needed: remove `Generate Allure Report` step

For more help, see:
- Allure Docs: https://docs.qameta.io/allure
- JMeter Docs: https://jmeter.apache.org/usermanual/index.html
- OrangeHRM: https://opensource-demo.orangehrmlive.com
