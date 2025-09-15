(function(){
    console.log("Hello from JS");
    document.addEventListener('DOMContentLoaded', function(){
    // find the admin changelist table
    var resultsDiv = document.querySelector('.results') || document.querySelector('.changelist');
    if(!resultsDiv) return;
    var table = resultsDiv.querySelector('table');
    if(!table) return;
    var thead = table.querySelector('thead');
    if(!thead) return;
    var secondRow = thead.querySelector('tr'); // this is the default header row

    var ths = Array.from(secondRow.querySelectorAll('th'));
    if(ths.length < 4) return; // sanity check

    // Remove first two headers (ID & Name) from the default row, we'll add them in top row with rowspan
    var idTh = ths[0];
    var nameTh = ths[1];
    idTh.remove();
    nameTh.remove();

    // Build the group header row
    var groupRow = document.createElement('tr');

    // ID and Name cells with rowspan=2
    var idCell = document.createElement('th');
    idCell.rowSpan = 2;
    idCell.innerText = 'ID';
    groupRow.appendChild(idCell);

    var nameCell = document.createElement('th');
    nameCell.rowSpan = 2;
    nameCell.innerText = 'Name';
    groupRow.appendChild(nameCell);

    // Add your groups — each group spans 2 columns (QTE + VALEUR ACHAT)
    var groups = [
      'TOTAL',
      '< 3 mois',
      '3 mois - 6 mois',
      '6 mois - 12 mois',
      '12 mois - 18 mois',
      '18 mois - 24 mois',
      '24 mois - 36 mois',
      '> 36 mois'
    ];
    groups.forEach(function(g){
      var th = document.createElement('th');
      th.colSpan = 2;
      th.innerText = g;
      groupRow.appendChild(th);
    });

    // Insert the group row above the default header row
    thead.insertBefore(groupRow, secondRow);

    // Now update the remaining header cells (the original ones) to be QTE / VALEUR ACHAT
    // After removing the first two headers above, secondRow's ths correspond to your data columns
    var dataThs = Array.from(secondRow.querySelectorAll('th'));
    for(var i=0;i<dataThs.length;i++){
      dataThs[i].innerText = (i % 2 === 0) ? 'QTE' : 'VALEUR ACHAT';
    }
  });
})();
