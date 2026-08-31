# Multi-language Code Audit Skill

用于 PHP、Java、Python、Go、.NET/C# 代码审计的 Codex Skill，主要面向 Web、API 和后台项目。

审计从入口和权限检查开始，追踪用户输入到数据库、文件、命令执行等操作，再整理漏洞证据、PoC 和修复建议。未完成验证的线索单独列出，便于继续排查。

## 安装

### 方式一：让 Codex 安装

把下面这段话发给 Codex：

```text
帮我安装这个 Codex Skill：
https://github.com/naixiao/multi-lang-code-audit-skill

安装仓库中的 multi-lang-code-audit/ 目录，并检查 SKILL.md 和引用文件是否完整。
```

### 方式二：手动安装

先克隆仓库：

```bash
git clone https://github.com/naixiao/multi-lang-code-audit-skill.git
cd multi-lang-code-audit-skill
```

将 `multi-lang-code-audit/` 复制到本地 skills 目录。默认路径下的命令如下；如果配置了自定义目录，请替换目标路径。

Windows：

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills" | Out-Null
Copy-Item -Recurse .\multi-lang-code-audit "$env:USERPROFILE\.codex\skills\"
```

Linux / macOS：

```bash
mkdir -p ~/.codex/skills
cp -r ./multi-lang-code-audit ~/.codex/skills/
```

安装后确认存在 `skills/multi-lang-code-audit/SKILL.md`。如果目标目录已有旧版，更新前请先保留自己的修改。

### 方式三：不安装，直接引用文件

在 Codex 中打开本仓库，然后发送：

```text
读取 multi-lang-code-audit/SKILL.md，按其中的流程审计 /path/to/source。
将报告保存到 /path/to/output。
```

## 使用

安装后，在新会话中指定源码路径和输出目录：

```text
使用 $multi-lang-code-audit 对源码目录进行完整代码审计，输出 Markdown 漏洞报告、证据链、PoC 和修复建议。需要提交报告时，可指定生成 CNVD（中文）或 CVE/GHSA/advisory 报告。
源码路径：/path/to/source
输出目录：/path/to/output
```

没有明确要求 CNVD/CVE 报告时，默认生成普通审计报告。提交稿中的截图、视频等缺失证据会标为人工复核项；生成提交稿不代表漏洞已被收录。

也可以限定审计范围：

```text
使用 $multi-lang-code-audit 审计当前 PHP 项目的 SQL 注入、文件上传、任意文件读取和未授权访问，输出 Markdown 报告。对证据完整的漏洞，同时生成中文 CNVD 报告。
```

```text
使用 $multi-lang-code-audit 审计当前 Java 项目的路由、鉴权、SQL 注入和 XXE，按严重程度整理报告。对证据完整的漏洞，同时生成 CVE/advisory 报告。
```

```text
使用 $multi-lang-code-audit 梳理当前 Python/FastAPI 项目的路由、参数和鉴权，检查 SSRF、命令执行和文件读取风险。
```

```text
使用 $multi-lang-code-audit 审计当前 Go 项目的归档解压逻辑，检查 Zip Slip、同前缀目录绕过及符号链接、硬链接逃逸。
```

```text
使用 $multi-lang-code-audit 审计当前 .NET 项目的鉴权、IDOR、文件上传、路径穿越和 SQL 注入风险。
```

项目较大时，可以按模块或漏洞类型分批审计。已有线索时，把路由、文件位置、运行环境和已验证的结果一起提供。

## 审计内容

各语言的入口、框架和危险 API 见 [PHP](multi-lang-code-audit/references/php.md)、[Java](multi-lang-code-audit/references/java.md)、[Python](multi-lang-code-audit/references/python.md)、[Go](multi-lang-code-audit/references/go.md)、[.NET](multi-lang-code-audit/references/dotnet.md) 参考。

主要检查范围：

- 注入：SQL/HQL/ORM、NoSQL、命令、模板、表达式和 LDAP。
- 文件操作：上传、读取、写入、删除、路径穿越和归档解压。
- Web 与解析器：SSRF、XSS、XXE、反序列化、开放重定向和 CRLF。
- 权限与业务：认证绕过、越权、CSRF、Session/JWT、默认凭据和业务状态检查。
- 配置与依赖：调试暴露、密钥、日志，以及依赖版本和使用路径。

[报告案例中的检查点](multi-lang-code-audit/references/report-corpus-patterns.md) 补充了动态 include、原始文件名上传、HQL 查询片段、同前缀路径绕过等模式。原始漏洞报告不随仓库发布。

## 报告输出

报告包含审计范围、已检查与未完成的项目、漏洞详情、待验证线索和修复优先级。每个漏洞需要说明入口、文件与行号、输入来源、校验缺陷、危险操作、触发条件及影响。

结论使用以下状态，严重程度另行评估：

| 状态 | 含义 |
|---|---|
| `CONFIRMED` | 已有完整的入口到危险操作的代码证据；是否完成动态复现需另行说明 |
| `ENV_DEPENDENT` | 代码存在危险行为，最终影响取决于部署条件 |
| `PENDING_TRACE` | 调用链、输入可控性或分支条件尚未查清 |
| `STATIC_ONLY` | 只命中搜索规则，尚未找到可达调用链 |
| `NOT_EXPLOITABLE` | 已找到阻断利用的具体证据 |

字段和示例见[报告模板](multi-lang-code-audit/references/report-template.md)。

## 索引脚本

`audit_inventory.py` 只依赖 Python 标准库，可单独运行：

```bash
python multi-lang-code-audit/scripts/audit_inventory.py /path/to/source --out /path/to/output
```

输出 `audit_inventory.json` 和 `audit_inventory.md`，记录语言分布、依赖清单以及路由、输入来源和危险操作的候选位置。

使用时注意：

- 脚本按文本模式匹配，不解析 AST，也不做跨文件数据流分析。
- 默认跳过 `vendor`、`node_modules`、`build`、`dist` 等目录和超过 2 MB 的文件；审计范围包含这些内容时需要另行检查。
- Markdown 中的路由、Source 和每类 Sink 最多展示 200 条，完整匹配结果在 JSON 中。
- 命中结果不是漏洞结论，需要继续检查调用链和防护逻辑。

## 文件说明

```text
multi-lang-code-audit/
  SKILL.md                  审计流程与输出要求
  agents/openai.yaml        Codex 元数据
  references/               语言规则、证据分级和报告模板
  scripts/audit_inventory.py 初始索引脚本
scripts/quick_validate.py    仓库内的 skill 结构校验
```

## 使用限制

结果受模型、上下文、源码完整性和运行环境影响，不能保证覆盖全部漏洞。部署配置缺失、动态路由、跨服务调用和运行时行为需要补充证据；报告应在人工复核后使用。

仅审计已获授权的项目。默认只读取源码并写入审计输出，不修改目标代码、不安装项目依赖、不提交目标仓库，也不执行破坏性 PoC。动态验证前需确认目标、账号和测试范围。公开报告时请移除凭据、个人信息和未公开的目标信息。

## 参与维护

规则补充、误报案例和脚本问题可以提交 Issue 或 PR。请附上脱敏代码、复现方式和预期结果，具体要求见[贡献指南](CONTRIBUTING.md)。

安全问题见[安全政策](SECURITY.md)，许可证为 [MIT](LICENSE)。

如果用得上，欢迎点个 Star。
