# surge-rules

个人维护的 Surge 规则集（Mac / iOS 共用配置）。

## 目录

| 目录 | 内容 | 能不能手改 |
|---|---|---|
| `rules/` | 自维护规则集：`*-Custom.list` 是自己挑选的网址，其余是按服务命名的流媒体、Apple、应用规则 | ✅ 直接改 |
| `upstream/` | 每天从上游自动同步的大列表（去广告、国内、代理、Microsoft、AI、中国 IP 等） | ❌ 不要手改，会被覆盖 |
| `exclude/` | 要从某个上游列表里去掉的规则，文件名与 `upstream/` 对应 | ✅ |
| `sources.json` | 上游来源网址 | ✅ |

## 在 Surge 中引用

```
RULE-SET,https://testingcf.jsdelivr.net/gh/imjasondai/surge-rules@main/rules/US-Custom.list,US,extended-matching
```

用 jsDelivr 是因为国内能直接访问；用 `testingcf` 子域名是为了固定走 Cloudflare——推送后 GitHub Actions 刷新缓存对 Cloudflare 有效，对 `fastly.jsdelivr.net`（Fastly）的部分节点无效，后者可能要等最多 12 小时。

## 日常维护

- 加一个网站：在 `rules/` 对应文件里加一行（如 `DOMAIN-SUFFIX,example.com`），提交推送即可
- 上游某条规则不想要：写进 `exclude/<名称>.list`（例如 `exclude/AdBlock.list`），下次同步时生效
- 手动触发同步：GitHub 网页 → Actions → 同步上游规则集 → Run workflow

## 规则集一览

| 文件 | 策略组 | 说明 |
|---|---|---|
| rules/US-Custom.list | US | 需要美国出口的网站 |
| rules/AI-Custom.list | AI Suite | 补充 upstream/AI-Suite 没有的 AI 网址（Grok/xAI、Poe、Sukka 独有的几条、M365 Copilot）；排在 Microsoft、AI-Suite、Proxy 之前 |
| rules/JP-Custom.list | JP | 需要日本出口的网站 |
| rules/Porn-Custom.list | Proxy | 成人视频网站（Jable、MissAV、Pornhub）；DMM/FANZA 需要日本 IP，在 JP-Custom |
| rules/Proxy-Custom.list | Proxy | 自定义代理 + 原 Global TV 组的海外网站主站（Prime Video、BBC、Hulu、DAZN 等）；排在 AdBlock、Max 之后 |
| rules/Direct-Custom.list | DIRECT | 自定义直连、P2P 下载软件、Apple 下载 |
| rules/Nintendo.list | Switch | 任天堂 |
| rules/Longbridge.list | Longbridge | 长桥证券 |
| rules/F1.list | F1 TV | F1 TV App |
| rules/AppleTV.list / AppleNews.list | Apple TV | Apple TV App（含 F1 直播）、Apple News；排在 Apple 之前 |
| rules/Netflix.list、DisneyPlus.list、YouTube.list、Max.list、Spotify.list | 同名 | 流媒体 |
| rules/AsianTV.list | Asian TV | 亚洲流媒体 |
| rules/CN-Media.list | Domestic | 国内流媒体，显式直连 |
| rules/AppleMusic.list、ApplePush.list、Apple-AI.list | 同名 | Apple 服务 |
| rules/Discord、GoogleFCM、PayPal、Speedtest、Steam、Telegram | 同名 | 应用 |
| upstream/AdBlock | AdBlock | 去广告（dler-io） |
| upstream/AI-Suite、Microsoft、Apple、Apple-CN | 同名 | dler-io / Sukka |
| upstream/Domestic、Proxy | Domestic / Proxy | dler-io |
| upstream/Domestic-IPs、China-ASN | Domestic | 中国 IP / ASN |

上游来源：[dler-io/Rules](https://github.com/dler-io/Rules)、[SukkaW/Surge](https://github.com/SukkaW/Surge)、[VirgilClyne/GetSomeFries](https://github.com/VirgilClyne/GetSomeFries)、[ryanbuu/surge-rules](https://github.com/ryanbuu/surge-rules)。
