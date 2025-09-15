document.addEventListener("DOMContentLoaded", function () {
    var resultsDiv = document.querySelector(".results");
    if (!resultsDiv) return;

    var table = resultsDiv.querySelector("table");
    if (!table) return;

    var thead = table.querySelector("thead");
    if (!thead) return;

    var secondRow = thead.querySelector("tr"); // default header row
    if (!secondRow) return;

    var ths = Array.from(secondRow.querySelectorAll("th"));
    if (ths.length < 4) return;

    // Remove ID + Name from default row
    var idTh = ths[0];
    var nameTh = ths[1];
    var chTh = ths[2];
    idTh.remove();
    nameTh.remove();
    chTh.remove();

    // Create new group row
    var groupRow = document.createElement("tr");
    
    // Checkbox column (rowspan=2)
    var cbCell = document.createElement("th");
    cbCell.rowSpan = 2;
    cbCell.className = "action-checkbox-column"; // admin CSS
    groupRow.appendChild(cbCell);

    // Add ID + Name with rowspan
    var idCell = document.createElement("th");
    idCell.rowSpan = 2;
    idCell.innerText = "ID";
    groupRow.appendChild(idCell);

    var nameCell = document.createElement("th");
    nameCell.rowSpan = 2;
    nameCell.innerText = "Name";
    groupRow.appendChild(nameCell);

    // Add grouped headers
    var groups = [
        "TOTAL",
        "< 3 mois",
        "3–6 mois",
        "6–12 mois",
        "12–18 mois",
        "18–24 mois",
        "24–36 mois",
        "> 36 mois"
    ];
    groups.forEach(function (g) {
        var th = document.createElement("th");
        th.colSpan = 2;
        th.innerText = g;
        groupRow.appendChild(th);
    });

    // Insert group row before the default row
    thead.insertBefore(groupRow, secondRow);

    // Rename the default headers to QTE / VALEUR ACHAT
    var dataThs = Array.from(secondRow.querySelectorAll("th"));
    for (var i = 0; i < dataThs.length; i++) {
        dataThs[i].innerText = (i % 2 === 0) ? "QTE" : "VALEUR ACHAT";
    }
});
