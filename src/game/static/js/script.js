const forms = document.getElementById("forms").children;

// if key is pressed on site
document.addEventListener("keydown", async ({ key }) => {
  if (document.activeElement.nodeName === "BODY") {

    // if it is first entry, focus first box
    if (!forms[0].children[2].children[0].value) {
      forms[0].children[2].children[0].focus();
    } else {

      // backspace across multiple element boxes
      const currentPosition = getRecentElement();
      if (key === "Backspace") {
        if (!(currentPosition.previousElementSibling && currentPosition.value.length && currentPosition.disabled))  {
          const previousForm = currentPosition.parentElement.parentElement.previousElementSibling;
          if (previousForm) {
            const newCurrentPosition = previousForm.children[2].children[previousForm.children[2].children.length - 1];
              
            // only delete if element is editable
            if (!newCurrentPosition.disabled) {
              newCurrentPosition.value = "";
              return newCurrentPosition.focus();
            }
          } else {
            const newCurrentPosition = currentPosition.previousElementSibling;
              
            // only delete if element is editable
            if (!newCurrentPosition.disabled) {
              newCurrentPosition.value = "";
              return newCurrentPosition.focus();
            }
          }
        } else {
          currentPosition.value = "";
          return currentPosition.focus();
        }
          
        currentPosition.previousElementSibling.value = "";
        return currentPosition.previousElementSibling.focus();
      }
      
      if (currentPosition.value) {
        const previousParent = currentPosition.parentElement.previousElementSibling;
        if (previousParent) {
          await sleep(1);
          return previousParent.children[previousParent.length - 1].focus();
        } else {
          await sleep(1);
          return currentPosition.previousElementSibling.focus();
        }
      }

      currentPosition.focus();
    }
  }
});

function getRecentElement() {
  for (const form of forms) {
    for (const input of form.children[2].children) {
      if (input.hidden) continue;
      if (!input.value) return input;
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
      
      if (!next) submitGuess(form, nextParent);
    
    } else {
      if (target.value && target.previousElementSibling) {
        const next = target.nextElementSibling;
        await sleep(1);

        if (next) next.focus();
      }
    }
  });
}

async function hintButton() {
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
      url: "/qr/",
      method: "POST",
      data,
      success: async ({ svg }) => {
        divElement.innerHTML = svg.replace(/58mm/g, "100%");
      },
      error: console.log
    });

    await sleep(10000);
  }
}

const closeElement = document.getElementById("close");
closeElement.addEventListener("click", () => {
  closeModal();
});


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

const keyboard = document.getElementsByClassName("keyboard")[0];
for (const row of keyboard.children) {
  for (const input of row.children) {
    input.addEventListener("click", () => {
      const currentPosition = getRecentElement();

      if (input.id.length > 1) {
        if (input.id === "backspace") {
          if (!(currentPosition.previousElementSibling && currentPosition.value.length && currentPosition.disabled))  {
            const previousForm = currentPosition.parentElement.parentElement.previousElementSibling;
            if (previousForm) {
              const newCurrentPosition = previousForm.children[2].children[previousForm.children[2].children.length - 1];
                
              // only delete if element is editable
              if (!newCurrentPosition.disabled) {
                newCurrentPosition.value = "";
                return newCurrentPosition.focus();
              }
            } else {
              const newCurrentPosition = currentPosition.previousElementSibling;
                
              // only delete if element is editable
              if (!newCurrentPosition.disabled) {
                newCurrentPosition.value = "";
                return newCurrentPosition.focus();
              }
            }
          } else {
            currentPosition.value = "";
            return currentPosition.focus();
          }
            
          currentPosition.previousElementSibling.value = "";
          return currentPosition.previousElementSibling.focus();
        }

        if (input.id === "enter") {
          const nextParent = currentPosition.parentElement.parentElement;
          const form = currentPosition.parentElement.parentElement.previousElementSibling;
          submitGuess(form, nextParent);
        }
      } else {
        if (currentPosition.disabled) return;
        currentPosition.value = input.id;
      }
    });
  }
}

async function submitGuess(form, nextParent) {
  const data = Object.fromEntries(new FormData(form)); 
  const wordArray = Object.values(data).filter(c => c != " ");
  wordArray.splice(-2);
  const word = wordArray.reduce((a, b) => a + b);

  if (word.length !== form.children[2].children.length) return;

  $.ajax({
    type: "POST",
    url: "/check/",
    data,
    success: async responseJSON => {
      let won = true;

      for (const input of form) {
        input.disabled = true;
      }

      for (const [position, value] of Object.entries(responseJSON)) {
        if (["correct", "wrong"].includes(value)) won = false;

        const idx = Number(position) - 1;
        const inputElement = form.children[2].children[idx];

        inputElement.classList.add("result");
        await sleep(300);
        inputElement.classList.add(value);
        await sleep(200);
        inputElement.classList.remove("result");

        const keyboardElement = document.getElementById(inputElement.value);     

        if (keyboardElement && !keyboardElement.classList.length) {
          keyboardElement.classList.add(value);
        } else {
          const currentClass = keyboardElement.classList[0];

          if (currentClass === "correct" && value === "perfect") {
            keyboardElement.classList.remove(currentClass);
            keyboardElement.classList.add(value);
          } 

          if (currentClass === "wrong" && value === "correct") {
            keyboardElement.classList.remove(currentClass);
            keyboardElement.classList.add(value);
          }
        }
      }

      if (won) {
        document.body.removeChild(keyboard);
        const hintButton = document.getElementById("hint");
        hintButton.innerText = "CHECK IN";
        return hintButton.onclick = () => {
          if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(({ coords: { latitude, longitude } }) => {
              const data = {
                latitude,
                longitude,
                csrfmiddlewaretoken: getCookie("csrftoken")
              }

              $.ajax({
                type: "POST",
                url: "/check_in",
                data,
                success: async ({ success, distance }) => {
                  if (success) {
                    alert("You are in the right place");
                  } else {
                    alert(`You are ${distance}m from the correct place`);
                  }
                },
                error: console.log
              });
            }, (err) => {
              console.log(err);
              alert("Please enable GPS");
            }, {
              maximumAge: 0, 
              timeout: 5000, 
              enableHighAccuracy: true
            });
          } else {
            alert("Please enable GPS");
          }
        }
      }
        
      if (nextParent) {              
        for (const input of nextParent) {
          input.disabled = false;
        }

        nextParent.children[2].children[0].focus();
      }
    },
    error: console.log
  });
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