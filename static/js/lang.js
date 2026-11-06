// Language preference: if the visitor chose a language before, open the matching page.
// Runs in <head> before paint. Visitors (and search engines) with no saved choice are never redirected.
(function () {
  try {
    var pref = localStorage.getItem("ras-lang");
    var cur = document.documentElement.getAttribute("data-lang");
    if (!pref || pref === cur) return;
    var alt = document.querySelector('link[rel="alternate"][data-lang="' + pref + '"]');
    if (!alt) return;
    var target = new URL(alt.getAttribute("href")).pathname + location.search + location.hash;
    if (target !== location.pathname + location.search + location.hash) location.replace(target);
  } catch (e) { /* storage blocked: just show the page */ }
})();
