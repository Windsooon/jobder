function get_user_data(url, token, user_name) {
    var query = `query {` + 
        'user(login: "' + user_name + '") {' +
          `name
          avatarUrl
          location
          email
          bio
          repositories(first:40, orderBy: {direction: DESC, field: CREATED_AT}) {
              edges {
                  node {
                      name
                      description
                      createdAt
                      homepageUrl
                      nameWithOwner
                      projectsUrl
                      url
                      primaryLanguage {
                        name 
                      }
                  }     
              }
          }
          repositoriesContributedTo(first:18, orderBy: {direction: DESC, field: CREATED_AT}) {
			  edges {
                  node {
                      name 
                      description
                      createdAt
                      homepageUrl
                      nameWithOwner
                      projectsUrl
                      url
                      primaryLanguage {
                        name 
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
		success: function(data){
            data = data.data.user;
            update_profile(data);
            update_chart(data);
        },
        error: function() {
            alert("You may reach rate limit, please try again later");
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
    var languages_sta = get_repo_create(data);
    window.myLine = new Chart(ctx, get_chart_config(languages_sta[0], languages_sta[1]));
};


function get_repo_create(data) {
    languages_array = new Array();
    count_array = new Array();
    $.each(data.repositories.edges, function(i, item) {
        if(item.node.primaryLanguage && item.node.primaryLanguage.name != "HTML")  {
            if (languages_array.indexOf(item.node.primaryLanguage.name) == -1) {
                languages_array.push(item.node.primaryLanguage.name);
                count_array.push(1);
            }
            else {
                count_array[languages_array.indexOf(item.node.primaryLanguage.name)] += 1
            }
        }
    });
    return [languages_array, count_array]
}

// return last 6 month list
function get_month_list(length) {
    var month_list = new Array()

    for (i = length; i < 0; i++) {
        month_list.push(addMonths(i));
    }
    return month_list
}

function addMonths(index) {
  var date = new Date()
  date.setMonth(date.getMonth() + index);
  locale = "en-us";
  return date.toLocaleString(locale, { month: "long" });
}

// Chart.js
function get_chart_config(label_list, data_list) {
    return {
        // type: 'line',
        type: 'horizontalBar',
        data: {
            labels: label_list,
            datasets: [{
                label: "count",
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
                text:'Primary Language'
            },
            scales: {
                yAxes: [{
                    ticks: {
                        suggestedMin: 0,
                        suggestedMax: 20
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
