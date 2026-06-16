document.addEventListener("DOMContentLoaded", () => {

  // MOBILE DROPDOWN
  document.querySelectorAll(".mobile-dropdown-header").forEach(header => {
    header.addEventListener("click", function(e) {
      if (e.target.tagName !== "A") {
        const parent = this.parentElement;

        document.querySelectorAll(".mobile-dropdown").forEach(drop => {
          if (drop !== parent) drop.classList.remove("active");
        });

        parent.classList.toggle("active");
      }
    });
  });

  // NAVBAR SCROLL
  const navbar = document.getElementById("navbar");

  if (navbar) {
    window.addEventListener("scroll", () => {
      navbar.classList.toggle("scrolled", window.scrollY > 20);
    });
  }

  // MOBILE MENU
  const toggle = document.getElementById("menuToggle");
  const mobileMenu = document.getElementById("mobileMenu");

  if (toggle && mobileMenu) {
    toggle.addEventListener("click", () => {
      mobileMenu.classList.toggle("show");
    });
  }

  // STATS COUNTER
  const statsSection = document.querySelector(".stats");
  const counters = document.querySelectorAll(".counter");

  if (statsSection && counters.length > 0) {
    const startCounter = () => {
      counters.forEach(counter => {
        const target = +counter.getAttribute("data-target");
        let count = 0;

        const update = () => {
          const increment = target / 100;

          if (count < target) {
            count += increment;
            counter.innerText = Math.floor(count);
            requestAnimationFrame(update);
          } else {
            counter.innerText = target;
          }
        };

        update();
      });
    };

    const observer = new IntersectionObserver(entries => {
      if (entries[0].isIntersecting) {
        startCounter();
        observer.disconnect();
      }
    });

    observer.observe(statsSection);
  }

  // TESTIMONIAL AUTO SCROLL
  const track = document.querySelector(".testimonial-track");

  if (track) {
    track.addEventListener("mouseenter", () => {
      track.style.animationPlayState = "paused";
    });

    track.addEventListener("mouseleave", () => {
      track.style.animationPlayState = "running";
    });
  }

  // BACK TO TOP
const backToTop = document.getElementById("backToTop");
const progressBar = document.querySelector(".progress-bar");

if (backToTop && progressBar) {
  const circleLength = window.innerWidth <= 768 ? 132 : 157;

  window.addEventListener("scroll", () => {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const scrollPercent = docHeight > 0 ? scrollTop / docHeight : 0;

    progressBar.style.strokeDashoffset =
      circleLength - circleLength * scrollPercent;

    if (scrollTop > 300) {
      backToTop.classList.add("show");
    } else {
      backToTop.classList.remove("show");
    }
  });

  backToTop.onclick = function () {
    window.scrollTo({
      top: 0,
      behavior: "smooth"
    });
  };
}
});