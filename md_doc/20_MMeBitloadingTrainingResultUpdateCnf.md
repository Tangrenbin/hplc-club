# MMeBitloadingTrainingResultUpdateCnf

## 协议章节

### 消息标识

- 管理消息名称：Bitloading训练结果更新确认（`MMeBitloadingTrainingResultUpdateCnf`）
- 管理消息类型：`0x0073`
- 来源文档：`doc/南网hplc+hrf双模模块2.0标准规范/通感一体化低压电力线宽带载波通信规约/4-通感一体化低压电力线宽带载波通信规约 第4部分 数据链路层通信协议 （初稿).pdf`
- 对应 PDF 物理页：`67-68`
- 对应正文页码：`65-66`
- 用户提到的“第67页”对应的是 PDF 物理页 `67`，本消息的数据表 `157` 跨到了下一页 `68`

### 5.1.4.20 Bitloading训练结果更新确认

规范原文说明：

发端站点在接收到训练结果更新请求报文后，需要向收端站点发送训练结果更新确认报文，作为回应确认，Bitloading训练结果更新确认数据格式如表 `157` 所示。

#### 表 157 Bitloading训练结果更新确认数据格式

| 字段 | 字节号 | 字段大小(比特) | 备注 |
| --- | --- | --- | --- |
| 源 TEI | 0-1 | 12 | - |
| 目的 TEI | 1-2 | 12 | - |
| 更新结果 | 3 | 1 | `0`：更新成功；`1`：更新失败 |
| 保留 | 3 | 7 | - |

## 实现说明

- `20_MMeBitloadingTrainingResultUpdateCnf.h/.c` 按固定 `4` 字节报文实现了完整编解码。
- 前 `3` 个字节使用连续 `24 bit` 打包两个 `12 bit` TEI：
- 低 `12 bit` 为 `SourceTei`
- 高 `12 bit` 为 `DestinationTei`
- 第 `4` 个字节使用 `MMeBitloadingTrainingResultUpdateCnfByte3_t` 表示：
- `bit[0]` 为 `UpdateResult`
- `bit[7:1]` 为 `Reserved`
- `validate` 当前做三类校验：
- `SourceTei` 不能超过 `0x0fff`
- `DestinationTei` 不能超过 `0x0fff`
- `UpdateResult` 只能为 `0/1`，且保留位必须全为 `0`
- `init` 默认把 `UpdateResult` 初始化为 `更新成功`

## 校准说明

- 原 PDF 为扫描版，`pdftotext` 对第 `67-68` 页几乎无法提取有效正文；本文件基于页图人工校准。
- 第 `67` 页给出 `5.1.4.20` 章节标题、说明文字和表 `157` 标题，第 `68` 页顶部给出表 `157` 的完整字段表。
- 本仓库与 SDK 中当前没有现成的 `MMeBitloadingTrainingResultUpdateCnf` 枚举或结构体定义，因此消息类型 `0x0073` 属于按章节顺序推定值：
- `5.1.4.17` 无线信道冲突上报报文在 SDK `mmsg.h` 中已确认是 `0x0070`
- 仓库现有 `5.1.4.18` 无线发现列表报文实现已按顺序推定为 `0x0071`
- 因此本次将 `5.1.4.19` / `5.1.4.20` 顺序对应推定为 `0x0072` / `0x0073`
- 若后续 SDK 或规范修订稿补充了明确枚举，应以正式定义为准回填此处类型值
