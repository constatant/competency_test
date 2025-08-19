// Mobile menu toggle
(function(){
  const header = document.querySelector('.site-header');
  const btn = document.querySelector('.nav-toggle');
  if (btn){
    btn.addEventListener('click', () => {
      const open = header.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }
})();

document.addEventListener('click', (e) => {
  if (e.target.classList.contains('copy-btn')) {
    const id = e.target.getAttribute('data-target');
    const input = document.getElementById(id);
    if (input) {
      input.select();
      navigator.clipboard.writeText(input.value);
    }
  }
});
