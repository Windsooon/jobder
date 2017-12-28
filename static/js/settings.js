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
        "Please enter your open source project."
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
            console.log("success"); 
        },
    });
});
