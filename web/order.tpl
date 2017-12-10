<!doctype html>
<html>
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <link rel="stylesheet" href="/incl/css/order.css" />
    <title>Panta</title>
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
        <form>
            <h3>Upplýsingar um leigjanda</h3>
            <input type="text" name="fullName"/>
            <input type="tel" name="phone" min="7" max="7"/>
            <input type="email" name="email"/>
            <input type="text" name="nationality" />
            <input type="number" name="driversLicense" min="7"/>
            <h3>Upplýsingar um leigu</h3>
            <select name="carSelect">
                % for car in cars:
                <option>{{str(car[1]) + str(car[2])}}</option>
                % end
            </select>
            <input type="date" name="startDate" />
            <input type="date" name="endDate" />
        </form>
    </main>
</body>
</html>