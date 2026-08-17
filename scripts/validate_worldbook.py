#!/usr/bin/env python3
"""Validate a worldbook JSON memory library.

无隐私依赖：只校验结构与字段类型，不读取任何真实记忆内容。

Usage:
    python validate_worldbook.py path/to/worldbook.json
"""
import json
import sys
from pathlib import Path


REQUIRED_ENTRY_FIELDS = {"uid", "title", "keys", "content"}
RESIDENCE_FIELDS = {"residence"}


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"JSON 解析失败: {exc}"]

    entries = data.get("entries", data if isinstance(data, list) else [])
    if not isinstance(entries, list):
        return ["entries 必须是列表"]

    seen_uids: set[int] = set()
    for i, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"条目 {i}: 必须是对象")
            continue
        missing = REQUIRED_ENTRY_FIELDS - entry.keys()
        if missing:
            errors.append(f"条目 {i}: 缺少字段 {sorted(missing)}")
        uid = entry.get("uid")
        if not isinstance(uid, int):
            errors.append(f"条目 {i}: uid 必须是整数")
        elif uid in seen_uids:
            errors.append(f"条目 {i}: uid {uid} 重复")
        else:
            seen_uids.add(uid)
        if not isinstance(entry.get("keys"), list):
            errors.append(f"条目 {i}: keys 必须是列表")
        if not isinstance(entry.get("content"), str) or not entry.get("content"):
            errors.append(f"条目 {i}: content 必须是非空字符串")
        for field in RESIDENCE_FIELDS:
            if field in entry and not isinstance(entry[field], bool):
                errors.append(f"条目 {i}: {field} 必须是布尔值")

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    errors = validate(Path(sys.argv[1]))
    if errors:
        for e in errors:
            print(f"[FAIL] {e}")
        return 1
    print("[OK] worldbook JSON 合法")
    return 0


if __name__ == "__main__":
    sys.exit(main())
