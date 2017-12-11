
var currentCarInfoView = null;
var currentTimer = null;

class CarInfoView {

    constructor(carId) {
        this.mainDiv = document.createElement("div");
        this.mainDiv.className = "carInfo";
        this.mainDiv.style.transform = "translateY(-400px)";
        this.mainDiv.style.opacity = "0";
        this.hiddenValue = true;

        // loading
        this.loadingLabel = document.createElement("h1");

        this.loadingLabel.className = "loading";
        this.loadingLabel.innerHTML = "Loading...";

        this.mainDiv.appendChild(this.loadingLabel);


        // img
        this.imgSection = document.createElement("section");
        this.imgView = document.createElement("img");

        this.imgSection.className = "img";

        this.imgSection.appendChild(this.imgView)


        // info
        this.infoSection = document.createElement("section");
        this.title = document.createElement("h2");
        this.productionYearLabel = document.createElement("p");
        this.horsepowerLabel = document.createElement("p");
        this.fuelConsumptionLabel = document.createElement("p");
        this.driveLabel = document.createElement("p");
        this.fuelTypeLabel = document.createElement("p");

        this.infoSection.className = "info";
        this.title.className = "title";
        this.productionYearLabel.className = "label";
        this.horsepowerLabel.className = "label";
        this.fuelConsumptionLabel.className = "label";
        this.driveLabel.className = "label";
        this.fuelTypeLabel.className = "label";

        this.infoSection.appendChild(this.title);
        this.infoSection.appendChild(this.productionYearLabel);
        this.infoSection.appendChild(this.horsepowerLabel);
        this.infoSection.appendChild(this.fuelConsumptionLabel);
        this.infoSection.appendChild(this.driveLabel);
        this.infoSection.appendChild(this.fuelTypeLabel);


        // actions
        this.actionsSection = document.createElement("section");
        this.orderButton = document.createElement("a");

        this.actionsSection.className = "actions";
        this.orderButton.className = "order";
        this.orderButton.innerHTML = "Panta";
        this.orderButton.href = "/order?selected=" + carId;

        this.actionsSection.appendChild(this.orderButton);


        // close button
        this.closeButton = document.createElement("a");
        var closeButtonUpArrow = document.createElement("i");
        var closeButtonText = document.createElement("p");

        this.closeButton.className = "closeButton";
        closeButtonUpArrow.className = "fas fa-angle-double-up fa-w-10 fa-3x";
        closeButtonText.innerHTML = "Loka";

        this.closeButton.appendChild(closeButtonUpArrow);
        this.closeButton.appendChild(closeButtonText);


        var carInfoViewInstance = this; // for use in onclick and car info onLoad()
        this.closeButton.onclick = function () {
            carInfoViewInstance.hidden = true;
        }


        API.carInfo(carId, function (data) {
            carInfoViewInstance.title.innerHTML = data[4] + " " + data[5];
            carInfoViewInstance.productionYearLabel.innerHTML = "Árgerð: " + data[6];
            carInfoViewInstance.horsepowerLabel.innerHTML = "Hestöfl: " + data[7];
            carInfoViewInstance.fuelConsumptionLabel.innerHTML = "Eyðsla: " + data[8];
            carInfoViewInstance.driveLabel.innerHTML = "Drif: " + data[9];
            carInfoViewInstance.fuelTypeLabel.innerHTML = "Eldsneyti: " + data[11];
            carInfoViewInstance.imgView.src = "/incl/imgs/" + data[12];

            carInfoViewInstance.mainDiv.removeChild(carInfoViewInstance.loadingLabel);

            carInfoViewInstance.mainDiv.appendChild(carInfoViewInstance.imgSection);
            carInfoViewInstance.mainDiv.appendChild(carInfoViewInstance.infoSection);
            carInfoViewInstance.mainDiv.appendChild(carInfoViewInstance.actionsSection);
            carInfoViewInstance.mainDiv.appendChild(carInfoViewInstance.closeButton);
        });
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
    function createNew()
    {
        currentCarInfoView = new CarInfoView(carId);
        currentCarInfoView.hidden = false;
        currentTimer = null;
    }
    if (currentCarInfoView != null && currentCarInfoView.hidden == false)
    {
        if (currentTimer != null)
        {
            clearTimeout(currentTimer);
        }
        currentCarInfoView.hidden = true;
        currentTimer = setTimeout(createNew, 300);
        return;
    }
    if (currentTimer != null)
    {
        clearTimeout(currentTimer);
    }
    createNew();
}