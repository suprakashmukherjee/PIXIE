async function runScan() {

    const sourcePath =
        document.getElementById(
            "sourcePath"
        ).value.trim();

    if (!sourcePath) {

        alert(
            "Please enter a source photo library path."
        );

        return;
    }

    const dryRun =
        document.getElementById(
            "dryRun"
        ).checked;

    const deleteAfterMove =
        document.getElementById(
            "deleteAfterMove"
        ).checked;

    try {

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
                    dry_run: dryRun,
                    delete_after_move:
                        deleteAfterMove
                })
            }
        );

        if (!response.ok) {

            const errorText =
                await response.text();

            throw new Error(errorText);
        }

        const data =
            await response.json();

        document
            .getElementById("results")
            .classList.remove("hidden");

        document
            .getElementById("summary")
            .innerHTML = `
                <p>
                    <strong>RAW Files Found:</strong>
                    ${data.total_raw_files}
                </p>

                <p>
                    <strong>JPEG Files Found:</strong>
                    ${data.total_jpeg_files}
                </p>

                <p>
                    <strong>Orphan RAW Files:</strong>
                    ${data.orphan_raw_files}
                </p>

                <p>
                    <strong>Potential Storage Recovery:</strong>
                    ${data.storage_recovered_gb} GB
                </p>

                <p>
                    <strong>PIXIE_DELETE Folder:</strong>
                    ${data.pixie_delete_folder}
                </p>

                <p>
                    <strong>Report File:</strong>
                    ${data.report_file}
                </p>
            `;

        const tbody =
            document.querySelector(
                "#orphansTable tbody"
            );

        tbody.innerHTML = "";

        data.orphans.forEach(row => {

            const tr =
                document.createElement(
                    "tr"
                );

            tr.innerHTML = `
                <td>
                    ${row.raw_file_name}
                </td>

                <td>
                    ${row.source_path}
                </td>
            `;

            tbody.appendChild(tr);

        });

    } catch (error) {

        console.error(error);

        alert(
            "Error: " +
            error.message
        );
    }
}