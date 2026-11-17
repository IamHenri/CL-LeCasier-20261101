// Navigation mobile
const toggle = document.querySelector('.nav-toggle');
const nav = document.getElementById('nav');
if (toggle && nav) {
  toggle.addEventListener('click', () => {
    const open = nav.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', open);
  });
}

// Visionneuse de menus (onglets + flèches)
document.querySelectorAll('[data-menu]').forEach(root => {
  const tabs = [...root.querySelectorAll('[role="tab"]')];
  const sheets = [...root.querySelectorAll('.menu-sheet')];
  let current = 0;
  const show = i => {
    current = (i + sheets.length) % sheets.length;
    tabs.forEach((t, k) => t.setAttribute('aria-selected', k === current));
    sheets.forEach((s, k) => s.classList.toggle('is-active', k === current));
  };
  tabs.forEach((t, i) => t.addEventListener('click', () => show(i)));
  root.querySelectorAll('[data-dir]').forEach(b =>
    b.addEventListener('click', () => show(current + Number(b.dataset.dir))));
});
