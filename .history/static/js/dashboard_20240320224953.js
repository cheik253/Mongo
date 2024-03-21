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
        chart.updateSeries(chartData.map(data => data.data));
        chart.updateOptions({
          xaxis: {
            categories: categories
          },
          colors: colors
        }, false); // Passing false to prevent re-rendering immediately
        chart.render(); // Manually re-render the chart
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
    series: [],
    chart: {
      type: "bar", // Corrected "char" to "bar"
      height: 345,
      foreColor: "#adb0bb",
      fontFamily: 'inherit',
      background: '#000000', // Setting background color to black
    },
    xaxis: {
      labels: {
        style: {
          colors: '#adb0bb' // Setting x-axis labels color
        }
      }
    },
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
