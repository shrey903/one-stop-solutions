// ---- Testimonials bar: pulls top-rated feedback and auto-rotates ----
const T_ROOT = document.getElementById("testimonialsRoot");

if (T_ROOT) {
  let items = [];
  let activeIndex = 0;
  let rotateTimer = null;

  function initials(name) {
    return name.trim().split(/\s+/).slice(0, 2).map(w => w[0].toUpperCase()).join("");
  }

  function starsMarkup(rating) {
    let out = "";
    for (let i = 1; i <= 5; i++) out += i <= rating ? '<i class="bi bi-star-fill"></i> ' : '<i class="bi bi-star"></i> ';
    return out;
  }

  function render() {
    if (!items.length) {
      T_ROOT.innerHTML = `<p class="t-empty">No feedback yet — be the first to <a href="/feedback.html">share your experience</a>.</p>`;
      return;
    }

    const slides = items.map((f, i) => `
      <div class="t-slide ${i === activeIndex ? "active" : ""}" data-index="${i}">
        <div class="t-slide__row">
          <div class="t-avatar">${initials(f.name)}</div>
          <div class="t-body">
            <div class="t-stars">${starsMarkup(f.rating)}</div>
            <p class="t-quote">"${f.message}"</p>
            <div class="t-meta">
              <span class="t-name">${f.name}</span>
              <span>·</span>
              <span class="t-service">${f.service}</span>
            </div>
          </div>
        </div>
      </div>
    `).join("");

    const dots = items.map((_, i) => `<button class="t-dot ${i === activeIndex ? "active" : ""}" data-index="${i}" aria-label="Show testimonial ${i + 1}"></button>`).join("");

    T_ROOT.innerHTML = `
      ${slides}
      <div class="t-controls">
        <div class="t-dots">${dots}</div>
        <div class="t-arrows">
          <button class="t-arrow" id="tPrev" aria-label="Previous"><i class="bi bi-arrow-left"></i></button>
          <button class="t-arrow" id="tNext" aria-label="Next"><i class="bi bi-arrow-right"></i></button>
        </div>
      </div>
    `;

    T_ROOT.querySelectorAll(".t-dot").forEach(dot => {
      dot.addEventListener("click", () => { setActive(Number(dot.dataset.index)); resetRotation(); });
    });
    const prevBtn = document.getElementById("tPrev");
    const nextBtn = document.getElementById("tNext");
    if (prevBtn) prevBtn.addEventListener("click", () => { setActive((activeIndex - 1 + items.length) % items.length); resetRotation(); });
    if (nextBtn) nextBtn.addEventListener("click", () => { setActive((activeIndex + 1) % items.length); resetRotation(); });
  }

  function setActive(i) {
    activeIndex = i;
    T_ROOT.querySelectorAll(".t-slide").forEach(el => el.classList.toggle("active", Number(el.dataset.index) === activeIndex));
    T_ROOT.querySelectorAll(".t-dot").forEach(el => el.classList.toggle("active", Number(el.dataset.index) === activeIndex));
  }

  function resetRotation() {
    if (rotateTimer) clearInterval(rotateTimer);
    // Auto-advance to the next testimonial — no faster than once a minute.
    rotateTimer = setInterval(() => {
      if (!items.length) return;
      setActive((activeIndex + 1) % items.length);
    }, 60000);
  }

  async function fetchTop() {
    try {
      const res = await fetch("/api/feedback/top");
      if (!res.ok) return;
      const data = await res.json();
      const changed = JSON.stringify(data.map(d => d.id)) !== JSON.stringify(items.map(d => d.id));
      items = data;
      if (activeIndex >= items.length) activeIndex = 0;
      if (changed) render();
    } catch (err) {
      // Silent — keep showing whatever is currently rendered.
    }
  }

  fetchTop().then(() => { render(); resetRotation(); });
  // Poll for newly submitted feedback so it appears within seconds.
  setInterval(fetchTop, 8000);
}
