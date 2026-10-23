# surge-rules

用户自维护的 Surge 规则集，公开仓库 https://github.com/imjasondai/surge-rules。
被 iCloud 里的 Surge 配置（Mac mini 透明网关 + iPhone 共用）通过 jsDelivr 引用：
`https://testingcf.jsdelivr.net/gh/imjasondai/surge-rules@main/<路径>`
（2026-10-23 实测：推送后 Actions 会请求 jsDelivr 清缓存，但 Cloudflare、Fastly 各节点都可能继续给旧版本，**最多 12 小时**（s-maxage=43200）后才全部更新；换哪个 jsDelivr 子域名都一样。核对改动以 GitHub 原始文件为准，不要以 CDN 为准）

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
| US-Custom.list | US | **在 AdBlock 之前**（sc.omtrdc.net 在 AdBlock 里，这里有意放行供阿拉斯加航空登录） |
| AI-Custom.list | AI Suite | **必须在 upstream/Microsoft、upstream/AI-Suite、upstream/Proxy 之前**（grok.x.com 不能被 x.com 截走） |
| JP-Custom.list | JP | **在 AdBlock 之前**（yahoo.co.jp 包含 AdBlock 里的 Yahoo Japan 广告子域名，07 起就是放行走 JP）；在 AsianTV 之前（DMM 也在 AsianTV 里） |
| Porn-Custom.list | JP | — （与其他规则集无重叠，位置不限） |
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
| GoogleFCM / Telegram | 同名 | — |
| Discord / PayPal / Speedtest / Steam | **Proxy**（2026-10-23 起不再单独分组） | — |
| upstream/Domestic、China-ASN | Domestic | 靠后，在 GEOIP,CN 和 FINAL 之前 |

## 配置文件中的完整推荐顺序（2026-10-23）

有重叠的网址谁排在前面就归谁。生成配置时按这个顺序（地址前缀 `https://testingcf.jsdelivr.net/gh/imjasondai/surge-rules@main/`）：

```
# 本地规则（不进公开仓库）
SRC-IP,192.168.0.109           → Switch         Switch 主机
WOL 个人 Worker 域名           → DIRECT
# 必须在 AdBlock 之前（有意放行的广告/统计域名）
rules/US-Custom                → US             sc.omtrdc.net
rules/JP-Custom                → JP             Yahoo Japan 广告子域名；含 DMM/FANZA（须在 AsianTV 之前，已满足）
# 去广告
upstream/AdBlock               → AdBlock
rules/Direct-Custom            → DIRECT         在 AdBlock 之后（迅雷广告要先被拦）；在 Apple-AI 之前（国内 Apple 地图直连）
rules/Apple-AI                 → Apple AI       在 AI-Suite、AppleNews、Apple 之前
rules/Longbridge               → Longbridge     在 Domestic 之前
rules/Nintendo                 → Switch         在 Proxy、Domestic 之前
# 流媒体
rules/Netflix                  → Netflix
rules/DisneyPlus               → Disney Plus
rules/YouTube                  → YouTube
rules/Max                      → Max
rules/Spotify                  → Spotify
rules/AsianTV                  → Asian TV
rules/F1                       → F1 TV
rules/Proxy-Custom             → Proxy          在 AdBlock、Max 之后
rules/Porn-Custom              → JP             位置不限
rules/CN-Media                 → Domestic       在 Proxy 之前
# Apple 专用（都在 upstream/Apple 之前）
upstream/Apple-CN              → Domestic
rules/AppleMusic               → Apple Music
rules/AppleNews                → Apple TV
rules/AppleTV                  → Apple TV
# 应用
rules/Discord                  → Proxy
rules/GoogleFCM                → Google FCM
rules/AI-Custom                → AI Suite       在 Microsoft、AI-Suite、Proxy 之前
upstream/AI-Suite              → AI Suite
upstream/Microsoft             → Microsoft
rules/PayPal                   → Proxy
rules/Speedtest                → Proxy
rules/Steam                    → Proxy
rules/ApplePush                → Apple Push
upstream/Apple                 → Apple Services 大后缀，放在所有 Apple 专用规则集之后
rules/Telegram                 → Telegram
# 兜底
upstream/Domestic              → Domestic
upstream/Proxy                 → Proxy
upstream/China-ASN             → Domestic
RULE-SET,LAN                   → DIRECT
GEOIP,CN                       → Domestic
FINAL                          → Direct,dns-failed
```

07 的 RULE-SET 行都没有加 `no-resolve`（域名类规则集加 `extended-matching`），08 沿用，不要顺手改。

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
