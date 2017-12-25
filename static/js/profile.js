function get_user_data(url, token, user_name) {
    var query = `query {` + 
        'user(login: "' + user_name + '") {' +
          `name
          avatarUrl
          location
          email
          bio
          repositories(first:30, orderBy: {direction: DESC, field: UPDATED_AT}) {
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
          repositoriesContributedTo(first:30, orderBy: {direction: DESC, field: UPDATED_AT}) {
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
            data = data.data.user;
            update_profile(data);
            update_chart(data);
        }
    }); 
}

function update_profile(data) {
    $("#avatar-img").attr("src", data.avatarUrl);
    $("#user-bio").text(data.bio);
}

function update_chart(data) {
    var ctx = document.getElementById("commit-canvas").getContext("2d");
    var state = document.getElementById("state-canvas").getContext("2d");
    // window.myLine = new Chart(ctx, get_chart_config(get_month_list(-6)), [1,2,3,4,5,6]);
    // window.myLine = new Chart(state, get_chart_config(get_month_list(-6)), [1,2,3,4,5,6]);
    window.myLine = new Chart(ctx, get_chart_config(get_month_list(-6), [10,20,30,40,50,26]));
};

function addMonths(index) {
  var date = new Date()
  date.setMonth(date.getMonth() + index);
  locale = "en-us";
  return date.toLocaleString(locale, { month: "long" });
}

function get_month_list(length) {
    var month_list = new Array()

    for (i = length; i < 0; i++) {
        month_list.push(addMonths(i));
    }
    return month_list
}

// Chart.js
function get_chart_config(last_six_month, data_list) {
    return {
        type: 'line',
        data: {
            labels: last_six_month,
            datasets: [{
                label: "My First dataset",
                backgroundColor: window.chartColors.red,
                borderColor: window.chartColors.red,
                data: data_list,
                fill: false,
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
                        suggestedMin: 10,
                        suggestedMax: 100
                    }
                }]
            }
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
