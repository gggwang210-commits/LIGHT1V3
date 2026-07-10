import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SAMPLE_FILES = [
    "sample_data/dashboard_member_example.json",
    "sample_data/dashboard_trainer_example.json",
    "sample_data/dashboard_admin_example.json",
]
FORBIDDEN_DIR_NAMES = {"real_member_data", "real_member_photos", "real_member_videos", "customer_pii", "health_records", "phi"}


def test_dashboard_sample_data_json_is_valid():
    for relative in SAMPLE_FILES:
        data = json.loads((REPO_ROOT / relative).read_text(encoding="utf-8"))
        assert isinstance(data, dict)
        assert data


def test_forbidden_real_data_directories_do_not_exist():
    bad = [
        str(path.relative_to(REPO_ROOT))
        for path in REPO_ROOT.rglob("*")
        if path.is_dir() and path.name.lower() in FORBIDDEN_DIR_NAMES and ".git" not in path.parts
    ]
    assert not bad, "Forbidden real-data directories found: " + ", ".join(bad)


def test_sample_data_uses_synthetic_labels():
    joined = "\n".join((REPO_ROOT / relative).read_text(encoding="utf-8") for relative in SAMPLE_FILES)
    assert "synthetic" in joined
    assert "010-" not in joined
