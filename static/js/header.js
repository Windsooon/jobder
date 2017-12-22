$(document).ready(function() {
    const token = $("#api-token").val(); 
    const url = "https://api.github.com/graphql"
    get_user_name(url, token);
});

function update_name(name) {
    $("#nav-user-name").text(name);
    $("#nav-user-name").append("<span class='caret'></span>");
}

function get_user_name(url, token) {
    var query = `query { viewer 
        { login 
          name
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
		success:function(data){
            data = data.data.viewer;
            update_name(data.name);
        }
    }); 
}

document.addEventListener("DOMContentLoaded", function (event) {
    navbarFixedTopAnimation();
});

document.addEventListener("DOMContentLoaded", function (event) {
    navActivePage();
    scrollRevelation('.reveal');
});
