
// iter all checked checkbox antiflag
$('#antiflag').on("change", "input[type='checkbox']", function () {
	var res = 0;
	$.each($('#antiflag input:checkbox:checked').serializeArray(), function(_, field) {
		res += (1 << field.value);
		// console.log(field.name+" "+field.value+" "+res);
	});
	$("#antiflag-result").val(res);
	$("#antiflag-reverse").val(res);
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
});

// prevent form submit with ENTER
$('#antiflag').on('keyup keypress', function(e) {
	var keyCode = e.keyCode || e.which;
	if (keyCode === 13) {
		e.preventDefault();
		return false;
	}
});

