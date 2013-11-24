(function () {
    function init() {
        var date = new Date();
        var month = date.getMonth() + 1;
        var year = date.getFullYear();
        Calendar(month, year);
    }
    window.addEventListener('load', init, false);
})();

Calendar = function (month, year) {
    var events = [];
    bindAllListeners();
    changeMonth(year, month);
    
    function changeMonth(year, month) {
        prepareView(year, month);
        removeAllMarks(); // borramos las descripciones anteriores y esperamos por los datos
        clearDescription();
        showLoading();
        
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange=function() {
            if (xhr.readyState==4) {
                switch (xhr.status) {
                    case 200: // OK!
                        response = JSON.parse(xhr.responseText);
                        markDays(response);
                    break;
                    case 404: // Error: 404 - Resource not found!
                        alert("Resource not found!");
                    break;
                    default: // Error: Unknown!
                }
            }
       }
       xhr.open('GET', 'http://localhost:8080/cgi-bin/month.py?year=' + year + '&month=' + month, true);
       xhr.send();
    }
    
    function bindAllListeners() {
        document.querySelector("#atras").addEventListener('click', onPrevMonth, false);
        document.querySelector("#adelante").addEventListener('click', onNextMonth, false);
        var days = document.querySelectorAll(".day");
        for (i=0; i < days.length; i++)
           days[i].addEventListener('click', onClickDay, false);
    }
    
    function removeAllMarks() {
        var placeHolder = document.querySelectorAll(".day-content");
        var day = document.querySelectorAll(".day");
        for (i=0; i < placeHolder.length; i++) {
            placeHolder[i].innerHTML = "";
            day[i].classList.remove("marked");
        }
    }
    
    function markDays(data) {
        //[[day, description, [tags]]]
        events = data;
        for (i=0; i < data.length; i++) {
            document.querySelector("#day" + data[i][0] + " .day-content").innerHTML += data[i][2][0] + " ";
            document.querySelector("#day" + data[i][0]).classList.add("marked");
        }
        
        hideLoading();
    }
    
    function onNextMonth() {
        if (month == 12) {
            month = 1;
            year++;
        }
        else
            month++;
        changeMonth(year, month);
    }
    
    function onPrevMonth() {
        if (month == 1) {
            month = 12;
            year--;
        }
        else
            month--;
        changeMonth(year, month);
    }
    
    function onClickDay() {
        clearDescription();
        var day = parseInt(this.firstElementChild.innerHTML);
        for (i=0; i < events.length; i++) {
            if (parseInt(events[i][0]) == day) {
                var span = document.createElement("li");
                span.appendChild(document.createTextNode(events[i][1] + " - " + events[i][2]));
                document.querySelector("#event-description").appendChild(span);
            }
        }
    }
    
    function prepareView(year, month) {
        // asignar número de dias del mes
        var days = daysInMonth(month, year);
        for (i=29; i<=31; i++) {
            if (days >= i)
                document.querySelector("#day" + i).classList.remove("hidden");
            else
                document.querySelector("#day" + i).classList.add("hidden");
        }
        
        // colocamos el primer dia del mes bajo el dia de la semana correcto
        var firstDay = firstDayOfMonth(month, year);
        for (i=1; i<=6; i++) {
            if (i < firstDay)
                document.querySelector("#space" + i).classList.remove("hidden");
            else
                document.querySelector("#space" + i).classList.add("hidden");
        }
        
        document.querySelector("#month").innerHTML = getMonthName(month) + " " + year;
    }
    
    function daysInMonth(month, year) {
        return new Date(year, month, 0).getDate();
        /* NOTA: la funcion date recibe month 0-11 pero en este caso le pasamos el mes siguiente, 
        y con day 0 obtenemos el ultimo dia del mes anterior.*/
    }
    
    function firstDayOfMonth(month, year) {
		var day = new Date(year, month-1, 1).getDay();
		if (day == 0) day = 7;
		return day;
	} 
	
	function getMonthName(month) {
	    var monthNames = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];
	    return monthNames[month-1];
	}
	
	function showLoading () {
	    document.querySelector("img.loading").classList.remove("hidden");
	}
	
	function hideLoading () {
	    document.querySelector("img.loading").classList.add("hidden");
	}
	
	function clearDescription() {
	    var desc = document.querySelector("#event-description")
	    while(desc.hasChildNodes()){
            desc.removeChild(desc.lastChild);
        }
	}
}
