$('#select-open-source').selectize({
    valueField: 'id',
    labelField: 'name', searchField: 'name',
    sortField: [
        {
            field: 'stargazers_count',
            direction: 'desc'
        },
        {
            field: '$score'
        },
    ],
    options: [],
    create: false,
    render: {
        item: function(item, escape) {
            return '<div>' +
                (item.name ? '<span id="repo-name">' + escape(item.name) + '</span>' : '') + 
                (item.owner.login ? '<span class="author">' + '</span>' : '') +
            '</div>';
        },
        option: function(item, escape) {
            return '<div>' +
                '<span class="title">' +
                    '<span class="repo-name"><i class="icon ' + (item.fork ? 'fork' : 'source') + '"></i>' + escape(item.name) + ' ' + '</span>' +
                    '<span class="by">' + escape(item.owner.login) + '</span>' +
                '</span>' +
                '<span class="description">' + escape(item.description) + '</span>' +
                '<ul class="meta">' +
                    (item.language ? '<li class="language">' + escape(item.language) + '</li>' : '') +
                    '<li class="watchers"><span>' + escape(item.stargazers_count) + '</span> stars</li>' +
                '</ul>' +
            '</div>';
        }
    },
    onItemAdd: function (value, item) {
        var data_id = this.options[value].id;
    },
    onItemRemove: function (value) {
        var data = this.options[value];
    },
    load: function(query, callback) {
        if (!query.length) return callback();
        $.ajax({
            url: 'https://api.github.com/search/repositories?q=' + encodeURIComponent(query),
            type: 'GET',
            error: function() {
                callback();
            },
            success: function(res) {
                callback(res.items.slice(0, 20));
            }
        });
    }
});

function check_repo(btn, repo) {
    btn.on("click", function(){
        if ($(repo).length <= 0){
            alert("Please type in a repo first.");
            return false;
        }
    });
}

function set_up_empty() {
    var $contri_h3 = $("<h3 />", {
        "class": "contri-empty-h3 col-xs-12",
        "text": "One valid job post is required to view contributers."
    });
    $(".contri-col").append($contri_h3);
}

function set_up_number(container, length, repo) {
    if (length == 0) {
        var text = "0 " + repo + " contributor looking for job.";
    }
    if (length == 1) {
        var text = "1 " + repo + " contributor looking for job.";
    }
    else {
        var text = length + " " + repo + " contributors looking for job.";
    }
    var $contri_h2 = $("<h2 />", {
        "id": "contri-h2",
        "text": text,
    });
    container.append($contri_h2);
}

function set_up_contributors(container, data) {
    $.each(data, function(key, value) {
        var $contri_a = $("<a />", {
            "class": "contri-a col-sm-3 col-xs-6",
            "target": "_blank",
            "href": base_url + value["username"] + "/"
        });
        var $contri_div = $("<div />", {
            "class": "contri-inner-div",
        });
        var $contri_img = $("<img />", {
            "class": "contri-img",
            "src": value["avatar_url"]
        });
        var $contri_wrapper_div = $("<div />", {
            "class": "contri-wrapper-div",
        });
        var $contri_span = $("<span />", {
            "class": "contri-span",
            "text": value["username"]
        });
        $contri_a.append($contri_div);
        $contri_div.append($contri_img);
        $contri_div.append($contri_wrapper_div);
        $contri_wrapper_div.append($contri_span);
        container.append($contri_a);
    });
}

$(document).ready(function(){
    check_repo($(".search-btn"), ".repo-name");
    $(".search-btn").on("click", function(){
        var csrftoken = getCookie("csrftoken");
        $(".contri-col").empty();
        $.ajax({
            url: base_url + "repo-search/?repo_id=" + 
                $(".selectize-input").children().attr("data-value"),
            type: 'GET',
            beforeSend:function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                } 
            },
            error: function(xhr, status, error) {
                set_up_number(
                    $(".contri-col"), xhr.responseJSON.length, $("#repo-name").text());
                set_up_empty();
            },
            success: function(res) {
                $(".contri-col").empty(); 
                set_up_number($(".contri-col"), res.length, $("#repo-name").text());
                if (res.data.length >= 0) {
                    set_up_contributors($(".contri-col"), res.data);
                }
            }
        });
    });
});

