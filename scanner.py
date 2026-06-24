import csv
import os
import shutil
from datetime import datetime
from pathlib import Path

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


def scan_orphan_raws(
    source_path: str,
    dry_run: bool = True,
    delete_after_move: bool = False
):

    source = Path(source_path)

    if not source.exists():
        raise FileNotFoundError(
            f"Source path does not exist: {source}"
        )

    if not source.is_dir():
        raise NotADirectoryError(
            f"Source path is not a directory: {source}"
        )

    pixie_delete_folder = source / "PIXIE_DELETE"

    total_raw_files = 0
    total_jpeg_files = 0
    orphan_raw_files = 0
    recovered_bytes = 0

    report_rows = []

    for current_dir, dirs, files in os.walk(source):

        # Do not scan PIXIE_DELETE
        dirs[:] = [
            d for d in dirs
            if d != "PIXIE_DELETE"
        ]

        current_dir = Path(current_dir)

        file_index = {
            file_name.lower()
            for file_name in files
        }

        for file_name in files:

            file_path = current_dir / file_name

            extension = file_path.suffix.lower()

            if extension in {".jpg", ".jpeg"}:
                total_jpeg_files += 1

            if extension not in RAW_EXTENSIONS:
                continue

            total_raw_files += 1

            stem = file_path.stem

            expected_jpg = f"{stem.lower()}.jpg"
            expected_jpeg = f"{stem.lower()}.jpeg"

            has_matching_jpeg = (
                expected_jpg in file_index
                or expected_jpeg in file_index
            )

            if has_matching_jpeg:
                continue

            orphan_raw_files += 1

            try:
                recovered_bytes += file_path.stat().st_size
            except Exception:
                pass

            relative_path = file_path.relative_to(source)

            destination_path = (
                pixie_delete_folder /
                relative_path
            )

            report_rows.append(
                {
                    "raw_file_name": file_path.name,
                    "source_path": str(file_path),
                    "destination_path": str(destination_path),
                    "status": (
                        "ORPHAN"
                        if dry_run
                        else "MOVED"
                    )
                }
            )

            if not dry_run:

                destination_path.parent.mkdir(
                    parents=True,
                    exist_ok=True
                )

                shutil.move(
                    str(file_path),
                    str(destination_path)
                )

    if not dry_run:
        pixie_delete_folder.mkdir(
            parents=True,
            exist_ok=True
        )

    report_folder = (
        pixie_delete_folder
        if not dry_run
        else source
    )

    report_file = (
        report_folder /
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
        "pixie_delete_folder": str(
            pixie_delete_folder
        ),
        "report_file": str(report_file),
        "orphans": report_rows
    }