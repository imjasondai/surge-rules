#!/usr/bin/env python3
"""把 sources.json 里的上游规则集同步到 upstream/，并去掉 exclude/ 里列出的规则。

用法: python3 scripts/sync.py
输出: 每个规则集的条数变化；有变化的文件名写入 changed.txt（供 Actions 刷新 CDN 缓存）。
安全阈值：下载失败，或者新规则数少于旧规则数的一半时，保留旧文件不覆盖。
"""
import json
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UP = ROOT / "upstream"
EX = ROOT / "exclude"


def rules_of(text):
    out = []
    for line in text.splitlines():
        s = line.strip()
        if s and not s.startswith(("#", "//", ";")):
            out.append(s)
    return out


def norm(rule):
    # 比较时忽略大小写和行尾注释
    return rule.split("//")[0].strip().lower()


def main():
    sources = {k: v for k, v in json.loads((ROOT / "sources.json").read_text("utf-8")).items() if not k.startswith("_")}
    UP.mkdir(exist_ok=True)
    changed, failed = [], []
    for name, url in sources.items():
        dst = UP / f"{name}.list"
        old = rules_of(dst.read_text("utf-8")) if dst.exists() else []
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "surge-rules-sync"})
            new = rules_of(urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "ignore"))
        except Exception as e:  # 网络或上游出错时保留旧文件
            print(f"{name:14} 下载失败，保留旧版：{e}")
            failed.append(name)
            continue
        ex_file = EX / f"{name}.list"
        excluded = {norm(r) for r in rules_of(ex_file.read_text("utf-8"))} if ex_file.exists() else set()
        seen, kept = set(), []
        for r in new:
            k = norm(r)
            if k in excluded or k in seen:
                continue
            seen.add(k)
            kept.append(r)
        if old and len(kept) < len(old) / 2:
            print(f"{name:14} 新版只有 {len(kept)} 条（旧版 {len(old)} 条），疑似上游异常，跳过")
            failed.append(name)
            continue
        if kept == old:
            print(f"{name:14} 无变化（{len(kept)} 条）")
            continue
        head = [
            f"# {name}（上游同步，请勿手改；要排除规则请写 exclude/{name}.list）",
            f"# 来源：{url}",
            f"# 同步时间：{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
            f"# 规则数：{len(kept)}（排除 {len(excluded)} 条）",
        ]
        dst.write_text("\n".join(head + kept) + "\n", "utf-8")
        changed.append(f"upstream/{name}.list")
        print(f"{name:14} 更新：{len(old)} → {len(kept)} 条")
    (ROOT / "changed.txt").write_text("\n".join(changed) + ("\n" if changed else ""), "utf-8")
    return 1 if failed and not changed and len(failed) == len(sources) else 0


if __name__ == "__main__":
    sys.exit(main())
