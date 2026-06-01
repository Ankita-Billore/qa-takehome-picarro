"""
Load test results integration with Allure reporting.
Reads JMeter results and reports them to Allure for centralized test dashboard.
"""

import csv
import json
import pytest
import allure
from pathlib import Path


@pytest.mark.critical
@pytest.mark.loadtest
class TestLoadTestResults:
    """Allure reporting for load test metrics"""

    @staticmethod
    def parse_jmeter_results(jtl_file):
        """Parse JMeter JTL CSV results"""
        results = {
            'total': 0,
            'passed': 0,
            'failed': 0,
            'error_rate': 0,
            'avg_response': 0,
            'min_response': 0,
            'max_response': 0,
            'all_responses': []
        }
        
        try:
            with open(jtl_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    results['total'] += 1
                    response_time = int(row.get('elapsed', 0))
                    results['all_responses'].append(response_time)
                    
                    if row.get('success') == 'true':
                        results['passed'] += 1
                    else:
                        results['failed'] += 1
            
            if results['total'] > 0:
                results['error_rate'] = (results['failed'] / results['total']) * 100
                results['avg_response'] = sum(results['all_responses']) / len(results['all_responses'])
                results['min_response'] = min(results['all_responses'])
                results['max_response'] = max(results['all_responses'])
        
        except FileNotFoundError:
            pytest.skip(f"JMeter results file not found: {jtl_file}")
        
        return results

    @allure.title("Load Test: 50 Concurrent Users - Request Success Rate")
    @allure.description("JMeter load test with 50 concurrent users - Total 1,500 requests")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_loadtest_50_users_success_rate(self):
        """Verify 50-user load test success rate"""
        
        jtl_file = Path('results/loadtest_complete.jtl')
        if not jtl_file.exists():
            pytest.skip("Load test results file not found")
        
        results = self.parse_jmeter_results(str(jtl_file))
        
        # Add metrics to Allure report
        allure.attach(
            json.dumps(results, indent=2),
            name="Load Test Metrics",
            attachment_type=allure.attachment_type.JSON
        )
        
        # Assertions
        assert results['total'] > 0, "No load test data found"
        assert results['failed'] == 0, f"Load test failed: {results['failed']} errors"
        assert results['error_rate'] == 0, f"Error rate too high: {results['error_rate']}%"
        assert results['error_rate'] < 5, f"Error rate exceeds 5%: {results['error_rate']}%"

    @allure.title("Load Test: Performance Metrics")
    @allure.description("Response time analysis from 50-user concurrent load test")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_loadtest_performance_metrics(self):
        """Verify performance metrics are acceptable"""
        
        jtl_file = Path('results/loadtest_complete.jtl')
        if not jtl_file.exists():
            pytest.skip("Load test results file not found")
        
        results = self.parse_jmeter_results(str(jtl_file))
        
        # Performance metrics
        metrics = {
            'total_requests': results['total'],
            'successful': results['passed'],
            'failed': results['failed'],
            'error_rate_percent': results['error_rate'],
            'avg_response_ms': results['avg_response'],
            'min_response_ms': results['min_response'],
            'max_response_ms': results['max_response'],
            'throughput_req_sec': results['total'] / 151,  # 2:31 = 151 seconds
        }
        
        allure.attach(
            json.dumps(metrics, indent=2),
            name="Performance Metrics",
            attachment_type=allure.attachment_type.JSON
        )
        
        # Create performance table for Allure
        table_html = f"""
        <table>
            <tr><td>Total Requests</td><td>{metrics['total_requests']}</td></tr>
            <tr><td>Successful</td><td>{metrics['successful']}</td></tr>
            <tr><td>Failed</td><td>{metrics['failed']}</td></tr>
            <tr><td>Error Rate</td><td>{metrics['error_rate_percent']:.2f}%</td></tr>
            <tr><td>Avg Response</td><td>{metrics['avg_response_ms']:.0f} ms</td></tr>
            <tr><td>Min Response</td><td>{metrics['min_response_ms']} ms</td></tr>
            <tr><td>Max Response</td><td>{metrics['max_response_ms']} ms</td></tr>
            <tr><td>Throughput</td><td>{metrics['throughput_req_sec']:.1f} req/sec</td></tr>
        </table>
        """
        
        allure.attach(
            table_html,
            name="Performance Table",
            attachment_type=allure.attachment_type.HTML
        )
        
        # Assertions
        assert results['avg_response'] < 30000, f"Average response time too high: {results['avg_response']}ms"
        assert results['max_response'] < 60000, f"Max response time too high: {results['max_response']}ms"

    @allure.title("Load Test: 50 Users - Concurrent User Handling")
    @allure.description("Validates server can handle 50 concurrent users without cascading failures")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_loadtest_concurrent_users_50(self):
        """Verify server handles 50 concurrent users"""
        
        jtl_file = Path('results/loadtest_complete.jtl')
        if not jtl_file.exists():
            pytest.skip("Load test results file not found")
        
        results = self.parse_jmeter_results(str(jtl_file))
        
        summary = f"""
        Load Test Configuration: 50 Concurrent Users
        Total Requests: {results['total']}
        Passed: {results['passed']}
        Failed: {results['failed']}
        Error Rate: {results['error_rate']:.2f}%
        
        ✅ STATUS: {'PASSED' if results['error_rate'] == 0 else 'FAILED'}
        """
        
        allure.attach(
            summary,
            name="Load Test Summary",
            attachment_type=allure.attachment_type.TEXT
        )
        
        # Test status
        assert results['error_rate'] == 0, f"Load test failed with {results['error_rate']}% error rate"
        assert results['failed'] == 0, f"Load test had {results['failed']} failures"

