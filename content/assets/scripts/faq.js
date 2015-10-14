$(document).ready(function () {
		$('.faq dd').hide(); // Hide all DDs inside .faqs
		$('.faq h4').hover(function(){$(this).addClass('hover')},function(){$(this).removeClass('hover')}).click(function(){ // Add class "hover" on dt when hover
		$(this).next().slideToggle('normal'); // Toggle dd when the respective dt is clicked
		}); 
});
