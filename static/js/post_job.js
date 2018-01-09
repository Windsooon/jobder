$('#select-open-source').selectize({
    valueField: 'url',
    labelField: 'name',
    searchField: 'name',
    persist: false,
    options: [],
    create: false,
    render: {
        item: function(item, escape) {
            return '<div>' +
                (item.name ? '<span class="repo-name">' + escape(item.name) + '</span>' : '') + 
                (item.username ? '<span class="author">' + "  by " + escape(item.username) + '</span>' : '') +
            '</div>';
        },
        option: function(item, escape) {
            return '<div>' +
                '<span class="title">' +
                    '<span class="repo-name"><i class="icon ' + (item.fork ? 'fork' : 'source') + '"></i>' + escape(item.name) + ' ' + '</span>' +
                    '<span class="by">' + escape(item.username) + '</span>' +
                '</span>' +
                '<span class="description">' + escape(item.description) + '</span>' +
                '<ul class="meta">' +
                    (item.language ? '<li class="language">' + escape(item.language) + '</li>' : '') +
                    '<li class="watchers"><span>' + escape(item.watchers) + '</span> stars</li>' +
                    '<li class="forks"><span>' + escape(item.forks) + '</span> forks</li>' +
                '</ul>' +
            '</div>';
        }
    },
    score: function(search) {
        var score = this.getScoreFunction(search);
        return function(item) {
            return score(item) * (1 + Math.min(item.watchers / 100, 1));
        };
    },
    onItemAdd: function (value, item) {
        // var repo_name = value.split("https://github.com/");
        // $("#front-btn-w").attr("href", host + "/thanks/" + repo_name[1] + "/");
        // $("#front-btn-b").attr("href", host + "/list/" + repo_name[1] + "/");
    },
    load: function(query, callback) {
        if (!query.length) return callback();
        $.ajax({
            url: 'https://api.github.com/legacy/repos/search/' + encodeURIComponent(query),
            type: 'GET',
            error: function() {
                callback();
            },
            success: function(res) {
                callback(res.repositories.slice(0, 20));
            }
        });
    }
});

$( document ).ready(function() {
    $.validator.addMethod(
        "regex_name",
        function(value, element, regexp) {
            var re = new RegExp(regexp);
            return this.optional(element) || re.test(value);
        },
        "Project name can't contain <, >"
    );
    var validator = $("#job-form").validate({
        rules: {
            job_title: {
                required: true,
                minlength: 5,
                maxlength: 50,
                regex_name: /^((?!<|>).)*$/
            },
            job_looking: {
                required: true,
                minlength: 20,
                maxlength: 600,
                regex_name: /^((?!<|>).)*$/
            },
            company: {
                required: true,
                minlength: 3,
                maxlength: 50,
                regex_name: /^((?!<|>).)*$/
            },
            location: {
                required: true,
                minlength: 3,
                maxlength: 50,
                regex_name: /^((?!<|>).)*$/
            },
            company_des: {
                required: true,
                minlength: 3,
                maxlength: 600,
                regex_name: /^((?!<|>).)*$/
            }
        },
        messages: {
            job_title: {
                required: "Please enter a job title.",
                minlength: jQuery.validator.format("Please Enter at least {0} characters."),
                maxlength: jQuery.validator.format("Please Enter up to {0} characters."),
            },
            job_looking: {
                required: "Please enter the job details.",
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
            company_des: {
                required: "Please enter your company's details.",
                minlength: jQuery.validator.format("Please Enter at least {0} characters."),
                maxlength: jQuery.validator.format("Please Enter up to {0} characters."),
            },
        },
        submitHandler: function(form) {
            var csrftoken = getCookie("csrftoken");
            if (!$('#select-open-source').selectize()[0].selectize.getValue()) {
                alert("Please enter which project's contributer you are looking for"); 
                return false;
            }
            $.ajax({
                url: "/api/post/",
                type: "POST",
                contentType: "application/json",
                datatype: "json",
                data:  JSON.stringify({
                    "user": $("#user-id").val(),
                    "title": $("#job_title").val(),"job_des": $("#job-looking").val(), 
                    "repo": $('#select-open-source').selectize()[0].selectize.getValue(),
                    "onsite": $("#location-select option:selected").val(), 
                    "salary": $("#salary-select").val(),
                    "company_name": $("#company").val(),
                    "location": $("#location").val(),
                    "company_des": $("#company-des").val(),
                    "apply": $("#apply").val(),
                }),
                beforeSend:function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    } 
                },
                success: function(data) {
                    console.log(data);  
                },
                error: function() {
                    alert("Something went wrong, please email to contact@jobder.net");
                }
            });
        },
    });
});
