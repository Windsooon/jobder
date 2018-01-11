function get_user_data(url, token, user_name) {
    var query = `query {` + 
        'user(login: "' + user_name + '") {' +
          `name
          avatarUrl
          location
          websiteUrl
          email
          bio
          repositories(first:54, orderBy: {direction: DESC, field: STARGAZERS}) {
              edges {
                  node {
                      name
                      description
                      createdAt
                      homepageUrl
                      url
                      nameWithOwner
                      stargazers {
                          totalCount
                      }
                      projectsUrl
                      primaryLanguage {
                          name 
                      }
                  }     
              }
          }
          repositoriesContributedTo(first:54, contributionTypes:[COMMIT,], orderBy: {direction: DESC, field: STARGAZERS}) {
			  edges {
                  node {
                      name 
                      description
                      createdAt
                      homepageUrl
                      url
                      nameWithOwner
                      stargazers {
                          totalCount
                      }
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
            
            update_repo($(".repo-class"), data.repositories.edges);
            update_repo($(".contributed-class"), data.repositoriesContributedTo.edges);

            update_blog(data);
            update_slider($('.repo-class'));
            update_slider($('.contributed-class'));
        },
        error: function() {
            alert("You may reach rate limit, please try again later");
        }
    }); 
}

function update_blog(data) {
    if (!$("#user-blog-a").text()) {
        $("#user-blog-a").text(data.websiteUrl);
    }
}

function update_repo(container, data) {
    $.each(data, function(i, item) {
        var $wrapper_div = $("<div />", {
            "class": "wrapper-div",
        });
        var $wrapper_border = $("<div />", {
            "class": "wrapper-border",
        });
        var $wrapper_span = $("<span />", {
            "class": "wrapper-span",
        });
        var $inside_span = $("<span />", {
            "class": "inside-span",
        });
        var $inside_a = $("<a />", {
            "class": "inside-a",
            "text": item.node.name,
            "href": item.node.url,
            "target": "_blank"
        });
        var $content_p = $("<p />", {
            "class": "content-p",
            "text": item.node.description || "None"
        });
        var $content_star = $("<span />", {
            "class": "content-star",
            "text": "     " + item.node.stargazers.totalCount,
        });
        var $star_icon = $("<i />", {
            "class": "fa fa-star star-icon",
            "aria-hidden": "true",
        });

        $wrapper_div.append($wrapper_border);
        $wrapper_border.append($wrapper_span);
        $wrapper_span.append($inside_span);
        $inside_span.append($inside_a);
        $wrapper_span.append($content_p);

        if (item.node.primaryLanguage) {
            var $content_language = $("<span />", {
                "class": "content-lan",
                "text": item.node.primaryLanguage.name
            });
            $wrapper_span.append($content_language);
        }
        $star_icon.append($content_star);
        $wrapper_span.append($star_icon);
        container.append($wrapper_div);
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
    var fork_sta = get_stars_count(data);
    window.myLine = new Chart(ctx, get_h_chart_config(languages_sta, 
        "horizontalBar", [0, 30], "Most Fluent Language"));
    window.myLine = new Chart(state, get_h_chart_config(fork_sta,
        "bar", [0, 30], "Star Count"));
};


function get_stars_count(data) {
    var fork_array = ["<100 stars", "100-500 stars", ">1000 stars"];
    var own_array = [0, 0, 0];
    var contribute_array = [0, 0, 0];
    $.each(data.repositories.edges, function(i, item) {
        if (item.node.stargazers.totalCount < 100) {

            own_array[0] += 1;
        }
        else if (item.node.stargazers.totalCount < 500) {
            own_array[1] += 1;
        }
        else {
            own_array[2] += 1;
        }
    });
    $.each(data.repositoriesContributedTo.edges, function(i, item) {
        if (item.node.stargazers.totalCount < 100) {
            contribute_array[0] += 1;
        }
        else if (item.node.stargazers.totalCount < 500) {
            contribute_array[1] += 1;
        }
        else {
            contribute_array[2] += 1;
        }
    });
    return [fork_array, own_array, contribute_array]
}

function get_repo_create(data) {
    languages_array = new Array();
    own_array = new Array();
    $.each(data.repositories.edges, function(i, item) {
        if(item.node.primaryLanguage && item.node.primaryLanguage.name != "HTML")  {
            if (languages_array.indexOf(item.node.primaryLanguage.name) == -1) {
                languages_array.push(item.node.primaryLanguage.name);
                own_array.push(1);
            }
            else {
                own_array[languages_array.indexOf(item.node.primaryLanguage.name)] += 1
            }
        }
    });
    contribute_array = Array.from(Array(languages_array.length), () => 0)
    $.each(data.repositoriesContributedTo.edges, function(i, item) {
        if(item.node.primaryLanguage && item.node.primaryLanguage.name != "HTML")  {
            if (languages_array.indexOf(item.node.primaryLanguage.name) == -1) {
                languages_array.push(item.node.primaryLanguage.name);
                contribute_array.push(1);
            }
            else {
                contribute_array[languages_array.indexOf(item.node.primaryLanguage.name)] += 1
            }
        }
    });
    return [languages_array, own_array, contribute_array]
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
function get_h_chart_config(data_list, type, suggest, title) {
    return {
        type: type,
        data: {
            labels: data_list[0],
            datasets: [
                {
                    label: "created",
                    backgroundColor: window.chartColors.red,
                    data: data_list[1],
                    fill: false,
                },
                {
                    label: "contributed_to",
                    backgroundColor: window.chartColors.blue,
                    data: data_list[2],
                    fill: false,
                }
            ]
        },
        options: {
            responsive: true,
            legend: {
                position: 'right',
            },
            title:{
                display:true,
                text: title,
                fontSize: 20,
                fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
                fontColor: '#555',
                fontStyle: 'normal',
            },
            scales: {
                yAxes: [{
                    ticks: {
                        suggestedMin: suggest[0],
                        suggestedMax: suggest[1]
                    },
                }],
            }
        }
    }
};

function update_slider(container) {
    container.slick({
        dots: true,
        slidesPerRow: 3,
        rows: 2,
        responsive: [
          {
            breakpoint: 1024,
            settings: {
              slidesToShow: 3,
              slidesToScroll: 3,
              infinite: true,
              dots: true
            }
          },
          {
            breakpoint: 600,
            settings: {
              slidesToShow: 1,
              slidesToScroll: 1
            }
          },
          {
            breakpoint: 480,
            settings: {
              slidesToShow: 1,
              slidesToScroll: 1
            }
          }
        ]
    });
}
