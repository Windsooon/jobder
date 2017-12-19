window.onload = function() {
    var ctx = document.getElementById("canvas").getContext("2d");
    window.myLine = new Chart(ctx, config);
};

document.addEventListener("DOMContentLoaded", function (event) {
    navbarFixedTopAnimation();
});

document.addEventListener("DOMContentLoaded", function (event) {
    navActivePage();
    scrollRevelation('.reveal');
});
