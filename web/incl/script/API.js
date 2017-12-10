
var API = {

    cars: function (onLoad) {
        var rq = new XMLHttpRequest()
        rq.open("get", "/api/cars", true)
        rq.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        rq.onload = function () {
            var data = JSON.parse(rq.responseText)
            onLoad(data)
        }
        rq.send()
    },

    carInfo: function (id, onLoad) {
        var rq = new XMLHttpRequest()
        rq.open("get", "/api/car/" + id, true)
        rq.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        rq.onload = function () {
            console.log(rq.responseText)
            var data = JSON.parse(rq.responseText)
            onLoad(data)
        }
        rq.send()
    }

}