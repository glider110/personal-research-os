# 源文件整理规则

## 分类顺序

源文件先按内容主题整理，再按文件类型（type）整理。正式归档路径为：

```text
02-sources/<主题>/<type>/<source-id>/<snapshot-id>/<原始文件名>
```

例如 `02-sources/real-estate/pdf/source.example-report/snapshot.2026-09-16.001/report.pdf`。这只是路径示例，不代表已经导入真实资料。

- 主题回答“资料讲什么”，例如房地产 `real-estate`、宏观经济 `macro`；尽量与模型主题的 slug 一致。
- type 回答“资料是什么形式”，不能把 PDF、视频等类型放在主题之前。
- source-id 标识来源，snapshot-id 标识一次不可覆盖的来源版本。ID 使用适合目录名的稳定字符串。
- 同一来源的新内容进入新的 snapshot 目录；保留原始文件名，不覆盖历史文件。

## 类型映射

| type | 内容 |
|---|---|
| video | MP4、MOV、MKV 等视频 |
| audio | MP3、WAV、M4A 等音频 |
| pdf | PDF，包括扫描件 |
| md | Markdown |
| txt | 纯文本 |
| image | PNG、JPG、WebP、TIFF 等图片 |
| url | 网页链接记录及网页快照，如 HTML 和配套资源 |
| excel | XLSX、XLS、XLSM 等工作簿 |
| csv | CSV、TSV 等分隔表格 |
| word | DOCX、DOC 等文档 |
| ppt | PPTX、PPT 等演示文稿 |
| json | JSON 原始数据或 API 返回 |
| other | 暂无对应分类的格式 |

类型根据实际内容判断，扩展名用于辅助识别。URL 指向的 PDF、视频等下载后按实际文件类型归档；网页本身归入 `url`，不能只保留可能失效的链接。来源网址仍登记在 source 中。

## 整理流程和边界

1. 新资料进入 `01-inbox/`；识别内容主题、实际类型、来源与版本。
2. 主题暂时无法确定、文件无法识别或来源待核实时，保留在 `01-inbox/`，不猜测性归入正式档案。
3. 确认后按上述目录归档，计算内容 hash，并登记 source、source_snapshot、storage_uri 和主题。
4. 跨主题资料只保存一份原件，选择最主要的主题归档；其他主题通过来源 ID 引用，避免复制原件形成多份版本。
5. OCR、转录、内容摘要等派生产物存入 `03-library/08-packages/`，记录来源 snapshot 和页码、时间戳等定位信息，不替换原件。
6. 已正式登记的文件调整路径时，同步更新存储定位信息并核对 hash；历史运行快照保持不变，原 snapshot ID 必须仍能解析到原内容。

当前目录和规则支持这些类型的归档，不代表已实现自动分类、下载、OCR、转录或解析。现阶段由人工或 Agent 按规则整理。
