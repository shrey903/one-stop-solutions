// ---- Scroll-reveal animations ----
if (window.AOS) AOS.init({ duration: 650, once: true, offset: 60, easing: "ease-out-cubic" });

// ---- Footer year ----
document.querySelectorAll("#year").forEach(el => { el.textContent = new Date().getFullYear(); });

// ---- Mobile nav toggle ----
const navToggle = document.getElementById("navToggle");
const navTabs = document.getElementById("navTabs");
if (navToggle && navTabs) {
  navToggle.addEventListener("click", () => navTabs.classList.toggle("open"));
}

// ---- Mobile: tap "Services" to expand dropdown instead of hover ----
const servicesDropdown = document.getElementById("servicesDropdown");
if (servicesDropdown) {
  const trigger = servicesDropdown.querySelector(".nav-tab");
  trigger.addEventListener("click", (e) => {
    if (window.innerWidth <= 991) {
      e.preventDefault();
      servicesDropdown.classList.toggle("open");
    }
  });
}
