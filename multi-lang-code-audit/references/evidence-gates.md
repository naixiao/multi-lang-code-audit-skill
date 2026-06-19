# Evidence Gates

Use these gates to prevent both false positives and silent misses.

## Status Labels

| Status | Use When | Required Evidence |
|---|---|---|
| CONFIRMED | The exploit path is closed from entry to sink | Entry, source, validation gap, sink, branch trigger, and impact are all evidenced |
| ENV_DEPENDENT | The dangerous primitive is real but impact depends on deployment | State the exact environmental dependency and fallback impact |
| PENDING_TRACE | Source or sink exists, but reachability/controllability/branch evidence is incomplete | List missing evidence and next trace action |
| STATIC_ONLY | A sink was found by search but no route/call chain is known yet | File/line, pattern, possible entry, suggested trace |
| NOT_EXPLOITABLE | A candidate is blocked | Show the exact guard, allowlist, type conversion, safe API, or unreachable condition |

## Confirmation Checklist

Every confirmed finding needs:

1. Entry: HTTP route, RPC method, CLI task, queue consumer, hook, include chain, or callable public API.
2. Source: attacker-controlled value, including route/path/query/body/header/cookie/file/database/config/message inputs.
3. Control: how the attacker controls the value and any required auth/session/role.
4. Guard analysis: missing, incomplete, misplaced, bypassable, or context-wrong validation.
5. Sink: exact dangerous operation and argument.
6. Trigger: branch, action value, feature flag, scheduler, plugin, DB backend, or environment condition.
7. Impact: what primitive is achieved and what it can realistically affect.
8. PoC: request, script, command, or reproducible steps.

## Common Downgrades

- SQLi behind `password_verify()` can remain SQLi, but do not claim login bypass unless the result row can satisfy password verification.
- File upload to `.php` is RCE only when the upload directory can execute PHP; otherwise report dangerous file upload/arbitrary write with environment-dependent RCE.
- Path traversal mitigated by `startswith(base)` is still suspect; require canonical path plus directory-boundary proof.
- Header-derived IP is user-controlled unless a trusted reverse proxy overwrites it and the app checks proxy trust.
- Admin-only issues can still be High/Critical if ordinary operational roles commonly have access or impact is server compromise.
- Dependency CVEs are findings only when affected version and reachable feature/usage are both evidenced; otherwise place in pending supply-chain risk.
