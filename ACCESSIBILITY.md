# Accessibility Commitment (ACCESSIBILITY.md)

## 1. Our commitment

We believe accessibility is a subset of quality. This project commits to **WCAG 2.2 AA** standards for all documentation and web-based visualizations. The VINDSNURR rotor is an open-source hardware project — our documentation and HTML tools should be usable by everyone.

## 2. Current status

| Component | Status |
| :--- | :--- |
| HTML visualizations (`docs/`) | Dark/light mode toggle implemented; keyboard accessible |
| Colour contrast (light mode) | Targets WCAG AA (4.5:1 normal text, 3:1 large text) |
| Colour contrast (dark mode) | Targets WCAG AA |
| Theme preference | Respects `prefers-color-scheme`; persisted via `localStorage` |
| Screen reader support | SVG icons marked `aria-hidden`; buttons have dynamic `aria-label` |
| Keyboard navigation | Toggle reachable by Tab; activatable by Enter/Space |
| Focus indicators | 2px solid outline with theme-aware colour |
| Markdown documentation | Plain text; readable by all tools |

## 3. Dark/light mode implementation

All seven HTML files in `docs/` share a single `site.css` stylesheet and `site.js` script. The sun/moon theme toggle in the top-right corner is implemented once in `site.js` and applies consistently across every page. The implementation follows these principles:

- **Respects system preference** via `prefers-color-scheme` media query
- **User override persisted** in `localStorage` — choice survives page reload
- **System changes followed** only when no manual override has been set
- **`aria-label` is dynamic** — describes the action, not the current state ("Switch to dark mode" / "Switch to light mode")
- **SVG icons are `aria-hidden="true"`** — the button's accessible name comes from `aria-label` alone
- **Focus ring** uses a theme-aware CSS custom property (`--focus-ring`) at 2px solid, offset 2px
- **CSS custom properties** drive all colour decisions — no hardcoded colours in component styles

Reference: [Light/Dark Mode Accessibility Best Practices](https://mgifford.github.io/ACCESSIBILITY.md/examples/LIGHT_DARK_MODE_ACCESSIBILITY_BEST_PRACTICES.html)

## 4. Colour contrast targets

| Context | Requirement | Notes |
| :--- | :--- | :--- |
| Body text | 4.5:1 minimum | Both light and dark modes |
| Large text (18pt+ / 14pt+ bold) | 3:1 minimum | Headings, labels |
| UI components (toggle border, focus ring) | 3:1 minimum | Against adjacent background |
| Informational colour (sail colours in visualization) | Not relied on alone | Shapes and labels also used |

The canvas visualization uses colour to distinguish node types and sail families. Labels are rendered alongside colour cues so the diagram is not colour-only.

## 5. Known limitations

- The canvas-based 3D visualization (`docs/viz.html`) is not accessible to screen readers — it renders to a `<canvas>` element with no text alternative. The information it conveys (rotor geometry, node labels, edge types) is fully described in `INSTRUCTIONS.md` and `README.md`.
- The step-by-step guide (`docs/step-by-step.html`) contains SVG diagrams that lack text descriptions for some assembly illustrations. This is a known gap for future improvement.
- No automated accessibility testing is currently configured for this project.

## 6. Reporting issues

If you find an accessibility barrier in any file in this project:

- Open an issue on the project repository
- Describe the barrier, the assistive technology or browser used, and what you expected to happen

## 7. Contributor guidelines

When adding or modifying HTML files in `docs/`:

- Use semantic HTML elements (`<header>`, `<nav>`, `<main>`, `<footer>`, `<button>`, `<table>`)
- Do not convey information by colour alone — always provide a text or shape alternative
- Ensure interactive elements are reachable by keyboard (Tab) and activatable (Enter/Space)
- Test in both light and dark modes before submitting
- New SVG icons must include `aria-hidden="true"` if decorative, or a `<title>` if meaningful
- Maintain a minimum 4.5:1 contrast ratio for all text in both colour modes

## 8. Further reading

- [WCAG 2.2 Quick Reference](https://www.w3.org/WAI/WCAG22/quickref/)
- [ACCESSIBILITY.md project](https://mgifford.github.io/ACCESSIBILITY.md) — template and examples
- [Light/Dark Mode Accessibility Best Practices](https://mgifford.github.io/ACCESSIBILITY.md/examples/LIGHT_DARK_MODE_ACCESSIBILITY_BEST_PRACTICES.html)

---

*Last updated: 2026-04-12*
