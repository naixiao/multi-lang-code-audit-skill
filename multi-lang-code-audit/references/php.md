# PHP Audit Reference

## Framework and Entry Detection

- Native/front controller: `index.php`, `admin/ajax.php`, `action` dispatchers, dynamic `include`.
- Laravel: `routes/web.php`, `routes/api.php`, controllers, middleware, policies, form requests.
- Symfony: `config/routes*`, controller attributes/annotations, voters, security config.
- ThinkPHP/CodeIgniter/Yii: route config, controller/action naming, filters/hooks.
- WordPress: `add_action`, `admin-ajax.php`, `admin-post.php`, REST routes, nonce/capability checks.

## Sources

`$_GET`, `$_POST`, `$_REQUEST`, `$_COOKIE`, `$_FILES`, `$_SERVER` headers, `php://input`, JSON/XML decoders, session values that can be set earlier by users, database-driven scripts/templates, uploaded filename/content.

Treat `HTTP_X_FORWARDED_FOR`, `HTTP_CLIENT_IP`, and similar headers as attacker-controlled unless trusted proxy checks are explicit.

## High-Risk Sinks

- SQL: `mysqli_query`, `$conn->query`, `PDO::query`, `DB::raw`, ThinkPHP `whereRaw`, string-built query fragments.
- Command: `system`, `exec`, `shell_exec`, `passthru`, `proc_open`, backticks, `eval`, `assert`, `preg_replace /e`.
- File read/write: `include`, `require`, `file_get_contents`, `readfile`, `fopen`, `unlink`, `rename`, `copy`, `file_put_contents`.
- Upload: `move_uploaded_file`, framework upload helpers, original filename APIs.
- SSRF: `curl_setopt(CURLOPT_URL)`, `file_get_contents($url)`, Guzzle URL construction.
- Deserialization: `unserialize`, PHAR metadata paths, session serializers.
- XML: `simplexml_load_string`, `DOMDocument::loadXML`, `XMLReader`.
- Template: Twig/Blade/raw template rendering, user-controlled template names.

## PHP-Specific Pitfalls

- Appending `.php` does not block `php://filter` local file inclusion.
- Deny lists miss `.phtml`, `.phar`, `.shtml`, double extensions, case variants, and web server handler quirks.
- MIME checks using `mime_content_type()` are insufficient without extension allowlist and image re-encoding.
- `extract($_POST)` often creates mass-assignment and SQL/action-dispatch surprises.
- Duplicate legacy class files can preserve vulnerabilities after the main dispatcher is fixed.
- `password_verify()` can block auth bypass but not remove the underlying SQL injection.

## Useful Searches

```bash
rg -n "\$_(GET|POST|REQUEST|COOKIE|FILES|SERVER)|php://input|json_decode" -g "*.php"
rg -n "query\(|mysqli_query|DB::raw|whereRaw|\$\{|\bexec\b|system\(|shell_exec|eval\(|assert\(" -g "*.php"
rg -n "include|require|file_get_contents|readfile|fopen|unlink|rename|copy|file_put_contents|move_uploaded_file" -g "*.php"
rg -n "csrf|token|nonce|check_admin_referer|middleware|auth|session|login|permission|role|capability" -g "*.php"
```
