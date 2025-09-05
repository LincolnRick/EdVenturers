(function(){
  function EvCarousel(root){
    this.root = root.closest('.ev-carousel');
    this.track = root.querySelector('.ev-carousel__track');
    this.slides = Array.from(root.querySelectorAll('.ev-carousel__slide'));
    this.prevBtn = this.root.querySelector('[data-ev-prev]');
    this.nextBtn = this.root.querySelector('[data-ev-next]');
    this.dotsWrap = this.root.querySelector('.ev-carousel__dots');
    this.dots = Array.from(this.root.querySelectorAll('[data-ev-dot]'));
    this.index = 0;
    this.count = this.slides.length;
    this.x = 0; this.startX = 0; this.delta = 0; this.dragging = false;
    this.init();
  }
  EvCarousel.prototype.init = function(){
    if(this.count <= 1){
      this.prevBtn?.classList.add('hidden');
      this.nextBtn?.classList.add('hidden');
      this.dotsWrap?.classList.add('hidden');
    }
    this.update();
    this.prevBtn?.addEventListener('click', ()=> this.go(this.index-1));
    this.nextBtn?.addEventListener('click', ()=> this.go(this.index+1));
    this.dots.forEach(d => d.addEventListener('click', ()=> this.go(parseInt(d.dataset.evDot))));
    // teclado
    this.root.addEventListener('keydown', (e)=>{
      if(e.key==='ArrowLeft'){ this.go(this.index-1); }
      if(e.key==='ArrowRight'){ this.go(this.index+1); }
      if(e.key==='Escape'){ closeLightbox(); }
    });
    // swipe
    const viewport = this.root.querySelector('.ev-carousel__viewport');
    viewport.addEventListener('touchstart', (e)=>{ this.startX = e.touches[0].clientX; this.dragging = true; }, {passive:true});
    viewport.addEventListener('touchmove', (e)=>{ if(!this.dragging) return; this.delta = e.touches[0].clientX - this.startX; }, {passive:true});
    viewport.addEventListener('touchend', ()=>{
      if(!this.dragging) return; this.dragging=false;
      if(this.delta > 40) this.go(this.index-1);
      else if(this.delta < -40) this.go(this.index+1);
      this.delta = 0;
    });
    // lightbox open
    this.slides.forEach((s,i)=>{
      s.addEventListener('click', ()=>{
        openLightbox(this, i);
      });
    });
  };
  EvCarousel.prototype.go = function(i){
    if(this.count===0) return;
    this.index = (i + this.count) % this.count;
    this.update();
  };
  EvCarousel.prototype.update = function(){
    const offset = this.index * -100;
    this.track.style.transform = `translateX(${offset}%)`;
    this.dots.forEach((d,idx)=> d.setAttribute('aria-selected', idx===this.index ? 'true' : 'false'));
  };

  // Lightbox
  const lb = document.getElementById('ev-lightbox');
  const lbStage = lb?.querySelector('.ev-lightbox__stage');
  let lbCarousel = null;

  function openLightbox(carousel, index){
    if(!lb || !lbStage) return;
    lbCarousel = carousel;
    lb.removeAttribute('hidden');
    renderLB(index);
  }
  function closeLightbox(){
    if(!lb) return;
    lb.setAttribute('hidden','');
    lbStage.innerHTML='';
    lbCarousel = null;
  }
  function renderLB(index){
    if(!lbCarousel) return;
    lbCarousel.index = index;
    lbCarousel.update();
    const slide = lbCarousel.slides[index];
    const media = slide.querySelector('img,video');
    lbStage.innerHTML = '';
    if(media.tagName.toLowerCase()==='img'){
      const img = document.createElement('img');
      img.src = media.currentSrc || media.src;
      img.alt = media.alt || '';
      lbStage.appendChild(img);
    }else{
      const v = document.createElement('video');
      v.controls = true;
      v.src = media.querySelector('source')?.src || media.src;
      lbStage.appendChild(v);
    }
  }
  document.querySelectorAll('[data-ev-close]').forEach(b=> b.addEventListener('click', closeLightbox));
  document.querySelector('[data-ev-lb-prev]')?.addEventListener('click', ()=> renderLB((lbCarousel.index-1+lbCarousel.count)%lbCarousel.count));
  document.querySelector('[data-ev-lb-next]')?.addEventListener('click', ()=> renderLB((lbCarousel.index+1)%lbCarousel.count));
  lb?.addEventListener('click', (e)=>{ if(e.target.classList.contains('ev-lightbox__backdrop')) closeLightbox(); });
  window.addEventListener('keydown', (e)=>{ if(e.key==='Escape') closeLightbox(); });

  // boot
  document.querySelectorAll('[data-ev-carousel]').forEach(vp => new EvCarousel(vp));
})();
