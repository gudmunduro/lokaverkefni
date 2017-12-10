<!doctype html>
<html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <link rel="stylesheet" type="text/css" href="incl/css/car_fleet.css">
		<script defer src="https://use.fontawesome.com/releases/v5.0.1/js/all.js"></script>
		<script src="/incl/script/API.js"></script>
		<script src="/incl/script/CarInfoView.js"></script>
		<title>Bílafloti</title>
    </head>
    <body>
        <header>
            <h1>G<p>&</p>H bílaleiga</h1>
            <ul>
                <li>
                    <a class="nav_underline" href="./">Heim</a>
                </li>
                <li>
                    <a class="nav_underline" href="./car_fleet">Bílafloti</a>
                </li>
                <li>
                    <a class="nav_underline" href="./order">Panta</a>
                </li>
            </ul>
        </header>
        <main>
            <div class="carList">
                % for car in cars:
				<div>
                    <section class="img">
                        <img src="incl/imgs/{{ str(car[12])}}">
                    </section>
                    <section class="info">
                        <h2>{{ str(car[4]) + " " + str(car[5]) }}</h2>
                        <p>Hestöfl: {{ str(car[7]) }}</p>
                        <p>Árgerð: {{ str(car[6]) }}</p>
                        <p>Drif: {{ str(car[9]) }}</p>
                        <p>Eldsneyti: {{ str(car[11]) }}</p>
                        <a onclick="showCarInfoView({{ str(car[0]) }})" class="moreInfo">Skoða nánar</a>
                        <a class="order">Panta</a>
                    </section>
                </div>
				% end
            </div>
        </main>
    </body>
</html>