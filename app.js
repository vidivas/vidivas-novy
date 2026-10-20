(function(){
var els=document.querySelectorAll('.reveal');
if(!('IntersectionObserver' in window)){els.forEach(function(e){e.classList.add('in')});}
else{var o=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');o.unobserve(x.target)}})},{threshold:.1});els.forEach(function(e){o.observe(e)});}
var f=document.getElementById('poptavka-form');
if(f){f.addEventListener('submit',function(ev){ev.preventDefault();var m=f.querySelector('.msg');m.textContent='Odesílám…';
fetch(f.action,{method:'POST',headers:{accept:'application/json'},body:new FormData(f)}).then(function(r){if(!r.ok)throw 0;m.textContent='Děkuji, ozvu se vám do 24 hodin.';f.reset();}).catch(function(){m.innerHTML='Odeslání se nepodařilo. Zavolejte prosím na <a href="tel:+420739878732">739 878 732</a> nebo napište na <a href="mailto:info@vidivas.cz">info@vidivas.cz</a>.';});});}
})();
