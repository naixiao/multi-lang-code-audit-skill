# 开源发布说明

## 推荐仓库名称

```text
multi-lang-code-audit-skill
```

## 推荐中文项目描述

```text
面向 PHP、Java、Python、Go、.NET/C# 的多语言代码审计 Codex Skill，支持白盒审计、源码审计、漏洞挖掘、Source/Sink 追踪、鉴权分析、PoC 与漏洞报告生成。
```

## 推荐 Topics / 标签

```text
code-audit
security-audit
white-box-audit
source-code-audit
vulnerability-research
php
java
python
golang
dotnet
csharp
web-security
sast
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
