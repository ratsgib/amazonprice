function write_graph(asin) {
    var myChart = Highcharts.chart("graph-" + asin, {
        title: {
            text: undefined,
        },
        data: {
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
            }
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
    });
}
