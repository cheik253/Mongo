$(function() {
    // AJAX request to your Flask endpoint
    $.ajax({
        url: "/count",  // Ensure this matches your Flask route
        type: "GET",
        success: function(response) {
            var categories = response.categories;
            var series = response.chartData[0].data;

            // Chart configuration
            var options = {
                chart: {
                    type: 'pie',
                    height: 300,
                    toolbar: {
                        show: true,
                        tools: {
                            download: true,  // Enable download icon
                            selection: true,
                            zoom: true,
                            zoomin: true,
                            zoomout: true,
                            pan: true,
                            reset: true | '<img src="/static/icons/reset.png" width="20">',
                            customIcons: [{
                                // Custom icon for CSV download
                                icon: '<img src="https://cdn-icons-png.flaticon.com/512/337/337946.png" width="20">',
                                title: 'Download CSV',
                                index: -1,
                                class: 'custom-csv-download',
                                click: function(chart, options, e) {
                                    // Call the function to download CSV
                                    downloadCSV({ filename: "chart-data.csv" }, categories, series);
                                }
                            }]
                        },
                        export: {
                            csv: {
                                filename: 'my-chart',
                                columnDelimiter: ',',
                                headerCategory: 'Category',
                                headerValue: 'Value',
                                dateFormatter(timestamp) {
                                    return new Date(timestamp).toDateString()
                                }
                            },
                            svg: {
                                filename: 'my-chart',
                            },
                            png: {
                                filename: 'my-chart',
                            }
                        },
                    }
                },
                series: series,
                labels: categories,
                responsive: [{
                    breakpoint: 480,
                    options: {
                        chart: {
                            width: 400
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

// Function to download CSV
function downloadCSV(options, categories, seriesData) {
    var data, filename, link;
    var csv = "";
    // Generate CSV content
    csv += "Category,Value\n";
    for (var i = 0; i < categories.length; i++) {
        csv += categories[i] + "," + seriesData[i] + "\n";
    }

    if (csv == null) return;

    filename = options.filename || 'chart-data.csv';

    if (!csv.match(/^data:text\/csv/i)) {
        csv = 'data:text/csv;charset=utf-8,' + csv;
    }
    data = encodeURI(csv);

    link = document.createElement('a');
    link.setAttribute('href', data);
    link.setAttribute('download', filename);
    link.click();
}
$(function() {
    // AJAX request to your Flask endpoint for the new chart
    $.ajax({
        url: "/age_can",  // Modify the URL to match your Flask route for the new chart data
        type: "GET",
        success: function(response) {
            var categories = response.categories;
            var series = [{
                name: 'Ages',
                data: response.chartData[0].data
            }];

            // Chart configuration for the new chart
            var options = {
                chart: {
                    type: 'bar', // Change the chart type to the appropriate type (e.g., 'bar', 'line', 'area', etc.)
                    height: 200,
                },
                series: series,
                xaxis: {
                    categories: categories
                },
                legend: {
                    show: true, // Show legend
                    position: 'top', // Position of the legend
                    horizontalAlign: 'left', // Horizontal alignment of the legend
                    offsetY: 5,
                      width: 500  // Offset the legend vertically
                },
                responsive: [{
                    breakpoint: 480,
                    options: {
                        chart: {
                            width: 300
                        },
                        legend: {
                            position: 'bottom'
                        }
                    }
                }]
            };

            // Initialize and render the new chart within the existing div
            var chart = new ApexCharts(document.querySelector("#breakup"), options); // Render within the existing div with id "breakup"
            chart.render();
        },
        error: function(error) {
            console.error("Error fetching data for the new chart:", error);
        }
    });
});
$(function() {
    // AJAX request to your Flask endpoint for the new chart
    $.ajax({
        url: "/age_vote",  // Modify the URL to match your Flask route for the new chart data
        type: "GET",
        success: function(response) {
            var categories = response.categories;
            var series = [{
                name: 'Ages',
                data: response.chartData[0].data
            }];

            // Chart configuration for the new chart
            var options = {
                chart: {
                    type: 'bar', // Change the chart type to the appropriate type (e.g., 'bar', 'line', 'area', etc.)
                    height: 200,
                },
                series: series,
                xaxis: {
                    categories: categories
                },
                legend: {
                    show: true, // Show legend
                    position: 'top', // Position of the legend
                    horizontalAlign: 'left', // Horizontal alignment of the legend
                    offsetY: 5,
                      width: 200  // Offset the legend vertically
                },
                responsive: [{
                    breakpoint: 480,
                    options: {
                        chart: {
                            width: 300
                        },
                        legend: {
                            position: 'bottom'
                        }
                    }
                }]
            };

            // Initialize and render the new chart within the existing div
            var chart = new ApexCharts(document.querySelector("#earning"), options); // Render within the existing div with id "breakup"
            chart.render();
        },
        error: function(error) {
            console.error("Error fetching data for the new chart:", error);
        }
    });
});
