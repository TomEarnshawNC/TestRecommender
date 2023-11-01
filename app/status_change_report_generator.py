""" compares the test results with the stated target/reference results to generate a list of tests that have changed results."""
import json

from pathlib import Path


def read_report(report_filename: str, report_dir: str="data") -> dict:
    with open(Path(report_dir, report_filename)) as report:
        return json.loads(report)
    

def find_results(report: dict) -> dict:
    return report["test_results"]    


def find_previous_results(report: dict) -> dict:
    previous_report = read_report(report["code_changes"]["target_info"]["reference_report"])
    return find_results(previous_report)


def get_results_diff(results: dict,  previous_results: dict) -> dict:
    results_diff = {
        "new_tests": [],
        "unrun_tests": [],
        "unchanged_status": [],
        "changed_status": []
    }

    for test in set(results.keys()).union(previous_results.keys()):
        if test not in previous_results.keys():
            results_diff["new_tests"].append(test)
            continue

        if test not in results.keys():
            results_diff["unrun_tests"].append(test)
            continue
        
        if results[test] == previous_results[test]:
            results_diff["unchanged_status"].append(test)
            continue

        results_diff["changed_status"].append(test)

    return results_diff


def main(report_filename: str, report_dir: str="data") -> dict:
    report = read_report(report_filename, report_dir)
    results = find_results(report)
    previous_results = find_previous_results(report)

    return get_results_diff(results, previous_results)