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
          labels: categories
        });
      },
      error: function(error) {
        console.error("Error fetching data:", error);
      }
    });
  }

  // Call the updateChartWithData function initially to load chart data
  updateChartWithData();

  // Pie chart configuration
  var chart = new ApexCharts(document.querySelector("#chart"), {
    series: [],
    chart: {
      type: "pie",
      height: 345,
      foreColor: "#adb0bb",
      fontFamily: 'inherit',
    },
    labels: [],
    colors: ["#5D87FF", "#49BEFF"],
    dataLabels: {
      enabled: true,
      formatter: function(val, opts) {
        return opts.w.globals.labels[opts.seriesIndex] + ":  " + val
      }
    },
    legend: {
      position: 'bottom'
    },
    tooltip: { theme: "light" }
  });

  // Render the chart
  chart.render();
});
