// Reliable Automotive Services — small progressive enhancements. Site works without JS.
(function () {
  "use strict";
  var KEY = "ras-lang";
  var html = document.documentElement;
  var lang = html.getAttribute("data-lang") || "en";

  function savePref(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }
  function getPref() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }

  // ---- Language: header switch link remembers the choice
  document.querySelectorAll("[data-set-lang]").forEach(function (a) {
    a.addEventListener("click", function () { savePref(a.getAttribute("data-set-lang")); });
  });

  // ---- Language setting (footer select)
  var sel = document.getElementById("lang-select");
  if (sel) {
    sel.addEventListener("change", function () {
      var v = sel.value;
      savePref(v);
      var dest = sel.getAttribute("data-" + v);
      if (dest && v !== lang) window.location.href = dest;
    });
  }

  // ---- Suggest Spanish to Spanish-language browsers that haven't chosen yet
  if (lang === "en" && !getPref()) {
    var langs = (navigator.languages || [navigator.language || ""]).map(function (l) { return String(l).toLowerCase(); });
    var alt = document.querySelector('link[rel="alternate"][data-lang="es"]');
    if (alt && langs.length && langs[0].indexOf("es") === 0) {
      var bar = document.createElement("div");
      bar.className = "lang-suggest";
      bar.setAttribute("role", "region");
      bar.setAttribute("aria-label", "Idioma");
      bar.innerHTML = '<span lang="es">¿Prefiere ver este sitio en español?</span>' +
        '<a class="btn btn-amber" lang="es" href="' + new URL(alt.getAttribute("href")).pathname + '">Ver en español</a>' +
        '<button type="button" class="lang-dismiss">Keep English</button>';
      document.body.insertBefore(bar, document.body.firstChild);
      bar.querySelector("a").addEventListener("click", function () { savePref("es"); });
      bar.querySelector("button").addEventListener("click", function () { savePref("en"); bar.remove(); });
    }
  }

  // ---- Mobile nav toggle
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");
  if (toggle && nav) {
    var openLbl = toggle.getAttribute("data-open") || "Menu";
    var closeLbl = toggle.getAttribute("data-close") || "Close";
    var setOpen = function (open) {
      nav.classList.toggle("open", open);
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.textContent = open ? closeLbl : openLbl;
    };
    toggle.addEventListener("click", function () { setOpen(!nav.classList.contains("open")); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("open")) { setOpen(false); toggle.focus(); }
    });
  }

  // ---- Service request form -> pre-filled text message to the shop's text line
  var form = document.getElementById("request-form");
  if (form) {
    var d = form.dataset;
    var err = form.querySelector(".error");
    var labels = (d.labels || "Name|Callback|Vehicle|Service|Location|Best time|Details").split("|");
    var names = ["name", "phone", "vehicle", "service", "location", "when", "details"];
    var val = function (n) { var el = form.elements[n]; return el ? String(el.value || "").trim() : ""; };
    var buildMessage = function () {
      var lines = [d.intro || "Service request"];
      names.forEach(function (n, i) { var v = val(n); if (v) lines.push(labels[i] + ": " + v); });
      if (d.langLine) lines.push(d.langLine);
      // Optional text-message consent: only added when the visitor checked the box.
      var consent = form.elements.smsConsent;
      if (consent && consent.checked && d.consentLine) lines.push(d.consentLine);
      return lines.join("\n");
    };
    var validate = function () {
      var missing = [];
      if (!val("name")) missing.push(d.mName);
      if (val("phone").replace(/\D/g, "").length < 10) missing.push(d.mPhone);
      if (!val("vehicle")) missing.push(d.mVehicle);
      if (!val("location")) missing.push(d.mLocation);
      if (missing.length) { err.textContent = (d.missing || "Please add {list}.").replace("{list}", missing.join(", ")); return false; }
      err.textContent = "";
      return true;
    };
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!validate()) return;
      // "?&body=" works on both iOS and Android
      window.location.href = "sms:" + (d.sms || "") + "?&body=" + encodeURIComponent(buildMessage());
    });
    var copyBtn = document.getElementById("copy-request");
    if (copyBtn) {
      copyBtn.addEventListener("click", function () {
        if (!validate()) return;
        var text = buildMessage();
        var done = function () { err.textContent = d.copied || "Copied."; };
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(text).then(done, function () { window.prompt(d.copyPrompt, text); });
        } else { window.prompt(d.copyPrompt, text); }
      });
    }
  }

  var y = document.getElementById("year");
  if (y) y.textContent = String(new Date().getFullYear());
})();
