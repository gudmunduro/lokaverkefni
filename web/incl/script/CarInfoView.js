
class CarInfoView {

    constructor(carId) {
        this.mainDiv = document.createElement("div");
        this.mainDiv.className = "carInfo";
        this.mainDiv.style.transform = "translateY(-400px)";
        this.mainDiv.style.opacity = "0";
        this.hiddenValue = true;

        var carInfoViewInstance = this; // for use in onclick
        this.mainDiv.onclick = function () {
            carInfoViewInstance.hidden = true;
        }
    }

    get hidden() {
        return this.hiddenValue;
    }

    set hidden(value) {
        if (value == this.hiddenValue) return;
        if (value) {
            this.mainDiv.style.transition = "transform 0.3s ease-in, opacity 0.3s ease-in";
            this.mainDiv.style.transform = "translateY(-400px)";
            this.mainDiv.style.opacity = "0";
            var mainDiv = this.mainDiv;
            setTimeout(function () {
                document.body.removeChild(mainDiv);
                mainDiv.style.transition = "";
            }, 300)
        }
        else {
            document.body.appendChild(this.mainDiv);
            var mainDiv = this.mainDiv
            setTimeout(function () {
                mainDiv.style.transform = "translateY(0)";
                mainDiv.style.opacity = "1";
            }, 40)
        }
        this.hiddenValue = value;
    }

}


function showCarInfoView(carId) {
    var carInfoView = new CarInfoView(carId);
    carInfoView.hidden = false;
}