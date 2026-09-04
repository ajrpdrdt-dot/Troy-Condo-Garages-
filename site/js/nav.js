// Troy Condo Garages — static site mobile nav toggle
(function () {
  document.addEventListener('DOMContentLoaded', function () {
    var toggle = document.querySelector('[data-nav-toggle]');
    var list = document.querySelector('[data-nav-list]');
    if (!toggle || !list) return;

    toggle.addEventListener('click', function () {
      var isOpen = list.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });

    // Close menu when a link is clicked (mobile)
    list.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        list.classList.remove('is-open');
        toggle.setAttribute('aria-expanded', 'false');
      });
    });
  });
})();
