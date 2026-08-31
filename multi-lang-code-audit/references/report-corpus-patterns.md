# Patterns from Vulnerability Reports

These checks come from vulnerability reports. Apply them to the relevant features in the target project; the original reports are not included in this repository.

## PHP Patterns

### Dynamic Include With Wrapper Bypass

Observed shape:

```php
$page = $_GET['page'] ?? 'home';
include $page . '.php';
```

Audit points:

- Appending `.php` is not a whitelist.
- Check wrapper prefixes: `php://filter`, `file://`, `phar://`, `zip://`.
- Check public front controllers and admin panels separately.
- Confirm whether included paths are executed or source-readable through filters.
- Report source disclosure as critical when DB config or secrets are reachable.

Search:

```bash
rg -n "include\\s+\\$|require\\s+\\$|page.*include|php://|file://|phar://" -g "*.php"
```

### Upload Uses MIME or Original Filename

Observed shapes:

- `mime_content_type()` or framework MIME APIs are accepted as proof of image type.
- `getClientOriginalName()` or `$_FILES['name']` becomes the saved name.
- Multi-extension names such as `shell.jpg.php` keep the executable suffix.
- GIF/polyglot headers such as `GIF89a` can satisfy content sniffers.

Audit points:

- Require extension allowlist, server-generated name, content decode/re-encode for images, webroot isolation, and execution disabled in upload directories.
- Treat RCE as environment-dependent when web server execution of the upload directory is not proven.
- Still report dangerous file upload/arbitrary write when executable interpretation is unproven.

Search:

```bash
rg -n "move_uploaded_file|getClientOriginalName|mime_content_type|tmp_name|\\$_FILES|UploadedFile|extension\\(" -g "*.php"
```

### Unauthenticated Action Dispatcher

Observed shape:

```php
$action = $_GET['action'];
if ($action == 'save_category') { $crud->save_category(); }
```

Audit points:

- Verify dispatcher-level authentication and method-level authorization.
- Check state-changing actions, admin actions, upload actions, and delete/update actions.
- `extract($_POST)` is a strong risk signal for SQL injection, mass assignment, and business logic flaws.

Search:

```bash
rg -n "action\\]|extract\\(\\$_POST\\)|save_|delete_|update_|confirm_|ajax\\.php" -g "*.php"
```

### Header-Derived SQL/Input

Observed shape: shopping cart or identity logic trusts `HTTP_X_FORWARDED_FOR`.

Audit points:

- Treat proxy headers as user-controlled unless trusted proxy enforcement is visible.
- Check whether header values enter SQL, cache keys, rate limits, ACLs, logs, or business identity decisions.

Search:

```bash
rg -n "HTTP_X_FORWARDED_FOR|HTTP_CLIENT_IP|REMOTE_ADDR|client_ip|real_ip" -g "*.php"
```

### Password Verification Does Not Remove SQLi

If username/email SQL is injectable before `password_verify()`, keep the SQLi finding even when simple login bypass is blocked. Do not claim login bypass unless a row can satisfy password verification or the query can control the verified hash.

## Java Patterns

### Path Field Controls Upload Directory

Observed shape:

- A model field such as `uniqueId`, `name`, `folder`, or `path` is stored after light normalization such as `trim()`.
- Later it is used in `Paths.get(base, field, filename)`.
- The extension or filename is derived from request headers such as `Content-Type`.

Audit points:

- Trace create/update permission for the object containing the path field.
- Check default registration or low-privilege object creation.
- Require canonical base-dir boundary validation after path resolution.
- Check whether write can reach static web directories or executable locations.

Search:

```bash
rg -n "Paths\\.get|Files\\.createDirectories|FileOutputStream|Content-Type|@HeaderParam|getOriginalFilename|transferTo|setUniqueId|set.*Path" -g "*.java"
```

### HQL/ORM Short Query Fragment Injection

Observed shape:

- REST/query API accepts `q`, `query`, `where`, `filter`, `order`, `sort`, or `type=hql`.
- Code builds an HQL/JPQL string from a partial query.
- Security checks treat short forms like `where ...` as safe before completing/parsing the query.

Audit points:

- Distinguish SQL, HQL, JPQL, and ORM DSL injection.
- Check backend-specific payload feasibility and version/fix commits.
- Do not assume ORM query managers are safe when raw fragments are accepted.

Search:

```bash
rg -n "createQuery|createNativeQuery|HQL|JPQL|whereSQL|queryString|type=hql|SearchSource|QueryManager|orderField|sort" -g "*.java"
```

### Mapper XML and Base DAO Expansion

Audit MyBatis XML and inherited DAO helpers even if controller code looks clean. Prioritize `${}`, dynamic `ORDER BY`, `GROUP BY`, `LIMIT`, report builders, and pagination helpers.

Search:

```bash
rg -n "\\$\\{|ORDER BY|GROUP BY|LIMIT|createQuery|Statement|StringBuilder.*sql|append\\(" -g "*.java" -g "*.xml"
```

## Cross-Language Patterns

### Same-Prefix Boundary Bypass

Observed in archive/path reports:

```text
base: /tmp/base/out
candidate: /tmp/base/out2/evil.txt
raw startsWith(base): true
actual directory: outside base
```

Audit points:

- Reject raw string prefix checks.
- Use canonical/absolute normalization and path-relative checks.
- Include Windows separator and backslash variants.
- For archives, reject absolute paths, `..`, same-prefix siblings, symlinks, hardlinks, device names, and metadata-changing entries.

### Weak Credentials and Unauthenticated Admin Surfaces

For admin/backend projects:

- Enumerate exposed admin panels and dashboards.
- Check default credentials from docs, seed data, docker compose, installation SQL, and README.
- Check source maps, static frontend route guards, unauthenticated API calls behind admin UIs, and direct backend endpoints.
- Report weak credentials separately from authorization bypass unless both are evidenced.

### Business Logic and State Transitions

Common report themes include recharge limit bypass, ranking manipulation, invitation/share logic defects, order/status transitions, and role-specific privilege gaps. For business logic:

- Define the intended invariant.
- Show the exact request sequence that violates it.
- Distinguish missing server-side checks from front-end-only restrictions.
- Include replay, race, negative value, duplicate submit, and cross-account object ownership checks.

## Reporting

Use [report-template.md](report-template.md) for the report structure. Where trace notes use evidence IDs, carry those IDs into the finding so the reader can locate the supporting code.
