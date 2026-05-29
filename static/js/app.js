const navToggle = document.querySelector("[data-nav-toggle]");
const navMenu = document.querySelector("[data-nav-menu]");

if (navToggle && navMenu) {
  navToggle.setAttribute("aria-expanded", "false");
  navToggle.addEventListener("click", () => {
    navMenu.classList.toggle("is-open");
    navToggle.setAttribute("aria-expanded", navMenu.classList.contains("is-open") ? "true" : "false");
  });

  navMenu.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      navMenu.classList.remove("is-open");
      navToggle.setAttribute("aria-expanded", "false");
    });
  });
}

const revealItems = document.querySelectorAll("[data-reveal]");
if ("IntersectionObserver" in window && revealItems.length) {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.16 }
  );

  revealItems.forEach((item) => observer.observe(item));
} else {
  revealItems.forEach((item) => item.classList.add("is-visible"));
}

const projectResults = document.getElementById("project-results");
const projectSearch = document.getElementById("project-search");
const projectCategory = document.getElementById("project-category");

function projectCardMarkup(project) {
  const tags = project.stack
    .map((item) => `<span>${item}</span>`)
    .join("");

  return `
    <article class="project-card accent-${project.accent}">
      <p class="project-category">${project.category}</p>
      <h3>${project.title}</h3>
      <p>${project.description}</p>
      <p class="project-impact">${project.impact}</p>
      <div class="tag-row">${tags}</div>
    </article>
  `;
}

async function refreshProjects() {
  if (!projectResults || !projectSearch || !projectCategory) {
    return;
  }

  const params = new URLSearchParams();
  if (projectSearch.value.trim()) {
    params.set("q", projectSearch.value.trim());
  }
  if (projectCategory.value.trim()) {
    params.set("category", projectCategory.value.trim());
  }

  try {
    const response = await fetch(`/api/projects?${params.toString()}`);
    const data = await response.json();
    if (!data.projects.length) {
      projectResults.innerHTML = `<div class="panel"><p>No projects matched your search yet.</p></div>`;
      return;
    }

    projectResults.innerHTML = data.projects.map(projectCardMarkup).join("");
  } catch (error) {
    projectResults.innerHTML = `<div class="panel"><p>Unable to load filtered projects right now.</p></div>`;
  }
}

if (projectSearch && projectCategory) {
  projectSearch.addEventListener("input", refreshProjects);
  projectCategory.addEventListener("change", refreshProjects);
}
