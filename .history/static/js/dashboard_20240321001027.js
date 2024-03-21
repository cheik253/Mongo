$(function() {
    $.ajax({
        url: "/count",  // Make sure this matches the route in your Flask app
        type: "GET",
        success: function(response) {
            // Extract categories and data for the chart
            var categories = response.categories;
            var series = response.chartData[0].data;

            // Configure the pie chart
            var options = {
                chart: {
                    type: 'pie',
                    height: 400  // Adjust height as needed
                },
                series: series,
                labels: categories,
                responsive: [{
                    breakpoint: 480,
                    options: {
                        chart: {
                            width: 300  // Adjust width for smaller screens as needed
                        },
                        legend: {
                            position: 'bottom'
                        }
                    }
                }]
            };

            // Initialize and render the chart
            var chart = new ApexCharts(document.querySelector("#chart"), options);
            chart.render();
        },
        error: function(error) {
            console.error("Error fetching data:", error);
        }
    });
});