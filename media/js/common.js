$(document).ready(function() {

	//прилипающие меню
	var $menu = $("#menu");
	$(window).scroll(function(){
		if ( $(this).scrollTop() > 600 && $menu.hasClass("default") ){
			$menu.removeClass("default").addClass("fixed");
		} else if($(this).scrollTop() <= 600 && $menu.hasClass("fixed")) {
			$menu.removeClass("fixed").addClass("default");
		}
	});

	$('.autoheight').equalHeights();
	//плавный скролл
	$(".navigat li a").mPageScroll2id();

	//открыть по клике карту
	$(".open_map").click(function()
	{
		var myDiv = document.getElementById('map');
		if(myDiv.style.display == 'none')
		{
			myDiv.style.display = 'block';
		}
		else
		{
			myDiv.style.display = 'none';
		}
		return false;
	});

	//кнопка sandwich
	$(" .btn_nav").click(function() {
		$(".btn_nav .sandwich").toggleClass("active");
	});
	$(".btn_nav").click(function() {
		$(".menu_mobile").addClass("active");
		$("body").addClass("body_menu");
	});
	$(".menu_navigation li a").click(function() {
		$(".menu_mobile").removeClass("active");
		$("body").removeClass("body_menu");
		$(".sandwich").removeClass("active");
	});
	$(".menu_navigation li a.dropdown-toggle").click(function() {
		$(".menu_mobile").addClass("active");
		$("body").addClass("body_menu");
		$(".sandwich").addClass("active");
	});
	$(document).mouseup(function (e) {
		var container = $(".menu_mobile");
		if (container.has(e.target).length === 0){
			$(".menu_mobile").removeClass("active");
			$(".menu_mobile").removeClass("menu_dn");
			$("body").removeClass("body_menu");
		$(".sandwich").removeClass("active");
		}
	});


	$(".top_navigation .list_navigation > li > a").click(function() {
		event.preventDefault();
		if ($(this).parent().children("ul").is(":visible")) {
			$(this).parent().children("ul").slideUp();
			$(".top_navigation .list_navigation > li").removeClass("open");
		} else {
			$(".top_navigation .list_navigation li ul").hide();
			$(this).parent().children("ul").slideToggle();
			$(".top_navigation .list_navigation > li").removeClass("open");
			$(this).parent().addClass("open");
		}
	});

	$(".down_navigation .list_navigation > li > a").click(function() {
		event.preventDefault();
		if ($(this).parent().children("ul").is(":visible")) {
			$(this).parent().children("ul").slideUp();
			$(".down_navigation .list_navigation > li").removeClass("open");
		} else {
			$(".down_navigation .list_navigation li ul").hide();
			$(this).parent().children("ul").slideToggle();
			$(".down_navigation .list_navigation > li").removeClass("open");
			$(this).parent().addClass("open");
		}
	});

	$(".drop_category").click(function() {
		if ($(this).parent().children("div").is(":visible")) {
			$(this).parent().children("div").slideUp();
			$(".category_list > li").removeClass("open");
		} else {
			$(".category_list li div").hide();
			$(this).parent().children("div").slideToggle();
			$(".category_list > li").removeClass("open");
			$(this).parent().addClass("open");
		}
	});

	

	{
		if ($(window).width() > 1240) {
			$(".drop_category").click(function() {
					event.preventDefault();
				});
		}
	}

	$(".btn_catalog_category").click(function() {
		$(".menu_mobile").addClass("active menu_dn");
		$("body").addClass("body_menu");
		$(".sandwich").addClass("active");
	});


	$("input[type='number']").stepper();
	$(".input_quantity").inputNumber();



	//слайдер
	$('.main_billboard').slick({
		infinite: true,
		dots: true,
		arrows:false,
		slidesToShow: 1,
		slidesToScroll: 1
	});

	$('.slider_products').slick({
		infinite: true,
		slidesToShow: 5,
		slidesToScroll: 1,
		responsive: [
		{
			breakpoint: 1200,
			settings: {
				slidesToShow: 3,
				slidesToScroll: 1
			}
		},
		{
			breakpoint: 992,
			settings: {
				slidesToShow: 2,
				slidesToScroll: 1
			}
		},
		{
			breakpoint: 768,
			settings: {
				slidesToShow: 1,
				slidesToScroll: 1
			}
		}
		]
	});

	$('.slider-for').slick({
		slidesToShow: 1,
		slidesToScroll: 1,
		arrows: true,
		dots: false,
		asNavFor: '.slider-nav'
	});

	$('.slider-nav').slick({
		slidesToShow: 5,
		slidesToScroll: 1,
		asNavFor: '.slider-for',
		dots: false,
		centerMode: true,
		focusOnSelect: true,
		responsive: [
			{
				breakpoint: 1240,
				settings: {
					slidesToShow: 5,
					slidesToScroll: 1
				}
			}
		]
	});

	 // стайлер для select
	 $('select').styler();


function getUrlParameter(sParam) {
    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : sParameterName[1];
        }
    }
}

	$('#show_items_on_page').change(function () {
		var current_URL = window.location.href,
			value = this.options[this.selectedIndex].value,
			items_on_page = getUrlParameter('items_on_page');

		if (items_on_page) {

			window.location.href = current_URL.replace('items_on_page' + '=' + items_on_page, 'items_on_page' + '=' + value);

		} else {

            if (current_URL.indexOf('/?') === -1) {
                window.location.href = current_URL + '?' + 'items_on_page' + '=' + value;
            } else {
                window.location.href = current_URL + '&' + 'items_on_page' + '=' + value;
            }
        }
    });

	$('#sorting_items_on_page').change(function () {
		var current_URL = window.location.href,
			value = this.options[this.selectedIndex].value,
			sorting = getUrlParameter('sorting');

		if (sorting) {

			window.location.href = current_URL.replace('sorting' + '=' + sorting, 'sorting' + '=' + value);

		} else {

            if (current_URL.indexOf('/?') === -1) {
                window.location.href = current_URL + '?' + 'sorting' + '=' + value;
            } else {
                window.location.href = current_URL + '&' + 'sorting' + '=' + value;
            }
        }
    });

$('.rating-loading').rating({hoverEnabled: true});
	 
	//Таймер обратного отсчета
	//Документация: http://keith-wood.name/countdown.html
	//<div class="countdown" date-time="2015-01-07"></div>
	var austDay = new Date($(".countdown").attr("date-time"));
	$(".countdown").countdown({until: austDay, format: 'yowdHMS'});

	//Попап менеджер FancyBox
	//Документация: http://fancybox.net/howto
	//<a class="fancybox"><img src="image.jpg" /></a>
	//<a class="fancybox" data-fancybox-group="group"><img src="image.jpg" /></a>
	$(".fancybox").fancybox();


	//Добавляет классы дочерним блокам .block для анимации
	//Документация: http://imakewebthings.com/jquery-waypoints/
	$(".block").waypoint(function(direction) {
		if (direction === "down") {
			$(".class").addClass("active");
		} else if (direction === "up") {
			$(".class").removeClass("deactive");
		};
	}, {offset: 100});

	//Плавный скролл до блока .div по клику на .scroll
	//Документация: https://github.com/flesler/jquery.scrollTo
	$("a.scroll").click(function() {
		$.scrollTo($(".div"), 800, {
			offset: -90
		});
	});


	//Кнопка "Наверх"
	//Документация:
	//http://api.jquery.com/scrolltop/
	//http://api.jquery.com/animate/
	$("#top").click(function () {
		$("body, html").animate({
			scrollTop: 0
		}, 800);
		return false;
	});
	
	//Аякс отправка форм
	//Документация: http://api.jquery.com/jquery.ajax/
	$("form").submit(function() {
		$.ajax({
			type: "GET",
			url: "mail.php",
			data: $("form").serialize()
		}).done(function() {
			alert("Спасибо за заявку!");
			setTimeout(function() {
				$.fancybox.close();
			}, 1000);
		});
		return false;
	});

});
$.fn.inputNumber = function(){
	var block = $(this) 
	if(block.find('input').attr('data-max')){ 
		maxV = block.find('input').attr('data-max') 
	} 
	var block = $(this) 
	block.find('input').before('<button class="minus">-</button>') 
	block.find('input').before('<button class="plus">+</button>') 
	block.find('button').click(function(){ 
		var val = $(this).parent().find('input').val() 
		if($(this).hasClass('minus')){ 
			if(val !== '1'){ 
				val--;
				$(this).parent().find('input').val(val) 
			} 
		} 
		if($(this).hasClass('plus')){ 

			val++ 
			$(this).parent().find('input').val(val) 
		} 

	}) 
}