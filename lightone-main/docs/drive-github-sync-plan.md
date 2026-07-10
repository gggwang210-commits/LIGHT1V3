# LIGHT ONE Drive-GitHub Sync Plan

Updated: 2026-06-24

## Purpose

This document defines how the LIGHT ONE GitHub repository and the Google Drive `lightone` folder should be used together.

GitHub is the source of truth for code, technical documentation, issue tracking, and version history.
Google Drive is the shared storage space for presentation files, interview materials, exported reports, screenshots, PDFs, and non-code working documents.

## Current Repository

Repository: `gggwang210-commits/lightone`

Current priority:

1. Reorganize the repository README so it represents the whole LIGHT ONE healthcare AI platform.
2. Keep camera calibration, lighting normalization, and center QC as technical modules.
3. Mark all synthetic demo outputs clearly as synthetic demo results.
4. Keep medical, regulatory, and performance claims conservative until verified with real center data.

## Google Drive Folder

Folder name: `lightone`

Recommended folder structure:

```text
lightone/
  01_GitHub_Sync/
  02_Proposal_and_Interview/
  03_Technical_Docs/
  04_Demo_Results/
  05_Design_and_Screenshots/
  99_Archive/
```

## File Responsibility

### GitHub

Use GitHub for:

- Python source code
- README and module documentation
- safety policy
- roadmap
- issue tracking
- reproducible demo pipeline
- test files
- requirements.txt

### Google Drive

Use Google Drive for:

- proposal PDFs
- interview decks
- exported GitHub snapshots
- screenshots
- meeting notes
- non-code drafts
- compressed backup files

## Immediate Sync Checklist

- [ ] Create or verify Google Drive folder: `lightone`
- [ ] Create Drive subfolders listed above
- [ ] Upload/export the current GitHub README to Drive
- [ ] Upload the correction plan document to Drive
- [ ] Upload demo result JSON or exported report to Drive
- [ ] Keep source code in GitHub, not only in Drive
- [ ] Avoid uploading `.env`, API keys, tokens, secrets, or personal image data

## Sharing Rule

Before sharing externally, check:

- no credentials
- no `.env` or `.project-config.json`
- no personal identifiable images
- no unverified medical or regulatory claims
- synthetic demo results are labeled as synthetic

## Next GitHub Issue

Recommended issue title:

`README 및 저장소 구조 정리: LIGHT ONE 통합 플랫폼 방향 명확화`

Recommended scope:

- rewrite the root README as a platform overview
- move camera calibration details into module documentation
- clarify implemented versus planned features
- clarify synthetic demo versus real center validation
- add Drive-GitHub sync policy link
