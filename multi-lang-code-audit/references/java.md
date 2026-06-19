# Java Audit Reference

## Framework and Entry Detection

- Spring MVC/Boot: `@RequestMapping`, `@GetMapping`, `@PostMapping`, `@RestController`, `@Controller`, filters, interceptors, Spring Security config.
- Servlet/JSP: `web.xml`, `HttpServlet`, `doGet`, `doPost`, filters.
- JAX-RS: `@Path`, `@GET`, `@POST`, resource classes.
- Struts: `struts.xml`, `ActionSupport`, interceptors.
- SOAP/CXF: service interfaces, endpoint config, generated WSDL mappings.
- CLI/cron/queue: scheduled jobs, `@Scheduled`, consumers, batch tasks.

## Sources

`HttpServletRequest` parameters, path variables, request bodies, multipart filenames/content, headers, cookies, session attributes, deserialized objects, XML bodies, message queues, uploaded archives, config values used as URLs/paths.

## High-Risk Sinks

- SQL/HQL: `Statement.execute*`, string-built `PreparedStatement`, MyBatis `${}`, `@Select` string concat, `createQuery`, Hibernate HQL fragments.
- Command: `Runtime.exec`, `ProcessBuilder`, shell wrappers.
- File: `new File`, `Paths.get`, `Files.read*`, `Files.write`, `FileInputStream`, `FileOutputStream`, `transferTo`.
- Upload: `MultipartFile.getOriginalFilename`, `transferTo`, Commons FileUpload.
- SSRF: `URL.openConnection`, `HttpClient`, Apache HttpClient, OkHttp, RestTemplate, WebClient.
- XXE: `DocumentBuilderFactory`, `SAXParserFactory`, `XMLInputFactory`, `SAXReader`, `SAXBuilder`, `TransformerFactory`, JAXB.
- Deserialization: `ObjectInputStream`, XStream, SnakeYAML unsafe load, Fastjson autoType, Jackson polymorphic typing.
- Archive: `ZipInputStream`, `ZipFile`, Commons Compress, tar entry extraction.

## Java-Specific Pitfalls

- MyBatis `#{}` is generally parameterized; `${}` is string substitution and high risk.
- `PreparedStatement` is not safe if the SQL string was already built with user input.
- `File.getCanonicalPath().startsWith(base)` needs directory-boundary validation, not raw prefix.
- XML factory hardening must disable external entities and DTDs on the exact parser used.
- Spring Security method annotations can be bypassed when service methods are called from unguarded internal routes or alternate controllers.
- Component CVEs need both vulnerable version and reachable usage.

## Useful Searches

```bash
rg -n "@(RequestMapping|GetMapping|PostMapping|PutMapping|DeleteMapping|Path)|extends HttpServlet|doGet|doPost" -g "*.java" -g "*.xml"
rg -n "execute(Query|Update)?\(|createQuery|Statement|\\$\\{|@Select|@Update|@Delete|@Insert" -g "*.java" -g "*.xml"
rg -n "Runtime\\.getRuntime\\(\\)\\.exec|ProcessBuilder|new File\\(|Paths\\.get|Files\\.|transferTo|getOriginalFilename" -g "*.java"
rg -n "DocumentBuilderFactory|SAXParserFactory|XMLInputFactory|ObjectInputStream|readObject|Yaml|XStream|autoType|ZipInputStream|ZipEntry" -g "*.java"
```
