window.onload = function() {
    var ctx = document.getElementById("commit-canvas").getContext("2d");
    var state = document.getElementById("state-canvas").getContext("2d");
    window.myLine = new Chart(ctx, config);
    window.myLine = new Chart(state, config);
};

document.addEventListener("DOMContentLoaded", function (event) {
    navbarFixedTopAnimation();
});

document.addEventListener("DOMContentLoaded", function (event) {
    navActivePage();
    scrollRevelation('.reveal');
});
