document.addEventListener('DOMContentLoaded', function () {
    var myChart = Highcharts.chart('graph-B07PLR3BTV', {
        title: {
            text: undefined,
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
            data: [[Date.parse('2016-07-29'), 59.8],
                [Date.parse('2016-07-30'), 60.2],
                [Date.parse('2016-07-31'), 59.9],
                [Date.parse('2016-08-02'), 60.8],
                [Date.parse('2016-08-05'), 61.7]],
        }],
        credits: {
            enabled: false
        },
        legend: {
            enabled: false
        },
    });
});