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

## Submission Mode Addendum

Use this addendum only when the user explicitly asks for a CNVD-ready or CVE-ready report. Otherwise do not add these sections.

### CNVD-Ready Evidence Markers

```markdown
## 提交前人工复核

- [ ] [人工复核-截图] 漏洞产品、组件或版本证明：{where_to_capture}
- [ ] [人工复核-截图] PoC 请求或本地复现命令：{where_to_capture}
- [ ] [人工复核-截图] 漏洞触发结果或敏感影响证明：{where_to_capture}
- [ ] [人工复核-视频] 从环境准备、触发漏洞到结果证明的完整复现过程：{what_to_record}
```

### CVE / Advisory Evidence Markers

```markdown
## Evidence To Attach

- [ ] [Manual Review - Screenshot] Affected version proof: {where_to_capture}
- [ ] [Manual Review - Screenshot] PoC execution and vulnerable result: {where_to_capture}
- [ ] [Manual Review - Screenshot] Fixed-version or patched-behavior comparison, if available: {where_to_capture}
- [ ] [Manual Review - Video] Optional only when interaction is complex or the user requests video proof: {what_to_record}
```
