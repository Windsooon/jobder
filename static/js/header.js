document.addEventListener("DOMContentLoaded", function (event) {
    navbarFixedTopAnimation();
});

document.addEventListener("DOMContentLoaded", function (event) {
    navActivePage();
    scrollRevelation('.reveal');
});

$("#find-match-btn").on("click", function(){
    var github_username = $("#github-name").val();
    $.ajax({
        url: base_url + "match/" + github_username + "/",
        type: "GET",
        success: function(res) {
            window.location.href = base_url + "match/" + github_username + "/";
        },
        error: function(xhr, status, error) {
            console.log("error");
        },
    });
});
