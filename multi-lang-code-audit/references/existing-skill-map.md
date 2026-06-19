# Existing Local Skill Map

Use this map when the relevant child skill exists in the current Codex environment. The multi-language skill remains the orchestrator: it chooses scope, preserves evidence gates, merges outputs, and produces the final report.

## Java

Default orchestration:

- `java-audit-pipeline`: full Java Web audit workflow when the user asks for a full Java project audit.

Core phases:

| Phase | Child Skill | Use For |
|---|---|---|
| Route and parameter mapping | `java-route-mapper` | Extract all Spring MVC, Servlet, JAX-RS, Struts 2, CXF/SOAP routes and parameters |
| Authentication/authorization | `java-auth-audit` | Identify Shiro, Spring Security, JWT, filters, interceptors, custom auth, bypass and authorization flaws |
| Dependency scan | `java-vuln-scanner` | Scan `pom.xml`, `build.gradle`, jars, and known Java component CVEs |
| Deep trace | `java-route-tracer` | Trace route/controller/action to service/DAO/sink |

Java sink skills:

| Type | Child Skill |
|---|---|
| SQL/HQL/MyBatis/Hibernate injection | `java-sql-audit` |
| File read/path traversal | `java-file-read-audit` |
| File upload | `java-file-upload-audit` |
| XXE/XML parser issues | `java-xxe-audit` |

Java delegation rule:

1. Run route mapping before sink-specific conclusions.
2. Run auth mapping before severity is finalized.
3. Run route tracing for multi-hop, inherited/base-class, XML-configured, or decompiled paths.
4. Use sink child skills only for categories evidenced by route/trace/static sink candidates.
5. Merge child outputs into the final report and list skipped child skills with a reason.

## PHP

Default orchestration:

- `php-audit-pipeline`: full PHP Web audit workflow when the user asks for a full PHP project audit.

Core phases:

| Phase | Child Skill | Use For |
|---|---|---|
| Route and parameter mapping | `php-route-mapper` | Extract all native PHP, Laravel, Symfony, Slim, WordPress, ThinkPHP/Yii/CodeIgniter routes and request templates |
| Authentication/authorization | `php-auth-audit` | Identify sessions, JWT, middleware, WordPress nonce/capability checks, bypass and IDOR |
| Deep trace | `php-route-tracer` | Trace route/handler through functions/classes/includes to sinks |
| Dependency scan | `php-vuln-scanner` | Scan Composer manifests and PHP package risks |
| Exploit chain aggregation | `php-exploit-chain-audit` | Combine confirmed findings into realistic chained attack paths |

PHP sink skills:

| Type | Child Skill |
|---|---|
| SQL injection | `php-sql-audit` |
| XSS | `php-xss-audit` |
| CSRF | `php-csrf-audit` |
| SSRF | `php-ssrf-audit` |
| XXE | `php-xxe-audit` |
| Command injection | `php-cmd-audit` |
| File read/path traversal/LFI | `php-file-read-audit` |
| File upload | `php-file-upload-audit` |
| File write | `php-file-write-audit` |
| Filesystem operations | `php-filesystem-audit` |
| Archive extract/Zip Slip | `php-archive-extract-audit` |
| Deserialization/object injection | `php-deser-audit` |
| Template/SSTI | `php-tpl-audit` |
| Expression injection | `php-expr-audit` |
| NoSQL injection | `php-nosql-audit` |
| LDAP injection | `php-ldap-audit` |
| Open redirect | `php-open-redirect-audit` |
| CRLF/response splitting | `php-crlf-audit` |
| Crypto/secrets | `php-crypto-audit` |
| Config exposure | `php-config-audit` |
| Logging/monitoring | `php-logging-audit` |
| Business logic | `php-logic-audit` |

PHP framework skills:

| Framework | Child Skill |
|---|---|
| Laravel | `php-laravel-audit` |
| Symfony | `php-symfony-audit` |
| ThinkPHP | `php-thinkphp-audit` |
| WordPress | `php-wordpress-audit` |
| Yii/Yii2 | `php-yii-audit` |
| CodeIgniter | `php-codeigniter-audit` |

PHP delegation rule:

1. Run route/parameter mapping first. Include native dispatchers, `action` parameters, admin AJAX handlers, hooks, CLI/cron/queue entries, and dynamic includes.
2. Run auth mapping before ranking unauthenticated/admin-only impact.
3. Build a high-risk candidate list from route params, auth gaps, dependency risks, and global sink search.
4. Use `php-route-tracer` or equivalent trace evidence for trace-gated sinks: SQL, command, SSRF, file read/write/upload, archive, XSS, redirect, CRLF, XXE, deserialization, template, LDAP, expression injection, auth, CSRF, and session flaws.
5. Use framework skills only when framework indicators are present.
6. Keep static sink hits that lack trace closure in the pending-risk pool.

## When a Child Skill Is Missing

Do not fail the audit. Use this skill's standalone references for the same category, record that the specialized child skill was unavailable, and preserve the evidence standard.
