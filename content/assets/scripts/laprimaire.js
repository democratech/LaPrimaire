$(document).ready(function() {
	$("a.joinus_action").click(function() {
			ga('send','event','button','click','Je participe');
	});
	if ($('#VoteNow')!=null) {
		$('#VoteNow').on('shown.bs.modal', function () {
			$.getScript('https://www.google.com/recaptcha/api.js', function(){

			});
		});
	}
	if ($('#JoinsUsNow')!=null) {
		$('#JoinUsNow').on('shown.bs.modal', function () {
			ga('send', 'pageview', '/inscription-popup/');
			var q4emv9q14p6f33;(function(d, t) {
			var s = d.createElement(t), options = {
			'userName':'democratech',
			'formHash':'q4emv9q14p6f33',
			'autoResize':true,
			'height':'456',
			'async':true,
			'defaultValues':'field12='+getURLParameter('ref')+'&field9='+getURLParameter('first')+'&field10='+getURLParameter('last')+'&field1='+getURLParameter('email'),
			'host':'wufoo.com',
			'header':'hide',
			'ssl':true};
			s.src = ('https:' == d.location.protocol ? 'https://' : 'http://') + 'www.wufoo.com/scripts/embed/form.js';
			s.onload = s.onreadystatechange = function() {
			var rs = this.readyState; if (rs) if (rs != 'complete') if (rs != 'loaded') return;
			try { q4emv9q14p6f33 = new WufooForm();q4emv9q14p6f33.initialize(options);q4emv9q14p6f33.display(); } catch (e) {}};
			var scr = d.getElementsByTagName(t)[0], par = scr.parentNode; par.insertBefore(s, scr);
			})(document, 'script');
			/*var qaj8t6m07xo97p;(function(d, t) {
			var s = d.createElement(t), options = {
			'userName':'democratech',
			'formHash':'qaj8t6m07xo97p',
			'autoResize':true,
			'height':'397',
			'async':true,
			'defaultValues':'field12='+getURLParameter('ref')+'&field9='+getURLParameter('first')+'&field10='+getURLParameter('last')+'&field1='+getURLParameter('email'),
			'host':'wufoo.com',
			'header':'hide',
			'ssl':true};
			s.src = ('https:' == d.location.protocol ? 'https://' : 'http://') + 'www.wufoo.com/scripts/embed/form.js';
			s.onload = s.onreadystatechange = function() {
			var rs = this.readyState; if (rs) if (rs != 'complete') if (rs != 'loaded') return;
			try { qaj8t6m07xo97p = new WufooForm();qaj8t6m07xo97p.initialize(options);qaj8t6m07xo97p.display(); } catch (e) {}};
			var scr = d.getElementsByTagName(t)[0], par = scr.parentNode; par.insertBefore(s, scr);
			})(document, 'script');*/
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
					goalAmount: 300000,
					currentAmount: amount,
					textBefore: '',
					textAfter: '€ de dons récoltés. Objectif : 300.000€'
				});
			});
		} else {
			$('#donations_bar').goalProgress({
				goalAmount: 300000,
				currentAmount: amount,
				textBefore: '',
				textAfter: '€ de dons récoltés. Objectif : 300.000€'
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

