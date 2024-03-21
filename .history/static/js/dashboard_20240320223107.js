$(function () {

  // Function to make AJAX request to Flask route and update the chart
  function updateChartWithData() {
    $.ajax({
      url: "/count",
      type: "GET",
      success: function(response) {
        // Extract data from response
        var chartData = response.chartData;
        var categories = response.categories;

        // Update chart series and categories
        chart.updateOptions({
          series: chartData,
          xaxis: {
            categories: categories
          }
        });
      },
      error: function(error) {
        console.error("Error fetching data:", error);
      }
    });
  }

  // Call the updateChartWithData function initially to load chart data
  updateChartWithData();

  // Bar chart configuration
  var chart = new ApexCharts(document.querySelector("#chart"), {
    series: [
      { name: "Earnings this month:", data: [] },
      { name: "Expense this month:", data: [] }
    ],
    chart: {
      type: "pie",
      height: 345,
      offsetX: -15,
      toolbar: { show: true },
      foreColor: "#adb0bb",
      fontFamily: 'inherit',
      sparkline: { enabled: false },
    },
    colors: ["#5D87FF", "#49BEFF"],
    plotOptions: {
      bar: {
        horizontal: false,
        columnWidth: "35%",
        borderRadius: [6],
        borderRadiusApplication: 'end',
        borderRadiusWhenStacked: 'all'
      },
    },
    markers: { size: 0 },
    dataLabels: {
      enabled: false,
    },
    legend: {
      show: false,
    },
    grid: {
      borderColor: "rgba(0,0,0,0.1)",
      strokeDashArray: 3,
      xaxis: {
        lines: {
          show: false,
        },
      },
    },
    xaxis: {
      type: "category",
      categories: [],
      labels: {
        style: { cssClass: "grey--text lighten-2--text fill-color" },
      },
    },
    yaxis: {
      show: true,
      min: 0,
      max: 400,
      tickAmount: 4,
      labels: {
        style: {
          cssClass: "grey--text lighten-2--text fill-color",
        },
      },
    },
    stroke: {
      show: true,
      width: 3,
      lineCap: "butt",
      colors: ["transparent"],
    },
    tooltip: { theme: "light" },
    responsive: [
      {
        breakpoint: 600,
        options: {
          plotOptions: {
            bar: {
              borderRadius: 3,
            }
          },
        }
      }
    ]
  });

  // Render the chart
  chart.render();
});
