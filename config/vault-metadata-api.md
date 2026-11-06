# Vault Metadata API — reading object fields

Status: In use
Last reviewed: 2026-10-26

How to read the field definitions of an IQMS Vault object (data type, required,
editable, length limits) without copying configuration by hand.

| Item | Value |
| --- | --- |
| Instance (DEV sandbox) | `bayersbx-iqms-3-1-dev.veevavault.com` |
| API version | `v26.2` |
| Script | [`../scripts/vault-object-fields.py`](../scripts/vault-object-fields.py) |

Only the DEV sandbox is used here. Do not point the script at production
without a reason — it is read-only, but the session ID is a real credential.

## Getting a session ID

A session ID is a short-lived token, valid for the configured session
timeout (20 minutes idle by default) and tied to one Vault instance.

Easiest route, using your own user:

```bash
curl -X POST "https://bayersbx-iqms-3-1-dev.veevavault.com/api/v26.2/auth" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=<user>" --data-urlencode "password=<password>"
```

The response contains `sessionId`. If Bayer SSO blocks password auth, take the
session ID from an authenticated browser session (DevTools → any API call →
`Authorization` header), or ask the IQMS Vault admin for an integration user.

## Running the script

The session ID is passed via the environment, never as an argument — arguments
land in the shell history and in the process list.

```bash
export VAULT_SESSION_ID='<sessionId>'
python scripts/vault-object-fields.py complaint__v
```

The script writes a field table and prints the absolute path of the file it
wrote. By default that file is `./<object_name>-fields.<format>` in the current
directory. Useful flags:

| Flag | Effect |
| --- | --- |
| `-f`, `--format md\|csv` | Output format (default: `md`) |
| `-p`, `--picklists [dir]` | Also export every picklist used by the object, as CSV *and* JSON, into a subfolder named after the object |
| `-o`, `--output <path>` | Path and file name of the output. Missing directories are created. `-` prints to the terminal instead |
| `--all-fields` | Include inactive fields (default: `active__v` only) |
| `--skip-types` | Skip the per-object-type calls (faster, loses per-type required flags) |
| `--json <path>` | Also write the raw API response, for diffing between environments |
| `--dns`, `--version` | Target another instance or API version |

To write the result straight into the repo:

```bash
python scripts/vault-object-fields.py complaint__v \
  -o docs/02-requirements/complaint-fields.md
```

`python scripts/vault-object-fields.py --help` lists these with examples.

In CSV the column header is the first row and the data below it stays a clean
rectangle; the title and source lines are appended at the *end* of the file, so
Excel and pandas can read it without skipping rows.

## Picklist values

`-p` additionally resolves every picklist referenced by the object's fields and
writes both formats into a subfolder named after the object:

```bash
python scripts/vault-object-fields.py complaint__v -f csv -p
# -> ./complaint__v/complaint__v-picklists.csv
# -> ./complaint__v/complaint__v-picklists.json
```

`-p docs/02-requirements` puts the `complaint__v/` subfolder under that path.

The CSV is one row per value (`Picklist, Value name, Value label, Order, Used by
fields`) and is the better format for review in Excel. The JSON keeps the
nesting plus `controlling_picklist`, which names the picklist a dependent
picklist hangs off — relevant where values are filtered by country or region.

Picklists are fetched once per picklist, not once per field; `Used by fields`
lists every field sharing it. Only **active** values are returned by the API.

Review the output before committing. The raw JSON is a configuration dump, not
a document — keep it out of git unless there is a reason to version it.

## Reading the output

- **Required** is the object-wide flag from the API. It is not the whole truth.
- **Required on type** is the per-object-type flag. A field that is optional on
  the object can be mandatory on *Pharma Complaint* but not on *MedTech
  Complaint*. For the classification logic this column usually matters more
  than the object-wide one.
- Neither column covers mandatory-ness that comes from **layout rules** or
  **lifecycle state / Atomic Security**. Those are not exposed by
  `/metadata/vobjects/` and have to come from the Admin UI or a configuration
  report.

## Which object?

Veeva QMS supports two data models for complaints: a standalone `complaint__v`
object, or `quality_event__v` with a *Complaint* object type. The field names
differ between them. Confirm which one this Vault uses before building on the
output — if `complaint__v` returns a 404, it is the Quality Event model:

```bash
python scripts/vault-object-fields.py quality_event__v
```

Related intake-side objects: `complaint_intake__v`, `reported_product__v`,
`reported_product_batch__v`, `complaint_contact__v`.

## Secrets

Never commit a session ID, a password, or a raw metadata dump containing
record data. `.env` and `.env.*` are gitignored; this file holds no secret.
