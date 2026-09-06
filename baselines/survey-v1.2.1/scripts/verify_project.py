#!/usr/bin/env python3
"""LIGHT ONE v1.2.1 정적·계약·ZIP 검증기."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from collections import Counter
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = ROOT / "qa" / "validation_results.json"
TEXT_SUFFIXES = {".html", ".md", ".json", ".py", ".example", ".gitignore", ".editorconfig", ".code-workspace"}


class InspectHTML(HTMLParser):
  def __init__(self) -> None:
    super().__init__(convert_charrefs=True)
    self.ids: list[str] = []
    self.form_name = ""
    self.forms: list[dict[str, str]] = []
    self.controls: list[dict[str, str]] = []
    self.questions: list[dict[str, str]] = []

  def handle_starttag(self, tag: str, attrs_list: list[tuple[str, str | None]]) -> None:
    attrs = {key: value or "" for key, value in attrs_list}
    if attrs.get("id"):
      self.ids.append(attrs["id"])
    if tag == "form":
      self.form_name = attrs.get("name", "")
      self.forms.append({
        "name": self.form_name,
        "method": attrs.get("method", ""),
        "action": attrs.get("action", ""),
      })
    if self.form_name and tag in {"input", "textarea", "select"} and attrs.get("name"):
      self.controls.append({
        "form": self.form_name,
        "tag": tag,
        "type": attrs.get("type", ""),
        "name": attrs["name"],
        "value": attrs.get("value", ""),
      })
    if attrs.get("data-cond") or attrs.get("data-max"):
      self.questions.append({
        "id": attrs.get("id", ""),
        "data_cond": attrs.get("data-cond", ""),
        "data_max": attrs.get("data-max", ""),
      })

  def handle_endtag(self, tag: str) -> None:
    if tag == "form":
      self.form_name = ""


def inspect_html(path: Path) -> tuple[InspectHTML, str]:
  text = path.read_text(encoding="utf-8")
  parser = InspectHTML()
  parser.feed(text)
  return parser, text


def contract(path: Path) -> dict[str, object]:
  parser, _ = inspect_html(path)
  return {
    "forms": sorted(parser.forms, key=lambda x: x["name"]),
    "controls": sorted(parser.controls, key=lambda x: (x["form"], x["name"], x["value"], x["type"])),
    "questions": sorted(parser.questions, key=lambda x: (x["id"], x["data_cond"], x["data_max"])),
  }


def sha256(path: Path) -> str:
  digest = hashlib.sha256()
  with path.open("rb") as handle:
    for chunk in iter(lambda: handle.read(1024 * 1024), b""):
      digest.update(chunk)
  return digest.hexdigest()


def main() -> int:
  ap = argparse.ArgumentParser()
  ap.add_argument("--zip", dest="zip_path", type=Path, help="최종 ZIP 경로")
  args = ap.parse_args()
  results: list[dict[str, object]] = []

  def add(check: str, status: str, detail: str) -> None:
    results.append({"check": check, "status": status, "detail": detail})

  required = [
    ".vscode/extensions.json", ".vscode/settings.json", ".vscode/tasks.json",
    "docs/BUILD_PROMPT.md", "docs/DEPLOY_CHECKLIST.md", "docs/FILE_TREE.md", "docs/SECURITY_CHECKLIST.md",
    "netlify/functions/README_REQUIRED.md", "qa/data_contract_snapshot.json", "qa/browser_regression.json",
    "screenshots/index-role-picker.png", "screenshots/admin-summary.png", "scripts/verify_project.py",
    ".editorconfig", ".env.example", ".gitignore", "admin.html", "index.html", "LIGHTONE.code-workspace",
    "BUILD_INFO.json", "MANIFEST.sha256", "QA_REPORT.md", "README.md",
  ]
  missing = [name for name in required if not (ROOT / name).is_file()]
  add("필수 파일", "PASS" if not missing else "FAIL", "모두 존재" if not missing else "누락: " + ", ".join(missing))

  bad_utf8: list[str] = []
  for path in ROOT.rglob("*"):
    if path.is_file() and (path.suffix.lower() in TEXT_SUFFIXES or path.name in {".gitignore", ".editorconfig"}):
      try:
        path.read_text(encoding="utf-8")
      except UnicodeDecodeError:
        bad_utf8.append(path.relative_to(ROOT).as_posix())
  add("UTF-8", "PASS" if not bad_utf8 else "FAIL", "모든 텍스트 파일 읽기 성공" if not bad_utf8 else ", ".join(bad_utf8))

  html_data: dict[str, tuple[InspectHTML, str]] = {}
  for name in ("index.html", "admin.html"):
    try:
      html_data[name] = inspect_html(ROOT / name)
      duplicates = sorted(key for key, count in Counter(html_data[name][0].ids).items() if count > 1)
      add(f"중복 id: {name}", "PASS" if not duplicates else "FAIL", "없음" if not duplicates else ", ".join(duplicates))
    except Exception as exc:
      add(f"HTML 읽기: {name}", "FAIL", str(exc))

  for name, (_, text) in html_data.items():
    add(f"meta charset: {name}", "PASS" if re.search(r"<meta\s+charset=", text, re.I) else "FAIL", "존재" if re.search(r"<meta\s+charset=", text, re.I) else "없음")
    add(f"viewport: {name}", "PASS" if re.search(r"<meta\s+name=[\"']viewport[\"']", text, re.I) else "FAIL", "존재" if re.search(r"<meta\s+name=[\"']viewport[\"']", text, re.I) else "없음")

  index_text = html_data.get("index.html", (None, ""))[1]
  admin_text = html_data.get("admin.html", (None, ""))[1]
  literal_checks = [
    ("index noscript", "<noscript" in index_text.lower(), "JavaScript 비활성 안내"),
    ("FormSubmit fallback 금지", not re.search(r"formsubmit\.(?:co|io)|api\.formsubmit", index_text, re.I), "외부 FormSubmit 주소 없음"),
    ("설문 endpoint", "/.netlify/functions/submit-survey" in index_text, "유지"),
    ("설문 버전", bool(re.search(r"SURVEY_VERSION:\s*['\"]1\.2\.1['\"]", index_text)), "1.2.1"),
    ("역할 코드", all(re.search(r'data-track=["\']' + role + r'["\']', index_text) for role in ("owner", "trainer", "member")), "owner/trainer/member"),
    ("admin-summary endpoint", "/.netlify/functions/admin-summary" in admin_text, "유지"),
    ("send-report endpoint", "/.netlify/functions/send-report" in admin_text, "유지"),
    ("관리자 인증 헤더", "X-Admin-Password" in admin_text, "유지"),
    ("집계 기간", all(f'value="{value}"' in admin_text for value in ("7d", "30d", "90d", "all")), "7d/30d/90d/all"),
    ("인쇄/PDF", "window.print()" in admin_text, "유지"),
  ]
  for label, ok, detail in literal_checks:
    add(label, "PASS" if ok else "FAIL", detail)

  snapshot_path = ROOT / "qa" / "data_contract_snapshot.json"
  if snapshot_path.is_file():
    try:
      snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
      current = contract(ROOT / "index.html")
      ok = snapshot.get("contract") == current
      add("설문 데이터 계약", "PASS" if ok else "FAIL", "원본 name/value·폼 action·조건 필드 일치" if ok else "원본 스냅샷과 다름")
    except Exception as exc:
      add("설문 데이터 계약", "FAIL", str(exc))
  else:
    add("설문 데이터 계약", "FAIL", "스냅샷 없음")

  secret_findings: list[str] = []
  secret_patterns = [
    re.compile(r"\bsk-[A-Za-z0-9_-]{16,}"),
    re.compile(r"\bpat[A-Za-z0-9_-]{20,}"),
    re.compile(r"\bBearer\s+[A-Za-z0-9._~-]{16,}", re.I),
  ]
  email_pattern = re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.I)
  scan_roots = [ROOT / "index.html", ROOT / "admin.html", ROOT / "README.md", ROOT / "docs", ROOT / "netlify"]
  scan_files: list[Path] = []
  for item in scan_roots:
    scan_files.extend(path for path in item.rglob("*") if path.is_file()) if item.is_dir() else scan_files.append(item)
  for path in scan_files:
    text = path.read_text(encoding="utf-8")
    if any(pattern.search(text) for pattern in secret_patterns):
      secret_findings.append(path.relative_to(ROOT).as_posix() + ": 키/토큰 패턴")
    for email in email_pattern.findall(text):
      if email.lower().endswith("@example.com") or email.lower().endswith("@lightone.example"):
        continue
      secret_findings.append(path.relative_to(ROOT).as_posix() + ": 실제 이메일 패턴")
      break
  add("비밀값 패턴", "PASS" if not secret_findings else "FAIL", "하드코딩 없음" if not secret_findings else "; ".join(sorted(set(secret_findings))))

  node = shutil.which("node")
  if node:
    failures: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
      for html_name, (_, text) in html_data.items():
        blocks = re.findall(r"<script\b[^>]*>(.*?)</script>", text, re.I | re.S)
        for idx, block in enumerate(blocks, 1):
          script_path = Path(tmp) / f"{html_name}-{idx}.js"
          script_path.write_text(block, encoding="utf-8")
          run = subprocess.run([node, "--check", str(script_path)], capture_output=True, text=True)
          if run.returncode:
            failures.append(f"{html_name} script {idx}: {run.stderr.strip()}")
    add("inline JavaScript 구문", "PASS" if not failures else "FAIL", f"node --check ({Path(node).name})" if not failures else " | ".join(failures))
  else:
    add("inline JavaScript 구문", "SKIP", "Node.js 없음")

  manifest_path = ROOT / "MANIFEST.sha256"
  if manifest_path.is_file():
    manifest_errors: list[str] = []
    for line in manifest_path.read_text(encoding="utf-8").splitlines():
      if not line.strip():
        continue
      try:
        expected, rel = line.split("  ", 1)
        path = ROOT / Path(rel)
        if not path.is_file() or sha256(path) != expected.lower():
          manifest_errors.append(rel)
      except ValueError:
        manifest_errors.append("형식 오류: " + line)
    add("MANIFEST", "PASS" if not manifest_errors else "FAIL", "기록 파일 해시 일치" if not manifest_errors else ", ".join(manifest_errors))
  else:
    add("MANIFEST", "FAIL", "MANIFEST.sha256 없음")

  if args.zip_path:
    try:
      with zipfile.ZipFile(args.zip_path) as archive:
        bad = archive.testzip()
        names = [name for name in archive.namelist() if name and not name.endswith("/")]
        unsafe = [name for name in names if name.startswith(("/", "\\")) or ".." in Path(name).parts or "\\" in name]
        roots = {name.split("/", 1)[0] for name in names}
        expected_root = ROOT.name
        ok = bad is None and not unsafe and roots == {expected_root}
        detail = "testzip 통과, 단일 프로젝트 루트" if ok else f"bad={bad}, unsafe={unsafe}, roots={sorted(roots)}"
        add("ZIP 무결성", "PASS" if ok else "FAIL", detail)
    except Exception as exc:
      add("ZIP 무결성", "FAIL", str(exc))

  failed = [item for item in results if item["status"] == "FAIL"]
  payload = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "project": ROOT.name,
    "overall": "PASS" if not failed else "FAIL",
    "summary": {
      "pass": sum(item["status"] == "PASS" for item in results),
      "skip": sum(item["status"] == "SKIP" for item in results),
      "fail": len(failed),
    },
    "results": results,
  }
  RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
  RESULT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
  for item in results:
    print(f"[{item['status']}] {item['check']}: {item['detail']}")
  print(f"OVERALL={payload['overall']} PASS={payload['summary']['pass']} SKIP={payload['summary']['skip']} FAIL={payload['summary']['fail']}")
  return 1 if failed else 0


if __name__ == "__main__":
  sys.exit(main())
