---
name: multi-lang-code-audit
description: Audit PHP, Java, Python, Go, and .NET/C# source code for security vulnerabilities. Use for white-box review of Web/API/backend projects, tracing suspected vulnerabilities, and writing audit or CNVD/CVE reports with code evidence, PoCs, and remediation.
---

# Multi-language Code Audit

## Scope

For each confirmed finding, connect the entry point, attacker-controlled input, validation gap, sink, trigger conditions, and impact. Keep unresolved traces in a pending section with the missing evidence and next check.

Stay within the requested project and audit scope. By default, read the source and write audit artifacts; do not change target code, install dependencies, commit the target repository, or run destructive PoCs. Confirm the target and permitted actions before dynamic testing.

## References

Read the reference for each language in scope: [PHP](references/php.md), [Java](references/java.md), [Python](references/python.md), [Go](references/go.md), or [.NET/C#](references/dotnet.md).

| Reference | When to use it |
|---|---|
| [Vulnerability matrix](references/vulnerability-matrix.md) | Select checks and finding type codes |
| [Report patterns](references/report-corpus-patterns.md) | Check include, upload, query, archive, and business-logic patterns from past reports |
| [Evidence requirements](references/evidence-gates.md) | Assign a finding status and identify missing proof |
| [Specialized skills](references/existing-skill-map.md) | Use installed PHP/Java helpers for relevant phases |
| [Remediation references](references/external-standards.md) | Check fix guidance and weakness classification |
| [Audit report](references/report-template.md) | Write the default Markdown report |
| [Submission reports](references/submission-reports.md) | Write a CNVD/CVE/GHSA/advisory report when explicitly requested |

## Working Method

For PHP/Java, use installed pipeline and specialized skills where they fit the requested scope. If unavailable, continue with this skill's references. For mixed repositories, map shared entry points once, split the review by module or language, and merge the findings.

When an initial index would help, run `python scripts/audit_inventory.py <source_path> --out <output_dir>`. It uses text matching, not AST or data-flow analysis. The Markdown output caps each candidate list at 200 entries; consult the JSON for the full results. Review excluded directories separately when they are in scope.

Continue from the index to call-chain tracing, exploitability analysis, and reporting.

## Audit Pipeline

### 1. Recon

- Record source root, language mix, framework indicators, dependency manifests, generated/vendor directories, test/demo code, and deploy-relevant config.
- Enumerate HTTP routes, RPC handlers, CLI/cron jobs, queue consumers, upload/download endpoints, template renderers, archive extractors, and admin/back-office surfaces.
- List input sources: path/query/body parameters, JSON/XML bodies, multipart fields, headers, cookies, session/JWT claims, uploaded filenames/content, database-controlled scripts, message queue payloads, environment variables, and config-driven URLs or paths.
- Map authentication and authorization gates for each route or entry. Distinguish authentication, role checks, resource ownership checks, CSRF checks, and business-state checks.

### 2. Source-to-Sink Triage

- Search globally for dangerous sinks and high-risk framework APIs.
- For each sink, record file, line, function/method, sink arguments, nearby validation, reachable entry, and suspected source.
- Prioritize public unauthenticated routes, login/reset/import/upload/admin actions, file/archive handlers, report/query builders, callback/webhook handlers, template customizers, and endpoints with `id`, `file`, `path`, `url`, `cmd`, `query`, `sort`, `order`, `redirect`, `template`, `xml`, or `upload` parameters.
- Check report-derived patterns where the corresponding features exist: dynamic include/page dispatch, original filename preservation, MIME/content-type-derived extension, path fields used as directories, header-derived IP, unauthenticated action dispatchers, weak/default credentials, source map exposure, HQL/ORM short-query fragments, and archive extraction boundary checks.
- Keep search hits without a known call chain as `STATIC_ONLY`; use `PENDING_TRACE` once a partial trace is available.
- For PHP/Java projects, map each candidate to the specialized child skill in `references/existing-skill-map.md`. If the child skill exists, load it before writing category-specific conclusions.

### 3. Trace

- Follow request dispatch to controller/handler/service/DAO/storage calls.
- Track variable assignment, transformations, validation, escaping, canonicalization, type conversion, allowlists, deny lists, and framework binders.
- Confirm whether the sink argument is attacker-controlled at the moment of use.
- For branches, state the exact trigger condition. For environment assumptions, name the dependency, such as database backend, web server script execution, writable directory, archive format, feature flag, scheduled task, or installed plugin.

### 4. Vulnerability Analysis

Assign status using `references/evidence-gates.md`. Record separately whether a PoC was executed; code confirmation alone does not mean runtime reproduction succeeded.

- Confirm a finding only when route or callable entry, controllable source, insufficient guard, reachable sink, and exploitability conditions are all present.
- Mark as environment-dependent when the code creates a dangerous primitive but impact depends on deployment, such as uploaded PHP execution, symlink behavior, same-prefix path layout, database-specific SQL functions, or proxy trust.
- Mark as pending when source or sink is real but reachability, controllability, or branch coverage is incomplete.
- Mark as non-exploitable only with concrete blocking evidence.

### 5. Reporting

Write a Markdown report using `references/report-template.md`:

- Executive summary and risk counts.
- Coverage matrix for routes, auth, dependencies, sink classes, and language/framework-specific checks.
- Findings ordered by severity and exploitability.
- For each finding: ID, severity, affected entry, location, source-to-sink chain, exploitability prerequisites, PoC/request sample, impact, remediation, and confidence.
- Unresolved traces and static sink hits, with the next check for each.
- Fix priority and regression-search commands.

Default to `GENERAL_AUDIT`. When the user explicitly requests a CNVD or CVE/GHSA/advisory report, follow `references/submission-reports.md` for language, sections, local examples, and manual evidence markers. Do not present missing screenshots, videos, assigned IDs, or vendor confirmations as existing evidence.

## Expected Output Layout

When the user does not specify an output path, create `{source_path}_audit` and write:

```text
{output_path}/
  inventory/
    audit_inventory.md
    audit_inventory.json
  working/
    routes.md
    auth_mapping.md
    high_risk_candidates.md
    trace_notes.md
  final/
    {project_name}_code_audit_{timestamp}.md
```

Preserve any specialized skill outputs and merge their findings into the final report.

## Severity Model

When a CVSS score is unavailable, use the following internal priority score. It is not a CVSS calculation and must not be reported as one:

```text
Score = Reachability * 0.40 + Impact * 0.35 + Complexity * 0.25
Priority = Score / 3.0 * 10.0
```

- Reachability: 3 unauthenticated/public, 2 normal authenticated user, 1 admin/internal/scheduled/local, 0 unreachable/dead code.
- Impact: 3 RCE/arbitrary write/full data exposure/account takeover, 2 sensitive read/write/authorization bypass, 1 limited info leak/config weakness, 0 no security impact.
- Complexity: 3 single request/simple payload, 2 multi-step or crafted payload, 1 strict environment/race/chain required, 0 blocked.

Map to `Critical` 9.0-10.0, `High` 7.0-8.9, `Medium` 4.0-6.9, `Low` 0.1-3.9.

Finding IDs use `{severity-prefix}-{type-code}-{sequence}`, such as `C-SQL-001`, `H-UPLOAD-002`, `M-AUTH-003`.

## Before Delivery

Before finishing, verify:

- No confirmed finding lacks file/line evidence.
- No PoC contains unreplaced route, parameter, host, token, or cookie placeholders except explicit `{host}`, `{cookie}`, `{token}`.
- Unresolved high-risk candidates are listed with the evidence still needed.
- Auth requirements and trigger conditions are stated for every finding.
- Remediation includes both a code-level fix direction and a command or pattern to find similar code.
