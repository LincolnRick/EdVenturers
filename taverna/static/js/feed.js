document.addEventListener('DOMContentLoaded', () => {
  const sk = document.getElementById('feed-skeleton');
  const grid = document.getElementById('feed-grid');
  if (sk && grid) { sk.classList.add('hidden'); grid.classList.remove('hidden'); }

  const form = document.getElementById('filter-form');
  const hidden = document.getElementById('hidden-fields');
  const active = document.getElementById('active-filters');
  function rebuildHidden(){
    hidden.innerHTML = ''; active.innerHTML = '';
    document.querySelectorAll('.chip-active').forEach(ch => {
      const name = ch.dataset.name, value = ch.dataset.value;
      const input = document.createElement('input');
      input.type='hidden'; input.name=name; input.value=value; hidden.appendChild(input);
      const pill = document.createElement('span');
      pill.className='inline-flex items-center gap-2 rounded-full bg-gray-100 px-3 py-1 text-sm';
      pill.textContent = ch.textContent.trim();
      const x = document.createElement('button'); x.type='button'; x.textContent='×';
      x.className='text-gray-500'; x.onclick=()=>{ ch.classList.remove('chip-active'); ch.classList.add('chip'); rebuildHidden(); };
      pill.appendChild(x); active.appendChild(pill);
    });
  }
  document.querySelectorAll('.chip-btn').forEach(chip=>{
    chip.addEventListener('click', ()=>{
      chip.classList.toggle('chip-active');
      chip.classList.toggle('chip');
      rebuildHidden();
    });
  });
  rebuildHidden();

  // Autocomplete perfis
  const search = document.getElementById('user-search');
  const box = document.getElementById('user-suggestions');
  let timer;
  async function fetchUsers(q){
    try{
      const r = await fetch(`/api/users/search?q=${encodeURIComponent(q)}`);
      if(!r.ok) return box.classList.add('hidden');
      const data = await r.json();
      box.innerHTML = (data.results||[]).map(u=>`
        <button type="button" class="w-full text-left px-3 py-2 hover:bg-gray-100" data-name="${u.name}" data-email="${u.email}">
          <div class="font-medium">${u.name}</div>
          <div class="text-xs text-gray-500">${u.email}</div>
        </button>`).join('');
      box.classList.toggle('hidden', !(data.results||[]).length);
      box.querySelectorAll('button').forEach(btn=>{
        btn.onclick=()=>{ search.value = btn.dataset.name; box.classList.add('hidden'); };
      });
    }catch{ box.classList.add('hidden'); }
  }
  search?.addEventListener('input', ()=>{
    clearTimeout(timer);
    const q = search.value.trim();
    if(q.length<2){ box.classList.add('hidden'); return; }
    timer = setTimeout(()=>fetchUsers(q), 180);
  });
});
