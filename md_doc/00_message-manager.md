# 管理消息

## 管理消息类型

> 下表中的“PDF 页”表示该小节在《通感一体化低压电力线宽带载波通信规约 第4部分 数据链路层通信协议（初稿）》中的起始物理页。

| 节号 | PDF 页 | 中文名 | 英文名 | 消息类型 |
| --- | --- | --- | --- | --- |
| 5.1.4.1 | 43 | 关联请求 | `MMeAssocReq` | `0x0030` |
| 5.1.4.2 | 46 | 关联确认 | `MMeAssocCnf` | `0x0031` |
| 5.1.4.3 | 50 | 关联指示 | `MMeAssocInd` | `0x0034` |
| 5.1.4.4 | 51 | 关联汇总指示 | `MMeAssocGatherInd` | `0x003A` |
| 5.1.4.5 | 52 | 代理变更请求 | `MMeChangeProxyReq` | `0x0032` |
| 5.1.4.6 | 53 | 代理变更请求确认 | `MMeChangeProxyCnf` | `0x0037` |
| 5.1.4.7 | 54 | 代理变更请求确认（位图版） | `MMeChangeProxyBitMapCnf` | `0x003B` |
| 5.1.4.8 | 55 | 离线指示 | `MMeLeaveInd` | `0x0049` |
| 5.1.4.9 | 55 | 延迟离线指示 | `MMeDelayLeaveInd` | `0x005D` |
| 5.1.4.10 | 56 | 心跳检测 | `MMeHeartBeatCheck` | `0x0051` |
| 5.1.4.11 | 57 | 发现列表 | `MMeDiscoverNodeList` | `0x0055` |
| 5.1.4.12 | 59 | 通信成功率上报 | `MMeSuccessRateReport` | `0x005E` |
| 5.1.4.13 | 60 | 网络冲突上报 | `MMeNetworkConflictReport` | `0x005F` |
| 5.1.4.14 | 60 | 过零NTB采集指示 | `MMeZeroCrossNTBCollectInd` | `0x0062` |
| 5.1.4.15 | 61 | 过零NTB上报 | `MMeZeroCrossNTBReport` | `0x0063` |
| 5.1.4.16 | 62 | 网络诊断 | `MMeDiagnose` | `0x0064` |
| 5.1.4.17 | 62 | 无线信道冲突上报 | `MMeRFChannelConflictReport` | `0x0070` |
| 5.1.4.18 | 63 | 无线发现列表 | `MMeRFDiscoverNodeList` | `0x0055` |
| 5.1.4.19 | 66 | Bitloading训练结果更新请求 | `MMeBitloadingTrainingResultUpdateReq` | `0x0080` |
| 5.1.4.20 | 67 | Bitloading训练结果更新确认 | `MMeBitloadingTrainingResultUpdateCnf` | `0x0081` |
| 5.1.4.21 | 68 | RU_SNR信息告知 | `MMeRuSnrInfoNotify` | `0x0082` |
| 5.1.4.22 | 68 | 站点TEI列表请求 | `MMeStationTeiListReq` | `0x0083` |
| 5.1.4.23 | 69 | 站点TEI列表回复 | `MMeStationTeiListReply` | `0x0084` |
| 5.1.4.24 | 69 | 扩展网络冲突上报 | `MMeExtendedNetworkConflictReport` | `0x0085` |

## 混合组网时的版本区分建议

基于各单消息文档中的“与 1.0 版本对比”章节，`1.0/2.0` 混合组网时，管理消息可按“同名消息按版本区分编解码”和“`2.0` 新增消息按版本门控”两类处理。

### 同名消息需按版本区分解析和发送组包

| 管理消息 | 解析 | 发送组包 | 主要区分点 |
| --- | --- | --- | --- |
| `MMeAssocReq` | 需要区分 | 需要区分 | `2.0` 复用了原保留字节和保留位，新增 `扩展特性版本号`、`PLC` 能力指示、通道数及扩展频段语义 |
| `MMeAssocCnf` | 需要区分 | 需要区分 | `byte 15` 的 `载波频段` 由 `2 bit` 扩展为 `3 bit` |
| `MMeAssocInd` | 需要区分 | 需要区分 | `byte 18` 的 `载波频段` 由 `2 bit` 扩展为 `3 bit` |
| `MMeAssocGatherInd` | 需要区分 | 需要区分 | `byte 12` 的 `载波频段` 由 `2 bit` 扩展为 `3 bit` |
| `MMeLeaveInd` | 需要区分 | 需要区分 | `原因` 枚举在 `2.0` 新增 `0x5`、`0x6`，不能直接按 `1.0` 原枚举处理 |
| `MMeDiscoverNodeList` | 需要区分 | 需要区分 | `2.0` 复用了原保留位和保留字节，新增 `PLC` 能力、通道数和 `RU_SNR` 评估信息 |

### `2.0` 新增消息需做版本门控

按当前仓库资料，以下消息仅在 `2.0` 文档中出现，混合组网时应仅对 `2.0` 节点启用；对 `1.0` 节点不发送，接收侧也不应按 `1.0` 同名消息处理。

| 管理消息 | 处理建议 | 说明 |
| --- | --- | --- |
| `MMeBitloadingTrainingResultUpdateReq` | 仅 `2.0` 启用 | `2.0` 新增的 Bitloading 训练结果更新流程 |
| `MMeBitloadingTrainingResultUpdateCnf` | 仅 `2.0` 启用 | `2.0` 新增的 Bitloading 训练结果更新确认 |
| `MMeRuSnrInfoNotify` | 仅 `2.0` 启用 | `2.0` 新增的 `RU_SNR` 信息告知 |
| `MMeStationTeiListReq` | 仅 `2.0` 启用 | `2.0` 新增的站点 `TEI` 列表请求 |
| `MMeStationTeiListReply` | 仅 `2.0` 启用 | `2.0` 新增的站点 `TEI` 列表回复 |
| `MMeExtendedNetworkConflictReport` | 仅 `2.0` 启用 | `2.0` 新增的扩展网络冲突上报 |

### 其余消息的处理建议

除上表消息外，当前已补“与 1.0 版本对比”章节的其他管理消息结论基本都是“报文线缆格式未变，只是规范迁移或表号调整”，混合组网时可优先共用一套解析和组包逻辑。

需要注意的是，`MMeAssocReq` 和 `MMeAssocCnf` 中虽然包含“管理消息版本”字段，但当前 `2.0` 文档中该字段仍固定为 `1`，因此不能把它作为 `1.0/2.0` 混合组网的可靠分流依据。
