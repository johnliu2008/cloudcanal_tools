# AGENTS.md — cloudcanal_tools

Flat Python CLI (no packages, tests, lint, or build). Entrypoint: `cloudcanal_tools.py` → `processor.py` (all logic) → `cloudcanal_api_request.py` (payloads) → `post.py` (HTTP) / `cloudcanal_api_response.py` (response check). No business code: schemas are user-supplied JSON/JSONC files.

## Commands

- `pip install -r requirements.txt` (only `requests requests-toolbelt`); a `venv/` exists but targets py3.9/Linux — verify interpreter first.
- `python cloudcanal_tools.py <subcommand> --help`; most subcommands take `cc_num` first (e.g. `python cloudcanal_tools.py listdatajobs 01`).
- Schema input: `create_datajob` / `create_datajob_migration` require `--src-schema-file` + `--dst-schema-file` (JSON/JSONC, see `examples/job_schema_example.jsonc`); optional `--mapping-file`, otherwise default MIRROR mapping. Get a real template via `export_job_schema <cc_num> -a <job_id> --out-dir ./myjob`.
- No test runner. Offline checks: `python -m py_compile *.py` plus direct calls into `cloudcanal_api_request` (pure) and `processor.load_jsonc` / `processor.parse_db_names` / schema-filter helpers.
- Always run from repo root: `sqlite3_operations.py` opens relative `datajobs.db`.

## Config / targeting servers

- `config.py` holds only placeholders; real values come from env: `CC_ACCESS_KEY_ID`, `CC_SECRET_KEY`, `CC_ENDPOINT_TEMPLATE` (supports `{Number}` placeholder, `post.py` does `config.CC_endpoint_str.format(Number=cc_number)`), `CC_SERVER_NUMS` (comma-separated, e.g. `01,02`).
- Never commit real credentials, exported schemas, or `datajobs.db` — all covered by `.gitignore`.

## API quirks (do not "fix" without verifying live)

- `post.py` signs every request via `authenticate.unquoted_public_params()` (retries once; first call can hit 497 signature error).
- JSON posts go via `send_post_request_json`; only `adddatasource` uses multipart `send_post_request_data` (`MultipartEncoder`). Keep that split.
- Schema payloads must be `json.dumps(...).replace(' ','')` — spaces break the API.
- `listdatajobs` defaults to `pageSize: 10, pageNum: 1`; pass `--page-size/--page-num` to page.
- `create_datajob` always runs `precheckbasic` then `precheckdetail` before create; `db_names` like `db1,db2` is only used for the job description — the actual synced DBs come from the schema files. `specId` default 16 (2GB). After `adddatasource` on RDS, user must click "test connection" in console or create fails with code `0001`.
- `cloudcanal_api_response.py` has two `listclusters` defs (second shadows first) and `processor.listworkers` parses via the `listclusters` formatter — fragile, leave as-is unless fixing live.
- Delete flow: CLI `delete_datajob` → `processor.stop_and_delete_datajob` (stop, poll `query_datajob` until `dataTaskStatus == STOP`, 20×3s, re-stop every 10th attempt). `update_delay_alert_threshold` subcommand has no API — it just prints a manual MySQL statement template (with placeholders, no credentials) and exits 1.

## SQLite delete-db flow

- `insert_sqlite3_cloudcanal_jobs` drops/recreates the table each run, then iterates `config.CC_server_nums`.
- `one_key_delete_db <db_name>`: refreshes cache only if not updated today; aborts if 0 or >1 matches (needs human).
- `delete_db_from_job` removes the named DBs (comma-separated) from source/target schemas and `serializeMapping`, then strips the names from the job desc; empty source schema deletes the whole job. `sqlite3_operations.update_records` uses f-string SQL — keep `job_desc` free of quotes.
