# Python Audit Reference

## Framework and Entry Detection

- Flask: `@app.route`, blueprints, `request`.
- Django: `urls.py`, class/function views, middleware, permissions, forms/serializers.
- FastAPI/Starlette: decorators, dependency injection, Pydantic models.
- Tornado/Sanic/Aiohttp: route tables and handlers.
- Celery/RQ/cron/management commands: async entry points and scheduled tasks.

## Sources

`request.args`, `request.form`, `request.json`, `request.files`, `request.headers`, cookies, path parameters, Django `request.GET/POST/FILES`, FastAPI body/path/query params, uploaded filenames, YAML/XML/pickle inputs, queue payloads.

## High-Risk Sinks

- SQL: raw cursor execute with `%`, `.format`, f-strings, SQLAlchemy `text`, Django `.raw`/`extra`.
- Command: `os.system`, `subprocess.*` with `shell=True`, `eval`, `exec`.
- File: `open`, `send_file`, `FileResponse`, `Path`, `shutil`, archive extraction.
- SSRF: `requests`, `urllib`, `httpx`, aiohttp clients with user URLs.
- Deserialization: `pickle`, `marshal`, `shelve`, unsafe `yaml.load`.
- Template: Jinja2 `Template`, `render_template_string`.
- XXE: `lxml`, `xml.etree` with unsafe parser choices.

## Python-Specific Pitfalls

- Pydantic type validation does not make URLs/paths safe for SSRF or traversal.
- `secure_filename` helps filename normalization but does not prove extension, content, or storage safety.
- `subprocess.run([...], shell=False)` is safer than shell strings, but command path and arguments may still be dangerous.
- `os.path.abspath().startswith(base)` has same-prefix bypass; use `resolve()` plus `relative_to()`/boundary checks.
- Debug mode, Werkzeug console, source maps, and stack traces often turn low-level config exposure into serious risk.

## Useful Searches

```bash
rg -n "request\\.(args|form|json|files|headers|cookies)|request\\.GET|request\\.POST|UploadFile|File\\(" -g "*.py"
rg -n "execute\\(|raw\\(|extra\\(|text\\(|os\\.system|subprocess|eval\\(|exec\\(|pickle|yaml\\.load|render_template_string" -g "*.py"
rg -n "requests\\.|httpx\\.|urllib|aiohttp|open\\(|send_file|FileResponse|extractall|ZipFile|TarFile" -g "*.py"
```
