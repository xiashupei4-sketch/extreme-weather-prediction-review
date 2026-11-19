"""Reaggregate the frozen, classified release data; Python standard library only.

Adapted from the archived recompute.py (12 Nov) and draw_figures.py (13 Nov).
This starts at the released coding layer, not raw WoS screening or text extraction.
"""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "results"
FAMILIES = ["ARIMA / SARIMA", "Tree / kernel ML", "Recurrent / convolutional DL",
            "Selected newer architectures"]
HAZARDS = ["Heavy precipitation", "Drought", "Heat / heatwaves", "Flood",
           "Storm / tropical cyclone", "Other / unassigned"]
CODES = ["C", "R", "P", "X", "U", "V"]
GROUPS = ["Meteorological", "Hydrological / soil", "Marine", "Impact chain"]


def read(name):
    with (DATA / name).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write(name, rows):
    with (OUT / name).open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def main():
    OUT.mkdir(exist_ok=True)
    for line in (ROOT / "SHA256SUMS").read_text().splitlines():
        expected, name = line.split("  ", 1)
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected, name
    corpus = read("corpus.csv")
    cases = read("cases.csv")
    intervals = read("target-intervals.csv")
    roles = read("model-roles.csv")
    strict = [r for r in corpus if int(r["strict_candidate"])]
    assert len(corpus) == len({r["ut"] for r in corpus}) == 4690
    assert len(strict) == 1344
    for r in corpus:
        assert 2006 <= int(r["year"]) <= 2025
        start = 2006 + ((int(r["year"]) - 2006) // 5) * 5
        assert r["period"] == f"{start}-{start+4}"
        assert all(r[k] in {"0", "1"} for k in FAMILIES + HAZARDS + ["strict_candidate"])
    assert set(int(r["case"]) for r in cases) == set(range(1, 31))
    assert {r["ut"] for r in cases} <= {r["ut"] for r in corpus}
    assert len(intervals) == 17 and len({r["case"] for r in intervals}) == 17
    assert all(r["validation_code"] in CODES for r in cases)
    assert all(r["independent_human_validation"] == "False" for r in roles)
    case_by_id = {r["case"]: r for r in cases}
    for r in intervals:
        assert r["doi"] == case_by_id[r["case"]]["doi"]
        assert r["validation"] == case_by_id[r["case"]]["validation_code"]
        assert all(float(x) > 0 for x in r["hours"].split(";"))

    periods = sorted({r["period"] for r in corpus})
    period_rows = []
    for period in periods:
        cohort = [r for r in corpus if r["period"] == period]
        for family in FAMILIES:
            n = sum(int(r[family]) for r in cohort)
            period_rows.append(dict(period=period, family=family, count=n,
                                    denominator=len(cohort), share=n / len(cohort)))
    write("method-family-period.csv", period_rows)
    hazard_rows, cross = [], []
    for hazard in HAZARDS:
        cohort = [r for r in strict if int(r[hazard])]
        for family in FAMILIES:
            n = sum(int(r[family]) for r in cohort)
            hazard_rows.append(dict(hazard=hazard, family=family, count=n,
                                    denominator=len(cohort), share=n / len(cohort)))
        for period in periods:
            sub = [r for r in cohort if r["period"] == period]
            cross.append(dict(hazard=hazard, period=period, denominator=len(sub),
                              **{f: sum(int(r[f]) for r in sub) for f in FAMILIES}))
    write("strict-hazard-method.csv", hazard_rows)
    write("strict-hazard-method-by-period.csv", cross)
    annual = []
    for year in range(2006, 2026):
        cohort = [r for r in corpus if int(r["year"]) == year]
        annual.append(dict(PY=year, papers=len(cohort),
                           TC=sum(int(r["global_citations"]) for r in cohort),
                           LCS=sum(int(r["local_citations"]) for r in cohort)))
    write("annual-reconciled.csv", annual)
    validations = []
    for group in GROUPS + ["All cases"]:
        cohort = [r for r in cases if group == "All cases" or r["task_group"] == group]
        for code in CODES:
            validations.append(dict(task_group=group, code=code,
                                    n=sum(r["validation_code"] == code for r in cohort),
                                    denominator=len(cohort)))
    write("figure10-source.csv", validations)
    networks = json.loads((DATA / "networks.json").read_text())
    coupling_nodes = networks["coupling_nodes"]
    coupling_edges = networks["coupling_edges"]
    assert len(coupling_nodes) == 40 and len(coupling_edges) == 80
    node_ids = {r["ut"] for r in coupling_nodes}
    assert all(e["ut_a"] in node_ids and e["ut_b"] in node_ids for e in coupling_edges)
    assert len({tuple(sorted((e["ut_a"], e["ut_b"]))) for e in coupling_edges}) == 80
    assert sum(any(t in r["title"].lower() for t in ("susceptibility", "susceptible"))
               for r in coupling_nodes) == 31
    matrix = networks["cocitation_matrix"]
    labels = list(matrix[0])[1:]
    assert len(matrix) == len(labels) == 60
    assert [list(r.values())[0] for r in matrix] == labels
    assert all(int(matrix[i][labels[j]]) == int(matrix[j][labels[i]])
               for i in range(60) for j in range(60))
    n_edges = sum(int(matrix[i][labels[j]]) > 0 for i in range(60) for j in range(i+1, 60))
    assert n_edges == 1399
    summary = dict(broad_units=len(corpus), strict_candidates=len(strict),
                   period_counts=dict(Counter(r["period"] for r in corpus)),
                   purposive_cases=len(cases), chronological_cases=sum(r["validation_code"] == "C" for r in cases),
                   numeric_target_intervals=len(intervals), local_citations=sum(r["LCS"] for r in annual),
                   coupling_nodes=40, coupling_display_edges=80,
                   susceptibility_or_susceptible_titles=31, cocitation_full_edges=n_edges,
                   input_integrity="SHA256SUMS verified", independent_human_review=False)
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
