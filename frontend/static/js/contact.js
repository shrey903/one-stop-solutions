// ---- Contact / Enquiry form logic (shared across contact.html + service pages) ----
const TRAVEL_SERVICES = ["Flight Tickets", "Bus Tickets", "Train Tickets"];

const form = document.getElementById("contactForm");
if (form) {
  const serviceSelect = document.getElementById("service");
  const travelFields = document.getElementById("travelFields");
  const isConditional = travelFields && travelFields.dataset.conditional === "true";
  const travelInputs = ["fromStation", "toStation", "journeyDate", "returnDate", "passengers"]
    .map(id => document.getElementById(id))
    .filter(Boolean);

  // Date pickers only exist where flatpickr + the inputs are present
  let journeyPicker, returnPicker;
  if (window.flatpickr && document.getElementById("journeyDate")) {
    journeyPicker = flatpickr("#journeyDate", {
      altInput: true, altFormat: "d M Y", dateFormat: "Y-m-d", minDate: "today",
      onChange: (selectedDates) => { if (returnPicker) returnPicker.set("minDate", selectedDates[0] || "today"); }
    });
    returnPicker = flatpickr("#returnDate", { altInput: true, altFormat: "d M Y", dateFormat: "Y-m-d", minDate: "today" });
  }

  function toggleTravelFields() {
    if (!isConditional || !travelFields) return;
    const isTravel = TRAVEL_SERVICES.includes(serviceSelect.value);
    travelFields.classList.toggle("d-none", !isTravel);
    travelInputs.forEach(input => { input.required = isTravel; });
  }
  if (serviceSelect && isConditional) {
    serviceSelect.addEventListener("change", toggleTravelFields);
    toggleTravelFields();
  }

  const status = document.getElementById("formStatus");
  const submitBtn = document.getElementById("submitBtn");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }

    const isTravel = travelInputs.length > 0 && (isConditional ? TRAVEL_SERVICES.includes(serviceSelect.value) : true);

    const payload = {
      name: document.getElementById("name").value.trim(),
      phone: document.getElementById("phone").value.trim(),
      email: document.getElementById("email").value.trim(),
      service: serviceSelect.value,
      message: document.getElementById("message").value.trim() || null,
      from_station: isTravel ? document.getElementById("fromStation").value.trim() : null,
      to_station: isTravel ? document.getElementById("toStation").value.trim() : null,
      journey_date: isTravel ? document.getElementById("journeyDate").value.trim() : null,
      return_date: isTravel ? document.getElementById("returnDate").value.trim() : null,
      passengers: isTravel ? document.getElementById("passengers").value.trim() : null,
    };

    submitBtn.disabled = true;
    submitBtn.innerHTML = `<span class="spinner-border spinner-border-sm"></span> Submitting…`;
    status.textContent = "";
    status.className = "form-status";

    try {
      const res = await fetch("/api/contact", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail ? JSON.stringify(err.detail) : "Something went wrong.");
      }

      status.textContent = "✓ Enquiry received — we'll reach out shortly.";
      status.classList.add("ok");
      form.reset();
      toggleTravelFields();
    } catch (err) {
      status.textContent = "Could not submit right now. Please try again shortly.";
      status.classList.add("err");
    } finally {
      submitBtn.disabled = false;
      submitBtn.innerHTML = `<i class="bi bi-send-check"></i> Submit Enquiry`;
    }
  });
}
