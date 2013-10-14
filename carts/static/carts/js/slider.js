//
// This program is free software; you can redistribute it and/or
// modify it under the terms of the GNU Affero General Public License
// version 3 as published by the Free Software Foundation.
//
// This program is distributed in the hope that it will be useful, but
// WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
// General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program; if not, write to the Free Software
// Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
// USA
//
// Authors:
// Caner Candan <caner@candan.fr>, http://caner.candan.fr
// Geraldine Starke <geraldine@starke.fr>, http://www.vegeclic.fr
//

$(function() {
    var sliders = $("#sliders .slider");
    var initial_percent = parseInt(100/sliders.length);
    var availableTotal = 100;

    sliders.each(function() {
	$(this).siblings().find('.value').text(initial_percent);
	$(this).siblings('.input_value').val(initial_percent);

	var s = $(this);

	$(this).siblings().find('.lock').click(function() {
	    s.slider('option', 'disabled', ! s.slider('option', 'disabled'));
	});

	$(this).empty().slider({
	    value: parseInt(initial_percent),
	    min: 0,
	    max: availableTotal,
	    range: "max",
	    step: 2,
	    animate: false,

	    stop: function(event, ui) {
		if (sliders.length < 2) {
		    $(this).slider('option', 'value', availableTotal)
		    return;
		}

		// Get current total
		var total = 0;
		sliders.not(this).each(function() {
		    total += $(this).slider('option', 'value');
		});

		if ((sliders.length - $('#sliders .ui-slider-disabled').length) < 2) {
		    $(this).slider('option', 'value', availableTotal - total)
		    return;
		}

		var upper_bound = availableTotal - total;
		$(this).slider('option', 'value', upper_bound)
		$(this).siblings().find('.value').text(upper_bound);
		$(this).siblings('.input_value').val(upper_bound);
		// $('#sliders_total').text(total+upper_bound);
	    },

	    slide: function(event, ui) {
		if ((sliders.length - $('#sliders .ui-slider-disabled').length) < 2) { return; }
		if (sliders.length < 2) { return; }

		// Update display to current value
		$(this).siblings().find('.value').text(ui.value);
		$(this).siblings('.input_value').val(ui.value);

		// Get current total
		var total = 0;
		sliders.not(this).each(function() {
		    total += $(this).slider('option', 'value');
		});

		// Need to do this because apparently jQ UI
		// does not update value until this event completes
		total += ui.value;

		var delta = availableTotal - total;

		// Update each slider
		sliders.not(this).each(function() {
		    var t = $(this);

		    if ( t.slider('option', 'disabled') ) { return; }

		    var value = t.slider('option', 'value');
		    var new_value = parseInt(value + (delta/(sliders.length-1)));

		    if (new_value < 0 || ui.value == 100) { new_value = 0; }
		    if (new_value > 100) { new_value = 100; }

		    t.siblings().find('.value').text(new_value);
		    t.siblings('.input_value').val(new_value);
		    t.slider('option', 'value', new_value);
		});
	    }
	});
    });

    $('.lock').tooltip();

    $('#balance').click(function() {
	var disabled_sliders = $('#sliders .ui-slider-disabled');
	var total = 0;
	disabled_sliders.each(function() {
	    total += $(this).slider('option', 'value');
	});

	var new_percent = parseInt((availableTotal - total) / (sliders.length - disabled_sliders.length));

	sliders.each(function() {
	    if ( $(this).slider('option', 'disabled') ) { return; }
	    $(this).slider('value', new_percent);
	    $(this).siblings().find('.value').text(new_percent);
	    $(this).siblings('.input_value').val(new_percent);
	});
    });
});

function create_one_slider(choices, id, default_value) {
    $('#' + id + '-slide').slider({
	range: 'max',
	min: 0,
	max: choices.length-1,
	value: default_value,
	slide: function( event, ui ) {
	    var v = choices[ parseInt(ui.value) ];
	    $('#id_' + id)[0].selectedIndex = v[0];
	    $('#' + id + '-slide-text').text( v[1] );
	}
    });

    var v = choices[ parseInt($('#' + id + '-slide').slider('value')) ];
    // $('#' + id)[0].value = v[0];
    $('#id_' + id)[0].selectedIndex = v[0];
    $('#' + id + '-slide-text').text( v[1] );
}
