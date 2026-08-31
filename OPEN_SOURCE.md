# 维护与发布

仓库地址：https://github.com/naixiao/multi-lang-code-audit-skill

## 提交前检查

- 只暂存本次修改的文件，检查 `git diff --cached`。
- 不提交原始漏洞报告、测试输出、凭据或客户信息。截图也需要脱敏。
- 修改规则时保留适用条件和误报说明；修改脚本时附上复现用例。
- 检查 README 中的命令、引用路径和报告说明是否与实现一致。

在仓库根目录运行结构校验：

```bash
python scripts/quick_validate.py multi-lang-code-audit
```

该脚本检查 skill 名称、frontmatter 和必要文件，不验证审计准确率。索引脚本有改动时，还需要用已知内容的小型测试项目检查 JSON 和 Markdown 输出。

## 推送

提交前同步远端，避免覆盖其他贡献者的更新。推送后确认 GitHub 上的分支、文档链接和代码块显示正常。

README 说明实际能力和限制，不放未经测试的准确率、覆盖率或工具对比。新增语言或漏洞类型时，同步补充参考文件和可复现的例子。
