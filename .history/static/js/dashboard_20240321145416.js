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
                    height: 400,
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
                            width: 300
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
function() {
    // AJAX request to your Flask endpoint
    $.ajax({
        url: "/age_can",  // Ensure this matches your Flask route
        type: "GET",
        success: function(response) {
            var categories = response.categories;
            var series = response.chartData[0].data;

            // Chart configuration
            var options = {
                chart: {
                    type: 'pie',
                    height: 400,
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
                            width: 300
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