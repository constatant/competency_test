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