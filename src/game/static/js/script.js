const forms = document.getElementById("forms").children;

document.addEventListener("keydown", async () => {
  if (document.activeElement.nodeName === "BODY") {
    if (!forms[0].children[2].children[0].value) {
      forms[0].children[2].children[0].focus();
    } else {
      const element = getRecentElement();
      if (element.value) {
        const previousParent = element.parentElement.previousElementSibling;
        if (previousParent) {
          await sleep(1);
          return previousParent.children[previousParent.length - 1].focus();
        } else {
          await sleep(1);
          return element.previousElementSibling.focus();
        }
      }

      element.focus();
    }
  }
});

function getRecentElement() {
  for (const form of forms) {
    for (const input of form.children[2].children) {
      if (input.hidden) continue;

      if (!input.value) {
        return input;
      }
    }
  }
}

for (const form of forms) {
  form.addEventListener("input", ({ data, target }) => {
    if (!data) return;

    if (target.value !== "") {
      const next = target.nextElementSibling;
      const nextParent = target.parentElement.parentElement.nextElementSibling;

      if (next && next.nodeName === "INPUT") next.focus();

      if (!next) {
        const data = Object.fromEntries(new FormData(form));   
        const wordArray = Object.values(data).filter(c => c != " ");
        wordArray.splice(-2);
        const word = wordArray.reduce((a, b) => a + b);

        if (word.length !== form.children[2].children.length) return;

        $.ajax({
          type: "POST",
          url: "/check",
          data,
          success: async responseJSON => {
            for (const input of form) {
              input.disabled = true;
            }

            for (const [position, value] of Object.entries(responseJSON)) {
              const idx = Number(position) - 1;
              const inputElement = form.children[2].children[idx];

              inputElement.classList.add("result");
              await sleep(300);
              inputElement.classList.add(value);
              await sleep(200);
              inputElement.classList.remove("result");
            }
      
            if (nextParent) {              
              for (const input of nextParent) {
                input.disabled = false;
              }

              nextParent.children[2].children[0].focus();
            }
          },
          error: data => {
            console.log(data);
          }
        });
      }
    }
  });

  form.addEventListener("keydown", async ({ key, target }) => {
    if (key == "Backspace" && target.previousElementSibling) {
      const previous = target.previousElementSibling;

      if (previous.nodeName === "INPUT") {
        await sleep(1);
        return previous.focus();
      }
        
      const previousParent = target.parentElement.previousElementSibling;
      if (previous.hidden && previousParent) {
        return previousParent.children[previousParent.length - 1].focus();
      }
    }
  });
}

function getCookie(name) {
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");

    for (let i = 0; i < cookies.length; i++) {
      const cookie = jQuery.trim(cookies[i]);
      if (cookie.substring(0, name.length + 1) === (name + "=")) {
        return decodeURIComponent(cookie.substring(name.length + 1));
      }
    }
  }
}

async function sleep(timeout=2000) {
  return new Promise(res => {
    setTimeout(res, timeout);
  })
}