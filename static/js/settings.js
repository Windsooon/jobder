$( document ).ready(function() {
   $.validator.addMethod(
        "regex_url",
        function(value, element, regexp) {
            var re = new RegExp(regexp);
            return this.optional(element) || re.test(value);
        },
        "Please enter a valid URL Address."
    );
    $.validator.addMethod(
        "regex_open_source",
        function(value, element, regexp) {
            var re = new RegExp(regexp);
            return this.optional(element) || re.test(value);
        },
        "Project name can't contain <, > or /"
    );
    var validator = $("#settings-form").validate({
        rules: {
            blog: {
                regex_url: /^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/
            },
            linkedin: {
                regex_url: /^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/
            },
            open_source: {
                regex_open_source: /^((?!<|>|\/).)*$/
            },
        },
        submitHandler: function(form) {
            var csrftoken = getCookie("csrftoken");
            if ($("#public-input").prop("checked")) {
                var visiable = 1;
            }
            else {
                var visiable = 0;
            }
            $.ajax({
                url: "/api/settings/" + $("#user-id").val() + "/",
                type: "PUT",
                datatype: "json",
                data:  ({"blog": $("#blog").val(),"linkedin": $("#linkedin").val(), 
                    "onsite": $("#location-select option:selected").val(), 
                    "visiable": visiable}),
                beforeSend:function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    } 
                },
                success: function(xhr) {
                    $(".save-setting").text("Saved");
                },
            });
        },
    });
});
