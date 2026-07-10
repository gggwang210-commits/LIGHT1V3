from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_DASHBOARD_DOCS = [
    "docs/dashboard_strategy.md",
    "docs/member_dashboard_spec.md",
    "docs/trainer_dashboard_spec.md",
    "docs/admin_dashboard_spec.md",
    "docs/dashboard_information_architecture.md",
    "docs/dashboard_component_library.md",
    "docs/dashboard_data_model.md",
    "docs/dashboard_sample_user_flows.md",
    "docs/dashboard_safety_copy_guidelines.md",
    "docs/dashboard_codex_implementation_plan.md",
]


def test_dashboard_docs_exist():
    missing = [path for path in REQUIRED_DASHBOARD_DOCS if not (REPO_ROOT / path).is_file()]
    assert not missing, "Missing dashboard docs: " + ", ".join(missing)


def test_readme_links_dashboard_docs_and_prototype():
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    expected_links = [
        "docs/dashboard_strategy.md",
        "docs/member_dashboard_spec.md",
        "prototype/dashboards/member_dashboard.html",
    ]
    for path in expected_links:
        assert path in readme


def test_prototype_files_exist_when_dashboard_prototype_exists():
    prototype_dir = REPO_ROOT / "prototype" / "dashboards"
    if prototype_dir.exists():
        required_files = [
            "member_dashboard.html",
            "trainer_dashboard.html",
            "admin_dashboard.html",
            "dashboard_theme.css",
            "dashboard_mock_data.js",
        ]
        for name in required_files:
            assert (prototype_dir / name).is_file()
