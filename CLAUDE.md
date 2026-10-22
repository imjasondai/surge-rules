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

- 每个文件开头保留 6 行头注释：名称、用途、策略组、来源、整理日期、规则数；改动后更新"整理日期"和"规则数"
- 每行一条 Surge 规则，如 `DOMAIN-SUFFIX,example.com`；按主题用 `# 小标题` 分组，必要时在小标题里写清原因
- 不写策略名（策略在配置文件的 RULE-SET 行指定）；同一文件内不重复
- 只用 Surge 支持的规则类型；IP 类规则按需加 `no-resolve`

## 文件 → 策略组

| 文件 | 策略组 | 顺序要求 |
|---|---|---|
| US.list | US | — |
| AI.list | AI Suite | **必须在 upstream/Microsoft、upstream/AI-Suite 之前** |
| JP.list | JP | 在 AsianTV 之前 |
| Proxy-Custom.list | Proxy | — |
| Direct-Custom.list | DIRECT | 在 AdBlock 之前（sc.omtrdc.net 等有意覆盖的情况见 US.list） |
| Nintendo.list | Switch | 在 upstream/Proxy、Domestic 之前 |
| Longbridge.list | Longbridge | 在 Domestic 之前 |
| F1.list | F1 TV（美国出口） | — |
| AppleTV.list、AppleNews.list | Apple TV（美国出口） | **必须在 upstream/Apple 之前** |
| Netflix / DisneyPlus / YouTube / Max / Spotify | 同名 | — |
| AsianTV.list | Asian TV | — |
| CN-Media.list | Domestic | 在 upstream/Proxy 之前 |
| AppleMusic / ApplePush / Apple-AI | 同名 | 在 upstream/Apple 之前 |
| Discord / GoogleFCM / PayPal / Speedtest / Steam / Telegram | 同名 | — |
| upstream/Domestic、Domestic-IPs、China-ASN | Domestic | 靠后，在 GEOIP,CN 和 FINAL 之前 |

## 工作流程

1. 改 `rules/` 下的文件 → 本地检查格式（规则类型合法、无重复）
2. 提交说明用中文写清加了/删了什么、为什么
3. `git push`：推送会触发 Actions，刷新改动文件的 jsDelivr 缓存；Surge 下次更新规则集时生效
4. 同时在上层 `Home Network/CHANGELOG.md` 记一笔
5. 新增文件或改策略组时，还要同步修改 Surge 配置（在 iCloud，Mac/iPhone 共用，改前先备份、先征得用户同意）

## 不放进本仓库的内容

- 节点信息、订阅链接、任何密码或 Token
- 家庭内网地址、DDNS 域名、自己的 Cloudflare Worker 等私人域名 → 留在 Surge 配置的本地规则里
