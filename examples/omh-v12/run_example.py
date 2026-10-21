"""Run the OMH data tools on the synthetic slide 14 fixture and record their facts.

Usage (from the project root):
    python3 examples/omh-v12/run_example.py --engine "/path/to/omh/core/engine.py"

The engine is the single-file, standard-library OMH core script of the integrated
v04 package (components/omh/core). It is not part of this repository and is only
read and executed as a local CLI; nothing is installed and no network is used.

The task: fill blank `amount` values with 0 and delete no rows. The first result
(after-first.csv) keeps three rows and clears the blank, but ID 0 is gone and an
unexpected ID 3 appears; the fixed result keeps IDs 0, 1 and 2.
Writes evidence/tool-results.json (verbatim tool output, values omitted) and
evidence/summary.json (the counts the slide uses, cross-checked with csv).
"""

import argparse
import csv
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CALLS = [
    ("inspect_before", "data_inspect", {"path": "data/before.csv"}),
    ("compare_first", "data_compare", {"left": "data/before.csv", "right": "data/after-first.csv", "key": "id",
                                       "include_values": False}),
    ("compare_fixed", "data_compare", {"left": "data/before.csv", "right": "data/after-fixed.csv", "key": "id",
                                       "include_values": False}),
    ("inspect_first", "data_inspect", {"path": "data/after-first.csv"}),
    ("inspect_fixed", "data_inspect", {"path": "data/after-fixed.csv"}),
]


def tool(engine, name, args):
    proc = subprocess.run([sys.executable, "-I", "-B", str(engine), "--root", str(HERE), name,
                           "--args-json", json.dumps(args)], capture_output=True, text=True, timeout=30)
    out = json.loads(proc.stdout)
    if not out.get("ok"):
        raise SystemExit(f"{name} failed: {out.get('error')}")
    return out


def kinds(facts):
    count = {"left_only": 0, "right_only": 0, "value_changed": 0}
    fields = set()
    for d in facts["differences"]:
        count[d["kind"]] += 1
        fields.update(d["location"].get("fields", []))
    return count, sorted(fields)


def plain(left, right):
    """Independent count with the csv module, to cross-check the tool facts."""
    def rows(name):
        with open(HERE / "data" / name, newline="", encoding="utf-8") as f:
            return {r["id"]: r for r in csv.DictReader(f)}
    a, b = rows(left), rows(right)
    return {"left_only": len(a.keys() - b.keys()), "right_only": len(b.keys() - a.keys()),
            "value_changed": sum(1 for k in a.keys() & b.keys() if a[k] != b[k])}


def nulls(facts, column):
    return next(n["count"] for n in facts["null_counts"] if n["name"] == column)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--engine", required=True, type=Path)
    engine = ap.parse_args().engine
    results = {key: tool(engine, name, args) for key, name, args in CALLS}
    summary = {"task": "fill blank amount with 0, delete no rows", "acceptance": "left_only == 0 and right_only == 0, "
               "changes only in amount, amount blanks 0, full scope"}
    for key, left, right in (("first", "before.csv", "after-first.csv"), ("fixed", "before.csv", "after-fixed.csv")):
        f = results[f"compare_{key}"]["facts"]
        count, fields = kinds(f)
        if f["differences_omitted"] or count != plain(left, right):
            raise SystemExit(f"{key}: tool facts and csv cross-check disagree")
        # tool terms kept as is: left_only = key only in before (missing after), right_only = key only after
        summary[key] = {"scope": f["scope"], "rows_before": f["left"]["records_scanned"],
                        "rows_after": f["right"]["records_scanned"], "left_only": count["left_only"],
                        "right_only": count["right_only"], "value_changed": count["value_changed"],
                        "amount_blanks_after": nulls(results[f"inspect_{key}"]["facts"], "amount"),
                        "changed_fields": fields, "differences_in_scope": f["differences_in_scope"],
                        "values_returned": f["values_returned"]}
        # the business criterion, decided here and not by the tool's ok flag (ok only means the call succeeded)
        summary[key]["meets_criterion"] = (f["scope"] == "full" and count["left_only"] == 0
                                           and count["right_only"] == 0 and fields == ["amount"]
                                           and summary[key]["amount_blanks_after"] == 0)
    summary["amount_blanks_before"] = nulls(results["inspect_before"]["facts"], "amount")
    summary["engine_version"] = results["compare_first"]["version"]
    out = HERE / "evidence"
    out.mkdir(exist_ok=True)
    (out / "tool-results.json").write_text(json.dumps(results, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                                           encoding="utf-8")
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                                      encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
