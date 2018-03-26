
// store get url parameters
$.urlParam = function(name){
    var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
    if (results==null){
       return null;
    }
    else{
       return decodeURI(results[1]) || 0;
    }
}

// function to update get parameters in url without refresh
var updateQueryStringParam = function (key, value) {
    var baseUrl = [location.protocol, '//', location.host, location.pathname].join(''),
        urlQueryString = document.location.search,
        newParam = key + '=' + value,
        params = '?' + newParam;

    // If the "search" string exists, then build params from it
    if (urlQueryString) {
        keyRegex = new RegExp('([\?&])' + key + '[^&]*');

        // If param exists already, update it
        if (urlQueryString.match(keyRegex) !== null) {
            params = urlQueryString.replace(keyRegex, "$1" + newParam);
        } else { // Otherwise, add it to end of query string
            params = urlQueryString + '&' + newParam;
        }
    }
    window.history.replaceState({}, "", baseUrl + params);
};

// set antiflag value
$(document).ready(function () {
	$("#antiflag-result").val($.urlParam('antiflag'));
});

// iter all checked checkbox antiflag
$('#antiflag').on("change", "input[type='checkbox']", function () {
	var res = 0;
	$.each($('#antiflag input:checkbox:checked').serializeArray(), function(_, field) {
		res += (1 << field.value);
		// console.log(field.name+" "+field.value+" "+res);
	});
	$("#antiflag-result").val(res);
	$("#antiflag-reverse").val(res);
	// update antiflag url
	updateQueryStringParam("antiflag", $('#antiflag-reverse').val());
});

// antiflag reverse value
$('#antiflag').on("change paste keyup", "input[id='antiflag-reverse']", function (e) {
	var flag = $("#antiflag-reverse").val();
	$.each($('#antiflag input:checkbox').get().reverse(), function(_, field) {
		var $field = $(field);
		var curflag = (1 << field.value);
		var hasflag = (flag & curflag) > 0;
		// console.log(field.name+" "+field.value+" "+curflag);
		if (hasflag)
			flag -= curflag;
		$field.prop('checked', hasflag);
	});
	$("#antiflag-result").val($('#antiflag-reverse').val());
	// update antiflag url
	updateQueryStringParam("antiflag", $('#antiflag-reverse').val());
});

// prevent form submit with ENTER
$('#antiflag').on('keyup keypress', function(e) {
	var keyCode = e.keyCode || e.which;
	if (keyCode === 13) {
		e.preventDefault();
		return false;
	}
});

$("#antiflag-reset").click(function() {
	$("#antiflag-reverse").val("").change();
});

