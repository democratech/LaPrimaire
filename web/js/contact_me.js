$(function() {
    $("input,textarea").jqBootstrapValidation({
        preventSubmit: true,
        submitError: function($form, event, errors) {
            // additional error messages or events
	    ga('send', 'event', 'signature', 'input_errors');
        },
        submitSuccess: function($form, event) {
            event.preventDefault(); // prevent default submit behaviour
            // get values from FORM
            var firstname = $("input#firstname").val();
            var lastname = $("input#lastname").val();
            var email = $("input#email").val();
            var zip = $("input#zip").val();
            var reason = $("textarea#message").val();
            // Check for white space in name for Success/Fail message
            if (firstname.indexOf(' ') >= 0) {
                firstname = name.split(' ').slice(0, -1).join(' ');
            }
	    ga('send', 'event', 'signature', 'signed');
            $.ajax({
                url: "http://prelaunch.democratech.co/api/petition/signFA",
                type: "POST",
                data: {
                    firstname: firstname,
                    lastname: lastname,
                    email: email,
		    postalcode: zip,
                    reason: reason
                },
                cache: false,
                success: function(e) {
		    if (e.result=="success") {
			    // Success message
			    $("#portfolioModal1").modal('show');
			    ga('send', 'event', 'signature', 'success');
		    } else if (e.result=="failure") {
			    // Success message mais on affiche quand meme la popup de success
			    $("#portfolioModal1").modal('show');
			    ga('send', 'event', 'signature', 'success');
			    ga('send', 'exception', {'exDescription':'Change.org API error', 'exFatal':false});
		    }
                    //clear all fields
		    $('#contactForm').trigger("reset");
                },
                error: function(e) {
                    // Fail message
		    $("#portfolioModal2").modal('show');
		    ga('send', 'event', 'signature', 'fail');
                },
            })
        },
        filter: function() {
            return $(this).is(":visible");
        },
    });

    $("a[data-toggle=\"tab\"]").click(function(e) {
        e.preventDefault();
        $(this).tab("show");
    });
});
