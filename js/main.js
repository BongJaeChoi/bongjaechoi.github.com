const progress = document.querySelector(".progress");
const navLinks = [...document.querySelectorAll(".nav a")];
const sections = navLinks
  .map((link) => document.querySelector(link.getAttribute("href")))
  .filter(Boolean);

const updateProgress = () => {
  const scrollable = document.documentElement.scrollHeight - window.innerHeight;
  const ratio = scrollable > 0 ? window.scrollY / scrollable : 0;
  progress.style.width = `${Math.min(100, Math.max(0, ratio * 100))}%`;
};

const updateActiveNav = () => {
  let current;
  sections.forEach((section) => {
    if (section.getBoundingClientRect().top <= 140) {
      current = section;
    }
  });
  navLinks.forEach((link) => {
    link.classList.toggle("is-active", current && link.getAttribute("href") === `#${current.id}`);
  });
};

window.addEventListener("scroll", () => {
  updateProgress();
  updateActiveNav();
});

updateProgress();
updateActiveNav();
