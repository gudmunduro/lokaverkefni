<!doctype html>
<html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <link rel="stylesheet" type="text/css" href="incl/css/car_fleet.css">
		<script src="incl/script/CarInfoView.js"></script>
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
                        <img src="incl/imgs/agerars-temp.jpg">
                    </section>
                    <section class="info">
                        <h2>{{ str(car[1]) + " " + str(car[2]) }}</h2>
                        <p>Hestöfl: {{ str(car[4]) }}</p>
                        <p>Árgerð: {{ str(car[3]) }}</p>
                        <p>Drif: {{ str(car[6]) }}</p>
                        <p>Eldsneyti: {{ str(car[8]) }}</p>
                        <a class="moreInfo">Skoða nánar</a>
                        <a class="order">Panta</a>
                    </section>
                </div>
				% end
            </div>
        </main>
    </body>
</html>