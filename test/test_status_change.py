from collections import Counter

from ..app.status_change_report_generator import get_results_diff


def test_get_results_diff():
    results = {
        "0": True,
        "1": False,
        "2": True,
        "4": True
    }

    previous_results = {
        "0": True,
        "1": True,
        "2": True,
        "3": True
    }

    expected_report = {
        "new_tests": ["4"],
        "unrun_tests": ["3"],
        "unchanged_status": ["0", "2"],
        "changed_status": ["1"]
    }

    report = get_results_diff(results, previous_results)

    for test_type in expected_report.keys():
        assert Counter(expected_report[test_type]) == Counter(report[test_type])