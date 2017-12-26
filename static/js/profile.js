function get_user_data(url, token, user_name) {
    var query = `query {` + 
        'user(login: "' + user_name + '") {' +
          `name
          avatarUrl
          location
          email
          bio
          repositories(first:50, orderBy: {direction: DESC, field: STARGAZERS}) {
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
          repositoriesContributedTo(first:50, orderBy: {direction: DESC, field: STARGAZERS}) {
			  edges {
                  node {
                      name 
                      description
                      createdAt
                      homepageUrl
                      nameWithOwner
                      forkCount
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
    // first sta
    var languages_sta = get_repo_create(data);
    // second sta
    var fork_sta = get_fork_count(data);
    window.myLine = new Chart(ctx, get_chart_config(languages_sta[0],
        languages_sta[1], "horizontalBar", [0, 30], "rgb(54, 162, 235)"));
    window.myLine = new Chart(state, get_chart_config(fork_sta[0],
        fork_sta[1], "bar", [0, 10], "rgb(255, 159, 64)"));
};


function get_fork_count(data) {
    var fork_array = ["<100", "100-500", ">1000"];
    var count_array = [0, 0, 0];
    $.each(data.repositoriesContributedTo.edges, function(i, item) {
        if (item.node.forkCount < 100) {
            count_array[0] += 1;
        }
        else if (item.node.forkCount < 500) {
            count_array[1] += 1;
        }
        else {
            count_array[2] += 1;
        }
    });
    return [fork_array, count_array]
}

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
function get_chart_config(label_list, data_list, type, suggest, color) {
    return {
        type: type,
        data: {
            labels: label_list,
            datasets: [{
                label: "count",
                backgroundColor: color,
                borderColor: color,
                data: data_list,
                fill: false,
            }]
        },
        options: {
            responsive: true,
            title:{
                display:true,
                text:"Top 50 Starred Repos's Language"
            },
            scales: {
                yAxes: [{
                    ticks: {
                        suggestedMin: suggest[0],
                        suggestedMax: suggest[1]
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
