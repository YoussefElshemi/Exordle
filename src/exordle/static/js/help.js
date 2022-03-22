const closeHelpElement = document.getElementById("closeHelp");
closeHelpElement.addEventListener("click", () => {
  closeModal();
});

window.onclick = event => {
  const backgroundElement = document.getElementsByClassName("container")[0];
  if (event.target == backgroundElement) {
    closeModal(document.getElementById("helpModal"));
    closeModal();
  }
}

function closeModal() {
  const modalElement = document.getElementById("helpModal");
  modalElement.style.display = "none";
}

function helpButton() {
  const modalElement = document.getElementById("helpModal");
  modalElement.style.display = "block";    
}
