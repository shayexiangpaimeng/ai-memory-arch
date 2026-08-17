# AI Memory Architecture — 本地大模型的防失忆方案

> 给长上下文 AI（本地部署、无云端）设计的一套「记忆分层 + 条目化 + 压缩检查点恢复」工程方案。

本地跑大模型的人都会撞上同一堵墙：上下文一长，模型必忘。云端有隐式缓存，本地没有。这套方案不靠运气，靠工程结构。

## 为什么值得看

- 不依赖云端 API，纯本地文件 + 检索
- 不是「我调通了某模型」的装车帖，是可抄走的机制
- 每一层都有踩坑记录（见 docs/）

## 目录结构

```
ai-memory-arch/
├── docs/
│   ├── memory-layering.md      # 记忆五层分区与写档五问
│   ├── checkpoint-recovery.md  # 压缩检查点检测与强制重读协议
│   └── worldbook-schema.md     # 世界书条目化：为什么用 JSON 条目而非长文
├── templates/
│   ├── MEMORY_template.md      # 长期记忆文件空模板（可直接用）
│   └── worldbook_schema.json   # 世界书条目 JSON schema（空示例）
└── scripts/
    └── validate_worldbook.py   # 世界书 JSON 合法性校验（无隐私依赖）
```

## 核心机制一句话

上下文会缩，记忆不该缩——把「必须记住的」从对话里搬进文件，把「怎么找回」变成协议。

## 许可证

MIT — 随便抄，注明出处即可。
