# QA Takehome: REST Countries API & OrangeHRM UI Automation

A comprehensive test automation project covering API and UI testing for two systems:
- **REST Countries API** (v3.1) - Public API for country data
- **OrangeHRM** - Open-source HR management system

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Quick Start](#quick-start)
3. [Tech Stack](#tech-stack)
4. [Project Structure](#project-structure)
5. [Running Tests](#running-tests)
6. [Test Coverage](#test-coverage)
7. [Architecture Decisions](#architecture-decisions)
8. [Known Limitations](#known-limitations)
9. [Future Enhancements](#future-enhancements)
10. [Troubleshooting](#troubleshooting)

---

## 🎯 Project Overview

### Objectives
✅ Verify API behavior and contract through automated tests  
✅ Automate UI critical flows (login, employee management)  
✅ Validate data consistency between UI and API  
✅ Map all requirements to test cases  
✅ Provide traceability matrix for coverage  

### What's Covered
- **API Tests:** REST Countries endpoints (name, code, region, currency, language filters)
- **UI Tests:** OrangeHRM login, navigation, and add employee flow
- **Negative Tests:** Error handling, edge cases, validation
- **Data Validation:** Verify saved data appears in system

---

## ⚡ Quick Start

### Prerequisites
- Python 3.8+
- pip
- Git
- macOS/Linux/Windows

### Setup (1-2 minutes)

```bash
# Clone repository
git clone <repo-url>
cd qa-takehome

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install
```

### Run All Tests

```bash
# Run all tests (API + UI)
pytest

# Run with HTML report
pytest --html=reports/report.html --self-contained-html
```

### Run Specific Test Suites

```bash
# API tests only
pytest tests/api/ -v

# UI tests only
pytest tests/ui/ -v

# Specific test file
pytest tests/api/test_country_by_name.py -v

# Specific test
pytest tests/api/test_country_by_name.py::TestCountryByName::test_get_country_by_valid_name -v

# By marker
pytest -m api         # API tests
pytest -m ui          # UI tests
pytest -m smoke       # Smoke tests
pytest -m negative    # Negative tests
```

---

## 🛠️ Tech Stack

| Component | Technology | Rationale |
|---|---|---|
| **API Testing** | Python + Requests | Lightweight, intuitive API client; excellent for REST API testing |
| **UI Testing** | Python + Playwright | Modern, cross-browser, better performance than Selenium; excellent DevTools integration |
| **Test Framework** | pytest | Most Pythonic; powerful fixtures; excellent reporting |
| **Language** | Python | Single language stack reduces context switching and complexity |
| **Test Data** | Faker | Generates realistic test data for regression testing |
| **Reporting** | pytest-html | Built-in HTML reports; self-contained output |

### Why These Choices?
1. **Consistency:** Single Python codebase for both API and UI (easier maintenance)
2. **Reliability:** Playwright's auto-waiting reduces flakiness vs Selenium
3. **Speed:** Requests is lightweight; Playwright is fast
4. **Simplicity:** pytest fixtures are cleaner than JUnit annotations
5. **Flexibility:** Easy to extend with custom utilities and helpers

---

## 📁 Project Structure

```
qa-takehome/
├── tests/                          # Test suites
│   ├── api/
│   │   ├── test_country_by_name.py        # Name/full-text search tests
│   │   ├── test_country_filters.py        # Region, currency, language filter tests
│   │   └── test_negative_cases.py         # Error handling, edge cases
│   └── ui/
│       ├── test_login.py                  # Login and authentication tests
│       ├── test_navigation.py             # Menu navigation tests
│       └── test_add_employee.py           # Employee CRUD tests
│
├── pages/                          # Page Object Models (UI)
│   ├── login_page.py               # Login page interactions
│   ├── dashboard_page.py           # Dashboard/main page
│   ├── pim_page.py                 # PIM (employee) list page
│   └── employee_page.py            # Employee form (add/edit)
│
├── api/                            # API Client
│   └── restcountries_client.py     # REST Countries API wrapper
│
├── utils/                          # Utilities & Helpers
│   ├── config.py                   # Configuration & URLs
│   └── base_page.py                # Base page class (common methods)
│
├── data/                           # Test Data
│   └── test_data.py                # Constants, test data, selectors
│
├── docs/                           # Documentation
│   ├── functional-test-cases.md    # Detailed test case specifications
│   └── coverage-matrix.md          # Requirements -> Test traceability
│
├── conftest.py                     # pytest configuration & fixtures
├── pytest.ini                      # pytest settings
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

---

## 🧪 Running Tests

### Run All Tests
```bash
pytest
```

### Run with Specific Options

```bash
# Verbose output with full paths
pytest -vv

# Stop on first failure
pytest -x

# Show local variables on failure
pytest -l

# Run last failed tests
pytest --lf

# Run with specific markers
pytest -m smoke
pytest -m "api and not negative"

# Parallel execution (install pytest-xdist first)
pytest -n auto
```

### Generate Reports

```bash
# HTML report (interactive)
pytest --html=reports/report.html --self-contained-html

# JUnit XML (for CI/CD)
pytest --junit-xml=reports/junit.xml

# Coverage report (install pytest-cov first)
pytest --cov=tests --cov-report=html
```

### Environment Variables

```bash
# Configure browser
export BROWSER=chromium          # chromium, firefox, webkit
export HEADLESS=true            # true/false
export SLOW_MO=100              # milliseconds for debugging

# Configure timeouts
export TIMEOUT=30000            # milliseconds

# Run tests
pytest
```

---

## 📊 Test Coverage

### Coverage Summary
- **API Tests:** 9 automated tests covering 9/9 requirements (100%)
- **UI Tests:** 12+ automated tests covering 6/6 requirements (100%)
- **Data Validation:** 2 scenarios validating data consistency
- **Negative Tests:** 6+ edge case and error handling tests
- **Total Automated Test Cases:** 22+

### Coverage by Requirement Priority

| Priority | Count | Coverage | Status |
|---|---|---|---|
| Must-have | 12 | 100% | ✅ |
| Should-have | 3 | 100% | ✅ |
| **Total** | **15** | **100%** | **✅** |

### Coverage by System

**REST Countries API:**
- ✅ Get by name (partial match)
- ✅ Get by name (full text match)
- ✅ Get by code (alpha2/alpha3)
- ✅ Get all with fields parameter
- ✅ Error cases (404, 400)
- ✅ Region filter
- ✅ Currency filter
- ✅ Language filter

**OrangeHRM UI:**
- ✅ Valid login
- ✅ Invalid login with error handling
- ✅ Navigation menus
- ✅ Add employee form
- ✅ Valid employee submission
- ✅ Form validation (required fields)
- ✅ Data consistency (employee appears in list)

See [docs/coverage-matrix.md](docs/coverage-matrix.md) for detailed traceability.

---

## 🏗️ Architecture Decisions

### 1. Page Object Model (UI)
```python
# ✅ Clean separation of concerns
# ✅ Reusable components
# ✅ Easy maintenance
class LoginPage(BasePage):
    USERNAME_INPUT = "input[name='username']"
    def login(self, username, password):
        self.fill(self.USERNAME_INPUT, username)
        ...
```

### 2. API Client Wrapper
```python
# ✅ Centralized API logic
# ✅ Consistent error handling
# ✅ Easy to mock/stub
client = RestCountriesClient()
response = client.get_country_by_name("France")
```

### 3. Fixture-Based Setup
```python
# ✅ Clean test code
# ✅ Reusable components
# ✅ Automatic cleanup
@pytest.fixture
def api_client():
    return RestCountriesClient()

def test_api(api_client):
    response = api_client.get_country_by_name("France")
```

### 4. Configuration Management
```python
# ✅ Environment-agnostic
# ✅ Easy to override
# ✅ Single source of truth
ORANGEHRM_BASE_URL = "https://opensource-demo.orangehrmlive.com"
API_TIMEOUT = 10
```

### Why These Patterns?
- **Maintainability:** Easy to update selectors/APIs in one place
- **Reusability:** Share fixtures and page objects across tests
- **Readability:** Tests read like business scenarios
- **Scalability:** Add new tests/pages without duplicating code

---

## 📝 Example Tests

### API Test Example

```python
@pytest.mark.api
def test_get_country_by_valid_name(api_client, country_test_data):
    """Test: Get country by valid name returns 200 and JSON array."""
    response = api_client.get_country_by_name("France")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "name" in data[0]
```

### UI Test Example

```python
@pytest.mark.ui
def test_login_with_valid_credentials(login_page, dashboard_page):
    """Test: Login with valid credentials leads to dashboard."""
    login_page.wait_for_page_load()
    login_page.login_with_valid_credentials()
    
    dashboard_page.wait_for_dashboard_load()
    assert dashboard_page.is_user_logged_in()
```

### Data Consistency Example

```python
def test_add_employee_then_verify_in_list(pim_page, employee_page):
    """Test: Added employee appears in list."""
    # Add employee
    employee_page.submit_employee_form("John", "Doe", "EMP001")
    assert employee_page.is_success_message_displayed()
    
    # Verify in list
    pim_page.search_employee("John Doe")
    assert pim_page.is_employee_in_list("John Doe")
```

---

## 🔍 Key Features

### 1. Comprehensive Logging
```
INFO - Starting login with valid credentials test
INFO - Waiting for login page to load
INFO - Entering username: Admin
INFO - Clicking login button
INFO - Waiting for dashboard to load
✓ Successfully logged in with valid credentials
```

### 2. Smart Waits
- Auto-waiting for elements (Playwright)
- Network idle detection
- Configurable timeouts
- No arbitrary sleeps (except where needed)

### 3. Test Data
- Realistic test data using Faker
- Centralized test constants
- Reusable across tests

### 4. Error Handling
- Graceful error messages
- Screenshots on failure (in UI tests)
- Full stack traces
- HTTP response details (in API tests)

---

## ⚠️ Known Limitations

### 1. OrangeHRM Backend Database Access
**Limitation:** Cannot directly query OrangeHRM database  
**Impact:** Data validation relies on UI/API state  
**Workaround:** Implemented UI-based verification (search employee list)  
**Future:** Document if REST API available for backend validation  

### 2. Dynamic Selectors
**Limitation:** Some OrangeHRM selectors are generated/fragile  
**Impact:** Tests may break with UI updates  
**Mitigation:** Using robust selectors (text-based, aria-labels)  
**Future:** Add visual regression testing; implement selector auto-healing  

### 3. Test Environment
**Current:** Public demo site (https://opensource-demo.orangehrmlive.com)  
**Limitation:** Shared environment; data changes affect tests  
**Impact:** Tests use unique employee IDs to avoid collisions  
**Future:** Dedicated test environment  

### 4. No API Authentication
**Note:** REST Countries API has no auth; OrangeHRM uses demo credentials  
**Impact:** No token refresh/OAuth testing  
**Future:** Test auth in dedicated environment  

### 5. Performance Testing
**Out of Scope:** Load/stress testing not included  
**Why:** PRD scope limited to functional testing  
**Future:** Add performance baselines, spike tests  

### 6. Mobile Testing
**Out of Scope:** Only desktop tested (Playwright at 1920x1080)  
**Future:** Add mobile viewport tests  

---

## 🚀 Future Enhancements

### High Priority (Next Sprint)
1. **API Contract Testing**
   - Add OpenAPI schema validation
   - Auto-generate tests from spec
   
2. **More UI Flows**
   - Edit employee
   - Delete employee
   - Leave request flow
   
3. **Test Data Cleanup**
   - Auto-delete test employees
   - Reset test data between runs
   
4. **CI/CD Integration**
   - GitHub Actions workflow
   - Automated test runs on PR
   - Slack notifications

### Medium Priority (Q2)
5. **Visual Regression**
   - Screenshot comparison
   - CSS breakage detection
   
6. **API Mocking**
   - Mock REST Countries for faster tests
   - Contract verification
   
7. **Performance Tracking**
   - Response time assertions
   - Performance trend graphs
   
8. **Better Reporting**
   - Custom HTML report
   - Trend analysis
   - Flakiness detection

### Low Priority (Q3+)
9. **Accessibility Testing**
   - WCAG 2.1 AA compliance
   - Screen reader validation
   
10. **Mobile/Responsive**
    - Multi-device testing
    - Responsive design validation
    
11. **Internationalization**
    - Multi-language testing
    - Locale-specific validation
    
12. **Advanced Scenarios**
    - Multi-user workflows
    - Race condition testing
    - Concurrent operations

---

## 🐛 Troubleshooting

### Common Issues

#### 1. "Module not found" Error
```bash
# Ensure venv is activated
source venv/bin/activate  # or: . venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

#### 2. Playwright Browser Issues
```bash
# Reinstall browsers
playwright install

# Clear Playwright cache
rm -rf ~/.cache/ms-playwright/
playwright install
```

#### 3. Tests Hang/Timeout
```python
# Check timeouts in utils/config.py
TIMEOUT = 30000  # milliseconds

# Run single test with verbose output
pytest tests/ui/test_login.py::TestOrangeHRMLogin::test_login_with_valid_credentials -vv
```

#### 4. API 404 Errors
```bash
# Verify API is accessible
curl https://restcountries.com/v3.1/all?fields=name

# Check your internet connection
ping restcountries.com
```

#### 5. OrangeHRM Login Fails
```
Issue: "Invalid credentials" error
Solution: 
- Verify username is "Admin" and password is "admin123"
- Check if demo site is down
- Try: https://opensource-demo.orangehrmlive.com
```

#### 6. Screenshots Not Generated
```bash
# Create reports directory
mkdir -p reports/
mkdir -p screenshots/

# Run tests with failure handling
pytest --tb=short
```

### Debug Mode

```bash
# Run with slow motion (500ms per action)
export SLOW_MO=500
pytest tests/ui/test_login.py

# Run in headed mode (see browser)
export HEADLESS=false
pytest tests/ui/test_login.py

# Run with extra verbose logging
pytest tests/api/test_country_by_name.py -vv --log-cli-level=DEBUG
```

---

## 📚 Additional Resources

### Test Documentation
- [Functional Test Cases](docs/functional-test-cases.md) - Detailed specifications
- [Coverage Matrix](docs/coverage-matrix.md) - Requirements traceability

### External Links
- [REST Countries API Docs](https://restcountries.com/)
- [OrangeHRM Docs](https://orangehrm.readthedocs.io/)
- [Playwright Docs](https://playwright.dev/python/)
- [pytest Docs](https://docs.pytest.org/)

---

## 🤝 Contributing

### Adding New Tests
1. Create test file in appropriate directory (`tests/api/` or `tests/ui/`)
2. Follow naming convention: `test_<feature>.py`
3. Use fixtures from `conftest.py`
4. Add markers: `@pytest.mark.api` or `@pytest.mark.ui`
5. Update coverage matrix

### Adding New Page Objects
1. Create file in `pages/` directory
2. Inherit from `BasePage`
3. Define selectors as class constants
4. Add to fixtures in `conftest.py`

---

## 📄 License

This project is for educational purposes as part of QA engineering interview process.

---

## ✍️ Submission Checklist

- [x] Public GitHub repo created and shared
- [x] README with setup and run instructions
- [x] API automation with single command execution
- [x] UI automation with single command execution
- [x] Data consistency validation (2+ scenarios)
- [x] Functional test cases document
- [x] Coverage matrix with requirement traceability
- [x] All Must-have requirements covered (100%)
- [x] All Should-have requirements covered (100%)
- [x] Well-structured, readable code
- [x] Proper logging and error messages
- [x] CI/CD ready structure

---

## 📞 Contact & Questions

For questions about test design or implementation, please refer to:
1. Inline code comments
2. Functional test cases document
3. Coverage matrix
4. Logger output

---

**Project Version:** 1.0  
**Last Updated:** 2026-05-26  
**Status:** Ready for Evaluation ✅

