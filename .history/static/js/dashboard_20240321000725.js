$(function () {
    $.ajax({
        url: "/count",
        type: "GET",
        success: function(response) {
            const categories = response.categories;
            const series = response.chartData[0].data;

            var options = {
                chart: {
                    type: 'pie'
                },
                labels: categories,
                series: series,
                responsive: [{
                    breakpoint: 480,
                    options: {
                        chart: {
                            width: 200
                        },
                        legend: {
                            position: 'bottom'
                        }
                    }
                }]
            };

            var chart = new ApexCharts(document.querySelector("#chart"), options);
            chart.render();
        },
        error: function(error) {
            console.error("Error fetching data: ", error);
        }
    });
});