var ItemsVue = new Vue({
    el: '#Itemlist',
    data: {
        items: []
    },
    created: function () {
        var self = this;
        $.ajax({
            url: '/items',
            method: 'GET',
            success: function (data) {
                self.items = data;
            },
            error: function (error) {
                console.log(error);
            }
        });
    }
});
