# 登记支持与反驳

引用关系由程序生成；支持/反驳是需要审核的研究解释，不自动推断。

每条声明新建一个 JSON 文件，字段如下（占位 ID 必须换成共享阅读页中真实存在的定义版本）：

```json
{
  "id": "assertion.example.v1",
  "from_revision": "revision.证据版本",
  "relation": "supports",
  "to_revision": "revision.因子或因果假设版本",
  "status": "pending",
  "rationale": "这条证据为何支持该机制、适用边界是什么"
}
```

`relation` 可取 `supports` / `refutes`，`status` 可取 `pending` / `reviewed`。运行 `python3 90-system/03-scripts/research.py library` 验证并载入。相同 ID 不同内容会被拒绝，修订需使用新 ID；旧声明继续保留，不能靠覆盖文件改写历史。

查看证据页的来源关系判断独立性：来自同一来源快照的转述不算独立验证。状态仅表示关系解释已审核，不会将 AI 说法升级为已核验事实。
