from __future__ import annotations

import html
import re
from pathlib import Path
from typing import Any

REGIONS = [
    "福建",
    "广东",
    "浙江",
    "辽宁",
    "重庆",
    "国网",
    "南网",
    "江苏",
    "山东",
    "四川",
    "湖北",
    "湖南",
    "河北",
    "河南",
    "安徽",
    "江西",
    "陕西",
    "山西",
]

GENERIC_HEADINGS = {
    "注意事项",
    "现场测试环境",
    "测试内容问题",
    "图片",
    "总结",
    "特性记录",
    "修改方案",
    "原因",
    "修改日期",
    "时间",
    "其他",
    "报文示例",
    "失败用例截图",
    "维护或投稿流程",
    "内容撰写建议",
    "推荐模板",
    "国网双模互联互通台体",
    "福建扩展协议测试",
    "协议一致性测试",
}

CN_BATCH_MAP = {
    "一": "1",
    "二": "2",
    "三": "3",
    "四": "4",
}


def _strip_frontmatter(text: str) -> tuple[dict[str, str], str]:
    meta: dict[str, str] = {}
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            raw_meta = text[4:end]
            for line in raw_meta.splitlines():
                if ":" in line and not line.startswith((" ", "-")):
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip().strip("'\"")
            return meta, text[end + 5 :]
    return meta, text


def _clean_md_inline(text: str) -> str:
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"[`*_~>#]", "", text)
    text = re.sub(r"^\s*[-*+]\s+", "", text)
    text = re.sub(r"^\s*\d+(?:\.\d+)*[.、)\]]\s*", "", text)
    text = re.sub(r"^(?:[一二三四五六七八九十]+[、.．]\s*|[（(][一二三四五六七八九十\d]+[）)]\s*)", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _extract_title(body: str, fallback: str) -> str:
    for line in body.splitlines():
        m = re.match(r"^#\s+(.+)$", line.strip())
        if m:
            return _clean_md_inline(m.group(1))
    return fallback


def _extract_region(title: str, stem: str) -> str:
    combined = f"{title} {stem}"
    if "维护" in combined or "投稿" in combined:
        return "社区"
    for r in REGIONS:
        if r in combined:
            return r
    return "通用"


def _extract_category(title: str, stem: str) -> tuple[str, str, str]:
    combined = f"{title} {stem}"
    if "维护" in combined or "投稿" in combined:
        return ("投稿指南", "cyan", "guide")
    if "台区识别" in combined or "算法" in combined:
        return ("台区算法", "violet", "bench")
    if "台体特性" in combined or ("台体" in combined and "送检" not in combined):
        return ("台体特性", "amber", "bench")
    if any(k in combined for k in ("归纳", "复盘", "总结")):
        return ("问题复盘", "blue", "review")
    return ("送检记录", "emerald", "test")


def _extract_date_and_batch(title: str, stem: str, body: str) -> tuple[str, str]:
    """Return (display_date_or_batch, sort_key_date)."""
    combined_title = f"{title} {stem}"
    is_guide = "维护" in combined_title or "投稿" in combined_title
    if is_guide:
        return ("常驻指南", "0000-00-00")

    candidates: list[str] = []

    # 1. Explicit YYYY-MM-DD in document
    candidates.extend(re.findall(r"(?<!\d)(202[4-9]-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01]))(?!\d)", body))

    # 2. Compact YYYYMMDD timestamps in log/image filenames
    for y, m, d in re.findall(r"(?<!\d)(202[4-9])(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])(?!\d)", body):
        candidates.append(f"{y}-{m}-{d}")

    if candidates:
        best = max(candidates)
        return (best, best)

    # 3. Batch pattern from title/filename: e.g. 26-1批, 26年1批, 2026 年一批, 25年2批
    batch_match = re.search(
        r"(?:20)?(\d{2})\s*(?:年|-)\s*第?\s*([1-4一二三四])\s*批",
        combined_title,
    )
    if batch_match:
        yy = batch_match.group(1)
        b_raw = batch_match.group(2)
        b_num = CN_BATCH_MAP.get(b_raw, b_raw)
        year = f"20{yy}"
        month_est = "09" if b_num == "2" else "04"
        return (f"{year} · 第 {b_num} 批", f"{year}-{month_est}-01")

    return ("技术归档", "2024-01-01")


def _extract_excerpt(body: str, title: str, is_guide: bool) -> str:
    if is_guide:
        return "克隆仓库、新增 Markdown 文档、图片归档规范及 PR / 邮件投稿完整说明。"

    lines = body.splitlines()
    in_code = False
    headings: list[str] = []
    bullets: list[str] = []

    for raw in lines:
        stripped = raw.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code or not stripped:
            continue

        # Skip H1 title and admonition markers
        if re.match(r"^#\s+", stripped) or stripped.startswith(("???", "!!!")):
            continue
        # Skip indented admonition lines
        if raw.startswith("    ") and stripped.startswith("- ["):
            continue

        h_match = re.match(r"^(#{2,5})\s+(.+)$", stripped)
        if h_match:
            h_text = _clean_md_inline(h_match.group(2))
            if (
                h_text
                and h_text != title
                and h_text not in GENERIC_HEADINGS
                and not re.match(r"^修改点[一二三四五六七八九十\d]+$", h_text)
                and len(h_text) >= 3
            ):
                headings.append(h_text)
            continue

        if stripped.startswith(("![", "[台体日志]", "[模块日志]", "---", "|", "Log File", "===")):
            continue

        cleaned = _clean_md_inline(stripped)
        if not cleaned or len(cleaned) < 6 or cleaned == title:
            continue
        if re.match(r"^20\d{2}-\d{2}-\d{2}$", cleaned):
            continue
        if cleaned.startswith(("首次编写日期", "Gitee 仓库", "GitHub 仓库")):
            continue
        bullets.append(cleaned)

    specific_headings = [
        h
        for h in headings
        if not any(g in h for g in ("送检问题归纳", "计量测试要求", "测试环境", "配合东软CCO测试", "手动测试"))
    ]
    if len(specific_headings) >= 3:
        summary = " · ".join(specific_headings[:4])
    elif bullets:
        summary = "；".join(bullets[:2])
    elif headings:
        summary = " · ".join(headings[:3])
    else:
        summary = "现场测试现象、原因分析与工程修改方案记录。"

    if len(summary) > 72:
        summary = summary[:71].rstrip("；，、 ·") + "…"
    return summary


def _count_assets(body: str) -> tuple[int, int]:
    code_blocks = body.count("```") // 2
    body_without_code = re.sub(r"```[\s\S]*?```", "", body)
    images = len(re.findall(r"!\[[^\]]*\]\([^)]+\.(?:png|jpg|jpeg|webp|gif|svg)\)", body_without_code, re.I))
    return images, code_blocks


def on_page_markdown(markdown: str, page: Any, config: Any, files: Any) -> str:
    if page.file.src_uri != "index.md":
        return markdown

    entries: list[dict[str, Any]] = []
    for f in files.documentation_pages():
        if f.src_uri == "index.md":
            continue
        src_path = Path(f.abs_src_path)
        if not src_path.exists():
            continue
        raw = src_path.read_text(encoding="utf-8")
        meta, body = _strip_frontmatter(raw)
        stem = src_path.stem
        title = meta.get("title") or _extract_title(body, stem)
        region = meta.get("region") or _extract_region(title, stem)
        cat_label, cat_tone, cat_group = _extract_category(title, stem)
        is_guide = cat_group == "guide"
        date_label, sort_date = _extract_date_and_batch(title, stem, body)
        excerpt = meta.get("summary") or _extract_excerpt(body, title, is_guide)
        img_count, code_count = _count_assets(body)

        body_clean = re.sub(r"^(?:\?\?\?|!!!).*$", "", body, flags=re.M)
        plain_body_sample = _clean_md_inline(body_clean)[:1200]
        search_blob = f"{title} {region} {cat_label} {date_label} {excerpt} {plain_body_sample}".lower()

        entries.append(
            {
                "title": title,
                "url": f.url,
                "region": region,
                "cat_label": cat_label,
                "cat_tone": cat_tone,
                "cat_group": cat_group,
                "is_guide": is_guide,
                "date_label": date_label,
                "sort_date": sort_date,
                "excerpt": excerpt,
                "img_count": img_count,
                "code_count": code_count,
                "search_blob": search_blob,
            }
        )

    tech_entries = sorted(
        [e for e in entries if not e["is_guide"]],
        key=lambda e: (e["sort_date"], e["title"]),
        reverse=True,
    )
    guide_entries = [e for e in entries if e["is_guide"]]
    ordered = tech_entries + guide_entries

    total_count = len(ordered)
    tech_count = len(tech_entries)
    regions_present = sorted(
        {e["region"] for e in tech_entries if e["region"] not in ("社区", "通用")},
        key=lambda r: (-sum(1 for e in tech_entries if e["region"] == r), r),
    )

    cat_counts = {
        "all": total_count,
        "test": sum(1 for e in ordered if e["cat_group"] == "test"),
        "bench": sum(1 for e in ordered if e["cat_group"] == "bench"),
        "review": sum(1 for e in ordered if e["cat_group"] == "review"),
        "guide": sum(1 for e in ordered if e["cat_group"] == "guide"),
    }

    region_pills_html = "".join(
        f'<button type="button" class="dir-chip" data-filter-region="{html.escape(r)}">'
        f'{html.escape(r)} <span>{sum(1 for e in tech_entries if e["region"] == r)}</span></button>'
        for r in regions_present
    )

    rows_html_parts: list[str] = []
    for idx, item in enumerate(ordered, start=1):
        is_latest = not item["is_guide"] and idx <= 2
        latest_badge = '<span class="dir-new-badge">NEW</span>' if is_latest else ""

        meta_indicators: list[str] = []
        if item["code_count"] > 0 and not item["is_guide"]:
            meta_indicators.append(f'<span class="dir-ind" title="含协议报文或代码片段">报文 ×{item["code_count"]}</span>')
        if item["img_count"] > 0 and not item["is_guide"]:
            meta_indicators.append(f'<span class="dir-ind" title="含现场截图或测试图">附图 ×{item["img_count"]}</span>')
        indicators_html = "".join(meta_indicators)

        rows_html_parts.append(
            f'<a class="dir-row{" dir-row--guide" if item["is_guide"] else ""}" '
            f'href="{html.escape(item["url"])}" '
            f'data-group="{html.escape(item["cat_group"])}" '
            f'data-region="{html.escape(item["region"])}" '
            f'data-search="{html.escape(item["search_blob"], quote=True)}">'
            f'  <span class="dir-row__idx">{idx:02d}</span>'
            f'  <div class="dir-row__main">'
            f'    <div class="dir-row__title-line">'
            f'      <span class="dir-row__title">{html.escape(item["title"])}</span>'
            f'      {latest_badge}'
            f'      {indicators_html}'
            f'    </div>'
            f'    <p class="dir-row__desc">{html.escape(item["excerpt"])}</p>'
            f'  </div>'
            f'  <div class="dir-row__meta">'
            f'    <span class="dir-region">{html.escape(item["region"])}</span>'
            f'    <span class="dir-badge dir-badge--{item["cat_tone"]}">{html.escape(item["cat_label"])}</span>'
            f'    <span class="dir-date">{html.escape(item["date_label"])}</span>'
            f'    <span class="dir-arrow" aria-hidden="true">→</span>'
            f'  </div>'
            f'</a>'
        )

    rows_html = "\n".join(rows_html_parts)
    guide_url = guide_entries[0]["url"] if guide_entries else "站点维护或投稿方法/"

    rendered = f"""<div class="dir-shell">
  <header class="dir-header">
    <div class="dir-header__left">
      <div class="dir-eyebrow">
        <span class="dir-pulse" aria-hidden="true"></span>
        <span>HPLC ENGINEERING ARCHIVE</span>
        <span class="dir-eyebrow__sep">/</span>
        <span class="dir-eyebrow__muted">电力线载波与双模技术社区</span>
      </div>
      <h1>HPLC 技术知识库</h1>
      <p class="dir-subtitle">沉淀各省网送检测试记录、台体特性、协议报文解析与现场问题复盘，打开即查。</p>
    </div>
    <div class="dir-header__right">
      <div class="dir-stats" aria-label="知识库统计">
        <div class="dir-stat">
          <span class="dir-stat__num">{tech_count}</span>
          <span class="dir-stat__label">技术归档</span>
        </div>
        <div class="dir-stat__divider"></div>
        <div class="dir-stat">
          <span class="dir-stat__num">{len(regions_present)}</span>
          <span class="dir-stat__label">覆盖省网</span>
        </div>
      </div>
      <div class="dir-header__actions">
        <a class="dir-btn dir-btn--primary" href="{html.escape(guide_url)}">
          <span>+ 投稿 / 维护指南</span>
        </a>
        <a class="dir-btn dir-btn--ghost" href="https://github.com/Tangrenbin/hplc-club" target="_blank" rel="noopener">
          <span>GitHub ↗</span>
        </a>
      </div>
    </div>
  </header>

  <section class="dir-panel" aria-label="全部文档目录">
    <div class="dir-toolbar">
      <div class="dir-tabs" role="tablist" aria-label="按类型筛选">
        <button type="button" class="dir-tab is-active" data-filter-group="all">
          全部 <span>{cat_counts["all"]}</span>
        </button>
        <button type="button" class="dir-tab" data-filter-group="test">
          送检记录 <span>{cat_counts["test"]}</span>
        </button>
        <button type="button" class="dir-tab" data-filter-group="bench">
          台体与算法 <span>{cat_counts["bench"]}</span>
        </button>
        <button type="button" class="dir-tab" data-filter-group="review">
          问题复盘 <span>{cat_counts["review"]}</span>
        </button>
        <button type="button" class="dir-tab" data-filter-group="guide">
          指南 <span>{cat_counts["guide"]}</span>
        </button>
      </div>

      <div class="dir-search-box">
        <svg class="dir-search-box__icon" viewBox="0 0 20 20" fill="none" aria-hidden="true">
          <circle cx="8.5" cy="8.5" r="5.75" stroke="currentColor" stroke-width="1.6"/>
          <path d="M13 13L17 17" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>
        </svg>
        <input
          type="search"
          id="dir-filter-input"
          class="dir-search-box__input"
          placeholder="筛选标题、省网、关键字 (698 / NTB / CCO)…"
          autocomplete="off"
          spellcheck="false"
        />
        <kbd class="dir-search-box__kbd" id="dir-filter-kbd" title="按 / 键聚焦筛选">/</kbd>
      </div>
    </div>

    <div class="dir-subbar">
      <div class="dir-regions" aria-label="按地区快速筛选">
        <span class="dir-regions__label">省网筛选:</span>
        <button type="button" class="dir-chip is-active" data-filter-region="all">全部地区</button>
        {region_pills_html}
      </div>
      <div class="dir-result-count" id="dir-result-count">共 {total_count} 篇文档</div>
    </div>

    <div class="dir-table-head" aria-hidden="true">
      <span>#</span>
      <span>文档标题 / 核心内容提要</span>
      <span class="dir-table-head__right">省网 · 分类 · 日期/批次</span>
    </div>

    <div class="dir-list" id="dir-list">
      {rows_html}
    </div>

    <div class="dir-empty" id="dir-empty" hidden>
      <p>未找到匹配当前筛选条件的文档。</p>
      <button type="button" class="dir-btn dir-btn--ghost" id="dir-reset-btn">重置筛选条件</button>
    </div>

    <footer class="dir-panel__footer">
      <span>提示：在 <code>md_doc/</code> 目录新增 <code>.md</code> 文件并推送后，首页目录与侧栏导航将自动收录。</span>
      <div class="dir-panel__links">
        <a href="https://github.com/Tangrenbin/hplc-club" target="_blank" rel="noopener">GitHub</a>
        <span>·</span>
        <a href="https://gitee.com/tangrenbin/hplc-club" target="_blank" rel="noopener">Gitee 镜像</a>
        <span>·</span>
        <a href="{html.escape(guide_url)}">投稿说明 →</a>
      </div>
    </footer>
  </section>
</div>
"""
    return rendered
