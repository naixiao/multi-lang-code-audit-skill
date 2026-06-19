# Report Template

```markdown
# {project_name} Code Security Audit Report

- Source path: `{source_path}`
- Audit scope: {scope}
- Languages/frameworks: {languages_frameworks}
- Audit time: {timestamp}
- Overall conclusion: {short conclusion}

## Risk Statistics

| Severity | Count | Notes |
|---|---:|---|
| Critical | 0 | |
| High | 0 | |
| Medium | 0 | |
| Low | 0 | |
| Pending | 0 | |

## Coverage Matrix

| Area | Status | Evidence |
|---|---|---|
| Route/entry mapping | Done / Partial / N/A | {files, commands, counts} |
| Authentication mapping | Done / Partial / N/A | {auth mechanisms} |
| Authorization/object ownership | Done / Partial / N/A | {checks} |
| Dependency review | Done / Partial / N/A | {manifest files} |
| Sink scanning | Done / Partial / N/A | {sink classes and commands} |
| Framework-specific checks | Done / Partial / N/A | {framework refs used} |

## Findings Overview

| ID | Severity | Title | Entry | Status |
|---|---|---|---|---|
| C-SQL-001 | Critical | Example | `/path` | CONFIRMED |

## Vulnerability Details

### [{id}] {title}

| Item | Information |
|---|---|
| Severity | {Critical/High/Medium/Low} (CVSS-like {score}) |
| Status | CONFIRMED / ENV_DEPENDENT / PENDING_TRACE / NOT_EXPLOITABLE |
| Type | {SQL/UPLOAD/AUTH/...} |
| Affected entry | `{route_or_entry}` |
| Auth requirement | None / user / admin / internal / scheduled |
| Location | `{file}:{line}` `{function_or_method}` |
| Reachability (R) | {0-3} - {reason} |
| Impact (I) | {0-3} - {reason} |
| Complexity (C) | {0-3} - {reason} |
| Confidence | High / Medium / Low |

#### Source-to-Sink Chain

1. `{file}:{line}` reads `{source}`.
2. `{file}:{line}` passes/transforms it as `{variable}`.
3. `{file}:{line}` lacks or misapplies `{validation}`.
4. `{file}:{line}` reaches `{sink}`.

#### Exploitability Prerequisites

- Authentication: {detail}
- Input controllability: {detail}
- Trigger condition: {detail}
- Environment dependency: {none/detail}

#### PoC / Verification

```http
{method} {path} HTTP/1.1
Host: {host}
Cookie: {cookie}

{body}
```

#### Impact

{realistic impact, with deployment caveats}

#### Remediation

- {code-level fix}
- {defense-in-depth}
- Regression search:

```bash
rg -n "{pattern}" {paths}
```

## Pending Risk Pool

| Candidate | Type | Known Evidence | Missing Evidence | Next Action |
|---|---|---|---|---|
| `{file}:{line}` | SQL | raw query sink | route trace | trace caller chain |

## Fix Priority

1. {highest priority}
2. {next}

## Completeness Checks

- [ ] Every confirmed finding has location, data flow, PoC, and remediation.
- [ ] Pending static hits are listed.
- [ ] No template placeholders remain except `{host}`, `{cookie}`, `{token}` where intentional.
```
