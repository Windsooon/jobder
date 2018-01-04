$('#select-open-source').selectize({
    delimiter: ',',
    persist: false,
    create: function(input) {
        return {
            value: input,
            text: input
        }
    }
});

$( document ).ready(function() {
    $.validator.addMethod(
        "regex_name",
        function(value, element, regexp) {
            var re = new RegExp(regexp);
            return this.optional(element) || re.test(value);
        },
        "Project name can't contain <, > or /"
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
            company_des: {
                required: "Please enter your company's details.",
                minlength: jQuery.validator.format("Please Enter at least {0} characters."),
                maxlength: jQuery.validator.format("Please Enter up to {0} characters."),
            },
        },
        submitHandler: function(form) {
            if (!$('#select-open-source').selectize()[0].selectize.getValue()) {
                alert("Please enter which project's contributer you are looking for"); 
                return false;
            }
            $.ajax({
                url: "/api/settings/" + $("#user-id").val() + "/",
                type: "PUT",
                datatype: "json",
                data:  ({"blog": $("#blog").val(),"linkedin": $("#linkedin").val(), 
                    "location": $("#location-select option:selected").val(), 
                    "visiable": visiable}),
                beforeSend:function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    } 
                },
                success: function(xhr) {
                    console.log("Successed");
                },
            });
        },
    });
});
