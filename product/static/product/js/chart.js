function write_graph(asin) {
    var myChart = Highcharts.chart("graph-" + asin, {
        title: {
            text: undefined,
        },
        data: {
            name: 'Price',
            firstRowAsNames: false,
            csv: document.getElementById('data-' + asin).innerHTML,
        },
        xAxis: {
            title: {
                text: undefined,
            },
            type: 'datetime',
        },
        yAxis: {
            title: {
                text: undefined,
            },
            min: 0,
        },
        series: [{
            name: 'Price',
        }],
        credits: {
            enabled: false
        },
        legend: {
            enabled: false
        },
        plotOptions: {
            series: {
                marker: {
                    enabled: true,
                }
            }
        },
});
}
