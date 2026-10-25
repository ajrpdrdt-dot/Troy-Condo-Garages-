/* Fires the "Calls from site" Google Ads conversion when a visitor clicks
   the business phone number (tel:6512478384) anywhere on the site.
   Does NOT fire for the financing partner's number (Alliance Bank / Gordon Boos). */
(function () {
  var TRACKED_NUMBER = "6512478384";
  var CONVERSION_LABEL = "AW-18398757431/4jBRCPOK7fAcELeEm8VE";

  function isTrackedTelLink(el) {
    if (!el || !el.getAttribute) return false;
    var href = el.getAttribute("href") || "";
    return href.replace(/[^0-9]/g, "").endsWith(TRACKED_NUMBER);
  }

  document.addEventListener("click", function (event) {
    var el = event.target.closest ? event.target.closest('a[href^="tel:"]') : null;
    if (!isTrackedTelLink(el)) return;
    if (typeof window.gtag === "function") {
      window.gtag("event", "conversion", {
        send_to: CONVERSION_LABEL,
        value: 1.0,
        currency: "USD",
      });
    }
  });
})();
