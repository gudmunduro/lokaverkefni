
var API = {

    loadCars: function (onLoad) {
        var rq = new XMLHttpRequest()
        rq.open("post", "/api/cars", true)
        rq.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        rq.onload = function () {
            var data = JSON.parse(rq.responseText)
            if (data.success == 1)
            {
                onLoad(data)
            }
        }
        rq.send()
    }

}