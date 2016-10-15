// Ascott 10-9
// Pretty unit site main js

//-------------------------- Graph Colors ----------------------------
var passColor = "rgba(43,247,149,1)";
var skipColor = "rgba(0,148,247,1)";
var errorColor = "rgba(247,152,121,1)";
var failColor = "rgba(247,66,0,1)";

var passColor_hover = "rgba(12,155,0,0.5)";
var skipColor_hover = "rgba(9,160,246,0.5)";
var errorColor_hover = "rgba(229,128,12,0.5)";
var failColor_hover = "rgba(204,0,39,0.5)";


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
            backgroundColor: skipColor,
            data: testcounts[0],
        },
        {
            label: "Error Count",
            backgroundColor: errorColor,
            data: testcounts[1],
        },
        {
            label: "Fail Count",
            backgroundColor: failColor,
            data: testcounts[2],
        },
        {
            label: "Pass Count",
            backgroundColor: passColor,
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
                    mirror: true,
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
                passColor,
                failColor,
                errorColor,
                skipColor
            ],
            hoverBackgroundColor: [
                passColor_hover,
                failColor_hover,
                errorColor_hover,
                skipColor_hover
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
                passColor,
                failColor,
                errorColor,
                skipColor
            ],
            hoverBackgroundColor: [
                passColor_hover,
                failColor_hover,
                errorColor_hover,
                skipColor_hover
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
                passColor,
                failColor,
                errorColor,
                skipColor
            ],
            hoverBackgroundColor: [
                passColor_hover,
                failColor_hover,
                errorColor_hover,
                skipColor_hover
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

// ------------------------------------- Description --------------------------------------------
function editDescription() {

    // Handle the UI for changing the project table between modes
    var name_edit_field = document.getElementById("project_name_field");
    var desc_edit_field = document.getElementById("project_description_field");
    var lang_edit_field = document.getElementById("project_language_field");
    var url_edit_field = document.getElementById("project_url_field");
    var changeImg = "";
    var description_button = document.getElementById("project_description_button");

    if (description_button.src.includes("save.png")) {
        name_edit_field.contentEditable = false;
        desc_edit_field.contentEditable = false;
        lang_edit_field.contentEditable = false;
        url_edit_field.contentEditable = false;
        changeImg = "/img/edit.png";
        description_button.state = "save"

        // Record project setting values
        var project_array = {}
        var project_details_table = document.getElementById("project_details_table");
        var row_length = project_details_table.rows.length;
        for (var i = 0; i < row_length; i++) {
            var oCells = project_details_table.rows.item(i).cells;
            project_array[oCells.item(0).innerHTML] = oCells.item(1).innerHTML
        }

        // PUT new project object via API
        var project_id = document.getElementById("project_id").innerHTML;
        var put_url = '/project/' + project_id;
        console.log(put_url);
        $.ajax({
        url: put_url,
        type: 'PUT',
        data: JSON.stringify(project_array),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        async: false });
    }
    else if (description_button.src.includes("edit.png")) {
        name_edit_field.contentEditable = true;
        desc_edit_field.contentEditable = true;
        lang_edit_field.contentEditable = true;
        url_edit_field.contentEditable = true;
        changeImg = "/img/save.png";
        description_button.state = "edit"
    }
    description_button.src = changeImg;
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
