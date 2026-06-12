// Hamburger menu toggle
const hamburger = document.getElementById('hamburger');
const mobileNav = document.getElementById('mobileNav');
if (hamburger && mobileNav) {
  hamburger.addEventListener('click', () => {
    mobileNav.classList.toggle('open');
  });
}

// Mark active nav link based on current page
const links = document.querySelectorAll('.navbar-nav a, .mobile-nav a');
links.forEach(link => {
  if (link.href === window.location.href) {
    link.classList.add('active');
  }
});
