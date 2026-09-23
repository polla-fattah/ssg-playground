(function () {
  var form = document.getElementById("contact-form");
  var status = document.getElementById("contact-status");

  if (!form || !status) {
    return;
  }

  var address = form.dataset.address;

  function valueOf(id) {
    var field = document.getElementById(id);
    return field ? field.value.trim() : "";
  }

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    var name = valueOf("contact-name");
    var subject = valueOf("contact-subject");
    var message = valueOf("contact-message");

    if (name === "" || subject === "" || message === "") {
      status.textContent = "Please fill in your name, a subject, and a message.";
      status.className = "contact-error";
      return;
    }

    if (!address) {
      status.textContent = "This form is not configured with an address yet.";
      status.className = "contact-error";
      return;
    }

    var body = message + "\n\n-- \n" + name;
    var href =
      "mailto:" + address +
      "?subject=" + encodeURIComponent(subject) +
      "&body=" + encodeURIComponent(body);

    status.textContent = "Opening your email program. Nothing has been sent yet.";
    status.className = "";
    window.location.href = href;
  });
})();
