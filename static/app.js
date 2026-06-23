async function runScan() {

    const sourcePath =
        document.getElementById(
            "sourcePath"
        ).value;

    const deleteFolder =
        document.getElementById(
            "deleteFolder"
        ).value;

    const dryRun =
        document.getElementById(
            "dryRun"
        ).checked;

    const deleteAfterMove =
        document.getElementById(
            "deleteAfterMove"
        ).checked;

    const response = await fetch(
        "/scan",
        {
            method: "POST",
            headers: {
                "Content-Type":
                    "application/json"
            },
            body: JSON.stringify({
                source_path: sourcePath,
                delete_folder: deleteFolder,
                dry_run: dryRun,
                delete_after_move:
                    deleteAfterMove
            })
        }
    );

    const data = await response.json();

    document
        .getElementById("results")
        .classList.remove("hidden");

    document
        .getElementById("summary")
        .innerHTML = `
            <p>
                RAW Files:
                ${data.total_raw_files}
            </p>

            <p>
                JPEG Files:
                ${data.total_jpeg_files}
            </p>

            <p>
                Orphan RAW Files:
                ${data.orphan_raw_files}
            </p>

            <p>
                Storage Recovered:
                ${data.storage_recovered_gb} GB
            </p>

            <p>
                Report:
                ${data.report_file}
            </p>
        `;

    const tbody =
        document.querySelector(
            "#orphansTable tbody"
        );

    tbody.innerHTML = "";

    data.orphans.forEach(row => {

        tbody.innerHTML += `
            <tr>
                <td>${row.raw_file_name}</td>
                <td>${row.source_path}</td>
            </tr>
        `;
    });
}