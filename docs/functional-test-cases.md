# Functional Test Cases

## API Test Cases

### Story 1: REST Countries API - Retrieve Countries

#### TC-API-1: Get Country by Valid Name
- **ID:** TC-API-1
- **Title:** Retrieve country data by valid name
- **Preconditions:** REST Countries API is accessible
- **Steps:**
  1. Call GET `/v3.1/name/France`
  2. Verify response status code
  3. Parse JSON response
  4. Validate response structure
- **Expected Result:** 
  - Status code: 200
  - Response is JSON array with at least one object
  - Object contains fields: name, capital, region, currencies, languages
  - Country name matches search term
- **Mapped Requirements:** FR-API-1, AC-API-1
- **Test Script:** `tests/api/test_country_by_name.py::TestCountryByName::test_get_country_by_valid_name`

#### TC-API-2: Get Country by Valid Full Name (Exact Match)
- **ID:** TC-API-2
- **Title:** Retrieve country with exact full name match
- **Preconditions:** REST Countries API is accessible
- **Steps:**
  1. Call GET `/v3.1/name/Germany?fullText=true`
  2. Verify response status code
  3. Validate exact match in results
- **Expected Result:**
  - Status code: 200
  - Response contains exact match for "Germany"
  - No partial matches
- **Mapped Requirements:** FR-API-2, AC-API-2
- **Test Script:** `tests/api/test_country_by_name.py::TestCountryByName::test_get_country_by_valid_full_name`

#### TC-API-3: Get Country by Alpha Code
- **ID:** TC-API-3
- **Title:** Retrieve country by alpha2/alpha3 code
- **Preconditions:** REST Countries API is accessible
- **Steps:**
  1. Call GET `/v3.1/alpha/US`
  2. Verify response status code
  3. Validate country object in response
- **Expected Result:**
  - Status code: 200
  - Response contains country object with name, capital, region
  - Alpha code matches requested code
- **Mapped Requirements:** FR-API-3, AC-API-3
- **Test Script:** `tests/api/test_country_filters.py::TestCountryByCode::test_get_country_by_valid_alpha2_code`

#### TC-API-4: Get All Countries with Fields Parameter
- **ID:** TC-API-4
- **Title:** Retrieve all countries with specific fields
- **Preconditions:** REST Countries API is accessible
- **Steps:**
  1. Call GET `/v3.1/all?fields=name,capital,currencies`
  2. Verify response status code
  3. Validate response structure and fields
- **Expected Result:**
  - Status code: 200
  - Response is JSON array with 200+ countries
  - Each object contains only requested fields (or superset)
- **Mapped Requirements:** FR-API-4, AC-API-4
- **Test Script:** `tests/api/test_country_filters.py::TestAllCountries::test_get_all_countries_with_fields`

#### TC-API-5: Get All Countries Without Fields Returns 400
- **ID:** TC-API-5
- **Title:** Validate fields parameter is required for /all endpoint
- **Preconditions:** REST Countries API is accessible
- **Steps:**
  1. Call GET `/v3.1/all` (without fields parameter)
  2. Verify response status code
- **Expected Result:**
  - Status code: 400
  - Error message indicates missing required parameter
- **Mapped Requirements:** FR-API-6, AC-API-6
- **Test Script:** `tests/api/test_country_filters.py::TestAllCountries::test_all_countries_without_fields_returns_400`

#### TC-API-6: Invalid Country Name Returns 404
- **ID:** TC-API-6
- **Title:** Verify 404 response for non-existent country
- **Preconditions:** REST Countries API is accessible
- **Steps:**
  1. Call GET `/v3.1/name/InvalidCountryXYZ`
  2. Verify response status code
- **Expected Result:**
  - Status code: 404
  - Error message or empty response
- **Mapped Requirements:** FR-API-5, AC-API-5
- **Test Script:** `tests/api/test_country_by_name.py::TestCountryByName::test_invalid_country_name_returns_404`

### Story 2: REST Countries API - Filter by Region, Currency, Language

#### TC-API-7: Get Countries by Region
- **ID:** TC-API-7
- **Title:** Filter countries by geographic region
- **Preconditions:** REST Countries API is accessible
- **Steps:**
  1. Call GET `/v3.1/region/Europe`
  2. Verify response status code
  3. Validate all results are in Europe region
- **Expected Result:**
  - Status code: 200
  - Response is array with 40+ countries
  - All countries have region = "Europe"
- **Mapped Requirements:** FR-API-7, AC-API-7
- **Test Script:** `tests/api/test_country_filters.py::TestCountryFilters::test_get_countries_by_region`

#### TC-API-8: Get Countries by Currency
- **ID:** TC-API-8
- **Title:** Filter countries by currency code
- **Preconditions:** REST Countries API is accessible
- **Steps:**
  1. Call GET `/v3.1/currency/usd`
  2. Verify response status code
  3. Validate results contain USD currency
- **Expected Result:**
  - Status code: 200
  - Response is array with countries using USD
  - At least 1 country returned
- **Mapped Requirements:** FR-API-8, AC-API-8
- **Test Script:** `tests/api/test_country_filters.py::TestCountryFilters::test_get_countries_by_currency`

#### TC-API-9: Get Countries by Language
- **ID:** TC-API-9
- **Title:** Filter countries by language
- **Preconditions:** REST Countries API is accessible
- **Steps:**
  1. Call GET `/v3.1/lang/english`
  2. Verify response status code
  3. Validate results contain English language
- **Expected Result:**
  - Status code: 200
  - Response is array with countries speaking English
  - Multiple countries returned
- **Mapped Requirements:** FR-API-9, AC-API-9
- **Test Script:** `tests/api/test_country_filters.py::TestCountryFilters::test_get_countries_by_language`

#### TC-API-10: Invalid Region Returns 404
- **ID:** TC-API-10
- **Title:** Verify 404 for invalid region filter
- **Preconditions:** REST Countries API is accessible
- **Steps:**
  1. Call GET `/v3.1/region/InvalidRegion`
  2. Verify response status code
- **Expected Result:**
  - Status code: 404
- **Mapped Requirements:** FR-API-5
- **Test Script:** `tests/api/test_country_filters.py::TestCountryFilters::test_invalid_region_returns_404`

---

## UI Test Cases

### Story 3: OrangeHRM Login and Dashboard

#### TC-UI-1: Valid Login - Admin Credentials
- **ID:** TC-UI-1
- **Title:** Login with valid admin credentials
- **Preconditions:** 
  - OrangeHRM application is accessible at https://opensource-demo.orangehrmlive.com
  - User is on login page
- **Steps:**
  1. Enter username: "Admin"
  2. Enter password: "admin123"
  3. Click Login button
  4. Wait for dashboard to load
- **Expected Result:**
  - Status code 200 (successful navigation)
  - Dashboard page displays with logged-in state
  - User profile/menu visible
  - Main navigation menu visible (PIM, Leave, Admin, etc.)
- **Mapped Requirements:** FR-UI-1, AC-UI-1
- **Test Script:** `tests/ui/test_login.py::TestOrangeHRMLogin::test_login_with_valid_credentials`

#### TC-UI-2: Invalid Login - Wrong Credentials
- **ID:** TC-UI-2
- **Title:** Login attempt with invalid credentials
- **Preconditions:**
  - OrangeHRM application is accessible
  - User is on login page
- **Steps:**
  1. Enter username: "InvalidUser"
  2. Enter password: "WrongPassword"
  3. Click Login button
  4. Observe error message
- **Expected Result:**
  - Status code remains on login page
  - Error message displayed: "Invalid credentials" or similar
  - Login button remains enabled for retry
  - Form data cleared or ready for new attempt
- **Mapped Requirements:** FR-UI-2, AC-UI-2
- **Test Script:** `tests/ui/test_login.py::TestOrangeHRMLogin::test_login_with_invalid_credentials`

#### TC-UI-3: Navigation Menu Visible After Login
- **ID:** TC-UI-3
- **Title:** Verify main navigation is accessible after login
- **Preconditions:**
  - User has successfully logged in
  - Dashboard page is loaded
- **Steps:**
  1. Verify PIM menu item visible
  2. Verify Leave menu item visible
  3. Verify Admin menu item visible
- **Expected Result:**
  - All main menu items visible and clickable
  - Menu structure intact
- **Mapped Requirements:** FR-UI-3, AC-UI-3
- **Test Script:** `tests/ui/test_navigation.py::TestOrangeHRMNavigation::test_pim_menu_is_accessible`

### Story 4: OrangeHRM Add Employee Flow

#### TC-UI-4: Add Employee Form Displays
- **ID:** TC-UI-4
- **Title:** Add Employee form loads with required fields
- **Preconditions:**
  - User is logged in
  - User is on PIM page
- **Steps:**
  1. Click "Add" button
  2. Wait for form to load
  3. Verify form structure
- **Expected Result:**
  - Form displays with title "Add Employee"
  - Fields visible: First Name, Last Name, Employee ID
  - Save button is enabled
  - Cancel button is present
- **Mapped Requirements:** FR-UI-4, AC-UI-4
- **Test Script:** `tests/ui/test_add_employee.py::TestOrangeHRMAddEmployee::test_add_employee_form_loads`

#### TC-UI-5: Add Employee - Valid Submission
- **ID:** TC-UI-5
- **Title:** Successfully add new employee with valid data
- **Preconditions:**
  - User is logged in and on Add Employee form
- **Steps:**
  1. Enter First Name: "John"
  2. Enter Last Name: "Doe"
  3. Enter Employee ID: "EMP12345"
  4. Click Save button
  5. Wait for success message
- **Expected Result:**
  - Success message displays: "Successfully Saved"
  - Page redirects to employee details/list
  - New employee appears in employee list
  - Employee ID assigned and visible
- **Mapped Requirements:** FR-UI-5, AC-UI-5
- **Test Script:** `tests/ui/test_add_employee.py::TestOrangeHRMAddEmployee::test_add_employee_with_valid_data`

#### TC-UI-6: Add Employee - Missing First Name Validation
- **ID:** TC-UI-6
- **Title:** Form validation - reject submission with missing first name
- **Preconditions:**
  - User is on Add Employee form
- **Steps:**
  1. Leave First Name field empty
  2. Enter Last Name: "Doe"
  3. Enter Employee ID: "EMP12345"
  4. Click Save button
- **Expected Result:**
  - Save does NOT proceed
  - Validation error message displays on First Name field
  - Form remains open with data retained
  - User can correct and retry
- **Mapped Requirements:** FR-UI-6, AC-UI-6
- **Test Script:** `tests/ui/test_add_employee.py::TestOrangeHRMAddEmployee::test_add_employee_missing_first_name`

#### TC-UI-7: Add Employee - Missing Last Name Validation
- **ID:** TC-UI-7
- **Title:** Form validation - reject submission with missing last name
- **Preconditions:**
  - User is on Add Employee form
- **Steps:**
  1. Enter First Name: "John"
  2. Leave Last Name field empty
  3. Enter Employee ID: "EMP12345"
  4. Click Save button
- **Expected Result:**
  - Save does NOT proceed
  - Validation error message displays on Last Name field
  - Form remains open
- **Mapped Requirements:** FR-UI-6, AC-UI-6
- **Test Script:** `tests/ui/test_add_employee.py::TestOrangeHRMAddEmployee::test_add_employee_missing_last_name`

#### TC-UI-8: Add Employee - Verify in List (Data Consistency)
- **ID:** TC-UI-8
- **Title:** Verify added employee appears in employee list
- **Preconditions:**
  - Employee has been successfully added
- **Steps:**
  1. After successful save, navigate to Employee list
  2. Search for newly added employee by name
  3. Verify employee appears in results
- **Expected Result:**
  - Employee list loads
  - Search finds the newly added employee
  - Employee details match what was entered
  - Full name and Employee ID visible
- **Mapped Requirements:** Data consistency validation requirement
- **Test Script:** `tests/ui/test_add_employee.py::TestOrangeHRMAddEmployee::test_add_employee_then_verify_in_list`

---

## Negative Test Cases

#### TC-NEG-1: API - Special Characters in Country Name
- **ID:** TC-NEG-1
- **Title:** Handle special characters in search
- **Preconditions:** REST Countries API is accessible
- **Steps:** Call GET `/v3.1/name/Côte d'Ivoire`
- **Expected Result:** Either 200 with results or 404 (not error)
- **Test Script:** `tests/api/test_negative_cases.py::TestAPIErrorHandling::test_special_characters_in_country_name`

#### TC-NEG-2: API - Empty Country Name
- **ID:** TC-NEG-2
- **Title:** Handle empty country name parameter
- **Preconditions:** REST Countries API is accessible
- **Steps:** Call GET `/v3.1/name/` (empty)
- **Expected Result:** 404 error
- **Test Script:** `tests/api/test_negative_cases.py::TestAPIErrorHandling::test_empty_name_parameter`

#### TC-NEG-3: UI - Multiple Login Attempts
- **ID:** TC-NEG-3
- **Title:** Multiple failed login attempts
- **Preconditions:** User on login page
- **Steps:**
  1. Enter invalid credentials 3 times
  2. Then enter valid credentials
- **Expected Result:** Valid login succeeds after multiple failures
- **Test Script:** `tests/ui/test_login.py::TestOrangeHRMLogin::test_multiple_login_attempts`

#### TC-NEG-4: UI - Cancel Add Employee
- **ID:** TC-NEG-4
- **Title:** Cancel button discards form data
- **Preconditions:** User on Add Employee form with data filled
- **Steps:**
  1. Fill form with data
  2. Click Cancel button
- **Expected Result:** Form closes without saving, returns to list
- **Test Script:** `tests/ui/test_add_employee.py::TestOrangeHRMAddEmployee::test_add_employee_cancel_button`

---

## Test Case Summary
- **Total API Test Cases:** 10
- **Total UI Test Cases:** 8
- **Total Negative Test Cases:** 4
- **Total Functional Test Cases:** 22
