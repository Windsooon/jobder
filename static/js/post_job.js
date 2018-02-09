var repos = [];
function removeFunction(Objects,prop,valu){
    return Objects.filter(function (val){
        return val[prop] !== valu;
    });
}

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
        var data = this.options[value];
        repos.push({
            "id": data.id,
            "name": data.name,
            "owner_name": data.owner.login,
            "description": data.description,
            "html_url": data.html_url,
            "language": data.language,
            "stargazers_count": data.stargazers_count,
            }
        );
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

$(document).ready(function() {
    var toolbarOptions = [
          [{ 'list': 'bullet'}, 'code-block'],
      ];
    var job_editor = new Quill('#job-editor', {
        modules: {
            toolbar: toolbarOptions
        },
        theme: 'snow'
    });
    var company_editor = new Quill('#company-editor', {
        modules: {
            toolbar: toolbarOptions
        },
        theme: 'snow'
    });
    var validator = $(".job-form").validate({
        rules: {
            job_title: {
                required: true,
                minlength: 5,
                maxlength: 50,
            },
            salary: {
                required: true,
                minlength: 5,
                maxlength: 50,
            },
            company: {
                required: true,
                minlength: 3,
                maxlength: 50,
            },
            location: {
                required: true,
                minlength: 3,
                maxlength: 50,
            },
            website: {
                required: true,
                minlength: 8,
                maxlength: 256,
            },
            apply: {
                required: true,
                minlength: 3,
                maxlength: 1024,
            },
        },
        messages: {
            job_title: {
                required: "Please enter a job title.",
                minlength: jQuery.validator.format("Please Enter at least {0} characters."),
                maxlength: jQuery.validator.format("Please Enter up to {0} characters."),
            },
            salary: {
                required: "Please enter the salary range.",
                minlength: jQuery.validator.format("Please Enter at least {0} characters."),
                maxlength: jQuery.validator.format("Please Enter up to {0} characters."),
            },
            company: {
                required: "Please enter your company name.",
                minlength: jQuery.validator.format("Please Enter at least {0} characters."),
                maxlength: jQuery.validator.format("Please Enter up to {0} characters."),
            },
            location: {
                required: "Please enter your company location.",
                minlength: jQuery.validator.format("Please Enter at least {0} characters."),
                maxlength: jQuery.validator.format("Please Enter up to {0} characters."),
            },
            apply: {
                required: "Please enter apply url or email.",
                minlength: jQuery.validator.format("Please Enter at least {0} characters."),
                maxlength: jQuery.validator.format("Please Enter up to {0} characters."),
            },
            website: {
                required: "Please enter your company's website.",
                minlength: jQuery.validator.format("Please Enter at least {0} characters."),
                maxlength: jQuery.validator.format("Please Enter up to {0} characters."),
            },
        },
        submitHandler: function(form) {
            if (job_editor.getLength() < 21) {
                alert("Please tell us more about your job.");
                return false;
            }
            if (company_editor.getLength() < 21) {
                alert("Please tell us more about your company.");
                return false;
            }
            var csrftoken = getCookie("csrftoken");
            if (!$("#select-open-source").selectize()[0].selectize.getValue()) {
                alert("Please add tech stack your are using"); 
                return false;
            }
            $.ajax({
                url: "/api/post/",
                type: "POST",
                contentType: "application/json",
                datatype: "json",
                data:  JSON.stringify({
                    "user": $("#user-id").val(),
                    "title": $("#job_title").val().trim(),
                    "job_des": JSON.stringify(job_editor.getContents()),
                    "repos": repos,
                    "type": $("#onsite-select option:selected").val(), 
                    "visa": $("#visa-select option:selected").val(), 
                    "salary": $("#salary").val().trim(),
                    "company_name": $("#company").val().trim(),
                    "location": $("#location").val().trim(),
                    "website": $("#website").val().trim(),
                    "company_des": JSON.stringify(company_editor.getContents()),
                    "apply": $("#apply").val().trim(),
                }),
                beforeSend:function(xhr, settings) {
                    $("#preview-btn").prop("disabled", true);
                    $("#preview-btn").text("Loading");
                    if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    } 
                },
                success: function(data) {
                    window.location = base_url + "job/" + data.id + "/";
                },
                error: function() {
                    alert("Something went wrong, please email to contact@jobder.net");
                },
                complete: function() {
                    $("#preview-btn").prop("disabled", false);
                }
            });
        },
    });
});
