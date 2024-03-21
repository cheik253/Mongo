$(function () {

  // Function to generate random hexadecimal color codes
  function getRandomColor() {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
  }

  // Function to make AJAX request to Flask route and update the chart
  function updateChartWithData() {
    $.ajax({
      url: "/count",
      type: "GET",
      success: function(response) {
        // Extract data from response
        var chartData = response.chartData;
        var categories = response.categories;
        var colors = [];

        // Generate random colors for each data point
        for (var i = 0; i < chartData.length; i++) {
          colors.push(getRandomColor());
        }

        // Update chart series, labels, and colors
        chart.updateOptions({
          series: chartData,
          labels: categories,
          colors: colors
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
