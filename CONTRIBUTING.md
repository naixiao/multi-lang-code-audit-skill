# 贡献指南

欢迎提交 issue、规则补充、语言适配、报告模板优化和脚本改进。

## 贡献方向

- 补充 PHP、Java、Python、Go、.NET 代码审计规则
- 增加框架识别能力
- 增加 Source/Sink 规则
- 优化漏洞报告模板
- 改进 `audit_inventory.py`
- 补充真实但已脱敏的审计模式

## 基本要求

- 不提交真实未脱敏漏洞报告。
- 不提交真实目标、Token、Cookie、密码、密钥。
- 不提交破坏性 PoC。
- 新增规则应说明适用语言、框架、Source、Sink、误报边界和修复建议。
- 修改 skill 后请运行：

```bash
python path/to/quick_validate.py path/to/multi-lang-code-audit
```

## 推荐规则格式

```markdown
### 规则名称

- 适用语言：
- 适用框架：
- Source：
- Sink：
- 危险模式：
- 安全写法：
- 常见误报：
- 推荐搜索：
```
