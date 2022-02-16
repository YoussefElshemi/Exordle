for (const form of document.forms) {
  form.addEventListener("input", ({ data, target }) => {
    if (!data) return;

    if (target.value !== "") {
      const next = target.nextElementSibling;
      const nextParent = target.parentElement.nextElementSibling;

      if (next && next.nodeName === "INPUT") return next.focus();
      if (!next && nextParent) return nextParent.children[1].focus();
    }

  });
}