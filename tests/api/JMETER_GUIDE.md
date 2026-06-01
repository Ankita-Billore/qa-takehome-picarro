# JMeter Load Testing Guide - REST Countries API

This guide explains how to use the `rest_countries_api.jmx` file for performance and load testing the REST Countries API.

## Overview

The JMX file (`rest_countries_api.jmx`) is an Apache JMeter test plan that includes:
- 8 different API endpoints being tested
- Configurable load testing parameters (threads, ramp-up time, iterations)
- Response assertions for validation
- Multiple result collectors (table view, graph, summary report)

## Test Scenarios Included

1. **Get Country by Name** - Fetch India country data
2. **Get Country by Code (Alpha2)** - Fetch using alpha-2 code (IN)
3. **Get All Countries with Fields** - Get all countries with specific fields
4. **Get Countries by Region** - Fetch all Asian countries
5. **Get Countries by Currency** - Fetch countries using INR currency
6. **Get Countries by Language** - Fetch countries speaking Hindi
7. **Invalid Country (404 Test)** - Test error handling for invalid input
8. **Multiple Countries by Codes** - Fetch multiple countries at once (IN, US, GB)

## Prerequisites

### Install JMeter

**On macOS:**
```bash
brew install jmeter
```

**On Ubuntu/Linux:**
```bash
sudo apt-get install jmeter
```

**On Windows:**
Download from: https://jmeter.apache.org/download_jmeter.cgi

**Verify Installation:**
```bash
jmeter --version
```

## Running the Test

### Method 1: Using JMeter GUI

```bash
# Navigate to the project directory
cd /Users/ankitabillore/qa-takehome

# Open JMeter GUI
jmeter

# Then:
# 1. File → Open → tests/api/rest_countries_api.jmx
# 2. Configure User Variables (if needed):
#    - THREADS: Number of concurrent users (default: 10)
#    - RAMPUP: Time to ramp up threads in seconds (default: 30)
#    - LOOPS: Number of iterations per thread (default: 5)
# 3. Click "Start" (green arrow) or use Ctrl+Shift+L
```

### Method 2: Command Line (Non-GUI Mode - Recommended for CI/CD)

```bash
# Navigate to the tests/api directory
cd /Users/ankitabillore/qa-takehome/tests/api

# Run the test (non-GUI mode)
jmeter -n -t rest_countries_api.jmx -l results.jtl -j jmeter.log

# Run with custom parameters
jmeter -n -t rest_countries_api.jmx -l results.jtl -j jmeter.log \
  -Jthreads=20 \
  -Jrampup=60 \
  -Jloops=10

# Run with report generation
jmeter -n -t rest_countries_api.jmx -l results.jtl -j jmeter.log -e -o jmeter_report
```

## Configurable Parameters

Edit these in the "User Defined Variables" section or pass via command line:

| Variable | Default | Description |
|----------|---------|-------------|
| `THREADS` | 10 | Number of concurrent threads/users |
| `RAMPUP` | 30 | Time (seconds) to ramp up all threads |
| `LOOPS` | 5 | Number of times each thread runs the test scenario |
| `BASE_URL` | https://restcountries.com/v3.1 | API base URL |

## Example Load Test Scenarios

### Light Load Test (Development)
```bash
jmeter -n -t rest_countries_api.jmx -l results.jtl \
  -Jthreads=5 -Jrampup=10 -Jloops=2
```

### Medium Load Test
```bash
jmeter -n -t rest_countries_api.jmx -l results.jtl \
  -Jthreads=50 -Jrampup=30 -Jloops=5
```

### Heavy Load Test (Stress Testing)
```bash
jmeter -n -t rest_countries_api.jmx -l results.jtl \
  -Jthreads=100 -Jrampup=60 -Jloops=10
```

### Endurance Test (Extended Duration)
```bash
jmeter -n -t rest_countries_api.jmx -l results.jtl \
  -Jthreads=30 -Jrampup=30 -Jloops=50
```

## Understanding Results

### Key Metrics

- **Response Time**: How long requests take to complete
- **Throughput**: Requests per second (req/s)
- **Error Rate**: Percentage of failed requests
- **Min/Max/Average**: Response time statistics

### Results Files

After running, check:

1. **results.jtl** - Raw results in CSV/XML format
2. **jmeter.log** - Detailed execution log
3. **jmeter_report/** - HTML report with graphs and statistics
4. **jmeter_results.csv** - Summary report

### Generating HTML Report (Post-Test)

```bash
# Generate report from existing results
jmeter -g results.jtl -o jmeter_report -j jmeter.log
```

## Interpreting Results

### View Results Table (GUI Mode)
Shows each request with:
- Sample # (request order)
- Sample Label (endpoint name)
- Sample Count (number of requests)
- Error Count (failed requests)
- Error % (failure percentage)
- Average Response Time
- Min/Max Response Times
- Throughput (req/sec)

### Success Criteria

- ✅ Error Rate < 1%
- ✅ Average Response Time < 500ms
- ✅ 95th Percentile < 1000ms
- ✅ No 404/5xx errors on valid requests

## CI/CD Integration

### GitHub Actions Example

```yaml
- name: Run JMeter Load Tests
  run: |
    cd tests/api
    jmeter -n -t rest_countries_api.jmx -l results.jtl \
      -Jthreads=10 -Jloops=5 -e -o jmeter_report
    
- name: Upload JMeter Report
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: jmeter-report
    path: tests/api/jmeter_report
```

## Comparison: Python Tests vs JMeter

| Aspect | Python Tests | JMeter |
|--------|--------------|--------|
| **Use Case** | Functional testing, validation | Load, stress, endurance testing |
| **Execution** | Run once per CI/CD cycle | Run periodically or on-demand |
| **Concurrency** | Single-threaded per test | Multi-threaded with configuration |
| **Response Assertions** | Via Python assertions | Built-in JMeter assertions |
| **Reporting** | HTML reports | Visual graphs, detailed metrics |
| **Configuration** | In code | JMX file with variables |

## Troubleshooting

### Test Hangs or Takes Too Long
```bash
# Increase timeout or reduce load
jmeter -n -t rest_countries_api.jmx -l results.jtl \
  -Jthreads=5 -Jloops=2
```

### Connection Refused Errors
```bash
# Verify API is accessible
curl -I https://restcountries.com/v3.1/name/india
```

### Memory Issues
```bash
# Increase JMeter heap size
export JVM_ARGS="-Xms1024m -Xmx2048m"
jmeter -n -t rest_countries_api.jmx -l results.jtl
```

### View Detailed Logs
```bash
# Check jmeter.log for errors
tail -f jmeter.log
```

## Next Steps

1. **Baseline Test**: Run with default parameters to establish baseline
2. **Stress Test**: Gradually increase THREADS to find breaking point
3. **Monitor**: Check server metrics during test (CPU, memory, requests)
4. **Optimize**: Adjust based on results and requirements
5. **Schedule**: Add to CI/CD for continuous monitoring

## References

- [JMeter Official Documentation](https://jmeter.apache.org/usermanual/)
- [JMeter Best Practices](https://jmeter.apache.org/usermanual/best-practices.html)
- [REST Countries API Documentation](https://restcountries.com/)

## Support

For issues with the test plan:
1. Check `jmeter.log` for error details
2. Verify API endpoints are accessible
3. Review test parameters match your requirements
4. Check network connectivity and firewall rules

---

**Created**: 29 May 2026  
**API Base**: https://restcountries.com/v3.1  
**Test Endpoints**: 8 major API scenarios
