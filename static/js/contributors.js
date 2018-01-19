$('#select-open-source').selectize({
    valueField: 'id',
    labelField: 'name',
    searchField: 'name',
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
                (item.name ? '<span class="repo-name">' + escape(item.name) + '</span>' : '') + 
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
        repos = removeFunction(repos, 'id', data.id);
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

function set_up_contributors(container, data) {

    <div class="contri-row row">
      <div class="col-xs-10 col-xs-offset-1 col-md-8 col-md-offset-2">
        <h2 id="job-details">Contributors List</h2>
      </div>
    </div>
    var $contri_row_div = $("<div />", {
        "class": "contri-row row"
    });
    var $contri_col = $("<div />", {
        "class": "col-xs-10 col-xs-offset-1 col-md-8 col-md-offset-2"
    });
    var $contri_h2 = $("<h2 />", {
        "text": "Contributors List",
    });
    container.append($contri_row_div);
    $contri_row_div.append($contri_col);
    $contri_col.append($contri_h2);

    $.each(data, function(key, value) {
        console.log(key, value);
    });
}

$(document).ready(function(){
    check_repo($(".search-btn"), ".repo-name");
    $(".search-btn").on("click", function(){
        var csrftoken = getCookie("csrftoken");
        $.ajax({
            url: base_url + "repo-search/?repo_id=" + 
                $(".selectize-input").children().attr("data-value"),
            type: 'GET',
            beforeSend:function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                } 
            },
            error: function() {
            },
            success: function(res) {
                if (res.data.length > 0) {
                    set_up_contributors(res.data);
                }
                else {
                    set_up_empty(); 
                }
            }
        });
    });
});

