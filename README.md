# Multi-language Code Audit Skill

面向 **PHP、Java、Python、Go、.NET/C#** 的多语言代码审计 Codex Skill。它不是简单的关键词扫描清单，而是一套围绕 **路由识别、鉴权分析、Source/Sink 追踪、数据流证据、漏洞确认、PoC 生成、修复建议、审计报告** 设计的白盒代码审计工作流。

## 项目简介

`multi-lang-code-audit` 是一个证据链驱动的代码审计 skill，适用于 Web/API/后台系统/开源 CMS/企业应用/组件项目的源码安全审计。它借鉴 SAST、人工白盒审计和真实漏洞报告的思路，把“发现疑似危险点”推进到“证明漏洞是否真实可利用”。

核心目标：

- 帮助审计人员快速理解陌生项目的入口、路由、参数、鉴权和危险操作。
- 从 Source 到 Sink 追踪用户输入，减少只靠关键词扫描带来的误报。
- 对未闭合的数据流保留“待验证风险池”，避免静默漏报。
- 输出可以提交、复核、修复的漏洞报告，而不是只给一句结论。

项目关键词：

`PHP`、`Java`、`Python`、`Go`、`.NET`、`C#`、`代码审计`、`白盒审计`、`源码审计`、`安全审计`、`漏洞挖掘`、`Web 安全`、`SQL 注入`、`文件上传`、`任意文件读取`、`SSRF`、`RCE`、`XSS`、`XXE`、`反序列化`、`权限绕过`、`越权`、`业务逻辑漏洞`、`Zip Slip`。

## 核心亮点

- **覆盖主流后端语言**：PHP、Java、Python、Go、.NET/C#，适合多语言仓库和企业混合技术栈。
- **面向真实代码审计**：围绕路由、鉴权、参数、调用链、Source/Sink、PoC、修复建议组织流程。
- **证据链优先**：每个漏洞要求给出入口、数据来源、校验缺陷、危险 Sink、触发条件和影响边界。
- **降低误报**：区分 `CONFIRMED`、`ENV_DEPENDENT`、`PENDING_TRACE`、`STATIC_ONLY`、`NOT_EXPLOITABLE`。
- **不漏掉半成品风险**：无法闭合的数据流不会被删除，而是进入待验证风险池，方便后续深挖。
- **融合实战模式**：内置动态 include、MIME 绕过、HQL 注入、Zip Slip、弱口令、未授权 action、Source Map 泄露等真实报告模式。
- **可调度专项 skill**：PHP/Java 项目可联动已有 route mapper、auth audit、route tracer、SQL/file/upload/XXE 等专项审计 skill。
- **报告即交付物**：内置统一报告模板，输出风险统计、覆盖矩阵、漏洞详情、PoC、修复优先级和回归搜索命令。
- **支持提交型报告**：用户明确要求时，可生成 CNVD/CVE 风格报告，并标注截图、视频等人工复核证据位。
- **适合 SRC/CNVD/CVE/Bug Bounty**：既能做项目全量审计，也能围绕单个高危入口做深度漏洞挖掘。
- **轻量可扩展**：规则、语言参考、报告模式都在 Markdown 中，方便安全研究员持续补充自己的方法论。

## 核心特性

### 1. 多语言白盒审计

支持 PHP、Java、Python、Go、.NET/C# 的常见 Web/API/后台项目审计，覆盖原生框架、MVC 框架、REST API、后台管理系统、上传/下载模块、任务队列、CLI/定时任务等入口。

### 2. Route -> Auth -> Trace -> Sink 流程

审计流程不是“搜危险函数就结束”，而是按以下路径推进：

```text
技术栈识别
  -> 路由/入口/参数枚举
  -> 鉴权与权限边界分析
  -> Source/Sink 候选点提取
  -> 调用链和数据流追踪
  -> 漏洞可利用性判断
  -> PoC 与修复建议
  -> 最终审计报告
```

### 3. 实战漏洞模式库

内置从真实漏洞报告提炼出的高价值检查点：

- PHP 动态 `include $page . '.php'` 与 `php://filter` 源码读取
- `mime_content_type()`、`Content-Type`、原始文件名导致的上传绕过
- `getClientOriginalName()`、双后缀、GIF polyglot 上传风险
- 未授权 `action` 分发器和后台 AJAX 接口
- `X-Forwarded-For` 等 Header 进入 SQL 或业务身份逻辑
- Java `uniqueId/path/name` 字段进入 `Paths.get()` 导致任意文件写入
- HQL/JPQL/ORM 短查询片段拼接导致注入
- Zip Slip、same-prefix path bypass、symlink/hardlink 解压逃逸
- 弱口令、默认账号、未授权访问、Source Map 泄露
- 充值、排名、邀请、订单状态等业务逻辑缺陷

### 4. 可运行的初始审计索引器

内置 `audit_inventory.py`，可快速生成项目语言、依赖、路由候选、Source 候选和 Sink 候选清单，作为人工审计和 Agent 审计的起点。

### 5. 统一漏洞报告模板

报告模板关注“可复核”和“可修复”：

- 风险统计
- 覆盖矩阵
- 漏洞总览
- Source-to-Sink 数据流
- 可利用前置条件
- HTTP PoC / 本地 PoC
- 影响分析
- 修复建议
- 回归搜索命令
- 待验证风险池

### 6. CNVD / CVE 提交报告模式

默认情况下，skill 会直接生成普通代码审计报告。只有当用户明确声明“生成可提交 CNVD 报告”或“生成可提交 CVE/GHSA/advisory 报告”时，才会切换到提交型报告模式。

- CNVD 模式会参考本地 `漏洞报告/CNVD/`、`漏洞报告/cnvd_reports/` 的报告风格，生成中文提交稿，并在需要截图、录制视频的位置添加人工复核标记。
- CVE 模式会参考本地 `漏洞报告/cve_reports/` 的报告风格，生成 CVE/advisory 披露稿，并在需要截图或终端输出证明的位置添加人工复核标记。
- skill 不会伪造截图、视频、编号、厂商确认或公开公告；缺少动态证据时会明确标注为人工复核项。

## 适用场景

- PHP、Java、Python、Go、.NET 项目的源码安全审计
- SRC、CNVD、CVE、Bug Bounty 漏洞挖掘辅助
- 开源 CMS、后台管理系统、API 服务、企业 Web 系统审计
- 路由、参数、鉴权、权限、文件操作、数据库操作梳理
- 生成结构化漏洞报告、PoC、修复建议和回归搜索语句
- 安全团队沉淀自己的代码审计方法论
- 红队/蓝队/安全研究员做源码级漏洞复现和根因分析

## 支持的审计类型

- SQL/HQL/ORM 注入
- NoSQL 注入
- 命令执行 / 命令注入
- SSRF
- XSS
- 任意文件读取 / 路径穿越 / LFI
- 任意文件上传 / 危险文件上传
- 任意文件写入 / 删除
- Zip Slip / 归档解压路径穿越
- XXE
- 反序列化 / 对象注入
- 模板注入 / SSTI
- 表达式注入
- LDAP 注入
- 开放重定向
- CRLF / 响应拆分
- 认证绕过 / 鉴权绕过 / 越权 / IDOR
- CSRF
- Session / Cookie / JWT 安全问题
- 弱口令 / 默认口令
- 配置暴露 / 调试信息 / Source Map 泄露
- 加密与密钥安全问题
- 日志与监控缺陷
- 业务逻辑漏洞

## 项目结构

```text
multi-lang-code-audit/
  SKILL.md
  agents/
    openai.yaml
  references/
    php.md
    java.md
    python.md
    go.md
    dotnet.md
    vulnerability-matrix.md
    evidence-gates.md
    report-corpus-patterns.md
    existing-skill-map.md
    external-standards.md
    report-template.md
    submission-reports.md
  scripts/
    audit_inventory.py
```

## 快速使用

### 安装方式一：让 Codex 根据项目链接安装（推荐）

在 Codex 新窗口中直接发送本项目地址，并让 Codex 帮你安装：

```text
帮我安装这个 Codex Skill：
https://github.com/naixiao/multi-lang-code-audit-skill

要求：
1. 将仓库中的 multi-lang-code-audit/ 安装到本地 Codex skills 目录。
2. 安装完成后检查 SKILL.md 是否存在。
3. 运行 skill 校验脚本，确认该 skill 可被 Codex 识别。
```

安装完成后，新窗口可以直接使用：

```text
使用 $multi-lang-code-audit 对源码目录进行完整代码审计，输出漏洞报告、证据链、PoC 和修复建议。
源码路径：/path/to/source
输出目录：/path/to/output
```

### 安装方式二：克隆后复制 Skill 目录

将本仓库中的 `multi-lang-code-audit/` 整个目录复制到 Codex 可识别的 skills 目录中。

Windows 示例：

```powershell
Copy-Item -Recurse .\multi-lang-code-audit $env:USERPROFILE\.codex\skills\
```

Linux / macOS 示例：

```bash
cp -r ./multi-lang-code-audit ~/.codex/skills/
```

安装后的目录结构应类似：

```text
~/.codex/skills/
  multi-lang-code-audit/
    SKILL.md
    agents/
      openai.yaml
    references/
      php.md
      java.md
      python.md
      go.md
      dotnet.md
      vulnerability-matrix.md
      evidence-gates.md
      report-corpus-patterns.md
      existing-skill-map.md
      external-standards.md
      report-template.md
      submission-reports.md
    scripts/
      audit_inventory.py
```

### 安装方式三：直接在当前仓库中使用

如果你在 Codex 中打开的是本仓库，也可以直接引用：

```text
使用 $multi-lang-code-audit 审计 /path/to/source，输出完整代码审计报告。
```

### 使用建议

代码审计类任务越明确，效果越好。推荐使用“审计目标 + 漏洞类型 + 输出要求”的方式提问。

在 Codex 中可以这样使用：

```text
使用 $multi-lang-code-audit 审计这个源码目录，输出完整代码审计报告。
```

更推荐的强指向用法：

```text
使用 $multi-lang-code-audit 审计当前 PHP 项目是否存在 SQL 注入、文件上传、任意文件读取和未授权访问，输出 Markdown 漏洞报告。
```

```text
使用 $multi-lang-code-audit 审计当前 Java 项目的路由、鉴权、SQL 注入、文件上传、任意文件读取和 XXE 风险，按严重程度输出报告。
```

```text
使用 $multi-lang-code-audit 梳理当前 Python/FastAPI 项目的路由、参数、鉴权和 SSRF/命令执行/文件读取风险。
```

```text
使用 $multi-lang-code-audit 审计当前 Go 项目的 archive/zip 解压逻辑，重点分析 Zip Slip、same-prefix 绕过、symlink/hardlink 逃逸。
```

```text
使用 $multi-lang-code-audit 审计当前 .NET 项目的鉴权、IDOR、文件上传、路径穿越和 SQL 注入风险。
```

生成可提交 CNVD 报告：

```text
使用 $multi-lang-code-audit 审计该项目，并生成可直接提交 CNVD 的漏洞报告。
如果需要截图或录制视频证明，请在对应位置用人工复核标记指出需要补充的内容。
源码路径：/path/to/source
输出路径：/path/to/output
```

生成 CVE / advisory 报告：

```text
使用 $multi-lang-code-audit 审计该开源组件，并生成可用于 CVE/GHSA/厂商披露的英文漏洞报告。
如果需要截图或终端输出证明，请在对应位置标记人工复核项。
源码路径：/path/to/source
输出路径：/path/to/output
```

### 推荐审计提示词

适合全量项目审计：

```text
使用 $multi-lang-code-audit 对源码目录进行白盒代码审计。

要求：
1. 先识别语言、框架、依赖、入口、路由、权限模型和危险函数。
2. 按漏洞类型拆分审计：SQL 注入、命令执行、SSRF、XSS、文件读取、文件上传、文件写入、Zip Slip、XXE、反序列化、鉴权绕过、越权、CSRF、弱口令、配置泄露、业务逻辑漏洞。
3. 每个漏洞必须包含：漏洞类型、风险等级、文件路径、行号、可达路径、Source-to-Sink 数据流、触发条件、PoC、影响、修复建议、置信度。
4. 无法闭合的数据流不要删除，放入“待验证风险池”。
5. 最终输出 Markdown 审计报告，按严重程度排序。

源码路径：/path/to/source
输出路径：/path/to/output
```

适合单类型深挖：

```text
使用 $multi-lang-code-audit 只审计当前项目的文件上传漏洞。

重点关注：
- 原始文件名是否可控
- 扩展名白名单是否完整
- MIME / Content-Type 是否可绕过
- 上传目录是否 Web 可访问或可执行
- 是否存在路径穿越写入
- 是否可与 include / 静态资源目录 / 解析配置形成利用链

输出要求：
- 给出所有上传入口
- 给出 Source-to-Sink 数据流
- 给出可执行 PoC
- 给出修复建议和回归搜索命令
```

### 使用 Codex Goal 持续审计

如果项目较大，可以用 Codex 的目标模式持续运行：

```text
/goal
你是代码审计编排器。

任务：
1. 使用 $multi-lang-code-audit 完整阅读并遵守 SKILL.md。
2. 先枚举目标仓库的语言、框架、入口、路由、权限模型、数据流、危险函数、配置与依赖。
3. 将审计拆分为多个漏洞类型，每次只聚焦一种漏洞类型，避免泛化。
4. 每轮结果必须包含：漏洞类型、风险等级、文件路径、行号、可达路径、触发条件、攻击方式、影响、证据、修复建议、置信度、是否需要动态验证。
5. 主审计员需要复核结果，去重、降噪、排除误报，并把所有单项结果合并成最终审计报告。
6. 最终报告按严重程度排序，并明确列出：确认漏洞、环境依赖漏洞、疑似漏洞、未发现但已覆盖的审计项、审计盲区。

源码路径：/path/to/source
输出路径：/path/to/output
```

也可以先运行内置索引脚本，对项目做第一轮语言、路由、Source/Sink 和依赖清点：

```bash
python multi-lang-code-audit/scripts/audit_inventory.py /path/to/source --out /path/to/output
```

### 安全边界

默认建议只做只读审计：

- 不修改目标源码。
- 不删除文件。
- 不提交 git。
- 不安装项目依赖，除非用户明确授权。
- 不执行破坏性 PoC。
- 如需运行命令，仅用于读取项目信息、搜索代码、运行只读测试或静态分析。
- 对真实目标、Cookie、Token、账号密码、密钥和未公开 PoC 做脱敏处理。

## 设计特点

- **多语言覆盖**：支持 PHP、Java、Python、Go、.NET/C#。
- **证据链优先**：每个漏洞都要求入口、Source、校验缺陷、Sink、触发条件、影响和 PoC。
- **不静默丢弃风险**：未闭合的数据流会进入待验证风险池，而不是直接忽略。
- **适配实战报告**：内置来自真实漏洞报告的审计模式，如动态 include、MIME 绕过、HQL 注入、Zip Slip、弱口令和未授权 action。
- **可组合现有 skill**：PHP/Java 项目可调度已有专项审计 skill，其他语言使用内置规则完成审计。
- **统一报告模板**：输出风险统计、覆盖矩阵、漏洞详情、PoC、修复建议、回归搜索命令。

## 与普通 SAST 的区别

普通 SAST 更擅长批量发现模式，本项目更强调“审计员式证据闭环”：

| 能力 | 普通关键词扫描 | 本项目 |
|---|---|---|
| 多语言覆盖 | 取决于规则 | PHP / Java / Python / Go / .NET |
| 路由与入口 | 常被弱化 | 优先枚举 |
| 鉴权分析 | 通常不足 | 单独建模 |
| Source/Sink | 有 | 强调数据流证据 |
| 误报处理 | 依赖规则质量 | 使用证据门禁和状态分级 |
| 未闭合风险 | 容易丢失 | 进入待验证风险池 |
| 报告输出 | 告警为主 | 可提交的漏洞报告 |
| 方法扩展 | 写规则成本较高 | Markdown 化，可持续沉淀 |

## 支持项目

如果这个项目对你的 PHP、Java、Python、Go、.NET 代码审计、白盒审计或漏洞挖掘有帮助，欢迎点一个 Star，方便后续持续更新规则、样例和实战审计模式。

## 免责声明

本项目仅用于合法授权的代码审计、安全研究、漏洞验证和防御建设。请勿在未授权目标上使用本项目进行攻击、入侵或破坏性测试。使用者应自行承担使用本项目产生的法律和安全责任。

## License

MIT License
