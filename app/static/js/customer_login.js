// Customer auth page scripts
(function(){
  const form = document.getElementById('auth-form');
  const regBtn = document.getElementById('register-btn');
  const msg = document.getElementById('message');
  if (form){
    form.addEventListener('submit', function(e){
      e.preventDefault();
      const email = document.getElementById('email').value.trim();
      msg.textContent = `Вход с email: ${email}`;
    });
  }
  if (regBtn){
    regBtn.addEventListener('click', function(){
      // navigation handled by link
    });
  }
})();
