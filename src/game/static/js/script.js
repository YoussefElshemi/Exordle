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
    
    const next = target.nextElementSibling;
    if (next && next.nodeName === "INPUT") next.focus();
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
    } else if (key == "Enter") {
      const next = target.nextElementSibling;
      const nextParent = target.parentElement.parentElement.nextElementSibling;
      
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
    } else {
      if (target.value && target.previousElementSibling) {
        const next = target.nextElementSibling;
        await sleep(1);

        if (next) next.focus();
      }
    }
  });
}

const hintButton = document.getElementById("hint");
hintButton.addEventListener("click", async () => {
  const modalElement = document.getElementById("myForm");

  if (modalElement.style.display === "block") return closeModal();

  const form = document.getElementById("submitHint");
  const divElement = document.createElement("div");

  divElement.setAttribute("id", "svg");
  modalElement.insertBefore(divElement, form);
  modalElement.style.display = "block";    


  while (modalElement.style.display === "block") {
    const data = {
      csrfmiddlewaretoken: getCookie("csrftoken")
    }

    $.ajax({
      url: "/qr",
      method: "POST",
      data,
      success: async ({ svg }) => {
        divElement.innerHTML = svg.replace(/58mm/g, "100%");
      },
      error: data => {
        console.log(data);
      }
    });

    await sleep(10000);
  }
});

const closeElement = document.getElementById("close");
closeElement.addEventListener("click", () => {
  closeModal();
})


function closeModal() {
  const modalElement = document.getElementById("myForm");
  modalElement.style.display = "none";

  for (const child of modalElement.children) {
    if (child.nodeName === "FORM") continue;
    modalElement.removeChild(child);
  }
}

const modalElement = document.getElementById("myForm");
window.onclick = event => {
  const backgroundElement = document.getElementsByClassName("parent")[0];
  if (event.target == backgroundElement) closeModal();
}

async function sleep(timeout=2000) {
  return new Promise(res => {
    setTimeout(res, timeout);
  })
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