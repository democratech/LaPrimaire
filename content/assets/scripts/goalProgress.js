/*
 *  Tinacious Design goalProgress jQuery plugin
 *  Plugin URL: https://github.com/tinacious/goalProgress
 *
 *  Christina Holly (Tinacious Design)
 *  http://tinaciousdesign.com
 *
 */
!function($){
	$.fn.extend({
		goalProgress: function(options) {
			var defaults = {
				goalAmount: 100,
				currentAmount: 50,
				indicatorAmount: 0,
				speed: 1000,
				textBefore: '',
				textAfter: '',
				milestoneNumber: 70,
				milestoneClass: 'almost-full',
				callback: function() {}
			}

			var options = $.extend(defaults, options);
			return this.each(function(){
				var obj = $(this);
				
				// Collect and sanitize user input
				var goalAmountParsed = parseInt(defaults.goalAmount);
				var currentAmountParsed = parseInt(defaults.currentAmount);

				// Calculate size of the progress bar
				var percentage = (currentAmountParsed / goalAmountParsed) * 100;
				var percentage_str = Math.round(percentage);
				var milestoneNumberClass = (percentage > defaults.milestoneNumber) ? ' ' + defaults.milestoneClass : '';

				// Generate the HTML
 				var progressBar = '<div class="progressBar">' + defaults.textBefore + currentAmountParsed + defaults.textAfter + '</div>';
 				//var progressBar = '<div class="progressBar">'+percentage_str+'% </div>';
 				var progressBarWrapped = '<div class="goalProgress' + milestoneNumberClass + '">' + progressBar + '</div>';
				if (defaults.indicatorAmount!=0) {
					var indicatorAmountParsed = parseInt(defaults.indicatorAmount);
					var percentageInd = (1-(indicatorAmountParsed / goalAmountParsed)) * 100;
					var indicatorBar = '<div class="indicatorBar"></div>';
					progressBarWrapped = '<div class="goalProgress' + milestoneNumberClass + '">' + progressBar + indicatorBar + '</div>';
				}

				// Append to the target
				obj.append(progressBarWrapped);

				// Ready
				var rendered = obj.find('div.progressBar');

				// Remove Spaces
				rendered.each(function() { $(this).html($(this).text().replace(/\s/g, '&nbsp;')); });

				// Animate!
				rendered.animate({width: percentage +'%'}, defaults.speed, defaults.callback);

				if (defaults.indicatorAmount!=0) {
					var renderedInd = obj.find('div.indicatorBar');
					renderedInd.each(function() { $(this).html($(this).text().replace(/\s/g, '&nbsp;')); });
					renderedInd.animate({width: percentageInd +'%'}, defaults.speed, defaults.callback);
				}

				if(typeof callback == 'function') {
					callback.call(this)
				}
			});
		}
	});
}(window.jQuery);
