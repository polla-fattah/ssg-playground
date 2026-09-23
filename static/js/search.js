(function () {
  var form = document.querySelector(".search-form");
  var input = document.getElementById("search-query");
  var list = document.getElementById("search-index");
  var status = document.getElementById("search-status");

  if (!form || !input || !list || !status) {
    return;
  }

  var items = list.querySelectorAll(".search-item");

  function filter() {
    var query = input.value.trim().toLowerCase();
    var shown = 0;

    items.forEach(function (item) {
      var match = query === "" || item.textContent.toLowerCase().includes(query);
      item.hidden = !match;
      if (match) {
        shown += 1;
      }
    });

    if (query === "") {
      status.textContent = "Showing all " + items.length + " pages.";
    } else if (shown === 0) {
      status.textContent = "No pages match that word.";
    } else {
      status.textContent = shown + " of " + items.length + " pages match.";
    }
  }

  form.addEventListener("submit", function (event) {
    event.preventDefault();
  });

  input.addEventListener("input", filter);
  filter();
})();
