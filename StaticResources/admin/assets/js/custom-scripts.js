/*------------------------------------------------------
    Author : www.webthemez.com
    License: Commons Attribution 3.0
    http://creativecommons.org/licenses/by/3.0/
---------------------------------------------------------  */

(function ($) {
    "use strict";
    var mainApp = {

        initFunction: function () {
            /*MENU 
            ------------------------------------*/
            $('#main-menu').metisMenu();
			
            $(window).bind("load resize", function () {
                if ($(this).width() < 768) {
                    $('div.sidebar-collapse').addClass('collapse')
                } else {
                    $('div.sidebar-collapse').removeClass('collapse')
                }
            });

            /* MORRIS BAR CHART



            /* MORRIS DONUT CHART
			----------------------------------------*/
            var children_sale_num = $('.children_sale_num').val();
            var men_sale_num = $('.men_sale_num').val();
            var women_sale_num = $('.women_sale_num').val();
            Morris.Donut({
                element: 'morris-donut-chart',
                data: [{
                    label: "男士专区",
                    value: men_sale_num
                }, {
                    label: "女士专区",
                    value: women_sale_num
                }, {
                    label: "儿童专区",
                    value: children_sale_num
                }],
				   colors: [
    '#A6A6A6','#414e63',
    '#e96562' 
  ],
                resize: true
            });

            var children_jing = $('.children_jing').val();
            var men_jing = $('.men_jing').val();
            var women_jing = $('.women_jing').val();
            Morris.Donut({
                element: 'morris-donut-chart1',
                data: [{
                    label: "男士专区",
                    value: men_jing
                }, {
                    label: "女士专区",
                    value: women_jing
                }, {
                    label: "儿童专区",
                    value: children_jing
                }],
				   colors: [
    '#A6A6A6','#414e63',
    '#e96562'
  ],
                resize: true
            });


            /* MORRIS AREA CHART
			----------------------------------------*/
            var yi = $('.yi').val();
            var er = $('.er').val();
            var san = $('.san').val();
            var si = $('.si').val();
            var wu = $('.wu').val();
            var liu = $('.liu').val();
            var qi = $('.qi').val();
            var ba = $('.ba').val();
            var mon_ba = $('.mon_ba').val();
            var mon_qi = $('.mon_qi').val();
            var mon_liu = $('.mon_liu').val();
            var mon_wu = $('.mon_wu').val();
            var mon_si = $('.mon_si').val();
            var mon_san = $('.mon_san').val();
            var mon_er = $('.mon_er').val();
            var mon_yi = $('.mon_yi').val();

            Morris.Area({
                element: 'morris-area-chart',
                data: [{
                    period: mon_ba,
                    iphone: ba,

                }, {
                    period: mon_qi,
                    iphone: qi,

                }, {
                    period: mon_liu,
                    iphone: liu,

                }, {
                    period: mon_wu,
                    iphone: wu,

                }, {
                    period: mon_si,
                    iphone: si,

                },
                    {
                    period: mon_san,
                    iphone: san,

                }, {
                    period: mon_er,
                    iphone: er,

                }, {
                    period: mon_yi,
                    iphone: yi,

                }, ],
                xkey: 'period',
                ykeys: ['iphone',],
                labels: ['销售额',],
                pointSize: 2,
                hideHover: 'auto',
				  pointFillColors:['#ffffff'],
				  pointStrokeColors: ['black'],
				  lineColors:['#A6A6A6','#414e63'],
                resize: true
            });

            /* MORRIS LINE CHART
			----------------------------------------*/
            var ba_month_num = $('.ba_month_num').val();
            var qi_month_num = $('.qi_month_num').val();
            var liu_month_num = $('.liu_month_num').val();
            var wu_month_num = $('.wu_month_num').val();
            var si_month_num = $('.si_month_num').val();
            var san_month_num = $('.san_month_num').val();
            var er_month_num = $('.er_month_num').val();
            var yi_month_num = $('.yi_month_num').val();
            Morris.Line({
                element: 'morris-line-chart',
                data: [
					  { y: mon_ba, a: ba_month_num, },
					  { y: mon_qi, a: qi_month_num,  },
					  { y: mon_liu, a: liu_month_num, },
					  { y: mon_wu, a: wu_month_num, },
					  { y: mon_si, a: si_month_num,  },
					  { y: mon_san, a: san_month_num,  },
					  { y: mon_er, a: er_month_num, },
					  { y: mon_yi, a: yi_month_num, },

				],


      xkey: 'y',
      ykeys: ['a'],
      labels: ['月订单量', ],
      fillOpacity: 0.6,
      hideHover: 'auto',
      behaveLikeLine: true,
      resize: true,
      pointFillColors:['#ffffff'],
      pointStrokeColors: ['black'],
      lineColors:['gray','#414e63']

            });

        
            $('.donut-chart').cssCharts({type:"donut"}).trigger('show-donut-chart');
            $('.line-chart').cssCharts({type:"line"});

            $('.pie-thychart').cssCharts({type:"pie"});
       
	 
        },

        initialization: function () {
            mainApp.initFunction();

        }

    };
    // Initializing ///

    $(document).ready(function () {
		$(".dropdown-button").dropdown();
		$("#sideNav").click(function(){
			if($(this).hasClass('closed')){
				$('.navbar-side').animate({left: '0px'});
				$(this).removeClass('closed');
				$('#page-wrapper').animate({'margin-left' : '260px'});
				
			}
			else{
			    $(this).addClass('closed');
				$('.navbar-side').animate({left: '-260px'});
				$('#page-wrapper').animate({'margin-left' : '0px'}); 
			}
		});
		
        mainApp.initFunction(); 
    });

	$(".dropdown-button").dropdown();
	
}(jQuery));
