const closeHelpElement = document.getElementById("closeHelp");
closeHelpElement.addEventListener("click", () => {
  closeHelpModal();
});

window.onclick = event => {
  const backgroundElement = document.getElementsByClassName("container")[0];
  if (event.target == backgroundElement) {
    closeHelpModal();
  }
}

function closeHelpModal() {
  const modalElement = document.getElementById("helpModal");
  modalElement.style.display = "none";
}

function helpButton() {
  const modalElement = document.getElementById("helpModal");
  modalElement.style.display = "block";    
}