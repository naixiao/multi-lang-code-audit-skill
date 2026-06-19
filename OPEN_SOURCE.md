# 开源发布说明

## 推荐仓库名称

```text
multi-lang-code-audit-skill
```

## 推荐中文项目描述

```text
面向 PHP、Java、Python、Go、.NET/C# 的多语言代码审计 Codex Skill：以 Route -> Auth -> Trace -> Sink 为核心，支持白盒审计、源码审计、漏洞挖掘、Source/Sink 数据流追踪、鉴权分析、PoC 生成和结构化漏洞报告输出。
```

## GitHub About 推荐短描述

```text
PHP/Java/Python/Go/.NET 多语言代码审计 Codex Skill，支持白盒审计、Source/Sink 追踪、鉴权分析、漏洞挖掘、PoC 与报告生成。
```

## README 首屏推荐卖点

```text
不是简单关键词扫描，而是一套面向真实代码审计的 Agent 工作流：

- 覆盖 PHP、Java、Python、Go、.NET/C#
- Route -> Auth -> Trace -> Sink 证据链审计
- 支持 SQLi、RCE、SSRF、XSS、XXE、文件上传、任意文件读取、Zip Slip、反序列化、越权、业务逻辑漏洞
- 内置真实漏洞报告沉淀的实战模式
- 区分 confirmed / environment-dependent / pending / static-only，减少误报和漏报
- 输出可提交、可复核、可修复的漏洞报告
```

## 推荐 Topics / 标签

```text
code-audit
security-audit
white-box-audit
source-code-audit
vulnerability-research
vulnerability-discovery
php
java
python
golang
dotnet
csharp
web-security
sast
source-sink
taint-analysis
bug-bounty
cnvd
cve
codex-skill
```

## 发布前检查

- [ ] 确认 `漏洞报告/` 没有提交到仓库。
- [ ] 确认没有真实目标、Cookie、Token、账号密码、密钥。
- [ ] 确认 `multi-lang-code-audit/SKILL.md` 校验通过。
- [ ] 确认 README 描述、许可证和免责声明符合预期。
- [ ] 创建公开仓库后再 push。

## GitHub 初始化示例

```bash
git init
git add README.md LICENSE SECURITY.md CONTRIBUTING.md OPEN_SOURCE.md .gitignore multi-lang-code-audit
git commit -m "Initial open source release"
git branch -M main
git remote add origin https://github.com/<your-name>/multi-lang-code-audit-skill.git
git push -u origin main
```
