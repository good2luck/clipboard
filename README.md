对应前端项目地址：https://github.com/good2luck/clipboard-app

项目部署细节，见博客文章：https://xudj.top/archives/clipboard

## Issue Handling Process

为了确保问题在 24 小时内得到反馈和修复，本项目遵循以下流程：

### 1. 发现（Detect）
* **自动化**：CI 中集成 `ruff`、`pytest` 与依赖漏洞扫描；若发现失败立即标红。
* **人工**：使用 Issue 模板提交，包括复现步骤、日志、期望结果和实际结果。

### 2. 评估与分级（Triage）
| 级别 | 示例 | SLA | 对应操作 |
| ---- | ---- | --- | -------- |
| P0   | 服务宕机、数据泄漏、安全漏洞 | 24 h | Hot-fix 分支、加急发布 |
| P1   | 主要功能缺陷，但有临时替代方案 | 3 d | 下一个迭代修复 |
| P2   | 体验优化、文档问题 | 7 d | Backlog 排期 |

### 3. 修复（Fix）
1. **定位根因**：2 h 内给出 Root Cause 分析（RCA）。
2. **制定方案**：4 h 内评估修复路径与风险。
3. **开发 & 测试**：12 h 内完成编码、单元/集成测试，灰度验证。
4. **发布**：22 h 内上线并验证监控；如需回滚准备回滚脚本。
5. **结案**：24 h 内更新 Changelog、关闭 Issue，并撰写 Post-mortem（若适用）。

### 4. 沟通（Communicate）
* 所有修复通过 PR 关联 Issue：`Fixes #<issue_id>`。
* PR 必须通过 CI 流水线（lint + test）方可合并。

以上流程保证了问题的可追溯性与快速响应能力。