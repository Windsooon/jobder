$(document).ready(function() {
    const token = $("#api-token").val(); 
    const url = "https://api.github.com/graphql"
    get_user_data(url, token);
});

function get_user_data(url, token) {
    var query = `query { viewer 
        { login 
          name
          avatarUrl
          location
          email
          bio
          repositories(first:24, orderBy: {direction: DESC, field: UPDATED_AT}) {
              edges {
                  node {
                      name
                      description
                      createdAt
                      homepageUrl
                      nameWithOwner
                      projectsUrl
                      url
                      languages(first:3) {
                          edges {
                              node {
                                  name
                              }
                          }
                      }
                  } 
              }
          }
          repositoriesContributedTo(first:24, orderBy: {direction: DESC, field: UPDATED_AT}) {
			  edges {
                  node {
                      name 
                      description
                      createdAt
                      homepageUrl
                      nameWithOwner
                      projectsUrl
                      url
                      languages(first:3) {
                          edges {
                              node {
                                  name
                              }
                          }
                      } 
                  }
              }
          }
        }}`

   	$.ajax({
		url: url,
		type: "POST",
		dataType: "json",
        headers: {
            Authorization: "bearer " + token,
        },
        data: JSON.stringify(
            {
                "query": query
            }),
		success:function(data){
            data = data.data.viewer;
            console.log(data);
            update_profile(data);
        }
    }); 
}

function update_profile(data) {
    $("#avatar-img").attr("src", data.avatarUrl);
    $("#user-name").text(data.name);
    $("#user-bio").text(data.bio);
}

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
