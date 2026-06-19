#!/usr/bin/env python3
"""Create a first-pass security audit inventory for PHP/Java/Python/.NET/Go projects."""

from __future__ import annotations

import argparse
import json
import os
import re
from collections import Counter, defaultdict
from pathlib import Path


SKIP_DIRS = {
    ".git", ".hg", ".svn", "node_modules", "vendor", "target", "build", "dist",
    "__pycache__", ".venv", "venv", "bin", "obj", ".idea", ".vs", ".gradle",
}

LANG_EXT = {
    ".php": "PHP",
    ".java": "Java",
    ".py": "Python",
    ".cs": ".NET/C#",
    ".go": "Go",
}

MANIFESTS = {
    "composer.json": "PHP Composer",
    "composer.lock": "PHP Composer lock",
    "pom.xml": "Java Maven",
    "build.gradle": "Java Gradle",
    "build.gradle.kts": "Java Gradle",
    "requirements.txt": "Python pip",
    "pyproject.toml": "Python project",
    "Pipfile": "Python pipenv",
    "go.mod": "Go module",
    "packages.config": ".NET NuGet",
    "global.json": ".NET SDK",
}

ROUTE_PATTERNS = [
    ("PHP route/dispatch", re.compile(r"\b(Route::|->(get|post|put|delete|patch)\s*\(|\$_GET\[['\"]action['\"]\]|admin-ajax|add_action\s*\()", re.I)),
    ("Java route", re.compile(r"@(RequestMapping|GetMapping|PostMapping|PutMapping|DeleteMapping|Path)\b|extends\s+HttpServlet")),
    ("Python route", re.compile(r"@(app|router|bp|blueprint)\.(route|get|post|put|delete|patch)\b|urlpatterns\s*=")),
    (".NET route", re.compile(r"\[(HttpGet|HttpPost|HttpPut|HttpDelete|Route|Authorize|AllowAnonymous)\]|Map(Get|Post|Put|Delete)\s*\(")),
    ("Go route", re.compile(r"\b(http\.HandleFunc|HandleFunc|\.GET\s*\(|\.POST\s*\(|\.Put\s*\(|\.Delete\s*\(|ServeHTTP)\b")),
]

SOURCE_PATTERNS = [
    ("HTTP input", re.compile(r"\$_(GET|POST|REQUEST|COOKIE|FILES|SERVER)|php://input|HttpServletRequest|@RequestParam|@PathVariable|request\.(args|form|json|files|headers)|Request\.(Query|Form|Body|Headers|Cookies)|FormValue|URL\.Query|c\.(Query|PostForm|ShouldBind)", re.I)),
    ("Uploaded file", re.compile(r"\$_FILES|MultipartFile|IFormFile|UploadFile|multipart|FormFile|getOriginalFilename|FileName", re.I)),
    ("Header/Cookie", re.compile(r"HTTP_X_FORWARDED_FOR|Header|headers|Cookies|Cookie|Authorization", re.I)),
]

SINK_PATTERNS = [
    ("SQL", re.compile(r"\b(query|executeQuery|executeUpdate|SqlCommand|FromSqlRaw|ExecuteSqlRaw|Raw\s*\(|Where\s*\(|mysqli_query|PDO::query|DB::raw)\b|\$\{|SELECT .*\\+", re.I)),
    ("Command", re.compile(r"system\s*\(|exec\s*\(|shell_exec|Runtime\.getRuntime\(\)\.exec|ProcessBuilder|subprocess|os\.system|Process\.Start|exec\.Command|eval\s*\(|assert\s*\(", re.I)),
    ("File", re.compile(r"file_get_contents|readfile|fopen|include|require|new File|Paths\.get|Files\.|open\s*\(|send_file|FileResponse|Path\.Combine|File\.|Directory\.|os\.(Open|ReadFile|WriteFile|Create)|filepath\.", re.I)),
    ("Upload", re.compile(r"move_uploaded_file|transferTo|getOriginalFilename|IFormFile|FileName|SaveAs|FormFile|UploadFile", re.I)),
    ("SSRF", re.compile(r"curl_setopt|CURLOPT_URL|HttpClient|RestTemplate|WebClient|URL\.openConnection|requests\.|httpx\.|urllib|WebRequest|http\.(Get|Post)|Client\.Do", re.I)),
    ("XML/XXE", re.compile(r"DocumentBuilderFactory|SAXParserFactory|XMLInputFactory|SAXReader|XmlDocument|XmlReader|XDocument|lxml|simplexml_load|DOMDocument|encoding/xml", re.I)),
    ("Deserialization", re.compile(r"unserialize|ObjectInputStream|readObject|pickle|yaml\.load|BinaryFormatter|NetDataContractSerializer|GobDecoder|jsonpickle", re.I)),
    ("Archive", re.compile(r"ZipInputStream|ZipFile|ZipArchive|archive/zip|archive/tar|extractTo|extractall|untar|unzip", re.I)),
]


def iter_files(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".cache")]
        for name in filenames:
            path = Path(dirpath) / name
            if path.stat().st_size > 2_000_000:
                continue
            yield path


def rel(root: Path, path: Path) -> str:
    return str(path.relative_to(root)).replace("\\", "/")


def scan(root: Path):
    languages = Counter()
    manifests = []
    routes = []
    sources = []
    sinks = defaultdict(list)
    files_scanned = 0

    for path in iter_files(root):
        files_scanned += 1
        ext = path.suffix.lower()
        if ext in LANG_EXT:
            languages[LANG_EXT[ext]] += 1
        if path.name in MANIFESTS or ext == ".csproj":
            manifests.append({"path": rel(root, path), "type": MANIFESTS.get(path.name, ".NET project")})
        if ext not in LANG_EXT and path.name not in {"web.xml", "struts.xml"}:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for i, line in enumerate(text.splitlines(), start=1):
            if len(line) > 1000:
                continue
            for label, pattern in ROUTE_PATTERNS:
                if pattern.search(line):
                    routes.append({"kind": label, "path": rel(root, path), "line": i, "text": line.strip()[:240]})
                    break
            for label, pattern in SOURCE_PATTERNS:
                if pattern.search(line):
                    sources.append({"kind": label, "path": rel(root, path), "line": i, "text": line.strip()[:240]})
                    break
            for label, pattern in SINK_PATTERNS:
                if pattern.search(line):
                    sinks[label].append({"path": rel(root, path), "line": i, "text": line.strip()[:240]})

    return {
        "root": str(root),
        "files_scanned": files_scanned,
        "languages": languages,
        "manifests": manifests,
        "routes": routes,
        "sources": sources,
        "sinks": dict(sinks),
    }


def write_report(data: dict, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "audit_inventory.json"
    md_path = out_dir / "audit_inventory.md"
    json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Audit Inventory",
        "",
        f"- Source root: `{data['root']}`",
        f"- Files scanned: {data['files_scanned']}",
        "",
        "## Language Mix",
        "",
    ]
    for lang, count in data["languages"].most_common():
        lines.append(f"- {lang}: {count}")
    lines.extend(["", "## Dependency Manifests", ""])
    for item in data["manifests"]:
        lines.append(f"- `{item['path']}`: {item['type']}")
    lines.extend(["", "## Route Candidates", ""])
    for item in data["routes"][:200]:
        lines.append(f"- `{item['path']}:{item['line']}` {item['kind']}: `{item['text']}`")
    lines.extend(["", "## Source Candidates", ""])
    for item in data["sources"][:200]:
        lines.append(f"- `{item['path']}:{item['line']}` {item['kind']}: `{item['text']}`")
    lines.extend(["", "## Sink Candidates", ""])
    for label, items in sorted(data["sinks"].items()):
        lines.append(f"### {label} ({len(items)})")
        for item in items[:200]:
            lines.append(f"- `{item['path']}:{item['line']}` `{item['text']}`")
        lines.append("")
    md_path.write_text("\n".join(lines), encoding="utf-8")
    return json_path, md_path


def main():
    parser = argparse.ArgumentParser(description="Create a first-pass multi-language security audit inventory.")
    parser.add_argument("source_path", type=Path)
    parser.add_argument("--out", type=Path, default=None, help="Output directory, default: <source>_audit_inventory")
    args = parser.parse_args()

    root = args.source_path.resolve()
    if not root.exists():
        raise SystemExit(f"source_path does not exist: {root}")
    out_dir = args.out or root.with_name(root.name + "_audit_inventory")
    data = scan(root)
    json_path, md_path = write_report(data, out_dir)
    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
