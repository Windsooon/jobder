// Chart.js
var config = {
    type: 'line',
    data: {
        labels: ["January", "February", "March", "April", "May", "June", "July"],
        datasets: [{
            label: "My First dataset",
            backgroundColor: window.chartColors.red,
            borderColor: window.chartColors.red,
            data: [10, 30, 39, 20, 25, 34, -10],
            fill: false,
        }, {
            label: "My Second dataset",
            fill: false,
            backgroundColor: window.chartColors.blue,
            borderColor: window.chartColors.blue,
            data: [18, 33, 22, 19, 11, 39, 30],
        }]
    },
    options: {
        responsive: true,
        title:{
            display:true,
            text:'Min and Max Settings'
        },
        scales: {
            yAxes: [{
                ticks: {
                    // the data minimum used for determining the ticks is Math.min(dataMin, suggestedMin)
                    suggestedMin: 10,

                    // the data maximum used for determining the ticks is Math.max(dataMax, suggestedMax)
                    suggestedMax: 50
                }
            }]
        }
    }
};

function addData(chart, label, data) {
    chart.data.labels.push(label);
    chart.data.datasets.forEach((dataset) => {
        dataset.data.push(data);
    });
    chart.update();
}

// get user repo
let user_repos = {
	url: 'https://api.github.com/graphql',
	method: 'post', 
    headers: { 'Authorization': 'bearer cfb0afc6e06cee4ae5ccb5c3527825ad38ccce6c' },
	data: {
        "query": "query { viewer { login avatarUrl }}"
    }
} 
