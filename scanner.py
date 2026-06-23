from pathlib import Path
import shutil
import csv
from datetime import datetime

RAW_EXTENSIONS = {
    ".arw",
    ".cr2",
    ".cr3",
    ".nef",
    ".raf",
    ".rw2",
    ".orf",
    ".dng"
}


def get_folder_file_index(folder_path: Path):
    """
    Create a case-insensitive filename lookup.
    """
    return {
        file.name.lower()
        for file in folder_path.iterdir()
        if file.is_file()
    }


def scan_orphan_raws(
    source_path: str,
    delete_folder: str,
    delete_after_move: bool = False,
    dry_run: bool = True
):
    source = Path(source_path)
    delete_root = Path(delete_folder)

    if not source.exists():
        raise FileNotFoundError(f"Source path does not exist: {source}")

    total_raw_files = 0
    total_jpeg_files = 0
    orphan_raw_files = 0
    recovered_bytes = 0

    report_rows = []

    for current_dir, _, files in __import__("os").walk(source):

        current_dir = Path(current_dir)

        file_index = {
            file_name.lower()
            for file_name in files
        }

        for file_name in files:

            file_path = current_dir / file_name

            suffix = file_path.suffix.lower()

            if suffix in [".jpg", ".jpeg"]:
                total_jpeg_files += 1

            if suffix not in RAW_EXTENSIONS:
                continue

            total_raw_files += 1

            stem = file_path.stem

            jpg_match = f"{stem.lower()}.jpg"
            jpeg_match = f"{stem.lower()}.jpeg"

            has_matching_jpeg = (
                jpg_match in file_index
                or jpeg_match in file_index
            )

            if has_matching_jpeg:
                continue

            orphan_raw_files += 1
            recovered_bytes += file_path.stat().st_size

            relative_path = file_path.relative_to(source)
            destination_path = delete_root / relative_path

            report_rows.append({
                "raw_file_name": file_path.name,
                "source_path": str(file_path),
                "destination_path": str(destination_path),
                "status": "ORPHAN"
            })

            if not dry_run:

                destination_path.parent.mkdir(
                    parents=True,
                    exist_ok=True
                )

                shutil.move(
                    str(file_path),
                    str(destination_path)
                )

    delete_root.mkdir(
        parents=True,
        exist_ok=True
    )

    report_file = (
        delete_root /
        f"orphan_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    )

    with open(
        report_file,
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=[
                "raw_file_name",
                "source_path",
                "destination_path",
                "status"
            ]
        )

        writer.writeheader()
        writer.writerows(report_rows)

    if delete_after_move and not dry_run:

        for row in report_rows:

            moved_file = Path(
                row["destination_path"]
            )

            if moved_file.exists():
                moved_file.unlink()

    return {
        "total_raw_files": total_raw_files,
        "total_jpeg_files": total_jpeg_files,
        "orphan_raw_files": orphan_raw_files,
        "storage_recovered_gb": round(
            recovered_bytes / (1024 ** 3),
            2
        ),
        "report_file": str(report_file),
        "orphans": report_rows
    }