#!/usr/bin/env python3
"""Structural check for the exported n8n workflow.

Catches the mistakes that are invisible in the n8n editor until a run fails:
an orphaned branch, a node referenced by name that was renamed, a duplicate id.

Does not validate node parameters against n8n's schema — only the graph.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / "workflows" / "ocr-transform-sharepoint.json"
NODE_REF = re.compile(r"\$\('([^']+)'\)")
TRIGGER_TYPES = ("scheduleTrigger", "webhook", "manualTrigger", "executeWorkflowTrigger")


def main() -> int:
    workflow = json.loads(WORKFLOW.read_text(encoding="utf-8"))
    nodes = workflow["nodes"]
    names = {n["name"] for n in nodes}
    problems: list[str] = []

    ids = [n["id"] for n in nodes]
    if len(ids) != len(set(ids)):
        problems.append("Duplicate node ids")
    if len(names) != len(nodes):
        problems.append("Duplicate node names")

    # Every connection endpoint must be a real node.
    for source, conn in workflow["connections"].items():
        if source not in names:
            problems.append(f"Connection from unknown node: {source}")
        for output in conn.get("main", []):
            for link in output:
                if link["node"] not in names:
                    problems.append(f"{source} -> unknown node {link['node']}")

    # Every node must be reachable from a trigger, or it is dead on import.
    triggers = {n["name"] for n in nodes if any(t in n["type"] for t in TRIGGER_TYPES)}
    if not triggers:
        problems.append("No trigger node")
    reachable = set(triggers)
    changed = True
    while changed:
        changed = False
        for source, conn in workflow["connections"].items():
            if source not in reachable:
                continue
            for output in conn.get("main", []):
                for link in output:
                    if link["node"] not in reachable:
                        reachable.add(link["node"])
                        changed = True
    for orphan in sorted(names - reachable):
        problems.append(f"Unreachable node: {orphan}")

    # $('Node name') references break silently when a node is renamed.
    for node in nodes:
        blob = json.dumps(node.get("parameters", {}))
        for ref in set(NODE_REF.findall(blob)):
            if ref not in names:
                problems.append(f"{node['name']}: references unknown node $('{ref}')")

    if problems:
        print("Problems found:")
        for item in problems:
            print(f"  {item}")
        return 1

    print(f"OK — {len(nodes)} nodes, all reachable, all references resolve.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
