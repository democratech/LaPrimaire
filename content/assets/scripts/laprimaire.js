$(document).ready(function() {
	$("a.joinus_action").click(function() {
			ga('send','event','button','click','Je participe');
	});
	if ($('#JoinsUsNow')!=null) {
		$('#JoinUsNow').on('shown.bs.modal', function () {
			ga('send', 'pageview', '/inscription-popup/');
			$('#input_email').on('focus', function(e) {
				$('#input_pb').hide();
			})
			$('#login_form').on('submit', function(e) {
				e.preventDefault();
				$('#input_loading').show();
				$('#input_email').prop('disabled',true);
				var email=$('#input_email').val();
				$.post("https://api.democratech.co/v2/auth/login",{'email':email})
					.done(function(data){
						window.location.href= data['redirect_url'];
					})
					.fail(function(data) {
						console.log(data);
						$('#input_pb').show();
						$('#input_loading').hide();
						$('#input_email').prop('disabled',false)
					});
			})
		});
	}
	if ($('#fundraising_bar')!=null) {
		var app_stats=readCookie('app_stats');
		if (app_stats==null) {
			$.get("https://api.democratech.co/v1/app/stats", function( data ){
				var nb_candidates=data['nb_candidates'];
				var nb_citizens=data['nb_citizens'];
				var nb_plebiscites=data['nb_plebiscites'];
				createCookie('app_stats',JSON.stringify({nb_candidates: nb_candidates, nb_citizens: nb_citizens, nb_plebiscites: nb_plebiscites}));
				$('#nb_citoyens_app').html("<span class='nb_citizens_fig'>"+nb_citizens+"</span> citoyens participent... Et vous ?");
				$('#nb_candidates').html("<a href='/candidats/'>"+nb_candidates+" candidats</a>");
				$('#nb_plebiscites').html("<a href='/citoyens/'>"+nb_plebiscites+" citoyens</a>");
				var supporteurs=nb_citizens;
				var percentage = supporteurs / 1000;
				var percentage_str = Math.round(percentage);
				$('#fundraising_bar').goalProgress({
					goalAmount: percentage,
					currentAmount: percentage,
					indicatorAmount: 100,
					textBefore: '',
					textAfter: " % de l'objectif de 100.000 citoyens atteint"
				});


			});
		} else {
			data=JSON.parse(app_stats);
			var nb_candidates=data['nb_candidates'];
			var nb_citizens=data['nb_citizens'];
			var nb_plebiscites=data['nb_plebiscites'];
			$('#nb_citoyens_app').html("<span class='nb_citizens_fig'>"+nb_citizens+"</span> citoyens participent... Et vous ?");
			$('#nb_candidates').html("<a href='/candidats/'>"+nb_candidates+" candidats</a>");
			$('#nb_plebiscites').html("<a href='/citoyens/'>"+nb_plebiscites+" citoyens</a>");
			var supporteurs=nb_citizens;
			var percentage = supporteurs / 1000;
			var percentage_str = Math.round(percentage);
			$('#fundraising_bar').goalProgress({
				goalAmount: percentage,
				currentAmount: percentage,
				indicatorAmount: 100,
				textBefore: '',
				textAfter: " % de l'objectif de 100.000 citoyens atteint"
			});
		}
	}
	if ($('#donations_bar')!=null) {
		var amount=readCookie('donations');
		var donateurs=readCookie('nb_adherents');
		if (amount==null || donateurs==null) {
			$.get("https://api.democratech.co/v1/payment/total", function( data ){
				amount=data['total'];
				donateurs=data['nb_adherents'];
				createCookie('donations',amount);
				createCookie('nb_adherents',donateurs);
				$('#donations_bar').goalProgress({
					goalAmount: 100000,
					currentAmount: amount,
					textBefore: '',
					textAfter: '€ de dons récoltés. Objectif : 100.000€'
				});
			});
		} else {
			$('#donations_bar').goalProgress({
				goalAmount: 100000,
				currentAmount: amount,
				textBefore: '',
				textAfter: '€ de dons récoltés. Objectif : 100.000€'
			});
		}
	}
	if ($('img.lazy')!=null || $('div.lazy')!=null) {
		$.getScript('https://cdnjs.cloudflare.com/ajax/libs/jquery.lazyload/1.9.1/jquery.lazyload.min.js', function() {
				$("img.lazy").lazyload({effect:"fadeIn"});
				$("div.lazy").lazyload({effect:"fadeIn"});
		});
	}
});

