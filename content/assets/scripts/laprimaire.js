/*!
 * Start Bootstrap - Agency Bootstrap Theme (http://startbootstrap.com)
 * Code licensed under the Apache License v2.0.
 * For details, see http://www.apache.org/licenses/LICENSE-2.0.
 */

function createCookie(name,value) {
	var date = new Date();
	date.setTime(date.getTime()+(5*60*1000)); // 5 minutes
	var expires = "; expires="+date.toGMTString();
	document.cookie = name+"="+value+expires+"; path=/";
}

function readCookie(name) {
	var nameEQ = name + "=";
	var ca = document.cookie.split(';');
	for(var i=0;i < ca.length;i++) {
		var c = ca[i];
		while (c.charAt(0)==' ') c = c.substring(1,c.length);
		if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
	}
	return null;
}

function eraseCookie(name) {
	createCookie(name,"",-1);
}

$(document).ready(function(){
	/* Navbar submenu init */
	$('[data-submenu]').submenupicker();
	/* FAQ show/hide */
	$('.faq dd').hide(); // Hide all DDs inside .faqs
	$('.faq h4').hover(function(){$(this).addClass('hover')},function(){$(this).removeClass('hover')}).click(function(){ // Add class "hover" on dt when hover
		$(this).next().slideToggle('normal'); // Toggle dd when the respective dt is clicked
	}); 
	/* Crowdfunding footer */
	var oneDay = 24*60*60*1000; // hours*minutes*seconds*milliseconds
	var now = new Date();
	var firstDate = (new Date(2015,12,31)).getTime();
	var secondDate= (new Date(now.getFullYear(),now.getMonth()+1,now.getDate())).getTime();

	var diffDays = Math.round(Math.abs((firstDate - secondDate)/(oneDay)));
	amount=readCookie('amount_raised');
	supporteurs=readCookie('nb_supporters');
	if (amount==null) {
		$.get("https://democratech.co/api/v1/stripe/total", function( data ){
			amount=data['total'];
			supporteurs=data['nb_donateurs'];
			createCookie('amount_raised',amount);
			createCookie('nb_supporters',supporteurs);

			$('#fundraising_bar').goalProgress({
				goalAmount: 100000,
				currentAmount: amount,
				textBefore: '',
				textAfter: ' €'
			});
			$('#fundraising_figures').html(amount+" € dons<br/>"+supporteurs+" donateurs");
			$('#nb_days_left').html(diffDays);

		});
	} else {
		$('#fundraising_bar').goalProgress({
			goalAmount: 100000,
			currentAmount: amount,
			textBefore: '',
			textAfter: ' € - '+supporteurs+' donateurs'
		});
		$('#fundraising_figures').html(amount+" € dons<br/>"+supporteurs+" donateurs");
		$('#nb_days_left').html(diffDays);
	}
});
