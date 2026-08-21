/* Render local Mermaid blocks after each Material document load. */
window.mermaid.initialize({
  startOnLoad: false,
  securityLevel: "strict",
  theme: "base",
  themeVariables: {
    background: "#fbf7ef",
    primaryColor: "#f0eadf",
    primaryTextColor: "#1b2631",
    primaryBorderColor: "#ad5d2e",
    lineColor: "#17324d",
    secondaryColor: "#e4edf4",
    tertiaryColor: "#ffffff"
  }
});

async function renderHermesMermaid() {
  const nodes = document.querySelectorAll(".mermaid:not([data-processed='true'])");
  if (nodes.length === 0) return;
  try {
    await window.mermaid.run({ nodes });
    document.documentElement.dataset.mermaidReady = "true";
  } catch (error) {
    document.documentElement.dataset.mermaidReady = "false";
    document.documentElement.dataset.mermaidError = String(error && error.message || error);
    console.error("Hermes Mermaid rendering failed", error);
  }
}

if (typeof document$ !== "undefined") {
  document$.subscribe(renderHermesMermaid);
} else {
  document.addEventListener("DOMContentLoaded", renderHermesMermaid);
}
