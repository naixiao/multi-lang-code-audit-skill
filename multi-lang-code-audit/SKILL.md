---
name: multi-lang-code-audit
description: Evidence-driven white-box security audit workflow for PHP, Java, Python, .NET/C#, and Go source code. Use when Codex needs to audit Web/API/backend projects for routes, authentication, authorization, user-controlled inputs, dangerous sinks, dependency risks, exploitability, PoC requests, CNVD Chinese DOCX reports, CVE/advisory reports, and vulnerabilities including SQL injection, command injection, SSRF, XSS, file read/write/upload, Zip Slip, deserialization, XXE, auth bypass, IDOR, CSRF, weak credentials, unauthenticated access, configuration exposure, and business logic flaws.
---

# Multi-language Code Audit

## Operating Rule

Audit by evidence chain, not keyword hits. Every confirmed finding must connect an entry point or callable surface to user-controlled data, missing or bypassable validation, a real sink, exploitability conditions, and remediation. Preserve suspicious but unclosed traces in a pending-risk section instead of silently dropping them.

## Quick Start

1. Identify the project language, framework, dependency manifests, entry points, and routing style.
2. Run `scripts/audit_inventory.py <source_path> --out <output_dir>` when a filesystem scan is useful.
3. Read only the needed language reference:
   - PHP: `references/php.md`
   - Java: `references/java.md`
   - Python: `references/python.md`
   - .NET/C#: `references/dotnet.md`
   - Go: `references/go.md`
4. Use `references/vulnerability-matrix.md` to select vulnerability classes and evidence requirements.
5. Read `references/report-corpus-patterns.md` for practical patterns mined from the local vulnerability report corpus.
6. Use `references/evidence-gates.md` to decide confirmed, environment-dependent, pending, or non-exploitable status.
7. For PHP or Java projects, read `references/existing-skill-map.md` and delegate to the listed specialized local skills when available.
8. Use `references/external-standards.md` only as a compact baseline for remediation and classification.
9. Choose the report mode. If the user did not explicitly request a submission-ready report, write the normal audit report with `references/report-template.md`. If the user asks to generate a CNVD vulnerability report, always create a Chinese `.docx` report and read `references/submission-reports.md`. If the user requests a CVE submission-ready report, read the same reference and use the CVE/advisory format.

## Operating Modes

Use the strongest available mode for the target project.

- **Delegated PHP mode**: If the project is PHP and the named PHP audit skills are installed, use `php-audit-pipeline` as the default orchestration model. Use `php-route-mapper`, `php-auth-audit`, `php-route-tracer`, and the relevant `php-*-audit` skills for sink-specific evidence.
- **Delegated Java mode**: If the project is Java and the named Java audit skills are installed, use `java-audit-pipeline` as the default orchestration model. Use `java-route-mapper`, `java-auth-audit`, `java-route-tracer`, `java-vuln-scanner`, and the relevant Java sink skills.
- **Standalone mode**: For Python, .NET/C#, Go, or when a specialized child skill is missing, use this skill's references and `audit_inventory.py` to complete the same evidence-driven workflow manually.
- **Hybrid mode**: For mixed repositories, run recon once, split by language/module, run delegated PHP/Java mode where possible, standalone mode for other languages, then merge into one report.

Never stop at inventory output. The inventory is only a starting index; a usable audit requires trace, exploitability judgment, and a report.

## Audit Pipeline

### 1. Recon

Map the repository before judging vulnerabilities.

- Record source root, language mix, framework indicators, dependency manifests, generated/vendor directories, test/demo code, and deploy-relevant config.
- Enumerate HTTP routes, RPC handlers, CLI/cron jobs, queue consumers, upload/download endpoints, template renderers, archive extractors, and admin/back-office surfaces.
- List input sources: path/query/body parameters, JSON/XML bodies, multipart fields, headers, cookies, session/JWT claims, uploaded filenames/content, database-controlled scripts, message queue payloads, environment variables, and config-driven URLs or paths.
- Map authentication and authorization gates for each route or entry. Distinguish authentication, role checks, resource ownership checks, CSRF checks, and business-state checks.

### 2. Source-to-Sink Triage

Build a candidate index, then prioritize.

- Search globally for dangerous sinks and high-risk framework APIs.
- For each sink, record file, line, function/method, sink arguments, nearby validation, reachable entry, and suspected source.
- Prioritize public unauthenticated routes, login/reset/import/upload/admin actions, file/archive handlers, report/query builders, callback/webhook handlers, template customizers, and endpoints with `id`, `file`, `path`, `url`, `cmd`, `query`, `sort`, `order`, `redirect`, `template`, `xml`, or `upload` parameters.
- Always add corpus-derived candidates: dynamic include/page dispatch, original filename preservation, MIME/content-type-derived extension, path fields used as directories, header-derived IP, unauthenticated action dispatchers, weak/default credentials, source map exposure, HQL/ORM short-query fragments, and archive extraction boundary checks.
- Keep static-only hits as `PENDING_STATIC` until reachability and controllability are closed.
- For PHP/Java projects, map each candidate to the specialized child skill in `references/existing-skill-map.md`. If the child skill exists, load it before writing category-specific conclusions.

### 3. Trace

For each high-priority candidate, trace actual data flow.

- Follow request dispatch to controller/handler/service/DAO/storage calls.
- Track variable assignment, transformations, validation, escaping, canonicalization, type conversion, allowlists, deny lists, and framework binders.
- Confirm whether the sink argument is attacker-controlled at the moment of use.
- For branches, state the exact trigger condition. For environment assumptions, name the dependency, such as database backend, web server script execution, writable directory, archive format, feature flag, scheduled task, or installed plugin.

### 4. Vulnerability Analysis

Classify with the matrix and avoid overclaiming.

- Confirm a finding only when route or callable entry, controllable source, insufficient guard, reachable sink, and exploitability conditions are all present.
- Mark as environment-dependent when the code creates a dangerous primitive but impact depends on deployment, such as uploaded PHP execution, symlink behavior, same-prefix path layout, database-specific SQL functions, or proxy trust.
- Mark as pending when source or sink is real but reachability, controllability, or branch coverage is incomplete.
- Mark as non-exploitable only with concrete blocking evidence.

### 5. Reporting

Use the report template and include:

- Executive summary and risk counts.
- Coverage matrix for routes, auth, dependencies, sink classes, and language/framework-specific checks.
- Findings ordered by severity and exploitability.
- For each finding: ID, severity, affected entry, location, source-to-sink chain, exploitability prerequisites, PoC/request sample, impact, remediation, and confidence.
- Pending-risk pool for unresolved traces and static sink hits.
- Fix priority and regression-search commands.

Report mode rules:

- Default to `GENERAL_AUDIT` when the user only asks for audit results, vulnerability report, PoC, or remediation.
- Use `CNVD_SUBMISSION` whenever the user explicitly asks to generate a CNVD vulnerability report, CNVD-ready report, CNVD-submittable report, or CNVD-style report. Generate it in Chinese and deliver it as a real `.docx` document, not Markdown renamed to `.docx`.
- Use `CVE_SUBMISSION` only when the user explicitly asks for a CVE-ready, CVE-submittable, advisory, GHSA, or responsible-disclosure style report.
- For CNVD/CVE submission modes, include manual evidence markers instead of pretending screenshots or videos were captured. CNVD usually needs screenshots and often a reproduction video; CVE/advisory reports usually need screenshots or terminal output, but not video unless requested.
- For `CNVD_SUBMISSION`, use available Word document tooling, preferably the installed documents skill. Apply professional Chinese report styles, render the DOCX to page images, inspect every page for layout defects, fix issues, and deliver the final `.docx` as the primary report artifact.

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

For `CNVD_SUBMISSION`, replace the normal final report with:

```text
{output_path}/final/{project_name}_CNVD漏洞报告_{timestamp}.docx
```

Do not treat an intermediate Markdown draft as the CNVD deliverable. The final CNVD report must be a valid Word document and must be visually verified after rendering when document rendering is available.

For delegated PHP/Java mode, preserve child skill outputs when they are generated, but also merge the findings into the single final report.

## Severity Model

Use this scoring when CVSS is not already known:

```text
Score = Reachability * 0.40 + Impact * 0.35 + Complexity * 0.25
CVSS-like = Score / 3.0 * 10.0
```

- Reachability: 3 unauthenticated/public, 2 normal authenticated user, 1 admin/internal/scheduled/local, 0 unreachable/dead code.
- Impact: 3 RCE/arbitrary write/full data exposure/account takeover, 2 sensitive read/write/authorization bypass, 1 limited info leak/config weakness, 0 no security impact.
- Complexity: 3 single request/simple payload, 2 multi-step or crafted payload, 1 strict environment/race/chain required, 0 blocked.

Map to `Critical` 9.0-10.0, `High` 7.0-8.9, `Medium` 4.0-6.9, `Low` 0.1-3.9.

Finding IDs use `{severity-prefix}-{type-code}-{sequence}`, such as `C-SQL-001`, `H-UPLOAD-002`, `M-AUTH-003`.

## Quality Bar

Before finishing, verify:

- No confirmed finding lacks file/line evidence.
- No PoC contains unreplaced route, parameter, host, token, or cookie placeholders except explicit `{host}`, `{cookie}`, `{token}`.
- No high-risk sink disappeared merely because the trace was incomplete; unresolved items are in the pending-risk pool.
- Auth requirements and trigger conditions are stated for every finding.
- Remediation includes both a code-level fix direction and a command or pattern to find similar code.
