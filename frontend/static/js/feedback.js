// ---- Feedback page: service tabs ----
const fbTabs = document.querySelectorAll(".fb-tab");
const fbServiceInput = document.getElementById("fbService");
fbTabs.forEach(tab => {
  tab.addEventListener("click", () => {
    fbTabs.forEach(t => t.classList.remove("active"));
    tab.classList.add("active");
    fbServiceInput.value = tab.dataset.service;
  });
});

// ---- Star picker ----
const starIcons = document.querySelectorAll("#starPicker i");
const ratingInput = document.getElementById("fbRating");
let currentRating = 0;

function paintStars(val) {
  starIcons.forEach(icon => {
    const v = Number(icon.dataset.val);
    icon.classList.toggle("bi-star-fill", v <= val);
    icon.classList.toggle("bi-star", v > val);
    icon.classList.toggle("on", v <= val);
  });
}
starIcons.forEach(icon => {
  icon.addEventListener("mouseenter", () => paintStars(Number(icon.dataset.val)));
  icon.addEventListener("click", () => {
    currentRating = Number(icon.dataset.val);
    ratingInput.value = currentRating;
    paintStars(currentRating);
  });
});
const starPicker = document.getElementById("starPicker");
if (starPicker) {
  starPicker.addEventListener("mouseleave", () => paintStars(currentRating));
}

// ---- Submit feedback ----
const feedbackForm = document.getElementById("feedbackForm");
if (feedbackForm) {
  const fbStatus = document.getElementById("fbStatus");
  const fbSubmitBtn = document.getElementById("fbSubmitBtn");

  feedbackForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    if (currentRating < 1) {
      fbStatus.textContent = "Please select a star rating before submitting.";
      fbStatus.className = "form-status err";
      return;
    }
    if (!feedbackForm.checkValidity()) {
      feedbackForm.reportValidity();
      return;
    }

    const payload = {
      name: document.getElementById("fbName").value.trim(),
      service: fbServiceInput.value,
      rating: currentRating,
      message: document.getElementById("fbMessage").value.trim(),
    };

    fbSubmitBtn.disabled = true;
    fbSubmitBtn.innerHTML = `<span class="spinner-border spinner-border-sm"></span> Submitting…`;
    fbStatus.textContent = "";
    fbStatus.className = "form-status";

    try {
      const res = await fetch("/api/feedback", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail ? JSON.stringify(err.detail) : "Something went wrong.");
      }

      fbStatus.textContent = "✓ Thank you! Your feedback is now live in our testimonials.";
      fbStatus.classList.add("ok");
      feedbackForm.reset();
      currentRating = 0;
      ratingInput.value = 0;
      paintStars(0);
    } catch (err) {
      fbStatus.textContent = "Could not submit right now. Please try again shortly.";
      fbStatus.classList.add("err");
    } finally {
      fbSubmitBtn.disabled = false;
      fbSubmitBtn.innerHTML = `<i class="bi bi-send-check"></i> Submit Feedback`;
    }
  });
}
