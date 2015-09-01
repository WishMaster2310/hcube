function projectSlider ()  {
	
	$('#projectSlider').owlCarousel({
		singleItem: true,
		addClassActive: true,
		pagination: false,
		slideSpeed: 350,
		navigation: true,
		rewindNav: false,
		navigationText: [null, null]
	});
}

function partnersSlider ()  {
	
	$('#partnersSlider').owlCarousel({
		pagination: false,
		slideSpeed: 350,
		itemsDesktop : [1199,4],
		itemsDesktopSmall : [980,3],
		itemsTablet: [768,2],
		itemsTabletSmall: false,
		itemsMobile : [479,1],
		navigation: true,
		rewindNav: false,
		navigationText: [null, null]
	});
}

function initMap () {

	myMap = new ymaps.Map('map', {
            
            center: [62.815, 34.46],
            zoom: 16,
            controls: []
        }, {}
    );

    myMap.behaviors
        .disable(['drag', 'scrollZoom', 'rightMouseButtonMagnifier']);

    myMap.geoObjects
    	.add(new ymaps.Placemark([55.804916, 37.585449], {
            balloonContent: ''
        }, {
            preset: 'islands#dotIcon',
            iconColor: '#ff7b08'
        }))

        .add(new ymaps.Placemark([56.833171, 60.599073], {
            balloonContent: ''
        }, {
            preset: 'islands#dotIcon',
            iconColor: '#ff7b08'
        }));

    $('.j-map-marker').eq(0).trigger('click');
}

$(document).ready(function() {
	projectSlider ();
	partnersSlider ();
	ymaps.ready(initMap);
	new WOW().init();

	$('.j-map-marker').on('click', function(e) {
		e.preventDefault();
		var center = $(this).data('center');
		var tel = $(this).data('tel');
		var email = $(this).data('email');
		var addr = $(this).data('addr');
		
		myMap.setCenter(center)

        $(this).addClass('active').siblings().removeClass('active');
        $('#j-map-addr').stop().fadeOut(200, function() {
        	if (addr.length > 0) {
        		$('#j-map-addr').html("&emsp;" + addr + "&emsp;");
        		$('#j-map-addr').fadeIn()
        	};
        });
        $('#j-map-contacts').html("&emsp;" + tel + "&emsp;");
	});

	var isCounterPlayed = false;

	$(window).on('scroll', function() {
		var counter = $('.j-counter');
		var a = $('.j-counter').offset().top;
		var b = $(this).scrollTop();
		var h = $(this).height();
		if ( !isCounterPlayed && a <= (b + h) ) {
		

			$(counter).prop('Counter',0).animate({
	            Counter: $(counter).text()
	        }, {
	            duration: 3500,
	            step: function (now) {
	                $(counter).text(Math.ceil(now));
	            }
	        });

	        isCounterPlayed = true;
		};
		
	});

	$('#nav a').on('click', function(e) {
		e.preventDefault();
		var targ = $(this).attr('href');
		$('html, body').stop().animate({
			scrollTop: $(targ).offset().top - 60
		}, 300)
	});

	$('.j-tel').mask('+7 (999) 999-99-99');

	$('.j-submit').on('click', function() {
		var form = $(this).closest('form');
		var tel = $(form).find('.j-tel');
		var name = $(form).find('.j-name');

		if(!name.val()) {
			$(name).addClass('error');
			$(name).focus();
		} else {
			$(name).removeClass('error');
		}

		if(!tel.val()) {
			$(tel).addClass('error');
			if (name.val()) {
				$(tel).focus();
			};
		} else {
			$(tel).removeClass('error');
		}

		if (tel.val() && name.val()) {
			// submit form
		};

	});



});
/*
*/