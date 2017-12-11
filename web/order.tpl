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
        <form method="post" action="/order">
            <h3>Upplýsingar um leigjanda</h3>
            <input placeholder="Fullt nafn" type="text" name="customer_fullname"/>
            <input placeholder="Símanúmer" type="tel" name="customer_phone" min="7" max="7"/>
            <input placeholder="Netfang" type="email" name="customer_email"/>
            <input placeholder="Þjóðerni" type="text" name="nationality" />
            <input placeholder="Ökunúmer" type="number" name="driver_id_nr" min="7"/>
            <h3>Upplýsingar um leigu</h3>
            <select name="car_id">
                % for car in cars:
                <option value={{ str(car[0]) }} {{ "selected" if selected is not None and selected == int(car[0]) else "" }}>{{str(car[4]) + " " + str(car[5] + " " + str(car[6]) )}}</option>
                % end
            </select>
            <input type="date" name="order_date" />
            <input type="date" name="return_date" />
			<h3>Kortaupplýsingar</h3>
			<input placeholder="Kortanúmer" type="text" name="card_number" />
			<input placeholder="Útrennslutími" type="text" name="card_exp_date" />
			<input placeholder="CVN" type="text" name="CVN" /> 
			<input type="submit" value="Panta" />
        </form>
		% if "order_status" in locals():
			<p class="orderStatusLabel" style="color: {{ "white" if order_status == True else "red" }};">{{"Pöntun tókst" if order_status == True else "Pöntun mistókst( " + error_msg + " )"}}</p>
		% end
    </main>
</body>
</html>