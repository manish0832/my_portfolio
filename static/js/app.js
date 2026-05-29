const navToggle = document.querySelector("[data-nav-toggle]");
const navMenu = document.querySelector("[data-nav-menu]");

if (navToggle && navMenu) {
  navToggle.setAttribute("aria-expanded", "false");

  navToggle.addEventListener("click", () => {
    const isOpen = navMenu.classList.toggle("is-open");
    navToggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
  });

  navMenu.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      navMenu.classList.remove("is-open");
      navToggle.setAttribute("aria-expanded", "false");
    });
  });

  window.addEventListener("resize", () => {
    if (window.innerWidth > 760) {
      navMenu.classList.remove("is-open");
      navToggle.setAttribute("aria-expanded", "false");
    }
  });
}

const revealItems = document.querySelectorAll("[data-reveal]");
const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

if (!reduceMotion && "IntersectionObserver" in window && revealItems.length) {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12, rootMargin: "0px 0px -5% 0px" }
  );

  revealItems.forEach((item) => observer.observe(item));
} else {
  revealItems.forEach((item) => item.classList.add("is-visible"));
}

const projectResults = document.getElementById("project-results");
const projectSearch = document.getElementById("project-search");
const projectCategory = document.getElementById("project-category");
const projectStatus = document.getElementById("project-status");

function projectCardMarkup(project) {
  const tags = project.stack.map((item) => `<span>${item}</span>`).join("");

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
  const query = projectSearch.value.trim();
  const category = projectCategory.value.trim();

  if (query) {
    params.set("q", query);
  }
  if (category) {
    params.set("category", category);
  }

  if (projectStatus) {
    projectStatus.textContent = "Loading filtered projects...";
  }

  try {
    const response = await fetch(`/api/projects?${params.toString()}`);
    const data = await response.json();

    if (!data.projects.length) {
      projectResults.innerHTML = `<div class="feature-card"><h3>No projects matched this filter.</h3><p>Try a different keyword or category.</p></div>`;
      if (projectStatus) {
        projectStatus.textContent = "No matching projects found.";
      }
      return;
    }

    projectResults.innerHTML = data.projects.map(projectCardMarkup).join("");
    if (projectStatus) {
      projectStatus.textContent = `Showing ${data.count} project${data.count === 1 ? "" : "s"}.`;
    }
  } catch (error) {
    projectResults.innerHTML = `<div class="feature-card"><h3>Unable to load projects right now.</h3><p>Please try again in a moment.</p></div>`;
    if (projectStatus) {
      projectStatus.textContent = "Project loading failed.";
    }
  }
}

if (projectSearch && projectCategory) {
  projectSearch.addEventListener("input", refreshProjects);
  projectCategory.addEventListener("change", refreshProjects);
}
