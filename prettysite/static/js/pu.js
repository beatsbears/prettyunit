function fitToContainer(canvas){
  canvas.style.width='100%';
  canvas.style.height='100%';
  canvas.width  = canvas.offsetWidth;
  canvas.height = canvas.offsetHeight;
}


function TimeLine(testcounts, dates) {
  var ctx = document.getElementById("TimeLineGraph");
  Chart.defaults.global.legend.display = false;


  var data = {
    labels: dates,
    datasets: [
        {
            label: "Skip Count",
            backgroundColor: "rgba(9,160,246,1)",
            data: testcounts[0],
        },
        {
            label: "Error Count",
            backgroundColor: "rgba(229,128,12,1)",
            data: testcounts[1],
        },
        {
            label: "Fail Count",
            backgroundColor: "rgba(204,0,39,1)",
            data: testcounts[2],
        },
        {
            label: "Pass Count",
            backgroundColor: "rgba(12,155,0,1)",
            data: testcounts[3],
        }

    ]
  };

  var TimeLineGraph = new Chart(ctx, {
    type: 'line',
    data: data,
    options: {
        scales: {
            yAxes: [{
                stacked: true,
                ticks: {
                    mirror: true
                }
            }],
            xAxes: [{
        ticks: {
            maxRotation: 45,
            minRotation: 15
        }}]
        },
        fullWidth: true
    }
  });
};


function SummaryBar(SummaryObj) {
  var ctx = document.getElementById("SummaryChart");
  Chart.defaults.global.legend.display = false;
  var data = {
    labels: ["Pass", "Fail", "Error", "Skip"],
    datasets: [
        {
            backgroundColor: [
                "rgba(12,155,0,1)",
                "rgba(204,0,39,1)",
                "rgba(229,128,12,1)",
                "rgba(9,160,246,1)"
            ],
            hoverBackgroundColor: [
                "rgba(12,155,0,.5)",
                "rgba(204,0,39,.5)",
                "rgba(229,128,12,.5)",
                "rgba(9,160,246,.5)"
            ],
            hoverBorderColor: "rgba(1,1,1,1)",
            data: SummaryObj,
        }
    ]
};
var SummaryChart = new Chart(ctx, {
    type: 'bar',
    data: data,
});
};


function SuitePie(SuiteObj){
  var ctx = document.getElementById("SuitePieChart");
  Chart.defaults.global.legend.labels.boxWidth = 10;
  Chart.defaults.global.legend.display = true;
  if (SuiteObj.length > 4) {
    console.error("Suite only has 4 States");
    return false
  }
  var data = {
    labels: [
        "Pass",
        "Fail",
        "Error",
        "Skip"
    ],
    datasets: [
        {
            data: SuiteObj,
            backgroundColor: [
                "#0c9b00",
                "#cc0027",
                "#e5620c",
                "#09a0f6"
            ],
            hoverBackgroundColor: [
                "#0c9b00",
                "#cc0027",
                "#e5620c",
                "#09a0f6"
            ]
        }]
};
var SuitePieChart = new Chart(ctx,{
    type: 'pie',
    data: data,
    options: {
    cutoutPercentage: 30
    }
});
};


function CasePie(CaseObj){
  var ctx = document.getElementById("CasePieChart");
  Chart.defaults.global.legend.labels.boxWidth = 10;
  Chart.defaults.global.legend.display = true;

  if (CaseObj.length > 4) {
    console.error("Suite only has 4 States");
    return false
  }

  var data = {
    labels: [
        "Pass",
        "Fail",
        "Error",
        "Skip"
    ],
    datasets: [
        {
            data: CaseObj,
            backgroundColor: [
                "#0c9b00",
                "#cc0027",
                "#e5620c",
                "#09a0f6"
            ],
            hoverBackgroundColor: [
                "#0c9b00",
                "#cc0027",
                "#e5620c",
                "#09a0f6"
            ]
        }]
};
var CasePieChart = new Chart(ctx,{
    type: 'pie',
    data: data,
    options: {
    cutoutPercentage: 30
    }
});
};


function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}

function goBack() {
    window.history.back();
}



//-------------------------------------- Settings Modal -----------------------------------------
function showSettings() {

}

// Ascott 10-5
// Generate API keys for the first time or recreate a new set
function refreshKeys() {
    console.log("clicked");
    $.ajax({
    url: '/token',
    type: 'GET',
    async: true,
    success: function(data){
        var keys = JSON.parse(data);
        var settings_table = document.getElementById("settings_table");
        if (!(doAPIKeysExist())) {
            for (var i = 0, len = 2; i < len; i++) {
                var row = settings_table.insertRow(-1);
                var cell1 = row.insertCell(0);
                var cell2 = row.insertCell(1);
                var cell3 = row.insertCell(2);
                var cell4 = row.insertCell(3);
                var key_name = "Key" + (i+1).toString();
                row.id = key_name + "_id";
                cell1.innerHTML = key_name;
                cell1.className = "settings_name_column";
                cell2.innerHTML = keys[key_name];
                cell2.className = "settings_value_column";
                cell4.innerHTML = "True";
                cell4.style.display = "none";
            }
        } else {
            var rowLength = settings_table.rows.length;
            for (i = 0; i < rowLength; i++){
                var oCells = settings_table.rows.item(i).cells;
                if (oCells.item(0).innerHTML == "Key1") {
                    oCells.item(1).innerHTML = keys["Key1"];
                } else if (oCells.item(0).innerHTML == "Key2") {
                    oCells.item(1).innerHTML = keys["Key2"];
                }
            }
        }
    }
    });
}

// Ascott 10-6
// Check if API keys exist
function doAPIKeysExist() {
    var settings_table = document.getElementById('settings_table');
    var rowLength = settings_table.rows.length;
    for (i = 0; i < rowLength; i++){
        var oCells = settings_table.rows.item(i).cells;
        if (oCells.item(0).innerHTML == "Key1") {
            return true;
        }
    }
    return false;
}

// Ascott 10-5
// Handle UI when API Keys are enabled/disabled
function toggleKeys() {
    var checkbox = document.getElementById('key_checkbox');
    var key1_row = document.getElementById('Key1_id');
    var key2_row = document.getElementById('Key2_id');
    var spinnerImg = document.getElementById('refresh_keys_spinner');
    var settings_table = document.getElementById("settings_table");

    if (checkbox.checked == true) {
        spinnerImg.style.display = 'block';
        key1_row.style.display = 'block';
        key2_row.style.display = 'block';

    } else {
        spinnerImg.style.display = 'none';
        key1_row.style.display = 'none';
        key2_row.style.display = 'none';
    }
}

// Ascott 10-5
// Check everything in the settings table and POST it back to /settings
// This should be improved in the future to only post things that have changed
function saveSettings() {
    var setting_array = {};
    var settings_table = document.getElementById('settings_table');

    var rowLength = settings_table.rows.length;

    for (i = 0; i < rowLength; i++){

    var oCells = settings_table.rows.item(i).cells;

    var cellLength = oCells.length;

    for(var j = 0; j < cellLength; j++){

      var setting_name = oCells.item(j).innerHTML;

      // If we're dealing with the API keys we can treat them differently
      if (setting_name == "API Tokens Enabled") {
            var enabled_keys = document.getElementById('key_checkbox');
            if (enabled_keys.checked) {
                setting_array[setting_name] = ["True", "False"];
            } else {
                setting_array[setting_name] = ["False", "False"];
            }
      } else {
          if(j==0){
            var setting_value = oCells.item(j+1).innerHTML;
            var setting_lock = oCells.item(j+3).innerHTML;
            setting_array[setting_name] = [setting_value, setting_lock];
          }
      }
   }
}

$.ajax({
    url: '/settings',
    type: 'POST',
    data: JSON.stringify(setting_array),
    contentType: 'application/json; charset=utf-8',
    dataType: 'json',
    async: false });

var modal = document.getElementById('SettingsModal');
modal.style.display = "none";
location.reload();
};
