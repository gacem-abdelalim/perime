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
    if (ths.length < 5) return; // must have checkbox + ID + Name + data

    // ---- Remove only ID & Name from default row ----
    var idTh = ths[1];   // after checkbox
    var nameTh = ths[2]; // after ID
    idTh.remove();
    nameTh.remove();
    var cbTh = ths[0];
    cbTh.remove();

    // ---- Build group header row ----
    var groupRow = document.createElement("tr");

    // Checkbox column (rowspan=2)
    var cbCell = document.createElement("th");
    cbCell.rowSpan = 2;
    cbCell.className = "action-checkbox-column"; // admin CSS
    
    groupRow.appendChild(cbCell);

    // ID column (rowspan=2)
    var idCell = document.createElement("th");
    idCell.rowSpan = 2;
    idCell.innerText = "ID";
    groupRow.appendChild(idCell);

    // Name column (rowspan=2)
    var nameCell = document.createElement("th");
    nameCell.rowSpan = 2;
    nameCell.innerText = "Name";
    groupRow.appendChild(nameCell);

    // Groups (TOTAL + ranges), each with 2 columns
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

    // Insert group row before the default header row
    thead.insertBefore(groupRow, secondRow);

    // ---- Update default header row (QTE / VALEUR ACHAT) ----
    var dataThs = Array.from(secondRow.querySelectorAll("th"));

    // Skip the first one (checkbox already handled)
    for (var i = 0; i < dataThs.length; i++) {
        var link = dataThs[i].querySelector("a");
        var label = (i % 2 === 1) ? "VALEUR ACHAT" : "QTE"; // odd → QTE, even → VALEUR

        if (link) {
            link.textContent = label; // keep sorting arrows
        } else {
            dataThs[i].textContent = label;
        }
    }
});
