/* ===================================================================
    
    Author          : Valid Theme
    Template Name   : Avrix - Digital Agency Portfolio Template
    Version         : 1.0
    
* ================================================================= */
(function($) {
	"use strict";

	$(document).ready(function() {



		/* ==================================================
		    # Tooltip Init
		===============================================*/
		$('[data-toggle="tooltip"]').tooltip();


		/* ==================================================
		    # Youtube Video Init
		 ===============================================*/
		$('.player').mb_YTPlayer();



		/* ==================================================
		    # Scrolla active
		===============================================*/
		$('.animate').scrolla();


		


		/* ==================================================
		    _Progressbar Init
		 ===============================================*/
		function animateElements() {
			$('.progressbar').each(function() {
				var elementPos = $(this).offset().top;
				var topOfWindow = $(window).scrollTop();
				var percent = $(this).find('.circle').attr('data-percent');
				var animate = $(this).data('animate');
				if (elementPos < topOfWindow + $(window).height() - 30 && !animate) {
					$(this).data('animate', true);
					$(this).find('.circle').circleProgress({
						// startAngle: -Math.PI / 2,
						value: percent / 100,
						size: 130,
						thickness: 13,
						lineCap: 'round',
						emptyFill: '#f1f1f1',
						fill: {
							gradient: ['#2667FF', '#6c19ef']
						}
					}).on('circle-animation-progress', function(event, progress, stepValue) {
						$(this).find('strong').text((stepValue * 100).toFixed(0) + "%");
					}).stop();
				}
			});

		}

		animateElements();
		$(window).scroll(animateElements);


		/* ==================================================
            # Services Carousel
         ===============================================*/
		const servicesCarousel = new Swiper(".services-carousel", {
			// Optional parameters
			loop: true,
			autoplay: true,
			freeMode: true,
			grabCursor: true,
			slidesPerView: 1,
			spaceBetween: 30,
			// Navigation arrows
			navigation: {
				nextEl: ".services-button-next",
				prevEl: ".services-button-prev"
			},
			breakpoints: {
				768: {
					slidesPerView: 2,
					spaceBetween: 50,
				},
				1400: {
					slidesPerView: 2.5,
					spaceBetween: 60,
				},

				1800: {
					spaceBetween: 60,
					slidesPerView: 2.8,
				},
			},
		});


		/* ==================================================
            # Testimonial Carousel
         ===============================================*/
		const testimonialOne = new Swiper(".testimonial-style-one-carousel", {
			// Optional parameters
			loop: true,
			slidesPerView: 1,
			spaceBetween: 0,
			autoplay: true,

			pagination: {
				el: '.testimonial-one-pagination',
				type: 'fraction',
				clickable: true,
			},

			// Navigation arrows
			navigation: {
				nextEl: ".testimonial-one-button-next",
				prevEl: ".testimonial-one-button-prev"
			}

			// And if we need scrollbar
			/*scrollbar: {
            el: '.swiper-scrollbar',
          },*/
		});


		/* ==================================================
            # Project Carousel
         ===============================================*/
		const projectStage = new Swiper(".project-center-stage-carousel", {
			// Optional parameters
			loop: true,
			freeMode: true,
			grabCursor: true,
			slidesPerView: 1,
			centeredSlides: true,
			spaceBetween: 30,
			autoplay: true,
			pagination: {
				el: ".swiper-pagination",
				clickable: true,
			},
			// Navigation arrows
			navigation: {
				nextEl: ".project-button-next",
				prevEl: ".project-button-prev"
			},
			breakpoints: {
				991: {
					slidesPerView: 2,
					spaceBetween: 30,
					centeredSlides: false,
				},
				1200: {
					slidesPerView: 2.5,
					spaceBetween: 60,
				},
				1800: {
					slidesPerView: 2.8,
					spaceBetween: 80,
				},
			},
		});

		
		/* ==================================================
            # Banner Carousel
         ===============================================*/
		 const swiperCounter = new Swiper(".banner-slide-counter", {
            // Optional parameters
            direction: "vertical",
            loop: true,
            grabCursor: true,
            mousewheel: true,
            autoplay: true,
            speed: 1000,
			autoplay: {
				delay: 5000,
				disableOnInteraction: false,
			},

            // If we need pagination
            pagination: {
                el: '.swiper-pagination',
				clickable: true,
            },


            // Navigation arrows
            navigation: {
                nextEl: ".swiper-button-next",
                prevEl: ".swiper-button-prev"
            }

            // And if we need scrollbar
            /*scrollbar: {
            el: '.swiper-scrollbar',
          },*/
        });


		/* ==================================================
		    Contact Form Validations
		================================================== */
		$('.contact-form').each(function() {
			var formInstance = $(this);
			formInstance.submit(function() {

				var action = $(this).attr('action');

				$("#message").slideUp(750, function() {
					$('#message').hide();

					$('#submit')
						.after('<img src="assets/img/ajax-loader.gif" class="loader" />')
						.attr('disabled', 'disabled');

					$.post(action, {
							name: $('#name').val(),
							email: $('#email').val(),
							phone: $('#phone').val(),
							comments: $('#comments').val()
						},
						function(data) {
							document.getElementById('message').innerHTML = data;
							$('#message').slideDown('slow');
							$('.contact-form img.loader').fadeOut('slow', function() {
								$(this).remove()
							});
							$('#submit').removeAttr('disabled');
						}
					);
				});
				return false;
			});
		});


		/* ===================================================================
			Horizontal Scroll Init JS
		* ================================================================= */
		var width = $(window).width();
		if (width > 1023) {

			/* ===============================  scroll  =============================== */

			let section_scroll = document.querySelector(".thecontainer");
			if (section_scroll) {
				gsap.registerPlugin(ScrollTrigger);

				let sections = gsap.utils.toArray(".panel");

				gsap.to(sections, {
					xPercent: -100 * (sections.length - 1),
					ease: "none",
					scrollTrigger: {
						trigger: ".thecontainer",
						pin: true,
						scrub: 1,
						// snap: 1 / (sections.length - 1),
						end: () => "+=" + document.querySelector(".thecontainer").offsetWidth
					}
				});
			}

		}


		/* ===================================================================
			Curosor Hover Init JS
		* ================================================================= */
		let accordion_animation = document.querySelector("#accordion");
		if (accordion_animation) {
            var expand;
            var $accordion, $wideScreen;
            $accordion = $('#accordion').children('li');
            $wideScreen = $(window).width() > 767;
            if ($wideScreen) {
                $accordion.on('mouseenter click', function (e) {
                    var $this;
                    e.stopPropagation();
                    $this = $(this);
                    if ($this.hasClass('out')) {
                        $this.addClass('out');
                    } else {
                        $this.addClass('out');
                        $this.siblings().removeClass('out');
                    }
                });
            } else {
                $accordion.on('touchstart touchend', function (e) {
                    var $this;
                    e.stopPropagation();
                    $this = $(this);
                    if ($this.hasClass('out')) {
                        $this.addClass('out');
                    } else {
                        $this.addClass('out');
                        $this.siblings().removeClass('out');
                    }
                });
            }
        }



		/* ===================================================================
			Curosor Hover Init JS
		* ================================================================= */
		let curosr_hover = document.querySelector(".preview");
		if (curosr_hover) {
			const cursor = document.querySelectorAll(".cursor");
			const cursorHover = document.querySelector(".cursor-hover");
			const preview = document.querySelector(".preview");



			gsap.set(cursor, {
				xPercent: -50,
				yPercent: -50,
				opacity: 1
			});

			gsap.set(cursorHover, {
				xPercent: -50,
				yPercent: -50,
				scale: 0,
				opacity: 0
			});

			const setX = gsap.quickTo(cursor, "x", {
				duration: 0.6,
				ease: "expo"
			});

			const setY = gsap.quickTo(cursor, "y", {
				duration: 0.6,
				ease: "expo"
			});

			window.addEventListener("mousemove", (e) => {
				setX(e.pageX);
				setY(e.pageY);
			});

			const tl = gsap.timeline({
				paused: true,
				defaults: {
					duration: 0.3,
					ease: "sine.inOut"
				}
			});

			tl.to(cursorHover, {
				scale: 1,
				opacity: 1
			});

			preview.addEventListener("mouseover", () => tl.play());
			preview.addEventListener("mouseout", () => tl.reverse());
		}
		


		/* ==================================================
		    Start GSAP ScrollTiger Animation JS
		================================================== */
		let parallax_Animation = document.querySelector(".parallax-container");
		if (parallax_Animation) {

			gsap.registerPlugin(ScrollTrigger)

			const Scroll = new function() {
				let sections
				let page
				let main
				let scrollTrigger
				let tl
				let win
				
				// Init
				this.init = () => {
					sections = document.querySelectorAll('section')
					page = document.querySelector('.parallax-container')
					main = document.querySelector('.parallax-items')
					win = {
						w: window.innerWidth,
						h: window.innerHeight
					}
					
					this.setupTimeline()
					this.setupScrollTrigger()
					window.addEventListener('resize', this.onResize)
				}
				
				// Setup ScrollTrigger
				this.setupScrollTrigger = () => {
					page.style.height = (this.getTotalScroll() + win.h) + 'px'
					
					scrollTrigger = ScrollTrigger.create({
						id: 'mainScroll',
						trigger: '.parallax-items',
						animation: tl,
						pin: true,
						scrub: true,
						snap: {
							snapTo: (value) => {
								
								let labels = Object.values(tl.labels)
								
								const snapPoints = labels.map(x => x / tl.totalDuration());
								const proximity = 0.1
								
								console.log(tl.labels , tl.totalDuration(), labels, snapPoints)
								
								for (let i = 0; i < snapPoints.length; i++) {
									if (value > snapPoints[i] - proximity && value < snapPoints[i] + proximity) {
										return snapPoints[i]
									}
								}
							},
							duration: { min: 0.2, max: 0.6 },
						},
						start: 'top top',
						end: '+=' + this.getTotalScroll(),
					})
				}
				
				// Setup timeline
				this.setupTimeline = () => {
					tl = gsap.timeline()
					tl.addLabel("label-initial")
					
					sections.forEach((section, index) => {
						const nextSection = sections[index+1]
						if (!nextSection) return

						tl.to(nextSection, {
							y: -1 * nextSection.offsetHeight,
							duration: nextSection.offsetHeight,
							ease: 'linear',
						})
						.addLabel(`label${index}`)
					})
				}
				
				// On resize
				this.onResize = () => {
					win = {
						w: window.innerWidth,
						h: window.innerHeight
					}
					
					this.reset()
				}
				
				// Reset
				this.reset = () => {
					if (typeof ScrollTrigger.getById('mainScroll') === 'object') {
						ScrollTrigger.getById('mainScroll').kill()
					}
					
					if (typeof tl === 'object') {
						tl.kill()
						tl.seek(0)
					}
					
					document.body.scrollTop = document.documentElement.scrollTop = 0
					this.init()
				}
				
				// Get total scroll
				this.getTotalScroll = () => {
					let totalScroll = 0
					sections.forEach(section => {
						totalScroll += section.offsetHeight
					})
					totalScroll -= win.h
					return totalScroll
				}
			}

			Scroll.init()

		}


		/* ==================================================
		    Services Hover JS
		================================================== */
		let image_hover_view = document.querySelector(".service-hover-wrapper");
		if (image_hover_view) {
			const link = document.querySelectorAll('.service-hover-item');
			const linkHoverReveal = document.querySelectorAll('.service-hover-wrapper');
			const linkImages = document.querySelectorAll('.service-hover-placeholder');
			for (let i = 0; i < link.length; i++) {
				link[i].addEventListener('mousemove', (e) => {
					linkHoverReveal[i].style.opacity = 1;
					linkHoverReveal[i].style.transform = `translate(-100%, -50% ) rotate(-3deg)`;
					linkImages[i].style.transform = 'scale(1, 1)';
					linkHoverReveal[i].style.left = e.clientX + "px";
				})
				link[i].addEventListener('mouseleave', (e) => {
					linkHoverReveal[i].style.opacity = 0;
					linkHoverReveal[i].style.transform = `translate(-50%, -50%) rotate(5deg)`;
					linkImages[i].style.transform = 'scale(0.8, 0.8)';
				})
			}
		}


		/* ==================================================
		    Scroll Smooth Init
		================================================== */
		var width = $(window).width();
		if (width > 1023) {
			let smooth_scroll_animation = document.querySelector(".smooth-scroll-container");
			if (smooth_scroll_animation) {
				ScrollSmoother.create({
					content: ".smooth-scroll-container",
					smooth: 1
				});
			}
		}
		


	}); // end document ready function


	$(window).scroll(function() {

		/* ==================================================
		    Background Zoom Init
		================================================== */
		let background_Zoom = document.querySelector("#js-hero");
		if (background_Zoom) {
			var scroll = $(window).scrollTop();
			$("#js-hero").css({
				width: (100 + scroll / 18) + "%"
			})
		}

		/* ==================================================
		    Image Move Init
		================================================== */
		let image_Move = document.querySelector(".bg-static");
		if (image_Move) {
			$(".bg-static").each(function() {
				var windowTop = $(window).scrollTop();
				var elementTop = $(this).offset().top;
				var leftPosition = windowTop - elementTop;
				$(this).find(".bg-move").css({left: leftPosition});
			});
		}

		
	})

	/* ==================================================
        Preloader Init
     ===============================================*/
	 function loader() {
		$(window).on('load', function() {
			$('#avrix-preloader').addClass('loaded');
			$("#loading").fadeOut(500);
			// Una vez haya terminado el preloader aparezca el scroll

			if ($('#avrix-preloader').hasClass('loaded')) {
				// Es para que una vez que se haya ido el preloader se elimine toda la seccion preloader
				$('#preloader').delay(900).queue(function() {
					$(this).remove();
				});
			}
		});
	}
	loader();

})(jQuery); // End jQuery