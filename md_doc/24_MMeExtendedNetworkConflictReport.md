# MMeExtendedNetworkConflictReport

## 协议章节

### 消息标识

- 管理消息名称：扩展网络冲突上报报文（`MMeExtendedNetworkConflictReport`）
- 管理消息类型：`0x0077`
- 来源文档：`doc/南网hplc+hrf双模模块2.0标准规范/通感一体化低压电力线宽带载波通信规约/4-通感一体化低压电力线宽带载波通信规约 第4部分 数据链路层通信协议 （初稿).pdf`
- 对应 PDF 物理页：`69`
- 对应正文页码：`67`

### 5.1.4.24 扩展网络冲突上报报文

扩展网络冲突上报报文格式的定义如表 `163` 所示。本网络运行 `ISAC-PLC` 协议时，站点通过扩展网络冲突上报报文向 `CCO` 上报邻居网络冲突情况。

#### 表 163 扩展网络冲突上报报文格式

| 字段 | 字节号 | 字段大小（比特） | 备注 |
| --- | --- | --- | --- |
| 冲突网络 CCO MAC 地址 | 0-5 | 48 | 表示与本网络发生冲突的邻居网络的 CCO MAC 地址 |
| 邻居网络个数 | 6 | 8 | 周边可见邻居网络的个数 |
| 邻居网络条目 | 可变 | 可变 | 邻居网络 snid 信息 |

#### 表 164 邻居网络条目

| 字段 | 字节号 | 字段大小（比特） | 备注 |
| --- | --- | --- | --- |
| 邻居网络（0） | 0 | 5 | 邻居网络 0 的 snid |
| 保留 | 0 | 3 | 保留 |
| 邻居网络（1） | 1 | 5 | 邻居网络 1 的 snid |
| 保留 | 1 | 3 | 保留 |
| ... | ... | ... | ... |
| 邻居网络（N） | N | 5 | 邻居网络 N 的 snid |
| 保留 | N | 3 | 保留 |

## 实现说明

- `24_MMeExtendedNetworkConflictReport.h/.c` 按“固定头 `7` 字节 + 邻居网络条目列表”的形式实现了完整编解码。
- 每个邻居网络条目使用 `MMeExtendedNetworkConflictReportItem_t` 表示，底层为 `1` 字节原始字段：
- 低 `5 bit` 为 `snid`
- 高 `3 bit` 为保留位
- 提供 `mme_extended_network_conflict_report_item_get_snid` / `mme_extended_network_conflict_report_item_set_snid` helper 读写条目中的 `snid`。
- `validate` 当前做两类校验：
- 当 `NeighborNetworkCount > 0` 时，`NeighborNetworkList` 不能为空
- 每个条目的保留位 `bit[7:5]` 必须为 `0`
- 规范页未给出 `邻居网络个数` 的上下限，本实现允许 `NeighborNetworkCount = 0`，此时报文只有固定 `7` 字节头。
- 规范页只给出 `snid` 为 `5 bit` 字段，没有声明条目去重约束；本实现不额外要求 `snid` 唯一。
- 解码成功后，`Message->NeighborNetworkList` 直接指向输入缓冲区中的条目列表，不额外拷贝。

## 校准说明

- 原 PDF 为扫描版，`pdftotext` 对第 `69` 页几乎无法直接提取表格，本文件依据页图局部裁剪和 `tesseract` OCR 结果人工校准。
- 第 `69` 页同时包含 `5.1.4.23` 和 `5.1.4.24`；其中下半页的表 `163`、表 `164` 已明确给出本报文布局。
- 页图中表 `163` 标题显示为“网络冲突上报报文”，但其所在章节标题明确是“扩展网络冲突上报报文”；本实现以章节标题作为消息名称。
- 当前 SDK `h2-link-v2-sdk/SDK/src/spg/mac/mmsg.h` 中没有现成的 `MMeExtendedNetworkConflictReport` 枚举或结构体定义，因此消息类型 `0x0077` 属于按章节顺序推定值：
- `5.1.4.17` 无线信道冲突上报报文在 SDK 中已确认是 `0x0070`
- 仓库现有 `5.1.4.18` 至 `5.1.4.23` 已分别按顺序实现为 `0x0071` 至 `0x0076`
- 因此本消息 `5.1.4.24` 顺序对应推定为 `0x0077`
- 文件名使用 `ExtendedNetworkConflictReport`，原因是规范中文名称为“扩展网络冲突上报报文”；若后续 SDK 给出官方英文名，应以官方命名为准。
