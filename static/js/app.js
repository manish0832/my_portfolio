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

const typedElement = document.querySelector("[data-typed]");
if (typedElement) {
  const phrases = JSON.parse(typedElement.dataset.typed);
  let phraseIndex = 0;
  let charIndex = 0;
  let deleting = false;

  const tick = () => {
    const current = phrases[phraseIndex];
    typedElement.textContent = deleting
      ? current.slice(0, charIndex--)
      : current.slice(0, charIndex++);

    if (!deleting && charIndex > current.length) {
      deleting = true;
      setTimeout(tick, 1100);
      return;
    }

    if (deleting && charIndex < 0) {
      deleting = false;
      phraseIndex = (phraseIndex + 1) % phrases.length;
      charIndex = 0;
    }

    setTimeout(tick, deleting ? 42 : 78);
  };

  if (!reduceMotion) {
    tick();
  }
}

const counters = document.querySelectorAll("[data-counter]");
if (counters.length && "IntersectionObserver" in window && !reduceMotion) {
  const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) {
        return;
      }

      const element = entry.target;
      const target = Number(element.dataset.counter || 0);
      let current = 0;
      const step = Math.max(1, Math.ceil(target / 30));

      const updateCounter = () => {
        current = Math.min(target, current + step);
        element.textContent = current >= 10 ? `${current}+` : `${current}`;
        if (current < target) {
          requestAnimationFrame(updateCounter);
        } else if (String(element.dataset.counter).includes("0")) {
          element.textContent = `${target}+`;
        }
      };

      updateCounter();
      counterObserver.unobserve(element);
    });
  }, { threshold: 0.4 });

  counters.forEach((counter) => counterObserver.observe(counter));
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

const assistantForm = document.getElementById("assistant-form");
const assistantInput = document.getElementById("assistant-input");
const assistantChat = document.getElementById("assistant-chat");

function appendAssistantBubble(text, role) {
  if (!assistantChat) {
    return;
  }

  const bubble = document.createElement("div");
  bubble.className = `assistant-bubble assistant-bubble-${role}`;
  bubble.textContent = text;
  assistantChat.appendChild(bubble);
  assistantChat.scrollTop = assistantChat.scrollHeight;
}

async function askAssistant(question) {
  appendAssistantBubble(question, "user");
  try {
    const response = await fetch(`/api/assistant?q=${encodeURIComponent(question)}`);
    const data = await response.json();
    appendAssistantBubble(data.answer, "bot");
  } catch (error) {
    appendAssistantBubble("Mandee AI is unavailable for a moment. Please try again.", "bot");
  }
}

if (assistantForm && assistantInput) {
  assistantForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const question = assistantInput.value.trim();
    if (!question) {
      return;
    }
    assistantInput.value = "";
    await askAssistant(question);
  });

  document.querySelectorAll("[data-assistant-prompt]").forEach((button) => {
    button.addEventListener("click", async () => {
      await askAssistant(button.dataset.assistantPrompt || "");
    });
  });
}
