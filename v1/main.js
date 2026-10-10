/* Pletánky.cz – ukázka vzhledu. Lehké vanilla JS, převoditelné do Shoptetu (vlastní JS v patičce). */
(function () {
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const FREE = 2000;
  const fmt = n => n.toLocaleString('cs-CZ', { maximumFractionDigits: 2 }) + ' Kč';

  /* rozdělení nadpisu na slova pro animaci */
  $$('[data-split]').forEach(h => {
    let i = 0;
    const wrap = node => {
      [...node.childNodes].forEach(n => {
        if (n.nodeType === 3) {
          const frag = document.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach(t => {
            if (!t) return;
            if (/^\s+$/.test(t)) { frag.append(' '); return; }
            const w = document.createElement('span'); w.className = 'w';
            const s = document.createElement('span'); s.textContent = t; s.style.setProperty('--i', i++);
            w.append(s); frag.append(w);
          });
          n.replaceWith(frag);
        } else if (n.nodeType === 1) wrap(n);
      });
    };
    wrap(h);
  });

  /* hlavička při scrollu */
  const hdr = $('#hdr');
  const sentinel = document.createElement('div');
  sentinel.style.cssText = 'position:absolute;top:120px;height:1px;width:1px';
  document.body.prepend(sentinel);
  new IntersectionObserver(([e]) => hdr.classList.toggle('is-stuck', !e.isIntersecting)).observe(sentinel);

  /* odhalování při scrollu */
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); }
  }), { rootMargin: '0px 0px -8% 0px' });
  $$('.reveal').forEach((el, i) => { el.style.transitionDelay = (i % 4) * 70 + 'ms'; io.observe(el); });

  /* šuplíky */
  const drawers = { menu: $('[data-menu]'), cart: $('[data-cart]'), about: $('[data-about]') };
  const open = k => { drawers[k].classList.add('is-open'); drawers[k].setAttribute('aria-hidden', 'false'); document.body.style.overflow = 'hidden'; };
  const close = k => { drawers[k].classList.remove('is-open'); drawers[k].setAttribute('aria-hidden', 'true'); document.body.style.overflow = ''; };
  Object.keys(drawers).forEach(k => {
    $$(`[data-${k}-open]`).forEach(b => b.addEventListener('click', () => open(k)));
    $$(`[data-${k}-close]`).forEach(b => b.addEventListener('click', () => close(k)));
    drawers[k].addEventListener('click', e => { if (e.target === drawers[k]) close(k); });
  });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') { Object.keys(drawers).forEach(close); filt && filt.classList.remove('is-open'); } });

  /* filtry na mobilu */
  const filt = $('[data-filters]');
  $$('[data-filters-open]').forEach(b => b.addEventListener('click', () => filt.classList.add('is-open')));
  $$('[data-filters-close]').forEach(b => b.addEventListener('click', () => filt.classList.remove('is-open')));

  /* košík (jen naoko, drží se v sessionStorage, aby přežil proklik mezi stránkami) */
  let cart = [];
  try { cart = JSON.parse(sessionStorage.getItem('pl-cart') || '[]'); } catch (e) {}
  const render = () => {
    const total = cart.reduce((s, i) => s + i.price * i.qty, 0);
    const count = cart.reduce((s, i) => s + i.qty, 0);
    $$('[data-cart-count]').forEach(el => el.textContent = count);
    $$('[data-cart-total]').forEach(el => el.textContent = fmt(total));
    const left = Math.max(0, FREE - total);
    $('[data-free-txt]').innerHTML = left > 0 ? `Do dopravy zdarma zbývá <b>${fmt(left)}</b>` : '<b>Máte dopravu zdarma!</b> 🎉';
    $('[data-free-bar]').style.width = Math.min(100, total / FREE * 100) + '%';
    const list = $('[data-cart-list]');
    list.innerHTML = cart.length ? cart.map(i => `<li class="ci"><img src="${i.img}" alt=""><span><b>${i.name}</b><small>${i.qty} × ${fmt(i.price)}</small></span><strong>${fmt(i.price * i.qty)}</strong></li>`).join('')
      : '<li class="cartlist__empty">Košík je zatím prázdný. Přidejte si první klubíčko 🧶</li>';
    sessionStorage.setItem('pl-cart', JSON.stringify(cart));
  };
  const toast = $('[data-toast]'); let tt;
  $$('[data-add]').forEach(b => b.addEventListener('click', () => {
    const qi = b.hasAttribute('data-qty-from') ? $('[data-qty-input]') : null;
    const qty = Math.max(1, parseInt(qi ? qi.value : 1, 10) || 1);
    const it = cart.find(i => i.name === b.dataset.name);
    if (it) it.qty += qty; else cart.push({ name: b.dataset.name, price: +b.dataset.price, img: b.dataset.img, qty });
    render();
    const cb = $('.cartbtn'); cb.classList.remove('is-bump'); void cb.offsetWidth; cb.classList.add('is-bump');
    if (b.classList.contains('pcard__add')) { b.classList.add('is-done'); setTimeout(() => b.classList.remove('is-done'), 1400); }
    toast.textContent = 'Přidáno do košíku';
    toast.classList.add('is-on'); clearTimeout(tt); tt = setTimeout(() => toast.classList.remove('is-on'), 2600);
  }));
  render();

  /* množství */
  $$('[data-qty]').forEach(b => b.addEventListener('click', () => {
    const i = $('[data-qty-input]'); i.value = Math.max(1, (parseInt(i.value, 10) || 1) + +b.dataset.qty);
  }));

  /* slidery produktů */
  $$('[data-rail]').forEach(r => {
    const sec = r.closest('section');
    const step = () => r.querySelector('.pcard').offsetWidth + 20;
    $('[data-rail-next]', sec)?.addEventListener('click', () => r.scrollBy({ left: step() * 2, behavior: 'smooth' }));
    $('[data-rail-prev]', sec)?.addEventListener('click', () => r.scrollBy({ left: -step() * 2, behavior: 'smooth' }));
  });

  /* záložky na detailu */
  $$('[data-tabs]').forEach(t => {
    const btns = $$('[data-tab]', t), panels = $$('.tabs__panel', t);
    btns.forEach((b, i) => b.addEventListener('click', () => {
      btns.forEach(x => x.classList.toggle('is-on', x === b));
      panels.forEach((p, j) => p.classList.toggle('is-on', j === i));
    }));
  });

  /* galerie na detailu */
  const main = $('.pd__main img');
  $$('.pd__thumbs button').forEach(b => b.addEventListener('click', () => {
    $$('.pd__thumbs button').forEach(x => x.classList.toggle('is-on', x === b));
    main.src = b.querySelector('img').src;
  }));

  /* řazení – jen přepínání stavu */
  $$('.sort button').forEach(b => b.addEventListener('click', () => $$('.sort button').forEach(x => x.classList.toggle('is-on', x === b))));
})();
