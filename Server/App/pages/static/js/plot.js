
var django_url = "http://localhost:1337/";

$(document).ready(function(){
	var todayDate = new Date().toISOString().split("T")[0]; //set the max date to Today
	$("#dateTo").attr("max", todayDate);
	$("#dateFrom").attr("max", todayDate);
	$("button[name='nbDays']").click(fetchDays);
	$("button[name='rangeDays']").click(fetchRange);
});


function fetchDays() { //call to django backend when clicked, then plot fetched datas

	$("#msgInfo").attr("class","alert alert-info")
	$("#msgInfo").html("Fetching to Django backend at localhost:8000 ....");
	enableButtons(false);

	var nbDays = $("input[name='nbDays']").val();
	var formatted_url ="/?nbDays=" + nbDays;
	sendAjax(formatted_url);
  }

  function fetchRange(){

	$("#msgInfo").attr("class","alert alert-info")
	$("#msgInfo").html("Fetching to Django backend at localhost:8000 ....");
	enableButtons(false);

	var dateFrom = $("#dateFrom").val();
	var dateTo = $("#dateTo").val();
	var formatted_url = "/?dateFrom=" + dateFrom + "&dateTo=" + dateTo;
	sendAjax(formatted_url);


  }

  function enableButtons(state){
		$(".spinner-border").prop("hidden",state)
		$("button[name='nbDays']").prop("disabled",!state);
		$("button[name='rangeDays']").prop("disabled",!state);
	}


  function sendAjax(urlRequest){


	$.ajax({url: urlRequest, dataType: "json", success: function(result){
		$("#div1").append("\n Done !");
		console.log(result);
		if(jQuery.isEmptyObject(result)){
			$("#msgInfo").html("No data on this interval of time, please select wider");
			$("#msgInfo").attr("class","alert alert-danger")
			enableButtons(true);
			return false
		}
		$("#plotZone").css("display","inline");
		plot(result);

		$("#msgInfo").attr("class","alert alert-success")
		$("#msgInfo").html("Done !");
		enableButtons(true);

		}
	});

	return false;


  }
function plot(datas){

	var layout = {
	  font: { size: 18},
		autosize:true
	 };


	for(i in datas) { // Each sensors (e.g. pressure)
		x_data = [];
		y_data = [];
		console.log(i)
		layout["title"] = $("#"+$.escapeSelector(i)).attr("name");
		tempArray = Object.keys(datas[i]).map((key) => [key, datas[i][key]]); //Convert the json object unordered to json array
		tempArray.sort()
		//TODO
		// Unstable sort, the timestamp are string, a simple sort() is not suitable but temporaly enough here since they are all the same length

		for (x of tempArray) { // Each sensor data sample
			x_data.push(new Date(parseInt(x[0]))); // Each Timestamp
			y_data.push(x[1]); //Each value
		}
		var trace1 = {
			x: x_data,
			y: y_data
		};

		Plotly.plot(i.toString(), [trace1], layout,{responsive: true});
	}
	/*
	console.log(x_data);
	console.log(y_data);
	*/


}
