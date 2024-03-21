$(function () {

  // Function to make AJAX request to Flask route and update the chart
  function updateChartWithData() {
    $.ajax({
      url: "/count",
      type: "GET",
      success: function(response) {
        // Extract data from response
        var numbers_of_elements = response.numbers_of_elements;
        var voter_name = response.voter_name;

        // Prepare data for pie chart
        var pieChartData = [];
        for (var i = 0; i < numbers_of_elements.length; i++) {
          pieChartData.push({
            x: voter_name[i],
            y: numbers_of_elements[i]
          });
        }

        // Update chart series with pie chart data
        chart.updateSeries([{
          data: pieChartData
        }]);
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
      height: 400,
    },
    labels: [],
    colors: ["#5D87FF", "#49BEFF"],
    tooltip: {
      theme: "light",
      fillSeriesColor: false,
    },
  });

  // Render the pie chart
  chart.render();

});
