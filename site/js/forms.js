(function () {
  var next = window.location.origin + "/thank-you/";
  document.querySelectorAll('form[action*="formsubmit.co"]').forEach(function (form) {
    var field = form.querySelector('input[name="_next"]');
    if (field) field.value = next;
  });
})();
