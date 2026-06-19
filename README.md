# Multi-language Code Audit Skill

一个面向 **PHP、Java、Python、Go、.NET** 项目的多语言代码审计 Codex Skill，用于辅助白盒代码审计、漏洞挖掘、安全评估和漏洞报告编写。

## 项目简介

`multi-lang-code-audit` 是一个证据链驱动的代码审计 skill，适用于 Web/API/后台系统/开源项目的源码安全审计。它以“入口识别 -> 路由与参数梳理 -> 鉴权分析 -> Source/Sink 追踪 -> 漏洞确认 -> PoC 与修复建议 -> 审计报告”为主线，帮助审计人员系统化分析 PHP、Java、Python、Go、.NET/C# 项目中的安全风险。

项目关键词：

`PHP`、`Java`、`Python`、`Go`、`.NET`、`C#`、`代码审计`、`白盒审计`、`源码审计`、`安全审计`、`漏洞挖掘`、`Web 安全`、`SQL 注入`、`文件上传`、`任意文件读取`、`SSRF`、`RCE`、`XSS`、`XXE`、`反序列化`、`权限绕过`、`越权`、`业务逻辑漏洞`、`Zip Slip`。

## 适用场景

- PHP、Java、Python、Go、.NET 项目的源码安全审计
- SRC、CNVD、CVE、Bug Bounty 漏洞挖掘辅助
- 开源 CMS、后台管理系统、API 服务、企业 Web 系统审计
- 路由、参数、鉴权、权限、文件操作、数据库操作梳理
- 生成结构化漏洞报告、PoC、修复建议和回归搜索语句

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
  scripts/
    audit_inventory.py
```

## 快速使用

将 `multi-lang-code-audit` 目录放到 Codex skills 目录中，例如：

```powershell
Copy-Item -Recurse .\multi-lang-code-audit $env:USERPROFILE\.codex\skills\
```

在 Codex 中可以这样使用：

```text
使用 $multi-lang-code-audit 审计这个源码目录，输出完整代码审计报告。
```

也可以先运行内置索引脚本，对项目做第一轮语言、路由、Source/Sink 和依赖清点：

```bash
python multi-lang-code-audit/scripts/audit_inventory.py /path/to/source --out /path/to/output
```

## 设计特点

- **多语言覆盖**：支持 PHP、Java、Python、Go、.NET/C#。
- **证据链优先**：每个漏洞都要求入口、Source、校验缺陷、Sink、触发条件、影响和 PoC。
- **不静默丢弃风险**：未闭合的数据流会进入待验证风险池，而不是直接忽略。
- **适配实战报告**：内置来自真实漏洞报告的审计模式，如动态 include、MIME 绕过、HQL 注入、Zip Slip、弱口令和未授权 action。
- **可组合现有 skill**：PHP/Java 项目可调度已有专项审计 skill，其他语言使用内置规则完成审计。
- **统一报告模板**：输出风险统计、覆盖矩阵、漏洞详情、PoC、修复建议、回归搜索命令。

## 免责声明

本项目仅用于合法授权的代码审计、安全研究、漏洞验证和防御建设。请勿在未授权目标上使用本项目进行攻击、入侵或破坏性测试。使用者应自行承担使用本项目产生的法律和安全责任。

## License

MIT License
