// ---- Scroll-reveal animations ----
if (window.AOS) AOS.init({ duration: 650, once: true, offset: 60, easing: "ease-out-cubic" });

// ---- Footer year ----
document.querySelectorAll("#year").forEach(el => { el.textContent = new Date().getFullYear(); });

// ---- Mobile nav toggle & outside click handling ----
const navToggle = document.getElementById("navToggle");
const navTabs = document.getElementById("navTabs");
const siteNav = document.getElementById("siteNav");

if (navToggle && navTabs) {
  navToggle.addEventListener("click", (e) => {
    e.stopPropagation();
    navTabs.classList.toggle("open");
  });

  // Close mobile nav when clicking outside
  document.addEventListener("click", (e) => {
    if (navTabs.classList.contains("open") && siteNav && !siteNav.contains(e.target)) {
      navTabs.classList.remove("open");
    }
  });

  // Close nav on direct link click on mobile
  navTabs.querySelectorAll("a:not(#servicesDropdown > .nav-tab)").forEach(link => {
    link.addEventListener("click", () => {
      if (window.innerWidth <= 991) {
        navTabs.classList.remove("open");
      }
    });
  });
}

// ---- Mobile: tap "Services" to expand dropdown instead of hover ----
const servicesDropdown = document.getElementById("servicesDropdown");
if (servicesDropdown) {
  const trigger = servicesDropdown.querySelector(".nav-tab");
  if (trigger) {
    trigger.addEventListener("click", (e) => {
      if (window.innerWidth <= 991) {
        e.preventDefault();
        e.stopPropagation();
        servicesDropdown.classList.toggle("open");
      }
    });
  }
}

