#!/usr/bin/env python3
"""Dump the field metadata of a Vault object as a Markdown table.

Reads the Vault Metadata API and reports, per field: data type, whether it is
required, whether it is editable, and the length limit. Object types are
fetched as well, because a field that is optional on the object can still be
required on a specific object type (Pharma Complaint vs. MedTech Complaint).

The session ID is read from $VAULT_SESSION_ID and never taken as an argument,
so it does not end up in the shell history or the process list.

See config/vault-metadata-api.md for how to obtain a session ID.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

DEFAULT_DNS = "bayersbx-iqms-3-1-dev.veevavault.com"
DEFAULT_VERSION = "v26.2"
TIMEOUT = 60

EXAMPLES = """\
Environment variables:
  VAULT_SESSION_ID   Required. Vault session token; never passed as an argument,
                     so it stays out of the shell history and the process list.
  VAULT_DNS          Optional. Default Vault host, overridden by --dns.
  VAULT_API_VERSION  Optional. Default API version, overridden by --version.

Examples:
  # Authenticate once per session; the token is short-lived.
  export VAULT_SESSION_ID='<sessionId>'

  # Write complaint__v to the default file ./complaint__v-fields.md
  python scripts/vault-object-fields.py complaint__v

  # Same as CSV, to ./complaint__v-fields.csv
  python scripts/vault-object-fields.py complaint__v -f csv

  # Choose path and file name yourself; missing directories are created.
  python scripts/vault-object-fields.py complaint__v -o docs/02-requirements/complaint-fields.md

  # Print to the terminal instead of writing a file
  python scripts/vault-object-fields.py complaint__v -f csv -o -

  # Also export all picklist values to ./complaint__v/complaint__v-picklists.{csv,json}
  python scripts/vault-object-fields.py complaint__v -p

  # Same, but put the complaint__v/ subfolder under docs/02-requirements/
  python scripts/vault-object-fields.py complaint__v -p docs/02-requirements

  # Intake object, including inactive fields, plus the raw API response
  python scripts/vault-object-fields.py complaint_intake__v --all-fields --json intake.json

  # Skip the per-object-type calls (faster, loses the "Required on type" column)
  python scripts/vault-object-fields.py complaint__v --skip-types
"""


def get(dns: str, version: str, path: str, session_id: str) -> dict[str, Any]:
    """GET a Vault API path and return the parsed JSON body."""
    url = f"https://{dns}/api/{version}/{path.lstrip('/')}"
    request = urllib.request.Request(
        url,
        headers={"Authorization": session_id, "Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        raise SystemExit(f"HTTP {error.code} on {url}: {error.read().decode('utf-8', 'replace')[:500]}")
    except urllib.error.URLError as error:
        raise SystemExit(f"Cannot reach {url}: {error.reason}")

    # Vault answers 200 with responseStatus FAILURE for an expired session.
    if payload.get("responseStatus") != "SUCCESS":
        errors = payload.get("errors") or payload.get("responseMessage") or payload
        raise SystemExit(f"Vault returned FAILURE for {path}: {json.dumps(errors)[:500]}")
    return payload


def required_by_type(
    dns: str, version: str, object_name: str, session_id: str, type_names: list[str]
) -> dict[str, list[str]]:
    """Map field name -> object type labels on which the field is required.

    Per-type required flags live under /configuration/Objecttype.{object}.{type},
    not under the /metadata/vobjects/ tree, which has no types sub-resource.
    """
    extra: dict[str, list[str]] = {}
    for type_name in type_names:
        try:
            payload = get(
                dns, version, f"configuration/Objecttype.{object_name}.{type_name}", session_id
            )
        except SystemExit as error:
            # A single unreadable type should not cost us the whole field table.
            print(f"warning: object type {type_name}: {error}", file=sys.stderr)
            continue
        object_type = payload.get("data", {})
        label = object_type.get("label") or type_name
        for field in object_type.get("type_fields", []):
            if field.get("required"):
                extra.setdefault(field["name"], []).append(label)
    return extra


def fetch_picklists(
    dns: str, version: str, session_id: str, fields: list[dict[str, Any]]
) -> dict[str, dict[str, Any]]:
    """Fetch the values of every picklist used by the given fields.

    Keyed by picklist name, because several fields can share one picklist and
    it should only be fetched, and exported, once.
    """
    # The attribute holding the picklist name is not consistent across Vault
    # versions, so try the known spellings before giving up on a field.
    keys = ("picklist", "picklist__sys", "picklist_name", "picklistName")
    wanted: dict[str, list[str]] = {}
    unresolved: list[str] = []
    for field in fields:
        if not str(field.get("type", "")).endswith("Picklist"):
            continue
        picklist = next((field[k] for k in keys if field.get(k)), None)
        if not picklist:
            unresolved.append(field.get("name", ""))
            continue
        wanted.setdefault(picklist, []).append(field.get("name", ""))

    if unresolved:
        print(
            f"warning: no picklist name on {len(unresolved)} picklist field(s): "
            f"{', '.join(unresolved[:5])}{' ...' if len(unresolved) > 5 else ''}. "
            "Re-run with --json to inspect the raw metadata.",
            file=sys.stderr,
        )

    picklists: dict[str, dict[str, Any]] = {}
    for name in sorted(wanted):
        try:
            payload = get(dns, version, f"objects/picklists/{name}", session_id)
        except SystemExit as error:
            # One unreadable picklist should not cost us the whole export.
            print(f"warning: picklist {name}: {error}", file=sys.stderr)
            continue
        picklists[name] = {
            "picklist": name,
            "used_by_fields": sorted(wanted[name]),
            "controlling_picklist": payload.get("controllingPicklistName"),
            "values": [
                {"name": value.get("name", ""), "label": value.get("label", "")}
                for value in payload.get("picklistValues", [])
            ],
        }
    return picklists


PICKLIST_COLUMNS = ["Picklist", "Value name", "Value label", "Order", "Used by fields"]


def render_picklists_csv(picklists: dict[str, dict[str, Any]], head: dict[str, Any]) -> str:
    """One row per picklist value; heading lines at the end, as in the field CSV."""
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(PICKLIST_COLUMNS)
    total = 0
    for name in sorted(picklists):
        entry = picklists[name]
        used_by = ", ".join(entry["used_by_fields"])
        # The API returns values in their configured order; keep it and number it.
        for order, value in enumerate(entry["values"], start=1):
            writer.writerow([name, value["name"], value["label"], order, used_by])
            total += 1
    writer.writerow([])
    writer.writerow([f"Picklist values on {head['object_name']} ({head['label']})"])
    writer.writerow(
        [
            f"Source: {head['dns']}, API {head['version']}. "
            f"Picklists: {len(picklists)}. Values: {total}."
        ]
    )
    return buffer.getvalue()


COLUMNS = ["Field", "Label", "Type", "Required", "Editable", "Max length", "Required on type"]


def render_markdown(rows: list[list[str]], head: dict[str, Any], note: str | None) -> str:
    """Render the field table as Markdown, with the heading lines on top."""
    lines = [
        f"# Fields on `{head['object_name']}` ({head['label']})",
        "",
        f"Source: `{head['dns']}`, API `{head['version']}`. Fields: {len(rows)}.",
        "",
        "| " + " | ".join(COLUMNS) + " |",
        "| " + " | ".join("---" for _ in COLUMNS) + " |",
    ]
    lines += ["| `" + row[0] + "` | " + " | ".join(row[1:]) + " |" for row in rows]
    if note:
        lines += ["", f"> {note}"]
    return "\n".join(lines) + "\n"


def render_csv(rows: list[list[str]], head: dict[str, Any], note: str | None) -> str:
    """Render the field table as CSV.

    The heading lines go to the *end* of the file, so that the column header is
    the first row and the data stays a clean rectangle — spreadsheets and
    pandas can then read it without a skiprows argument.
    """
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(COLUMNS)
    writer.writerows(rows)
    writer.writerow([])
    writer.writerow([f"Fields on {head['object_name']} ({head['label']})"])
    writer.writerow([f"Source: {head['dns']}, API {head['version']}. Fields: {len(rows)}."])
    if note:
        writer.writerow([note])
    return buffer.getvalue()


def truthy(value: Any) -> str:
    if value is True:
        return "yes"
    if value is False:
        return "no"
    return "-"


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        epilog=EXAMPLES,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "object_name",
        nargs="?",
        default="complaint__v",
        help=(
            "Vault object to read, e.g. complaint__v, complaint_intake__v, "
            "reported_product__v (default: complaint__v)."
        ),
    )
    parser.add_argument(
        "-f",
        "--format",
        choices=("md", "csv"),
        default="md",
        help="Output format (default: md).",
    )
    parser.add_argument(
        "-o",
        "--output",
        help=(
            "Path and file name of the output. Missing directories are "
            "created. Use '-' to print to the terminal instead. "
            "Default: ./<object_name>-fields.<format>"
        ),
    )
    parser.add_argument(
        "--dns",
        default=os.environ.get("VAULT_DNS", DEFAULT_DNS),
        help="Vault host to query. Overrides $VAULT_DNS (default: %(default)s).",
    )
    parser.add_argument(
        "--version",
        default=os.environ.get("VAULT_API_VERSION", DEFAULT_VERSION),
        help=(
            "Vault API version. Overrides $VAULT_API_VERSION "
            "(default: %(default)s)."
        ),
    )
    parser.add_argument(
        "--all-fields",
        action="store_true",
        help="Include inactive fields. By default only active__v fields are listed.",
    )
    parser.add_argument(
        "--skip-types",
        action="store_true",
        help="Do not query object types for per-type required flags (fewer API calls).",
    )
    parser.add_argument(
        "-p",
        "--picklists",
        nargs="?",
        const=True,
        default=None,
        metavar="DIR",
        help=(
            "Also export the values of every picklist used by this object, as "
            "CSV and JSON. Files are written into a subfolder named after the "
            "object. Optionally give the parent directory for that subfolder. "
            "Default: ./<object_name>/<object_name>-picklists.{csv,json}"
        ),
    )
    parser.add_argument(
        "--json",
        dest="json_path",
        help="Also write the raw object metadata response to this file.",
    )
    args = parser.parse_args()

    session_id = os.environ.get("VAULT_SESSION_ID")
    if not session_id:
        print("VAULT_SESSION_ID is not set. See config/vault-metadata-api.md.", file=sys.stderr)
        return 2

    payload = get(
        args.dns, args.version, f"metadata/vobjects/{args.object_name}", session_id
    )
    json_target: Path | None = None
    if args.json_path:
        json_target = Path(args.json_path).expanduser().resolve()
        json_target.parent.mkdir(parents=True, exist_ok=True)
        json_target.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    obj = payload["object"]
    fields = obj.get("fields", [])
    if not args.all_fields:
        fields = [f for f in fields if "active__v" in (f.get("status") or [])]
    fields.sort(key=lambda f: f.get("name", ""))

    per_type: dict[str, list[str]] = {}
    type_names: list[str] = []
    if obj.get("allow_types") and not args.skip_types:
        # The object metadata does not reliably list the types, so ask the
        # configuration API which types exist for this object.
        catalogue = get(args.dns, args.version, "configuration/Objecttype", session_id)
        type_names = [
            entry["name"]
            for entry in catalogue.get("data", [])
            if entry.get("object") == args.object_name
            and entry.get("active")
            and entry.get("name")
        ]
    if type_names and not args.skip_types:
        per_type = required_by_type(
            args.dns, args.version, args.object_name, session_id, type_names
        )

    rows = [
        [
            field.get("name", ""),
            field.get("label", ""),
            field.get("type", ""),
            truthy(field.get("required")),
            truthy(field.get("editable")),
            "-" if field.get("max_length") is None else str(field["max_length"]),
            ", ".join(per_type.get(field.get("name", ""), [])) or "-",
        ]
        for field in fields
    ]
    head = {
        "object_name": args.object_name,
        "label": obj.get("label", "?"),
        "dns": args.dns,
        "version": args.version,
    }
    note = (
        "This object has object types, but they were not queried. "
        "Per-type required flags are missing; re-run without --skip-types."
        if obj.get("allow_types") and args.skip_types
        else None
    )

    if args.format == "csv":
        text = render_csv(rows, head, note)
    else:
        text = render_markdown(rows, head, note)

    if args.output == "-":
        sys.stdout.write(text)
    else:
        default_name = f"{args.object_name}-fields.{args.format}"
        target = Path(args.output or default_name).expanduser().resolve()
        target.parent.mkdir(parents=True, exist_ok=True)
        # newline="" keeps the csv module from turning its \r\n into \r\r\n on Windows.
        target.write_text(text, encoding="utf-8", newline="")
        print(f"{len(fields)} fields written to {target}")

    if args.picklists:
        picklists = fetch_picklists(args.dns, args.version, session_id, fields)
        parent = Path("." if args.picklists is True else args.picklists)
        folder = (parent / args.object_name).expanduser().resolve()
        folder.mkdir(parents=True, exist_ok=True)

        csv_target = folder / f"{args.object_name}-picklists.csv"
        csv_target.write_text(
            render_picklists_csv(picklists, head), encoding="utf-8", newline=""
        )
        json_pl_target = folder / f"{args.object_name}-picklists.json"
        json_pl_target.write_text(
            json.dumps(
                {
                    "object": args.object_name,
                    "label": head["label"],
                    "source": {"dns": args.dns, "api_version": args.version},
                    "picklists": [picklists[name] for name in sorted(picklists)],
                },
                indent=2,
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )
        values = sum(len(entry["values"]) for entry in picklists.values())
        print(f"{len(picklists)} picklists, {values} values written to {folder}")
        print(f"  {csv_target.name}")
        print(f"  {json_pl_target.name}")

    if json_target:
        print(f"Raw API response written to {json_target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
