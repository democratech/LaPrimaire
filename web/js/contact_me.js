$(function() {

    $("input,textarea").jqBootstrapValidation({
        preventSubmit: true,
        submitError: function($form, event, errors) {
            // additional error messages or events
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
            $.ajax({
                url: "http://prelaunch.democratech.co/api/petition/sign",
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

                // Analytics : apparaition popup confirmation
                ga('send', 'event', 'form', 'validation / ask to share', 'form_validated');
                
			    $('#contactForm').trigger("reset");
			    //$('#success').html("<div class='alert alert-success'>");
			    //$('#success > .alert-success').html("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;")
				//.append("</button>");
			    //$('#success > .alert-success')
				//.append("<strong>Merci pour votre soutien. </strong>");
			    //$('#success > .alert-success')
			//	.append('</div>');
		    } else if (e.result=="failure") {
			    // Fail message
			    $("#portfolioModal2").modal('show');
			    
                // Analytics : apparaition popup confirmation
                ga('send', 'event', 'form', 'error', 'form_error');

                //$('#success').html("<div class='alert alert-danger'>");
			    //$('#success > .alert-danger').html("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;")
				//.append("</button>");
			    //$('#success > .alert-danger').append("<strong>Desole " + firstname + ", il y a eu un probleme lors de la signature :( Merci de reessayer plus tard !");
			    //$('#success > .alert-danger').append('</div>');
		    }
                    //clear all fields
                },
                error: function(e) {
                    // Fail message
		       $("#portfolioModal2").modal('show');
                    /*$('#success').html("<div class='alert alert-danger'>");
                    $('#success > .alert-danger').html("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;")
                        .append("</button>");
                    $('#success > .alert-danger').append("<strong>Desole " + firstname + ", il y a eu un probleme lors de la signature :( Merci de reessayer plus tard !");
                    $('#success > .alert-danger').append('</div>');*/
                    //clear all fields
                    //$('#contactForm').trigger("reset");
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


/*When clicking on Full hide fail/success boxes */
$('#name').focus(function() {
    $('#success').html('');
});
