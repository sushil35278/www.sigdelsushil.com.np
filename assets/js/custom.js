(function ($) {

  "use strict";

  // Throttle function to improve performance
  const throttle = (func, limit) => {
    let inThrottle;
    return function () {
      const args = arguments;
      const context = this;
      if (!inThrottle) {
        func.apply(context, args);
        inThrottle = true;
        setTimeout(() => inThrottle = false, limit);
      }
    }
  }

  // Header Type = Fixed
  $(window).scroll(throttle(function () {
    var scroll = $(window).scrollTop();
    var box = $('.header-text').height();
    var header = $('header').height();

    if (scroll >= box - header) {
      $("header").addClass("background-header");
    } else {
      $("header").removeClass("background-header");
    }
  }, 50));


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

  const initHeroToggle = () => {
    const wrappers = document.querySelectorAll('.hero-image-wrapper');
    if (!wrappers.length) return;

    const img1 = 'hero_final.png';
    const img2 = 'portfolio_hero_new.png';

    wrappers.forEach(wrapper => {
      wrapper.addEventListener('click', function (e) {
        // If click was on a link hotspot, let it pass
        if (e.target.closest('.h-link')) return;

        const img = this.querySelector('#hero-img-toggle');
        if (!img) return;

        img.style.opacity = '0';
        setTimeout(() => {
          if (img.src.includes(img1)) {
            img.src = 'assets/images/' + img2;
          } else {
            img.src = 'assets/images/' + img1;
          }
          img.style.opacity = '1';
        }, 500);
      });
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
    $(document).on("scroll", throttle(onScroll, 100));
    initTheme();
    initParticles();
    initSkillAnimations();
    initTerminal();
    initHeroToggle();
    initTyped();

    // Vanilla Tilt
    if (typeof VanillaTilt !== 'undefined') {
      VanillaTilt.init(document.querySelectorAll(".portfolio-item, .hero-image-wrapper"), {
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

    // Global state for pagination
    let currentBlogPage = 1;
    const blogsPerPage = 4;

    // Load dynamic blogs from JSON
    const loadBlogs = (page = 1) => {
      // If page is an event object (from $(window).on('load')), default to 1
      const pageNum = (typeof page === 'number') ? page : 1;

      currentBlogPage = pageNum;
      const blogContainer = $('#blog-container');
      const pagContainer = $('#blog-pagination');
      if (!blogContainer.length) return;

      const isJapanese = $('html').attr('lang') === 'ja';
      const seeMoreText = isJapanese ? '詳細はこちら...' : 'see more...';
      const discoverMoreText = isJapanese ? 'さらに発見' : 'Discover More';
      const byText = isJapanese ? '投稿者:' : 'By:';

      fetch('assets/data/blogs.json')
        .then(response => response.json())
        .then(blogs => {
          if (!blogs || blogs.length === 0) {
            blogContainer.html(`<div class="col-lg-12 text-center"><p>${isJapanese ? 'ブログ記事が見つかりませんでした。' : 'No blogs found.'}</p></div>`);
            pagContainer.empty();
            return;
          }

          blogContainer.empty();
          pagContainer.empty();

          // Pagination logic
          const totalPages = Math.ceil(blogs.length / blogsPerPage);
          const startIndex = (pageNum - 1) * blogsPerPage;
          const paginatedBlogs = blogs.slice(startIndex, startIndex + blogsPerPage);

          if (pageNum === 1) {
            // --- PAGE 1: Featured + Sidebar Layout ---
            const popularBlogs = blogs.filter(b => b.isPopular).slice(0, 2);
            const featuredBlog = popularBlogs.length > 0 ? popularBlogs[0] : blogs[0];
            const sideBlogs = blogs.filter(b => b.id !== featuredBlog.id).slice(0, 3);

            let featuredHtml = `
              <div class="col-lg-6 show-up wow fadeInUp" data-wow-duration="1s" data-wow-delay="0.3s">
                <div class="blog-post">
                  <div class="thumb">
                    <a href="${featuredBlog.link}" target="_blank" rel="noopener">
                      <img src="${featuredBlog.image}" alt="${featuredBlog.title}" width="550" height="350" loading="lazy" decoding="async" onerror="this.src='assets/images/bloghome.png'">
                    </a>
                  </div>
                  <div class="down-content">
                    <span class="category">${featuredBlog.category}</span>
                    <span class="date">${featuredBlog.date}</span>
                    <a href="${featuredBlog.link}" target="_blank" rel="noopener">
                      <h4>${featuredBlog.title}</h4>
                    </a>
                    <p>${featuredBlog.summary}... <a href="${featuredBlog.link}" target="_blank" rel="noopener"> ${seeMoreText}</a></p>
                    <span class="author">
                      <img src="assets/images/sushil.JPG" alt="${featuredBlog.author}" width="40" height="40" loading="lazy" decoding="async">
                      ${byText} ${featuredBlog.author}
                    </span>
                    <div class="border-first-button">
                      <a href="${featuredBlog.link}" target="_blank" rel="noopener">${discoverMoreText}</a>
                    </div>
                  </div>
                </div>
              </div>
            `;
            blogContainer.append(featuredHtml);

            if (sideBlogs.length > 0) {
              let sideContainerHtml = `
                <div class="col-lg-6 wow fadeInUp" data-wow-duration="1s" data-wow-delay="0.3s">
                  <div class="blog-posts">
                    <div class="row" id="side-blogs-list"></div>
                  </div>
                </div>
              `;
              blogContainer.append(sideContainerHtml);
              const sideList = $('#side-blogs-list');

              sideBlogs.forEach((blog, index) => {
                const isLast = (index === 2 || index === sideBlogs.length - 1);
                sideList.append(createPostItemHtml(blog, isLast, seeMoreText));
              });
            }
          } else {
            // --- PAGE 2+: Uniform Grid Layout ---
            let gridHtml = `<div class="col-lg-12"><div class="row"></div></div>`;
            const $gridRow = $(gridHtml).appendTo(blogContainer).find('.row');

            paginatedBlogs.forEach((blog) => {
              let itemHtml = `
                <div class="col-lg-6">
                  ${createPostItemHtml(blog, false, seeMoreText)}
                </div>
              `;
              $gridRow.append(itemHtml);
            });
          }

          renderPagination(totalPages, pageNum, pagContainer);

          // Re-trigger WOW animations for newly added dynamic content
          if (window.wow && typeof window.wow.start === 'function') {
            window.wow.start();
          }
        })
        .catch(error => {
          console.error('Error loading blogs:', error);
          blogContainer.html(`<div class="col-lg-12 text-center"><p>${isJapanese ? 'エラーが発生しました。' : 'An error occurred while loading blogs.'}</p></div>`);
        });
    };

    // Helper: Create Small Post Item HTML
    const createPostItemHtml = (blog, isLast, seeMoreText) => {
      return `
        <div class="col-lg-12">
          <div class="post-item ${isLast ? 'last-post-item' : ''}">
            <div class="thumb">
              <a href="${blog.link}" target="_blank" rel="noopener">
                <img src="${blog.image}" alt="${blog.title}" width="150" height="150" style="object-fit: cover;" loading="lazy" decoding="async" onerror="this.src='assets/images/bloghome.png'">
              </a>
            </div>
            <div class="right-content">
              <div class="blog-meta-wrapper">
                <span class="category">${blog.category}</span>
                <span class="date">${blog.date}</span>
              </div>
              <a href="${blog.link}" target="_blank" rel="noopener">
                <h4>${blog.title}</h4>
              </a>
              <p>${blog.summary}... <a href="${blog.link}" target="_blank" rel="noopener">${seeMoreText}</a></p>
            </div>
          </div>
        </div>
      `;
    };

    // Helper: Render Pagination Controls
    const renderPagination = (totalPages, currentPage, container) => {
      if (totalPages <= 1) return;

      let paginationHtml = `<ul class="pagination-list">`;

      // Previous button
      if (currentPage > 1) {
        paginationHtml += `<li><a href="#blog" onclick="loadBlogs(${currentPage - 1})"><i class="fa fa-angle-left"></i></a></li>`;
      }

      // Page numbers
      for (let i = 1; i <= totalPages; i++) {
        paginationHtml += `<li><a href="#blog" class="${i === currentPage ? 'active' : ''}" onclick="loadBlogs(${i})">${i}</a></li>`;
      }

      // Next button
      if (currentPage < totalPages) {
        paginationHtml += `<li><a href="#blog" onclick="loadBlogs(${currentPage + 1})"><i class="fa fa-angle-right"></i></a></li>`;
      }

      paginationHtml += `</ul>`;
      container.html(paginationHtml);
    };

    // Expose to global for onclick events
    window.loadBlogs = loadBlogs;

    // --- Cookie Consent Logic ---
    const initCookieConsent = () => {
      const isJapanese = $('html').attr('lang') === 'ja';
      const cookieKey = 'cookie_consent_accepted';

      if (localStorage.getItem(cookieKey)) return;

      const message = isJapanese
        ? 'このウェブサイトでは、ユーザーエクスペリエンスの向上と広告のパーソナライズのためにクッキーを使用しています。詳細は <a href="privacy-policy.html">プライバシーポリシー</a> をご覧ください。'
        : 'This website uses cookies to ensure you get the best experience and to personalize ads. Check our <a href="privacy-policy.html">Privacy Policy</a> for details.';
      const btnText = isJapanese ? '同意する' : 'Accept';

      const bannerHtml = `
        <div id="cookie-consent-banner" class="cookie-consent">
          <p>${message}</p>
          <button class="btn-accept" id="btn-accept-cookies">${btnText}</button>
        </div>
      `;

      $('body').append(bannerHtml);

      // Delay to trigger animation
      setTimeout(() => {
        $('#cookie-consent-banner').addClass('show');
      }, 1000);

      $('#btn-accept-cookies').on('click', function () {
        localStorage.setItem(cookieKey, 'true');
        $('#cookie-consent-banner').removeClass('show');
        setTimeout(() => $('#cookie-consent-banner').remove(), 500);
      });
    };

    // Scroll to Top Logic with Progress Circle
    const initScrollTop = () => {
      const scrollTopBtn = document.getElementById('scroll-top');
      const progressPath = document.querySelector('.progress-circle path');
      if (!scrollTopBtn || !progressPath) return;

      const pathLength = progressPath.getTotalLength();
      progressPath.style.strokeDasharray = `${pathLength} ${pathLength}`;
      progressPath.style.strokeDashoffset = pathLength;

      const updateProgress = () => {
        const scroll = window.pageYOffset;
        const height = document.documentElement.scrollHeight - window.innerHeight;
        const progress = pathLength - (scroll * pathLength / height);
        progressPath.style.strokeDashoffset = progress;

        if (scroll > 300) {
          scrollTopBtn.classList.add('active');
        } else {
          scrollTopBtn.classList.remove('active');
        }
      };

      scrollTopBtn.addEventListener('click', () => {
        window.scrollTo({
          top: 0,
          behavior: 'smooth'
        });
      });

      window.addEventListener('scroll', throttle(updateProgress, 10));
      updateProgress();
    };

    $(window).on('load', () => {
      loadBlogs(1);
      initCookieConsent();
      initScrollTop();
    });

  });

})(window.jQuery);

// Newsletter Form Handler
const setupNewsletter = (formId, successId) => {
  const form = document.getElementById(formId);
  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const btn = form.querySelector('button');
      const originalBtnText = btn.textContent;
      btn.textContent = $('html').attr('lang') === 'ja' ? '登録中...' : 'Subscribing...';
      btn.disabled = true;

      // Use Formspree AJAX submission
      fetch('https://formspree.io/f/mlgaeeag', {
        method: 'POST',
        body: new FormData(form),
        headers: { 'Accept': 'application/json' }
      })
        .then(response => {
          if (response.ok) {
            form.style.display = 'none';
            document.getElementById(successId).style.display = 'block';
          } else {
            throw new Error('Form submission failed');
          }
        })
        .catch(error => {
          console.error('Error:', error);
          btn.textContent = $('html').attr('lang') === 'ja' ? 'エラー' : 'Error';
          setTimeout(() => {
            btn.textContent = originalBtnText;
            btn.disabled = false;
          }, 2000);
        });
    });
  }
};

setupNewsletter('newsletter-form', 'nl-success');
setupNewsletter('newsletter-form-ja', 'nl-success-ja');
