# Go Audit Reference

## Framework and Entry Detection

- Standard library: `http.HandleFunc`, `ServeHTTP`, routers.
- Gin: `router.GET/POST`, `c.Query`, `c.PostForm`, `ShouldBind`.
- Echo/Fiber/Chi/Beego: route registrations and handlers.
- gRPC: service implementations and generated method bindings.
- Workers/CLI: Cobra commands, cron jobs, queue consumers.

## Sources

`r.URL.Query`, `r.FormValue`, `r.PostForm`, JSON decoders, path params, headers, cookies, multipart filenames/content, Gin/Echo/Fiber context getters, gRPC request fields, archive entry names, config URLs/paths.

## High-Risk Sinks

- SQL: `database/sql` `Query/Exec`, string-built SQL, GORM `Raw`, `Where` with raw fragments.
- Command: `os/exec.Command`, shell invocation through `sh -c`.
- File: `os.Open`, `os.ReadFile`, `os.WriteFile`, `os.Create`, `filepath.Join`, `http.ServeFile`.
- Upload/archive: multipart save, `archive/zip`, `archive/tar`, symlink/hardlink extraction.
- SSRF: `http.Get`, `http.Client.Do`, custom transports.
- XML: `encoding/xml` entity behavior, custom decoders.
- Template: `html/template` vs `text/template`, dynamic template parsing.

## Go-Specific Pitfalls

- `filepath.Join(base, user)` cleans traversal but does not prove the result stays under base.
- `strings.HasPrefix(path, base)` has same-prefix sibling bypass; use `filepath.Rel` and reject `..` or absolute relatives.
- `exec.Command` with separated args avoids shell injection, but attacker-controlled executable name or flags can still matter.
- `html/template` autoescapes HTML contexts; `text/template` does not.
- Archive extraction must reject absolute paths, `..`, symlinks/hardlinks, Windows backslashes, and same-prefix sibling paths.

## Useful Searches

```bash
rg -n "http\\.HandleFunc|ServeHTTP|\\.GET\\(|\\.POST\\(|c\\.Query|c\\.PostForm|ShouldBind|FormValue|URL\\.Query" -g "*.go"
rg -n "db\\.(Query|Exec)|Raw\\(|Where\\(|fmt\\.Sprintf.*SELECT|exec\\.Command|sh -c" -g "*.go"
rg -n "os\\.(Open|ReadFile|WriteFile|Create)|filepath\\.(Join|Clean|Rel)|ServeFile|zip\\.|tar\\.|http\\.(Get|Post)|Client\\.Do" -g "*.go"
```
