$(document).ready(function() {
	twttr.ready(
		function (twttr) {
			twttr.events.bind('follow',function (ev) {
				ga('send', 'social', 'twitter', 'follow',{'eventCategory':'twitter_action','eventAction':'follow','eventLabel':ev.data.screen_name});
			});
			twttr.events.bind('tweet',function (ev) {
				ga('send', 'social', 'twitter', 'tweet',{'eventCategory':'twitter_action','eventAction':'tweet','eventLabel':'tweet'});
			});
			twttr.events.bind('retweet',function (ev) {
				ga('send', 'social', 'twitter', 'retweet',{'eventCategory':'twitter_action','eventAction':'retweet','eventLabel':ev.data.source_tweet_id});
			});
			twttr.events.bind('favorite',function (ev) {
				ga('send', 'social', 'twitter', 'favorite',{'eventCategory':'twitter_action','eventAction':'favorite','eventLabel':'favorite'});
			});
			twttr.events.bind('click',function (ev) {
				ga('send', 'social', 'twitter', 'click',{'eventCategory':'twitter_action','eventAction':'click','eventLabel':ev.region});
			});
		}
		);
	$(".facebook-follow").click(function (e) {
		ga('send', 'social', 'facebook', 'follow',{'eventCategory':'facebook_action','eventAction':'follow','eventLabel':e.currentTarget.attributes["data-orig"].value});
	});
	$(".facebook-share").click(function (e) {
		ga('send', 'social', 'facebook', 'share',{'eventCategory':'facebook_action','eventAction':'share','eventLabel':e.currentTarget.attributes["data-orig"].value});
	});
	$(".google-share").click(function (e) {
		ga('send', 'social', 'google', 'share',{'eventCategory':'google_action','eventAction':'share','eventLabel':e.currentTarget.attributes["data-orig"].value});
	});
	$(".donate-link").click(function (e) {
		ga('send', 'event', 'fundraising', 'donate-link','fundraising-campaign-1');
	});
});

