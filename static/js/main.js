// main.js

document.addEventListener("DOMContentLoaded", function () {
  // Toggle mobile navbar
  const hamburger = document.querySelector("#hamburger");
  const navLinks = document.querySelector("#nav-links");

  if (hamburger && navLinks) {
    hamburger.addEventListener("click", () => {
      navLinks.classList.toggle("show");
    });
  }

  // Show toast (for later use)
  const toast = (message, type = "info") => {
    const toast = document.createElement("div");
    toast.className = `toast ${type}`;
    toast.innerText = message;

    document.body.appendChild(toast);
    setTimeout(() => {
      toast.remove();
    }, 3000);
  };

  // Sample usage
  // toast("Welcome to Book Catalogue!", "success");

  // Handle form submission (if any)
  const bookForm = document.querySelector("#book-form");
  if (bookForm) {
    bookForm.addEventListener("submit", (e) => {
      e.preventDefault();
      toast("Book submitted!", "success");
    });
  }

  // Future: Add animations, filtering, etc. here
});
