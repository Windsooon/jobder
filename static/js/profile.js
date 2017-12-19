var ItemsVue = new Vue({
    el: '#Itemlist',
    data: {
        items: []
    },
    created: function () {
        var self = this;
        $.ajax({
            url: '/items',
            method: 'GET',
            success: function (data) {
                self.items = data;
            },
            error: function (error) {
                console.log(error);
            }
        });
    }
});

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

window.onload = function() {
    var ctx = document.getElementById("canvas").getContext("2d");
    window.myLine = new Chart(ctx, config);
};
