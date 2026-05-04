// MOBILE DROPDOWN (FIXED)
document.querySelectorAll(".mobile-dropdown-header").forEach(header => {

  header.addEventListener("click", function(e) {

    // prevent navigation only if arrow clicked
    if (e.target.tagName !== "A") {

      const parent = this.parentElement;

      // CLOSE ALL FIRST
      document.querySelectorAll(".mobile-dropdown").forEach(drop => {
        if (drop !== parent) {
          drop.classList.remove("active");
        }
      });

      // TOGGLE CURRENT
      parent.classList.toggle("active");

      // ROTATE ARROW
      const arrow = this.querySelector(".dropdown-arrow");
      arrow.classList.toggle("rotate");

    }

  });

});

// SCROLL EFFECT
const navbar = document.getElementById("navbar");

window.addEventListener("scroll", () => {
  if (window.scrollY > 20) {
    navbar.classList.add("scrolled");
  } else {
    navbar.classList.remove("scrolled");
  }
});

// MOBILE MENU TOGGLE
const toggle = document.getElementById("menuToggle");
const mobileMenu = document.getElementById("mobileMenu");

toggle.addEventListener("click", () => {
  mobileMenu.classList.toggle("show");
});

// STAST REAL TIME COUNTER

const counters = document.querySelectorAll(".counter");

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
        counter.innerText = target + "+";
      }
    };

    update();
  });
};

/* TRIGGER ON SCROLL */
const statsSection = document.querySelector(".stats");

const observer = new IntersectionObserver(entries => {
  if (entries[0].isIntersecting) {
    startCounter();
    observer.disconnect();
  }
});

observer.observe(statsSection);

// AUTO SCROLL TESTIMONIALS

const track = document.querySelector(".testimonial-track");

track.addEventListener("mouseenter", () => {
  track.style.animationPlayState = "paused";
});

track.addEventListener("mouseleave", () => {
  track.style.animationPlayState = "running";
});


 

 