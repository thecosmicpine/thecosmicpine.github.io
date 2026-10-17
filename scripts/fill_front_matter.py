#!/usr/bin/env python3
"""글 front matter 보강.

- description 이 없으면 본문 첫 문단에서 150자 안으로 만든다 (검색 결과·공유 미리보기 문구)
- image 가 없고 본문에 그림이 있으면 첫 그림을 image 로 (공유 미리보기 그림)
- 연재 파일명(grok-bot-01, dots-02 …)에 series / series_order 를 붙인다
- --check : 고치지 않고 빠진 항목만 출력 (새 글 올리기 전 점검용)

사용: python3 scripts/fill_front_matter.py [--check] [파일 ...]
파일을 안 주면 _posts/*.md 전체.
"""
import glob
import re
import sys

SERIES = [
    (re.compile(r"-grok-bot-(\d+)-"), "Grok Bot 사용기"),
    (re.compile(r"-dots-(\d+)-"), "Dots 사용기"),
]
MAX = 150


def split(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None, text
    return m.group(1), text[m.end():]


def first_paragraph(body):
    for block in re.split(r"\n\s*\n", body):
        b = block.strip()
        if not b or b.startswith(("!", "#", "|", "<", "{:", "```", ">", "- ", "* ", "1. ", "---")):
            continue
        b = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", b)
        b = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", b)
        b = re.sub(r"[*_`]", "", b)
        b = re.sub(r"\s+", " ", b).strip()
        if len(b) >= 40:
            return b
    return None


def shorten(s):
    if len(s) <= MAX:
        return s
    cut = s[:MAX]
    ends = [m.end() for m in re.finditer(r"[.?!](?=\s)", cut)]
    if ends and ends[-1] >= 60:
        return cut[: ends[-1]].strip()
    return cut.rstrip() + "…"


def yaml_str(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def process(path, check):
    text = open(path, encoding="utf-8").read()
    fm, body = split(text)
    if fm is None:
        return []
    add, missing = [], []
    if not re.search(r"^description:", fm, re.M):
        p = first_paragraph(body)
        if p:
            add.append("description: " + yaml_str(shorten(p)))
        missing.append("description")
    if not re.search(r"^image:", fm, re.M):
        m = re.search(r"!\[[^\]]*\]\((/[^)\s]+)\)", body)
        if m:
            add.append("image: " + m.group(1))
            missing.append("image")
    if not re.search(r"^series:", fm, re.M):
        for rx, name in SERIES:
            m = rx.search(path)
            if m:
                add.append("series: " + yaml_str(name))
                add.append("series_order: " + str(int(m.group(1))))
                missing.append("series")
    if check:
        return missing
    if add:
        new = "---\n" + fm.rstrip("\n") + "\n" + "\n".join(add) + "\n---\n" + body
        open(path, "w", encoding="utf-8").write(new)
    return missing


def main():
    args = sys.argv[1:]
    check = "--check" in args
    files = [a for a in args if a != "--check"] or sorted(glob.glob("_posts/*.md"))
    bad = 0
    for f in files:
        missing = process(f, check)
        if missing:
            bad += 1
            print(("빠짐 " if check else "보강 ") + f + ": " + ", ".join(missing))
    if check and bad:
        sys.exit(1)


if __name__ == "__main__":
    main()
