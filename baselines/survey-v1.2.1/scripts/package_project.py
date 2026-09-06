#!/usr/bin/env python3
"""MANIFEST.sha256을 만들고 단일 루트 ZIP을 생성한다."""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "MANIFEST.sha256"
MANIFEST_EXCLUDES = {"MANIFEST.sha256", "qa/validation_results.json"}


def digest(path: Path) -> str:
  value = hashlib.sha256()
  with path.open("rb") as handle:
    for chunk in iter(lambda: handle.read(1024 * 1024), b""):
      value.update(chunk)
  return value.hexdigest()


def project_files() -> list[Path]:
  return sorted(
    path for path in ROOT.rglob("*")
    if path.is_file()
    and "__pycache__" not in path.parts
    and path.suffix.lower() != ".pyc"
    and "node_modules" not in path.parts
  )


def write_manifest() -> None:
  lines = []
  for path in project_files():
    rel = path.relative_to(ROOT).as_posix()
    if rel in MANIFEST_EXCLUDES:
      continue
    lines.append(f"{digest(path)}  {rel}")
  MANIFEST.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
  parser = argparse.ArgumentParser()
  parser.add_argument("--output-dir", type=Path, default=ROOT.parent)
  args = parser.parse_args()
  args.output_dir.mkdir(parents=True, exist_ok=True)
  write_manifest()
  zip_path = args.output_dir / f"{ROOT.name}.zip"
  with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
    for path in project_files():
      archive.write(path, (Path(ROOT.name) / path.relative_to(ROOT)).as_posix())
  with zipfile.ZipFile(zip_path) as archive:
    bad = archive.testzip()
    roots = {name.split("/", 1)[0] for name in archive.namelist() if name and not name.endswith("/")}
  if bad is not None or roots != {ROOT.name}:
    raise SystemExit(f"ZIP 검증 실패: bad={bad}, roots={sorted(roots)}")
  print(json.dumps({"zip": str(zip_path), "sha256": digest(zip_path), "testzip": "PASS"}, ensure_ascii=False))


if __name__ == "__main__":
  main()
