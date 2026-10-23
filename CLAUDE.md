# surge-rules

用户自维护的 Surge 规则集，公开仓库 https://github.com/imjasondai/surge-rules。
被 iCloud 里的 Surge 配置（Mac mini 透明网关 + iPhone 共用）通过 jsDelivr 引用：
`https://fastly.jsdelivr.net/gh/imjasondai/surge-rules@main/<路径>`

本仓库位于 `Home Network/repos/` 下，上层 `Home Network/CLAUDE.md` 的家庭网络约定同样适用（设备、拓扑、变更记录都在上层）。

## 目录与改动规则

- `rules/`：自维护规则集，**可以直接改**
- `upstream/`：GitHub Actions 每天从 `sources.json` 同步，**不要手改**；要去掉某条上游规则，写进 `exclude/<同名>.list`
- `scripts/sync.py`：同步脚本，本地可运行 `python3 scripts/sync.py` 验证

## 规则文件格式

- 命名：`<名称>-Custom.list` = 自己从零挑选的网址（AI-Custom、US-Custom、JP-Custom、Direct-Custom、Proxy-Custom、Porn-Custom）；按服务命名的（Netflix、Apple-AI 等）是复制后自维护的服务规则集；`upstream/` 下是上游同步的

- 每个文件开头保留 6 行头注释：名称、用途、策略组、来源、整理日期、规则数；改动后更新"整理日期"和"规则数"
- 每行一条 Surge 规则，如 `DOMAIN-SUFFIX,example.com`；按主题用 `# 小标题` 分组，必要时在小标题里写清原因
- 不写策略名（策略在配置文件的 RULE-SET 行指定）；同一文件内不重复
- 只用 Surge 支持的规则类型；IP 类规则按需加 `no-resolve`

## 文件 → 策略组

| 文件 | 策略组 | 顺序要求 |
|---|---|---|
| US-Custom.list | US | — |
| AI-Custom.list | AI Suite | **必须在 upstream/Microsoft、upstream/AI-Suite、upstream/Proxy 之前**（grok.x.com 不能被 x.com 截走） |
| JP-Custom.list | JP | 在 AsianTV 之前 |
| Porn-Custom.list | JP | 在 AsianTV 之前（AsianTV 里也有 DMM）；DMM 必须日本 IP，所以整个规则集走 JP |
| Proxy-Custom.list | Proxy | **在 AdBlock 和 Max 之后**（含原 Global TV 主站 hulu.com、bbc.co.uk、litix.io 等，与 AdBlock、Max 里的子域名重叠） |
| Direct-Custom.list | DIRECT | **在 AdBlock 之后**（否则迅雷等广告域名会被放行；sc.omtrdc.net 的有意放行见 US-Custom.list） |
| Nintendo.list | Switch | 在 upstream/Proxy、Domestic 之前 |
| Longbridge.list | Longbridge | 在 Domestic 之前 |
| F1.list | F1 TV（美国出口） | — |
| AppleTV.list、AppleNews.list | Apple TV（美国出口） | **必须在 upstream/Apple 之前** |
| Netflix / DisneyPlus / YouTube / Max / Spotify | 同名 | — |
| AsianTV.list | Asian TV | — |
| CN-Media.list | Domestic | 在 upstream/Proxy 之前 |
| Apple-AI.list | Apple AI（建议选美国） | **在 Direct-Custom 之后、upstream/AI-Suite 之前**（apple-relay、cp4、gspe1-ssl 与 AI-Suite 重叠，要归 Apple AI）；也在 AppleNews、upstream/Apple 之前 |
| AppleMusic / ApplePush | 同名 | 在 upstream/Apple 之前 |
| Discord / GoogleFCM / PayPal / Speedtest / Steam / Telegram | 同名 | — |
| upstream/Domestic、Domestic-IPs、China-ASN | Domestic | 靠后，在 GEOIP,CN 和 FINAL 之前 |

## 配置文件中的推荐顺序（AI 与 Apple 部分，2026-10-23 评估）

有重叠的网址谁排在前面就归谁。生成配置时按这个顺序：

```
AdBlock                        → AdBlock        与 Apple-AI 无重叠
rules/Direct-Custom            → DIRECT         在 Apple-AI 之前：cn.ls.apple.com 等国内 Apple 地图保持直连（Apple-AI 有 ls.apple.com 后缀）
rules/Apple-AI                 → Apple AI       在 AI-Suite、AppleNews、Apple 之前
rules/AI-Custom                → AI Suite
upstream/AI-Suite              → AI Suite       含 IP-CIDR，加 no-resolve；在 Microsoft、Proxy 之前
upstream/Microsoft             → Microsoft
…
upstream/Apple-CN              → Domestic
rules/AppleMusic / AppleNews / AppleTV / ApplePush
upstream/Apple                 → Apple Services 大后缀，放在所有 Apple 专用规则集之后
…
upstream/Proxy                 → Proxy
```

与 07 版的差别：07 把 Apple-AI 放在最前面，导致国内 Apple 地图（cn.ls.apple.com 等）走了 Apple AI 组；改为在 Direct-Custom 之后，只有这 3 个网址改为直连，其余不变。

## 工作流程

1. 改 `rules/` 下的文件 → 本地检查格式（规则类型合法、无重复）
2. 提交说明用中文写清加了/删了什么、为什么
3. `git push`：推送会触发 Actions，刷新改动文件的 jsDelivr 缓存；Surge 下次更新规则集时生效
4. 同时在上层 `Home Network/CHANGELOG.md` 记一笔
5. 新增文件或改策略组时，还要同步修改 Surge 配置（在 iCloud，Mac/iPhone 共用，改前先备份、先征得用户同意）

## 不放进本仓库的内容

- 节点信息、订阅链接、任何密码或 Token
- 家庭内网地址、DDNS 域名、自己的 Cloudflare Worker 等私人域名 → 留在 Surge 配置的本地规则里
