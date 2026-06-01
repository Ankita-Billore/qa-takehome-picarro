# Quick Reference: Load Test Results Interpretation

## 🎯 Is My Test PASSED or FAILED?

### ✅ PASSED Indicators
- `Err: 0 (0.00%)` - Zero errors
- All requests completed
- No "Connection refused" errors
- Response times are reasonable (< 30 seconds)
- No timeout exceptions

### ❌ FAILED Indicators
- `Err: > 5%` - More than 5% error rate
- `Err: 600 (100%)` - All requests failed
- "java.net.ConnectException" errors
- "Read timed out" messages
- Server crashes or hangs

---

## 📊 Reading JMeter Output Format

```
summary + 121 in 00:00:12 = 10.1/s Avg: 2565 Min: 2043 Max: 2861 Err: 0 (0.00%)
```

| Value | Meaning | Your Test |
|-------|---------|-----------|
| `+ 121` | Requests in this interval | 600 total |
| `00:00:12` | Time elapsed in interval | 2:19 total |
| `10.1/s` | Requests per second | 4.3/s avg |
| `Avg: 2565` | Average response time (ms) | 6,518 ms |
| `Min: 2043` | Minimum response time (ms) | 1,243 ms |
| `Max: 2861` | Maximum response time (ms) | 17,098 ms |
| `Err: 0` | Number of errors | 0 ✅ |
| `0.00%` | Error percentage | 0.00% ✅ |

---

## 📈 Load Test Pass Criteria Quick Check

```
Error Rate Check:     0.00%  ✅ < 5% = PASS
Completion Check:     600/600 ✅ 100% = PASS
Response Time Check:  6,518 ms ✅ < 30s = PASS
Connection Check:     No errors ✅ = PASS

OVERALL: ✅ PASSED
```

---

## 🔴 Common Failure Scenarios

### Scenario 1: 100% Error Rate
```
summary = 600 in 01:00 = 10.0/s Avg: 0 Min: 0 Max: 0 Err: 600 (100.00%)
```
**Meaning:** All requests failed  
**Common Causes:**
- URL variables not substituting (e.g., `${BASE_URL}` literal)
- Server down or unreachable
- Wrong credentials
- Firewall blocking

**Fix:** Check URL hardcoding, verify server is running

---

### Scenario 2: High Error Rate (5-50%)
```
summary = 600 in 01:00 = 10.0/s Avg: 4523 Min: 100 Max: 8932 Err: 120 (20.00%)
```
**Meaning:** 20% of requests failed  
**Common Causes:**
- Server overloaded
- Rate limiting kicked in
- Some users rejected (authentication)
- Database connection pool exhausted

**Fix:** Reduce user count, add think time between requests

---

### Scenario 3: Very Slow Response Times
```
summary = 600 in 05:00 = 2.0/s Avg: 45000 Min: 30000 Max: 60000 Err: 0 (0.00%)
```
**Meaning:** 0% error but very slow (45+ seconds average)  
**Assessment:** Technically PASSED but performance is poor  
**Action:** Optimize server, increase resources, or reduce concurrent users

---

## 📊 JMeter vs Allure: When to Use Each

### Use JMeter When:
- ✅ Testing performance under load
- ✅ Simulating many concurrent users
- ✅ Measuring response times
- ✅ Finding breaking point (how many users before failure?)
- ✅ Testing APIs for load handling

### Use Allure When:
- ✅ Testing features work correctly
- ✅ Running functional/integration tests
- ✅ Need screenshots and detailed logs
- ✅ Tracking test trends over time
- ✅ Reporting to stakeholders (beautiful dashboards)

### Use Both When:
- ✅ Comprehensive QA (feature works + performs well)
- ✅ Production validation
- ✅ Performance regression testing

---

## 🚀 Command Quick Reference

### Run with Different User Counts
```bash
# 5 users (validation)
jmeter -n -t tests/loadtest/orangehrm_login_loadtest_fixed.jmx -Jthreads=5 -Jloops=1

# 50 users (standard load)
jmeter -n -t tests/loadtest/orangehrm_login_loadtest_fixed.jmx -Jthreads=50 -Jrampup=60 -Jloops=3

# 100 users (heavy load)
jmeter -n -t tests/loadtest/orangehrm_login_loadtest_fixed.jmx -Jthreads=100 -Jrampup=120 -Jloops=2
```

### Analyze Results
```bash
# Quick analysis script
./analyze_loadtest.sh results/loadtest_fixed.jtl

# View detailed report
cat results/LOADTEST_REPORT.md

# Understanding guide
cat docs/LOAD_TEST_UNDERSTANDING.md
```

### Generate Allure Report
```bash
# Run functional tests with Allure
pytest tests/ui/ -v --alluredir=reports/allure-results

# Generate HTML report
allure generate reports/allure-results -o reports/allure-report --clean

# Open in browser
allure open reports/allure-report
```

---

## 📋 Your Test Summary

| Aspect | Status | Details |
|--------|--------|---------|
| **Error Rate** | ✅ PASS | 0.00% (< 5% required) |
| **Requests** | ✅ PASS | 600/600 successful |
| **Performance** | ✅ GOOD | 1.2-17 sec response range |
| **Server Stability** | ✅ PASS | No crashes or hangs |
| **Overall Result** | ✅ **PASSED** | Production-ready for 5 users |

---

## 💡 What This Means

**Your OrangeHRM login endpoint can handle 5 concurrent users without any failures.**

Next: Test with 50 users to verify it scales properly.

---

Last Updated: June 1, 2026
