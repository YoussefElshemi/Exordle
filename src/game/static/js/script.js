for (const form of document.forms) {
  form.addEventListener("input", ({ data, target }) => {
    if (!data) return;

    if (target.value !== "") {
      const next = target.nextElementSibling;
      const nextParent = target.parentElement.nextElementSibling;

      if (next && next.nodeName === "INPUT") next.focus();

      if (!next) {
        const formData = new FormData(form);
        const data = {
          ...Object.fromEntries(formData.entries()),
          csrfmiddlewaretoken: getCookie("csrftoken")
        };
        
        $.ajax({
          type: "POST",
          url: "/check",
          data,
          success: responseJSON => {
            responseJSON = JSON.parse(responseJSON);
          
            for (const [position, value] of Object.entries(responseJSON)) {
              const idx = Number(position);
              const inputElement = form.children[idx];
              inputElement.classList.add(value);
            }
          },
          error: data => {
            console.log(data);
          }
        });

        nextParent.children[1].focus();
      }
    }

  });
}

function getCookie(name) {
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');

    for (let i = 0; i < cookies.length; i++) {
      const cookie = jQuery.trim(cookies[i]);
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        return decodeURIComponent(cookie.substring(name.length + 1));
      }
    }
  }
}