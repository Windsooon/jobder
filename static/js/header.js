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
        beforeSend:function(xhr, settings) {
            $("#find-match-btn").prop("disabled", true);
            $("#find-match-btn").text("Loading");
        },
        success: function(res) {
            window.location.href = base_url + "match/" + github_username + "/";
        },
        error: function(xhr, status, error) {
            alert("Please make sure Username is correct.");
        },
        complete: function() {
            $("#find-match-btn").prop("disabled", false);
            $("#find-match-btn").text("Find Your Match");
        }
    });
});

$("#profile-btn").on("click", function(){
    var github_username = $("#github-name").val();
    $.ajax({
        url: base_url + github_username + "/",
        type: "GET",
        beforeSend:function(xhr, settings) {
            $("#profile-btn").prop("disabled", true);
            $("#profile-btn").text("Loading");
        },
        success: function(res) {
            window.location.href = base_url + github_username + "/";
        },
        error: function(xhr, status, error) {
            alert("Please make sure Username is correct.");
        },
        complete: function() {
            $("#profile-btn").prop("disabled", false);
            $("#profile-btn").text("Profile");
        }
    });
});
