# .NET/C# Audit Reference

## Framework and Entry Detection

- ASP.NET MVC/Web API: controllers, actions, route attributes, filters, authorization attributes.
- ASP.NET Core: endpoint routing, minimal APIs, middleware, `MapGet/MapPost`, Razor Pages.
- Legacy WebForms/ASHX: handlers, page events, query/form access.
- Background services: hosted services, queues, scheduled jobs.

## Sources

`Request.Query`, `Request.Form`, route values, model-bound DTOs, headers, cookies, uploaded files, JWT claims, session, XML/JSON bodies, SignalR messages, queue messages.

## High-Risk Sinks

- SQL: `SqlCommand`, Dapper raw SQL, EF Core `FromSqlRaw`, `ExecuteSqlRaw`, interpolated SQL misuse.
- Command: `Process.Start`, `cmd.exe`, PowerShell invocation.
- File: `File.*`, `Path.Combine`, `Directory.*`, `PhysicalFile`, upload `IFormFile.FileName`.
- SSRF: `HttpClient`, `WebRequest`, `RestSharp` with user URL.
- XML/XXE: `XmlDocument`, `XmlReader`, `XDocument`, `DataSet.ReadXml` with unsafe resolver/settings.
- Deserialization: `BinaryFormatter`, `NetDataContractSerializer`, unsafe JSON type handling.
- Template: Razor view path/name control, string-based template engines.

## .NET-Specific Pitfalls

- `[Authorize]` on controllers does not protect endpoints mapped elsewhere or actions marked `[AllowAnonymous]`.
- Model validation attributes do not enforce authorization or object ownership.
- `Path.Combine(base, userPath)` ignores `base` if `userPath` is rooted; canonicalize after combining.
- `FromSqlInterpolated` differs from `FromSqlRaw`; do not treat all interpolated-looking SQL equally.
- XML safety depends on actual `XmlReaderSettings` and resolver usage.

## Useful Searches

```bash
rg -n "\\[Http(Get|Post|Put|Delete)|Map(Get|Post|Put|Delete)|Controller|Request\\.(Query|Form|Body|Headers|Cookies)" -g "*.cs"
rg -n "SqlCommand|FromSqlRaw|ExecuteSqlRaw|Dapper|Query\\(|Execute\\(|Process\\.Start|BinaryFormatter|NetDataContractSerializer" -g "*.cs"
rg -n "IFormFile|FileName|Path\\.Combine|File\\.|Directory\\.|HttpClient|WebRequest|XmlDocument|XmlReader|XDocument" -g "*.cs"
```
