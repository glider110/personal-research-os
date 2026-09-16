# 原始资料区

`raw/` 保存已经确认需要进入正式研究链路的原始资料。它是不可覆盖的来源档案，不是临时下载目录。

先按内容主题，再按文件类型整理：

```text
raw/
└── real-estate/                 房地产主题
    ├── video/
    ├── audio/
    ├── pdf/
    ├── md/
    ├── txt/
    ├── image/
    ├── url/
    ├── excel/
    ├── csv/
    ├── word/
    ├── ppt/
    ├── json/
    └── other/
```

每个类型下使用 `<source-id>/<snapshot-id>/<原始文件名>` 保存来源和版本。新增主题时沿用这一结构，跨主题资料通过来源 ID 引用，不重复保存原件。类型说明和整理流程见 [源文件整理规则](../docs/source-organization.md)。

每个正式来源都应在数据库的 `source` 和 `source_snapshot` 中登记。文件内容改变时，新建文件或新建版本，不要直接覆盖旧来源。
