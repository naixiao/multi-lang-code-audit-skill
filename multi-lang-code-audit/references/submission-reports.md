# CNVD and CVE Reports

Use this reference for an explicitly requested CNVD, CVE, GHSA, or advisory report. Otherwise use `report-template.md`. Output Markdown unless the user requests another format. A submission draft does not establish acceptance, an assigned ID, or successful reproduction.

## Mode Selection

- `GENERAL_AUDIT`: Default. Use for ordinary code audit reports, vulnerability summaries, PoCs, remediation, and internal review output.
- `CNVD_SUBMISSION`: The user asks for a CNVD report or submission draft.
- `CVE_SUBMISSION`: The user asks for a CVE, GHSA, CNA, advisory, or vendor-disclosure report.

A request to check known CVEs or review an existing CNVD finding does not, by itself, request a submission report.

Do not ask which mode to use unless the user's wording is ambiguous and the output format materially changes the deliverable.

## Local Examples

When the local `漏洞报告/` folder exists, use it as a style and field reference:

- CNVD examples: `漏洞报告/CNVD/` and `漏洞报告/cnvd_reports/`.
- CVE/advisory examples: `漏洞报告/cve_reports/`.
- SRC/Butian examples may inform readable PoC style, but do not use them as the primary CNVD/CVE structure unless CNVD/CVE examples are missing.

Use the corpus for report shape, section order, evidence granularity, and wording style. Do not copy target names, private data, tokens, cookies, screenshots, or unrelated vulnerability facts into the new report.

The example folders are optional and are not distributed with the skill. If unavailable, use the sections below.

## Evidence Placeholder Rules

Never fabricate screenshots, videos, scan results, CVE IDs, CNVD IDs, vendor confirmation, or public advisory links.

When the report needs visual proof, insert explicit manual-review markers:

```text
[人工复核-截图] 请在此处插入：{what_to_capture}
[人工复核-视频] 请在此处插入：{what_to_record}
```

CNVD evidence expectation:

- Include at least one screenshot marker for vulnerable version, affected page/API, PoC execution, and result proof.
- Include a video marker when the reproduction requires multi-step interaction, login, upload, command execution, data extraction, or time-based behavior.
- Add a short checklist titled `提交前人工复核` with screenshot and video items.

CVE/advisory evidence expectation:

- Include screenshot or terminal-output markers for version confirmation, PoC execution, vulnerable behavior, and fixed-version behavior if available.
- Video is optional and should be marked only when the user requests it or the vulnerability is hard to understand from static output.
- Add a duplicate-check section for existing CVE/GHSA/advisory/public issue searches. If not actually searched, mark it as pending manual verification.

## CNVD Submission Template

Write in Chinese. State what was verified, what remains untested, and which evidence needs to be attached.

Required sections:

1. 漏洞标题
2. 漏洞概述
3. 影响产品/组件/版本
4. 漏洞类型与危害等级
5. 漏洞成因
6. 复现环境
7. 漏洞证明
8. PoC/复现步骤
9. 影响范围
10. 修复建议
11. 参考链接
12. 提交前人工复核

The `漏洞证明` section should include:

- Vulnerable route/API/function.
- Source-to-sink evidence with file and line numbers.
- Request or local PoC.
- Expected vulnerable result.
- `[人工复核-截图]` markers.
- `[人工复核-视频]` marker when the report needs CNVD-style reproduction proof.

## CVE / Advisory Submission Template

Use English when reporting to global maintainers/CNA/GHSA unless the user requests Chinese.

Required sections:

1. Title
2. Summary
3. Affected Product and Versions
4. Vulnerability Type / CWE
5. Root Cause
6. Attack Preconditions
7. Technical Details
8. Proof of Concept
9. Impact
10. Suggested Fix
11. Workarounds
12. Duplicate Check
13. Disclosure Timeline
14. Evidence To Attach

The `Evidence To Attach` section should include:

- `[Manual Review - Screenshot]` for version proof, PoC result, and fixed-version comparison where available.
- `[Manual Review - Video]` only when requested or needed for complex interaction.

## Before Submission

Before finishing CNVD/CVE mode, verify:

- The report contains no unreplaced target placeholders except intentional `{host}`, `{cookie}`, `{token}`, or `{version}` placeholders.
- All exploit claims are backed by code evidence, runtime evidence, or marked as needing manual verification.
- Screenshot/video requirements are visible and cannot be mistaken for already captured evidence.
- CNVD reports are in Chinese unless the user requests otherwise.
- CVE/advisory reports are in English unless the user requests otherwise.
