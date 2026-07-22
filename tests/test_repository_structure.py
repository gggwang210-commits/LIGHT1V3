from pathlib import Path
import subprocess


REPO_ROOT = Path(__file__).resolve().parents[1]


def tracked_repository_paths():
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
    )
    return {
        Path(raw.decode("utf-8"))
        for raw in result.stdout.split(b"\0")
        if raw
    }


def test_required_repository_documents_exist():
    required_paths = [
        REPO_ROOT / "README.md",
        REPO_ROOT / "CHANGELOG.md",
        REPO_ROOT / "CONTRIBUTING.md",
        REPO_ROOT / "SECURITY.md",
        REPO_ROOT / "requirements-dev.txt",
        REPO_ROOT / "docs",
        REPO_ROOT / "docs" / "architecture.md",
        REPO_ROOT / "docs" / "business_direction.md",
        REPO_ROOT / "docs" / "LIGHT_ONE_final_business_plan_v1_2026-07-07.md",
        REPO_ROOT / "docs" / "safety_and_privacy_policy.md",
        REPO_ROOT / "docs" / "judge_risk_review.md",
        REPO_ROOT / "docs" / "trainer_dashboard_validation.md",
        REPO_ROOT / "docs" / "pilot_interview_checklist.md",
        REPO_ROOT / "docs" / "release-checklist.md",
        REPO_ROOT / ".github" / "pull_request_template.md",
        REPO_ROOT / ".github" / "workflows" / "python-app.yml",
    ]

    missing = [str(path.relative_to(REPO_ROOT)) for path in required_paths if not path.exists()]

    assert not missing, "Missing required repository paths: " + ", ".join(missing)
    assert (REPO_ROOT / "docs").is_dir(), "docs must be a directory"


def test_public_repository_does_not_include_sensitive_data_directories():
    """Guard against committing real member PII, media, or sensitive health data."""

    forbidden_directory_names = {
        "actual_member_data",
        "customer_pii",
        "health_records",
        "member_health_data",
        "member_pii",
        "personal_health_information",
        "phi",
        "private_member_data",
        "real_member_data",
        "real_member_photos",
        "real_member_videos",
        "sensitive_health_data",
        "user_uploads",
    }
    forbidden_path_fragments = {
        "member/photos",
        "member/videos",
        "members/photos",
        "members/videos",
        "private/photos",
        "private/videos",
        "real/photos",
        "real/videos",
        "uploads/photos",
        "uploads/videos",
    }

    discovered_directories = [
        path
        for path in REPO_ROOT.rglob("*")
        if path.is_dir() and ".git" not in path.parts
    ]

    bad_names = [
        str(path.relative_to(REPO_ROOT))
        for path in discovered_directories
        if path.name.lower() in forbidden_directory_names
    ]
    bad_fragments = [
        str(path.relative_to(REPO_ROOT))
        for path in discovered_directories
        if any(fragment in path.relative_to(REPO_ROOT).as_posix().lower() for fragment in forbidden_path_fragments)
    ]

    assert not bad_names, "Forbidden sensitive-data directory names found: " + ", ".join(bad_names)
    assert not bad_fragments, "Forbidden sensitive-data directory paths found: " + ", ".join(bad_fragments)


def test_canonical_app_has_no_public_demo_secrets_or_tracked_database():
    canonical_root = REPO_ROOT / "lightone_v2_django"
    inspected_paths = [
        canonical_root / "mysite" / "settings.py",
        canonical_root / "lightone" / "management" / "commands" / "seed_lightone.py",
        canonical_root / "setup_dummy.py",
        canonical_root / "README.md",
        canonical_root / "RUN_WINDOWS.md",
    ]
    forbidden = {
        "lightone-local-" + "dev-key",
        "admin/" + "admin",
        "member1/" + "1234",
        "member2/" + "1234",
    }

    for path in inspected_paths:
        content = path.read_text(encoding="utf-8")
        hits = sorted(value for value in forbidden if value in content)
        assert not hits, f"Public demo secret in {path.relative_to(REPO_ROOT)}: {hits}"

    assert not (REPO_ROOT / "lightone_django" / "db.sqlite3").exists()


def test_tracked_files_exclude_generated_data_and_secrets():
    tracked = tracked_repository_paths()
    forbidden_suffixes = {".sqlite3", ".db", ".pem", ".key", ".zip"}
    unsafe = sorted(
        path.as_posix()
        for path in tracked
        if path.suffix.lower() in forbidden_suffixes
        or (
            path.name.startswith(".env")
            and path.name != ".env.example"
        )
        or "__pycache__" in path.parts
        or path.suffix.lower() in {".pyc", ".pyo"}
    )

    assert not unsafe, "Generated or sensitive files are tracked: " + ", ".join(unsafe)


def test_only_supported_github_workflow_is_active():
    workflow_dir = REPO_ROOT / ".github" / "workflows"
    workflows = sorted(path.name for path in workflow_dir.glob("*.yml"))

    assert workflows == ["python-app.yml"]
    assert not (REPO_ROOT / "python-app.yml").exists()
    assert not (REPO_ROOT / "github-workflows" / "python-publish.yml").exists()


def test_runtime_baseline_is_consistent():
    app_requirements = (
        REPO_ROOT / "lightone_v2_django" / "requirements.txt"
    ).read_text(encoding="utf-8")
    app_readme = (
        REPO_ROOT / "lightone_v2_django" / "README.md"
    ).read_text(encoding="utf-8")
    workflow = (
        REPO_ROOT / ".github" / "workflows" / "python-app.yml"
    ).read_text(encoding="utf-8")

    assert "Django>=6.0.7,<6.1" in app_requirements
    assert "Python 3.12+ + Django 6.0" in app_readme
    assert '"3.12"' in workflow
    assert '"3.13"' in workflow
