// Role cards interactions (index page only)
(function(){
  document.querySelectorAll('.role').forEach(role => {
    role.addEventListener('click', () => {
      const link = role.querySelector('.btn');
      if (link) link.click();
    });
    role.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault(); role.click();
      }
    });
  });
})();