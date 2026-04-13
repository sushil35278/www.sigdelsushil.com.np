(function ($) {

  "use strict";

  // Header Type = Fixed
  $(window).scroll(function () {
    var scroll = $(window).scrollTop();
    var box = $('.header-text').height();
    var header = $('header').height();

    if (scroll >= box - header) {
      $("header").addClass("background-header");
    } else {
      $("header").removeClass("background-header");
    }
  });


  $('.loop').owlCarousel({
    center: true,
    items: 1,
    loop: true,
    autoplay: true,
    autoplayTimeout: 4000,
    autoplayHoverPause: true,
    nav: true,
    margin: 20,
    responsive: {
      1200: {
        items: 3
      },
      992: {
        items: 3
      },
      760: {
        items: 2
      }
    }
  });


  // Menu Dropdown Toggle
  if ($('.menu-trigger').length) {
    $(".menu-trigger").on('click', function () {
      $(this).toggleClass('active');
      $('.header-area .nav').slideToggle(200);
    });
  }


  // Menu elevator animation
  $('.scroll-to-section a[href*=\\#]:not([href=\\#])').on('click', function () {
    if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
      if (target.length) {
        var width = $(window).width();
        if (width < 991) {
          $('.menu-trigger').removeClass('active');
          $('.header-area .nav').slideUp(200);
        }
        $('html,body').animate({
          scrollTop: (target.offset().top) + 1
        }, 700);
        return false;
      }
    }
  });

  function onScroll(event) {
    var scrollPos = $(document).scrollTop();
    $('.nav a').each(function () {
      var currLink = $(this);
      var refElement = $(currLink.attr("href"));
      if (refElement.length && refElement.position().top <= scrollPos && refElement.position().top + refElement.height() > scrollPos) {
        $('.nav ul li a').removeClass("active");
        currLink.addClass("active");
      }
      else {
        currLink.removeClass("active");
      }
    });
  }

  // Acc
  $(document).on("click", ".naccs .menu div", function () {
    var numberIndex = $(this).index();

    if (!$(this).hasClass("active")) {
      $(".naccs .menu div").removeClass("active");
      $(".naccs ul li").removeClass("active");

      $(this).addClass("active");
      $(".naccs ul").find("li:eq(" + numberIndex + ")").addClass("active");

      var listItemHeight = $(".naccs ul")
        .find("li:eq(" + numberIndex + ")")
        .innerHeight();
      $(".naccs ul").height(listItemHeight + "px");
    }
  });


  // Page loading animation
  $(window).on('load', function () {
    $('#js-preloader').addClass('loaded');
  });

  // Theme Toggle Logic
  const initTheme = () => {
    const themeToggle = document.getElementById('theme-toggle');
    const themeToggleMobile = document.getElementById('theme-toggle-mobile');
    const currentTheme = localStorage.getItem('theme') || 'light';

    if (currentTheme === 'dark') {
      document.documentElement.setAttribute('data-theme', 'dark');
      updateThemeIcons('dark');
    }

    const toggleTheme = () => {
      let theme = document.documentElement.getAttribute('data-theme');
      if (theme === 'dark') {
        document.documentElement.setAttribute('data-theme', 'light');
        localStorage.setItem('theme', 'light');
        updateThemeIcons('light');
      } else {
        document.documentElement.setAttribute('data-theme', 'dark');
        localStorage.setItem('theme', 'dark');
        updateThemeIcons('dark');
      }
    };

    if (themeToggle) themeToggle.addEventListener('click', toggleTheme);
    if (themeToggleMobile) themeToggleMobile.addEventListener('click', toggleTheme);
  };

  const updateThemeIcons = (theme) => {
    const icons = document.querySelectorAll('.theme-toggle i');
    icons.forEach(icon => {
      if (theme === 'dark') {
        icon.classList.remove('fa-moon');
        icon.classList.add('fa-sun');
      } else {
        icon.classList.remove('fa-sun');
        icon.classList.add('fa-moon');
      }
    });
  };

  // Particles.js Init
  const initParticles = () => {
    if (document.getElementById('particles-js') && typeof particlesJS !== 'undefined') {
      particlesJS('particles-js', {
        "particles": {
          "number": { "value": 80, "density": { "enable": true, "value_area": 800 } },
          "color": { "value": "#fa65b1" },
          "shape": { "type": "circle" },
          "opacity": { "value": 0.5, "random": false },
          "size": { "value": 3, "random": true },
          "line_linked": { "enable": true, "distance": 150, "color": "#726ae3", "opacity": 0.4, "width": 1 },
          "move": { "enable": true, "speed": 2, "direction": "none", "random": false, "straight": false, "out_mode": "out", "bounce": false }
        },
        "interactivity": {
          "detect_on": "canvas",
          "events": { "onhover": { "enable": true, "mode": "grab" }, "onclick": { "enable": true, "mode": "push" }, "resize": true },
          "modes": { "grab": { "distance": 140, "line_linked": { "opacity": 1 } }, "push": { "particles_nb": 4 } }
        },
        "retina_detect": true
      });
    }
  };

  // Skill Bar Animation Trigger
  const initSkillAnimations = () => {
    const skillProgress = document.querySelectorAll('.progress');
    if (!skillProgress.length) return;

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('animate');
        }
      });
    }, { threshold: 0.5 });

    skillProgress.forEach(progress => {
      observer.observe(progress);
    });
  };

  // Hacker Terminal Logic
  const initTerminal = () => {
    const termInput = document.getElementById('term-input');
    const termBody = document.getElementById('term-body');
    if (!termInput || !termBody) return;

    termInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        const cmd = termInput.value.toLowerCase().trim();
        const line = document.createElement('p');
        line.innerHTML = `<span class="prompt">></span> ${termInput.value}`;
        termBody.appendChild(line);
        termInput.value = '';

        const response = document.createElement('p');
        response.className = 'response';

        switch (cmd) {
          case 'help':
            response.innerHTML = 'Available: help, bio, skills, matrix, clear, contact';
            break;
          case 'matrix':
            response.innerHTML = 'Executing Matrix Sequence...';
            setTimeout(() => {
              toggleMatrixMode();
            }, 500);
            break;
          case 'bio':
            response.innerHTML = 'Sushil Sigdel | Full Stack Dev & System Engineer based in Japan.';
            break;
          case 'skills':
            response.innerHTML = 'Python, Django, PHP, Laravel, JS, AI/ML, AWS...';
            break;
          case 'contact':
            response.innerHTML = 'Email: sigsushil98@gmail.com';
            break;
          case 'clear':
            termBody.innerHTML = '';
            return;
          default:
            response.innerHTML = `Unknown command: ${cmd}. Type 'help'.`;
        }
        termBody.appendChild(response);
        termBody.scrollTop = termBody.scrollHeight;
      }
    });
  };

  // Matrix Mode Logic
  let matrixInterval;
  const toggleMatrixMode = () => {
    const body = document.body;
    const canvas = document.getElementById('matrix-canvas');
    if (!canvas) return;

    if (body.classList.contains('matrix-mode')) {
      body.classList.remove('matrix-mode');
      canvas.style.display = 'none';
      clearInterval(matrixInterval);
    } else {
      body.classList.add('matrix-mode');
      canvas.style.display = 'block';
      initMatrix(canvas);
    }
  };

  const initMatrix = (canvas) => {
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const katakana = 'アァカサタナハマヤャラワガザダバパイィキシチニヒミリヰギジヂビピウゥクスツヌフムユュルグズヅブプエェケセテネヘメレヱゲゼデベペオォコソトノホモヨョロヲゴゾドボポヴッン';
    const nums = '0123456789';
    const alphabet = katakana + nums;

    const fontSize = 16;
    const columns = canvas.width / fontSize;
    const rainDrops = [];

    for (let x = 0; x < columns; x++) {
      rainDrops[x] = 1;
    }

    const draw = () => {
      ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      ctx.fillStyle = '#0F0';
      ctx.font = fontSize + 'px monospace';

      for (let i = 0; i < rainDrops.length; i++) {
        const text = alphabet.charAt(Math.floor(Math.random() * alphabet.length));
        ctx.fillText(text, i * fontSize, rainDrops[i] * fontSize);

        if (rainDrops[i] * fontSize > canvas.height && Math.random() > 0.975) {
          rainDrops[i] = 0;
        }
        rainDrops[i]++;
      }
    };

    window.addEventListener('resize', () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    });

    matrixInterval = setInterval(draw, 30);
  };
  const initTyped = () => {
    if (document.getElementById('typed')) {
      const isJapanese = window.location.pathname.includes('index-ja.html');
      const strings = isJapanese
        ? ["システムエンジニア", "フルスタックエンジニア", "AI/ML愛好家", "ソリューションアーキテクト"]
        : ["System Engineer", "Full Stack Developer", "AI/ML Enthusiast", "Solution Architect"];

      new Typed('#typed', {
        strings: strings,
        typeSpeed: 60,
        backSpeed: 40,
        loop: true,
        backDelay: 2000
      });
    }
  };

  $(document).ready(function () {
    $(document).on("scroll", onScroll);
    initTheme();
    initParticles();
    initSkillAnimations();
    initTerminal();
    initTyped();

    // Vanilla Tilt
    if (typeof VanillaTilt !== 'undefined') {
      VanillaTilt.init(document.querySelectorAll(".portfolio-item"), {
        max: 15,
        speed: 400,
        glare: true,
        "max-glare": 0.3,
      });
    }

    // Smooth scroll fix
    $('.scroll-to-section a[href^="#"]').on('click', function (e) {
      e.preventDefault();
      $(document).off("scroll");

      $('.scroll-to-section a').each(function () {
        $(this).removeClass('active');
      })
      $(this).addClass('active');

      var target = this.hash;
      var $target = $(target);
      if ($target.length) {
        $('html, body').stop().animate({
          scrollTop: ($target.offset().top) + 1
        }, 500, 'swing', function () {
          window.location.hash = target;
          $(document).on("scroll", onScroll);
        });
      }
    });

  });

})(window.jQuery);
