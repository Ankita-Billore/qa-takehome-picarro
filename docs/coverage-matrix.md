# Test Coverage Matrix

## Overview
This document maps all functional requirements and acceptance criteria to their corresponding automated tests and test cases.

---

## API Coverage Matrix

### Story 1: REST Countries - Retrieve Countries

| Requirement ID | Requirement Description | Acceptance Criteria | Test Case ID | Automated Test Script | Coverage Status |
|---|---|---|---|---|---|
| FR-API-1 | GET /v3.1/name/{name} returns 200 and valid JSON array for valid name | AC-API-1: Valid country name returns 200 and array with name, capital, region | TC-API-1 | test_country_by_name.py::test_get_country_by_valid_name | ✅ Covered |
| FR-API-2 | GET /v3.1/name/{name}?fullText=true returns 200 for exact full name match | AC-API-2: Full name match returns exact match | TC-API-2 | test_country_by_name.py::test_get_country_by_valid_full_name | ✅ Covered |
| FR-API-3 | GET /v3.1/alpha/{code} returns 200 and valid country object(s) for valid code | AC-API-3: Valid alpha2/alpha3 code returns 200 and country object | TC-API-3 | test_country_filters.py::test_get_country_by_valid_alpha2_code | ✅ Covered |
| FR-API-4 | GET /v3.1/all?fields=...returns 200 and array; response respects requested fields | AC-API-4: /all endpoint with fields returns 200 with requested fields | TC-API-4 | test_country_filters.py::test_get_all_countries_with_fields | ✅ Covered |
| FR-API-5 | Invalid name/code returns 404 (or documented error) | AC-API-5: Invalid country name/code returns 404 | TC-API-6, TC-API-10 | test_country_by_name.py::test_invalid_country_name_returns_404 | ✅ Covered |
| FR-API-6 | GET /v3.1/all without fields returns 400 (or documented) | AC-API-6: Missing fields parameter returns 400 | TC-API-5 | test_country_filters.py::test_all_countries_without_fields_returns_400 | ✅ Covered |

### Story 2: REST Countries - Filter by Region, Currency, Language

| Requirement ID | Requirement Description | Acceptance Criteria | Test Case ID | Automated Test Script | Coverage Status |
|---|---|---|---|---|---|
| FR-API-7 | GET /v3.1/region/{region} returns 200 and array of countries in region | AC-API-7: Region filter returns countries in that region | TC-API-7 | test_country_filters.py::test_get_countries_by_region | ✅ Covered |
| FR-API-8 | GET /v3.1/currency/{currency} returns 200 and array | AC-API-8: Currency filter returns countries using currency | TC-API-8 | test_country_filters.py::test_get_countries_by_currency | ✅ Covered |
| FR-API-9 | GET /v3.1/lang/{language} returns 200 and array | AC-API-9: Language filter returns countries speaking language | TC-API-9 | test_country_filters.py::test_get_countries_by_language | ✅ Covered |

### API Coverage Summary
- **Must-have FRs:** 6/6 covered (100%)
- **Should-have FRs:** 3/3 covered (100%)
- **Total API Requirements:** 9/9 covered ✅

---

## UI Coverage Matrix

### Story 3: OrangeHRM - Login and Dashboard

| Requirement ID | Requirement Description | Acceptance Criteria | Test Case ID | Automated Test Script | Coverage Status |
|---|---|---|---|---|---|
| FR-UI-1 | Valid login leads to dashboard / home and visible logged-in state | AC-UI-1: Valid credentials lead to dashboard with logged-in state (menu, user indicator) | TC-UI-1 | test_login.py::test_login_with_valid_credentials | ✅ Covered |
| FR-UI-2 | Invalid login shows error and does not navigate | AC-UI-2: Invalid credentials show error and remain on login | TC-UI-2 | test_login.py::test_login_with_invalid_credentials | ✅ Covered |
| FR-UI-3 | Main navigation (PIM, Leave) is visible and usable when logged in | AC-UI-3: PIM and Leave modules accessible from main navigation | TC-UI-3 | test_navigation.py::test_pim_menu_is_accessible | ✅ Covered |

### Story 4: OrangeHRM - Add Employee Business Flow

| Requirement ID | Requirement Description | Acceptance Criteria | Test Case ID | Automated Test Script | Coverage Status |
|---|---|---|---|---|---|
| FR-UI-4 | Add Employee (or chosen flow) form loads and has required fields | AC-UI-4: Add Employee form opens with required fields | TC-UI-4 | test_add_employee.py::test_add_employee_form_loads | ✅ Covered |
| FR-UI-5 | Valid form submission completes with success and data visible | AC-UI-5: Valid submission saves and employee appears in list | TC-UI-5, TC-UI-8 | test_add_employee.py::test_add_employee_with_valid_data | ✅ Covered |
| FR-UI-6 | Missing required fields show validation and block submit | AC-UI-6: Missing first name/last name shows validation | TC-UI-6, TC-UI-7 | test_add_employee.py::test_add_employee_missing_first_name | ✅ Covered |

### UI Coverage Summary
- **Must-have FRs:** 6/6 covered (100%)
- **Total UI Requirements:** 6/6 covered ✅

---

## Data Consistency & Validation Coverage

| Scenario ID | Scenario Description | Validation Approach | Test Case ID | Coverage Status |
|---|---|---|---|---|
| DC-1 | After adding employee via UI, verify data appears in employee list | Search for new employee by name in PIM list | TC-UI-8 | ✅ Covered |
| DC-2 | API response data consistency across endpoints | Same country retrieved by name and code returns identical data | test_country_filters.py::test_multiple_filters_consistency | ✅ Covered |
| DC-3 | API response structure validates against schema | Verify all responses contain expected fields | test_country_by_name.py::test_response_structure_for_country_by_name | ✅ Covered |

---

## Negative Test Case Coverage

| Test Case ID | Scenario | Type | Covered |
|---|---|---|---|
| TC-NEG-1 | Special characters in country name | Negative/Edge case | ✅ Covered |
| TC-NEG-2 | Empty country name parameter | Negative/Boundary | ✅ Covered |
| TC-NEG-3 | Multiple failed login attempts | Negative/Recovery | ✅ Covered |
| TC-NEG-4 | Cancel form (discard changes) | Negative/State | ✅ Covered |
| TC-NEG-5 | Case insensitivity handling | Edge case | ✅ Covered |
| TC-NEG-6 | Invalid region filter | Negative/Error | ✅ Covered |

---

## Acceptance Criteria Traceability

### AC-API-1 through AC-API-6
- **AC-API-1:** Valid country name → ✅ test_country_by_name.py::test_get_country_by_valid_name
- **AC-API-2:** Full name exact match → ✅ test_country_by_name.py::test_get_country_by_valid_full_name
- **AC-API-3:** Alpha code lookup → ✅ test_country_filters.py::test_get_country_by_valid_alpha2_code
- **AC-API-4:** /all endpoint with fields → ✅ test_country_filters.py::test_get_all_countries_with_fields
- **AC-API-5:** Invalid input returns 404 → ✅ test_country_by_name.py::test_invalid_country_name_returns_404
- **AC-API-6:** Missing fields returns 400 → ✅ test_country_filters.py::test_all_countries_without_fields_returns_400

### AC-API-7 through AC-API-9
- **AC-API-7:** Region filter → ✅ test_country_filters.py::test_get_countries_by_region
- **AC-API-8:** Currency filter → ✅ test_country_filters.py::test_get_countries_by_currency
- **AC-API-9:** Language filter → ✅ test_country_filters.py::test_get_countries_by_language

### AC-UI-1 through AC-UI-6
- **AC-UI-1:** Valid login → ✅ test_login.py::test_login_with_valid_credentials
- **AC-UI-2:** Invalid login error → ✅ test_login.py::test_login_with_invalid_credentials
- **AC-UI-3:** Navigation accessible → ✅ test_navigation.py::test_pim_menu_is_accessible
- **AC-UI-4:** Add Employee form → ✅ test_add_employee.py::test_add_employee_form_loads
- **AC-UI-5:** Valid submission → ✅ test_add_employee.py::test_add_employee_with_valid_data
- **AC-UI-6:** Validation errors → ✅ test_add_employee.py::test_add_employee_missing_first_name

---

## Coverage Statistics

### By Type
| Category | Total | Covered | Percentage |
|---|---|---|---|
| API Tests (Must-have) | 6 | 6 | 100% |
| API Tests (Should-have) | 3 | 3 | 100% |
| UI Tests | 6 | 6 | 100% |
| Data Consistency Tests | 3 | 3 | 100% |
| Negative/Edge Cases | 6+ | 6+ | 100% |

### By Requirement Priority
| Priority | Total | Covered | Coverage |
|---|---|---|---|
| Must-have | 12 | 12 | ✅ 100% |
| Should-have | 3 | 3 | ✅ 100% |
| **Total** | **15** | **15** | **✅ 100%** |

---

## Known Gaps & Limitations

| Gap | Reason | Mitigation |
|---|---|---|
| Database direct validation | OrangeHRM backend DB not accessible | Use UI/API state as source of truth (documented) |
| Performance testing | Out of scope per PRD | Future work: Load testing, benchmarking |
| Security testing | Out of scope per PRD | Future work: Penetration testing, auth validation |
| Mobile responsive UI | Out of scope per PRD | Current: Desktop only via Playwright |
| API contract schema validation | Currently manual inspection | Future: Add OpenAPI/JSON Schema validation |
| Accessibility testing | Not in scope | Future: WCAG compliance checks |

---

## Recommendations for Extension

### High Priority
1. **Add contract testing:** Validate API responses against OpenAPI schema
2. **Expand employee flows:** Test Edit, Delete, Search employee scenarios
3. **Add more UI flows:** Leave request, Admin settings
4. **API pagination:** Test large result sets if applicable

### Medium Priority
5. **CI/CD integration:** GitHub Actions for automated test execution
6. **Visual regression:** Add screenshot comparison for UI stability
7. **Performance baselines:** Track response times over iterations
8. **Test data management:** Cleanup/reset test data between runs

### Low Priority
9. **Mobile testing:** Responsive design validation
10. **Accessibility:** WCAG 2.1 AA compliance checks
11. **Localization:** Multi-language UI testing

---

**Document Version:** 1.0  
**Last Updated:** 2026-05-26  
**Coverage Status:** ✅ All Must-have Requirements Covered
