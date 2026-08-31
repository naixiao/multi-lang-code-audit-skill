# Remediation References

Use these references for fixes and CWE mapping. Finding status still depends on the target code.

## SQL Injection

Baseline:

- Prefer parameterized queries/prepared statements for data values.
- Use allowlists for identifiers that cannot be parameterized, such as column names, sort fields, and sort direction.
- Stored procedures are not automatically safe if they build dynamic SQL internally.

Reference: OWASP SQL Injection Prevention Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html

## File Upload

Baseline:

- Validate extension with an allowlist after decoding/normalizing the filename.
- Do not rely on `Content-Type` alone.
- Change the filename to a server-generated safe name.
- Store uploads outside the webroot when possible.
- Disable script execution in upload locations and enforce size/content checks.

Reference: OWASP File Upload Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html

## Path Traversal and File Access

Baseline:

- Prefer fixed allowlist mapping over user-supplied paths.
- Canonicalize/normalize the combined path and verify it remains inside the intended base directory.
- Raw `startsWith(base)` or `indexOf(base) == 0` is insufficient because of same-prefix sibling paths.
- Check encoded traversal, backslash separators, absolute paths, null bytes where relevant, symlinks, and wrapper/protocol prefixes.

References:

- OWASP Path Traversal, https://owasp.org/www-community/attacks/Path_Traversal
- CWE-23 Relative Path Traversal, https://cwe.mitre.org/data/definitions/23.html

## Archive Extraction

Baseline:

- Treat every archive entry name and link target as untrusted.
- Reject absolute paths, `..`, same-prefix siblings, symlinks/hardlinks that escape, and platform separator tricks.
- Validate the final canonical destination before writing.

Reference: CWE-23 notes Zip Slip as archive-based relative path traversal, https://cwe.mitre.org/data/definitions/23.html

For finding status and required proof, see [evidence-gates.md](evidence-gates.md).
