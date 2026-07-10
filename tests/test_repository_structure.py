from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_required_repository_documents_exist():
    required_paths = [
        REPO_ROOT / "README.md",
        REPO_ROOT / "docs",
        REPO_ROOT / "docs" / "LIGHT_ONE_final_business_plan_v1_2026-07-07.md",
        REPO_ROOT / "docs" / "safety_and_privacy_policy.md",
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
