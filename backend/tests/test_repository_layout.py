from pathlib import Path


def test_legacy_files_are_organized():
    project_root = Path(__file__).resolve().parents[2]

    archived_files = [
        "app.py",
        "api_client.py",
        "database.py",
        "requirements.txt",
        "PHASE2_PLAN.md",
        "START_HERE.md",
    ]

    for filename in archived_files:
        assert not (project_root / filename).exists()
        assert (project_root / "archive" / filename).is_file()

