"""Candidate readiness must follow every check, not an empty or stale summary."""
import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from build_status import evaluate
from qa_contract import MANDATORY_CHECKS


class CandidateStatus(unittest.TestCase):
    def passing(self):
        return {"checks": dict.fromkeys(MANDATORY_CHECKS, "PASS"), "mandatory_failed": [], "release_gate": "PASS"}

    def test_complete_verification_with_only_visual_review_pending_is_ready(self):
        status = self.passing()
        self.assertEqual(evaluate(status, "")[0], "CANDIDATE_READY")
        status["checks"]["visual_review_currency"] = "FAIL"
        status.update(mandatory_failed=["visual_review_currency"], release_gate="FAIL")
        self.assertEqual(evaluate(status, "")[0], "CANDIDATE_READY")

    def test_each_nonvisual_mandatory_failure_blocks_the_candidate(self):
        for name in MANDATORY_CHECKS:
            if name == "visual_review_currency":
                continue
            with self.subTest(name=name):
                status = self.passing()
                status["checks"][name] = "FAIL"
                status.update(mandatory_failed=[name], release_gate="FAIL")
                self.assertEqual(evaluate(status, "")[0], "FAILED")

    def test_missing_or_inconsistent_report_never_passes(self):
        malformed = [None, {}, [], {"mandatory_failed": []}, {"mandatory_failed": ["visual_review_currency"]}]
        missing = self.passing()
        del missing["checks"]["one_page_keeps"]
        malformed.append(missing)
        bad_value = self.passing()
        bad_value["checks"]["visual_review_currency"] = "unknown"
        malformed.append(bad_value)
        summary = self.passing()
        summary["release_gate"] = "FAIL"
        malformed.append(summary)
        hidden = self.passing()
        hidden["checks"]["one_page_keeps"] = "FAIL"
        malformed.append(hidden)
        for status in malformed:
            with self.subTest(status=status):
                self.assertEqual(evaluate(copy.deepcopy(status), "")[0], "FAILED")


if __name__ == "__main__":
    unittest.main()
