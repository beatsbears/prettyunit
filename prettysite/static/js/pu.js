function fitToContainer(canvas){
  canvas.style.width='100%';
  canvas.style.height='100%';
  canvas.width  = canvas.offsetWidth;
  canvas.height = canvas.offsetHeight;
}


function TimeLine(testcounts) {
  var ctx = document.getElementById("TimeLineGraph");
  Chart.defaults.global.legend.display = false;

  var counts = []
  for (i = 0; i < testcounts.length; i++ ) {
     counts.push("");
  };

  var data = {
    labels: counts,
    datasets: [
        {
            label: "Test Count",
            backgroundColor: "rgba(9,160,246,0.6)",
            data: testcounts,
        }
    ]
  };

  var TimeLineGraph = new Chart(ctx, {
    type: 'line',
    data: data,
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
});
};