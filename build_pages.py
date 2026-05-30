#!/usr/bin/env python3
"""
onlinefdr.com.au — Page generator
All pages share the same nav, marquee, entity bar, footer, base CSS and JS.
Page-specific content is injected into the shell.

═══════════════════════════════════════════════════════════════════════════
STAT TILE RULE (sitewide pattern)
═══════════════════════════════════════════════════════════════════════════

Stat tiles use a consistent two-tone treatment everywhere they appear
(WIFDR hero, home social-proof, home why-online, and any future placements).

  RULE: White value leads. Ochre unit tails. Units match parent height.
        Plain word-tiles (e.g. "National", "AGD") stay full white.

  NUMERIC TILE markup:
    <div class="stat-val">18&ndash;36<span class="unit">mo</span></div>
    <div class="stat-val">2<span class="unit">wks</span></div>

  WORD-TILE markup (smaller font, single class to balance visual weight):
    <div class="stat-val text">National</div>
    <div class="stat-val text">AGD</div>

  CSS (each container's stat-val class - hero-stat-val, proof-val,
  why-stat-val - follows the same pattern):
    .{prefix}-val      { font-size: clamp(1.9rem, 3vw, 2.4rem); color: var(--white); font-weight: 800; }
    .{prefix}-val .unit { color: var(--ochre); font-weight: 800; margin-left: 4px; }   // SAME size as parent
    .{prefix}-val.text  { font-size: clamp(1.6rem, 2.6vw, 2.1rem); }                   // word-tiles only

  WHAT THIS RULE IS NOT:
    - Do not use .accent on stat values. .accent is for heading-text emphasis
      (e.g. "<span class='accent'>a lawyer</span>") which intentionally
      reverses to ochre. Stat values lead white.
    - Do not dim units with font-size:60% or rgba opacity. Units match
      parent height in ochre. No shrinking, no fading.
    - Do not give word-tiles a .unit span. Word-tiles are single-colour white
      at the smaller .text size. No tail to colour.
"""

with open('/home/claude/base.css') as f:
    BASE_CSS = f.read()

NAV_LINKS = """
      <li><a href="/about/">About</a></li>
      <li><a href="/what-is-fdr/">What is FDR?</a></li>
      <li><a href="/how-it-works/">How It Works</a></li>
      <li class="nav-has-sub"><button type="button" class="nav-sub-trigger" aria-haspopup="true" aria-expanded="false">Services<svg class="nav-sub-caret" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="6 9 12 15 18 9"/></svg></button>
        <ul class="nav-sub" role="menu">
          <li role="none"><a href="/parenting/" role="menuitem">Parenting</a></li>
          <li role="none"><a href="/financial-settlement/" role="menuitem">Financial Settlement</a></li>
          <li role="none"><a href="/section-60i/" role="menuitem">Section 60I</a></li>
        </ul>
      </li>
      <li><a href="/book/">Book</a></li>
      <li class="nav-has-sub"><button type="button" class="nav-sub-trigger" aria-haspopup="true" aria-expanded="false">Resources<svg class="nav-sub-caret" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="6 9 12 15 18 9"/></svg></button>
        <ul class="nav-sub" role="menu">
          <li role="none"><a href="/faq/" role="menuitem">FAQ</a></li>
          <li role="none"><a href="/blog/" role="menuitem">Blog</a></li>
          <li role="none" class="nav-sub-divider" aria-hidden="true"></li>
          <li role="none"><a href="https://www.facebook.com/onlinefdr/" role="menuitem" target="_blank" rel="noopener noreferrer">Facebook<svg class="nav-sub-ext" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg></a></li>
          <li role="none"><a href="https://www.instagram.com/onlinefdr.com.au/" role="menuitem" target="_blank" rel="noopener noreferrer">Instagram<svg class="nav-sub-ext" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg></a></li>
          <li role="none"><a href="https://www.linkedin.com/company/onlinefdr/" role="menuitem" target="_blank" rel="noopener noreferrer">LinkedIn<svg class="nav-sub-ext" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg></a></li>
        </ul>
      </li>
      <li class="nav-cta-mobile-only"><a href="tel:0399617544" class="nav-cta" aria-label="Call us on 0 3 9 9 6 1 7 5 4 4"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" style="margin-right:6px;vertical-align:-2px"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>(03) 9961 7544</a></li>"""

NAV_CTA = """<a href="tel:0399617544" class="nav-cta" aria-label="Call us on 0 3 9 9 6 1 7 5 4 4"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" style="margin-right:6px;vertical-align:-2px"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>(03) 9961 7544</a>"""

GTAG = """  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=AW-18195606042"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'AW-18195606042');
  </script>"""

MARQUEE_ITEMS = """
      <span class="marquee-item">AGD-Accredited FDRP <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Australian Mediation Association Member <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Section 60I Certificates (s 66H in WA) <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Conducted Securely Online <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Available Anywhere in Australia <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Free Discovery Call <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">No Obligation <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Confidential under the Family Law Act <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Both Parenting and Financial Matters <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">AGD-Accredited FDRP <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Australian Mediation Association Member <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Section 60I Certificates (s 66H in WA) <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Conducted Securely Online <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Available Anywhere in Australia <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Free Discovery Call <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">No Obligation <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Confidential under the Family Law Act <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Both Parenting and Financial Matters <span class="marquee-sep">&bull;</span></span>"""

ENTITY_BAR = """<div class="entity-bar" role="complementary" aria-label="Accreditation">
  <div class="wrap">
    <div class="entity-bar-inner">
      <div class="entity-item"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>AGD-Accredited Family Dispute Resolution Practitioner &middot; Reg. F2003011</div>
      <div class="entity-item"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>Authorised to issue Section 60I Certificates nationally</div>
      <div class="entity-item"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>Serving all Australian states and territories</div>
    </div>
  </div>
</div>"""

FOOTER = """<footer role="contentinfo">
  <div class="wrap">
    <div class="footer-top">
      <div>
        <div class="footer-brand-lockup">
          <svg class="footer-brand-mark" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#C4873A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">
            <path d="m11 17 2 2a1 1 0 1 0 3-3"/>
            <path d="m14 14 2.5 2.5a1 1 0 1 0 3-3l-3.88-3.88a3 3 0 0 0-4.24 0l-.88.88a1 1 0 1 1-3-3l2.81-2.81a5.79 5.79 0 0 1 7.06-.87l.47.28a2 2 0 0 0 1.42.25L21 4"/>
            <path d="m21 3 1 11h-2"/>
            <path d="M3 3 2 14l6.5 6.5a1 1 0 1 0 3-3"/>
            <path d="M3 4h8"/>
          </svg>
          <div class="footer-brand-name">online<span class="brand-fdr">fdr</span>.com.au</div>
        </div>
        <div class="footer-tagline">The call you make before you call a lawyer.</div>
        <p class="footer-desc">Accredited online Family Dispute Resolution, available anywhere in Australia. Registered with the Australian Government Attorney-General's Department.</p>
        <div class="footer-socials">
          <a href="https://www.facebook.com/onlinefdr/" aria-label="Follow onlinefdr.com.au on Facebook" rel="noopener" target="_blank">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true" focusable="false"><path d="M16 8.049c0-4.446-3.582-8.05-8-8.05C3.58 0-.002 3.603-.002 8.05c0 4.017 2.926 7.347 6.75 7.951v-5.625h-2.03V8.05H6.75V6.275c0-2.017 1.195-3.131 3.022-3.131.876 0 1.791.157 1.791.157v1.98h-1.009c-.993 0-1.303.621-1.303 1.258v1.51h2.218l-.354 2.326H9.25V16c3.824-.604 6.75-3.934 6.75-7.951"/></svg>
          </a>
          <a href="https://www.instagram.com/onlinefdr.com.au/" aria-label="Follow onlinefdr.com.au on Instagram" rel="noopener" target="_blank">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true" focusable="false"><path d="M8 0C5.829 0 5.556.01 4.703.048 3.85.088 3.269.222 2.76.42a3.9 3.9 0 0 0-1.417.923A3.9 3.9 0 0 0 .42 2.76C.222 3.268.087 3.85.048 4.7.01 5.555 0 5.827 0 8.001c0 2.172.01 2.444.048 3.297.04.852.174 1.433.372 1.942.205.526.478.972.923 1.417.444.445.89.719 1.416.923.51.198 1.09.333 1.942.372C5.555 15.99 5.827 16 8 16s2.444-.01 3.298-.048c.851-.04 1.434-.174 1.943-.372a3.9 3.9 0 0 0 1.416-.923c.445-.445.718-.891.923-1.417.197-.509.332-1.09.372-1.942C15.99 10.445 16 10.173 16 8s-.01-2.445-.048-3.299c-.04-.851-.175-1.433-.372-1.941a3.9 3.9 0 0 0-.923-1.417A3.9 3.9 0 0 0 13.24.42c-.51-.198-1.092-.333-1.943-.372C10.443.01 10.172 0 7.998 0zm-.717 1.442h.718c2.136 0 2.389.007 3.232.046.78.035 1.204.166 1.486.275.373.145.64.319.92.599s.453.546.598.92c.11.281.24.705.275 1.485.039.843.047 1.096.047 3.231s-.008 2.389-.047 3.232c-.035.78-.166 1.203-.275 1.485a2.5 2.5 0 0 1-.599.919c-.28.28-.546.453-.92.598-.28.11-.704.24-1.485.276-.843.038-1.096.047-3.232.047s-2.39-.009-3.233-.047c-.78-.036-1.203-.166-1.485-.276a2.5 2.5 0 0 1-.92-.598 2.5 2.5 0 0 1-.6-.92c-.109-.281-.24-.705-.275-1.485-.038-.843-.046-1.096-.046-3.233s.008-2.388.046-3.231c.036-.78.166-1.204.276-1.486.145-.373.319-.64.599-.92s.546-.453.92-.598c.282-.11.705-.24 1.485-.276.738-.034 1.024-.044 2.515-.045zm4.988 1.328a.96.96 0 1 0 0 1.92.96.96 0 0 0 0-1.92m-4.27 1.122a4.109 4.109 0 1 0 0 8.217 4.109 4.109 0 0 0 0-8.217m0 1.441a2.667 2.667 0 1 1 0 5.334 2.667 2.667 0 0 1 0-5.334"/></svg>
          </a>
          <a href="https://www.linkedin.com/company/onlinefdr/" aria-label="Follow onlinefdr.com.au on LinkedIn" rel="noopener" target="_blank">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true" focusable="false"><path d="M0 1.146C0 .513.526 0 1.175 0h13.65C15.474 0 16 .513 16 1.146v13.708c0 .633-.526 1.146-1.175 1.146H1.175C.526 16 0 15.487 0 14.854zm4.943 12.248V6.169H2.542v7.225zm-1.2-8.212c.837 0 1.358-.554 1.358-1.248-.015-.709-.52-1.248-1.342-1.248S2.4 3.226 2.4 3.934c0 .694.521 1.248 1.327 1.248zm4.908 8.212V9.359c0-.216.016-.432.08-.586.173-.431.568-.878 1.232-.878.869 0 1.216.662 1.216 1.634v3.865h2.401V9.25c0-2.22-1.184-3.252-2.764-3.252-1.274 0-1.845.7-2.165 1.193v.025h-.016l.016-.025V6.169h-2.4c.03.678 0 7.225 0 7.225z"/></svg>
          </a>
        </div>
      </div>
      <div class="footer-col"><h5>Services</h5><ul>
        <li><a href="/parenting/">Parenting</a></li>
        <li><a href="/financial-settlement/">Financial Settlements</a></li>
        <li><a href="/section-60i/">Section 60I Certificate</a></li>
      </ul></div>
      <div class="footer-col"><h5>Learn</h5><ul>
        <li><a href="/what-is-fdr/">What is FDR?</a></li>
        <li><a href="/how-it-works/">How It Works</a></li>
        <li><a href="/faq/">FAQ</a></li>
        <li><a href="/blog/">Blog</a></li>
        <li><a href="/locations/">Locations</a></li>
        <li><a href="/get-help/">Get Help</a></li>
      </ul></div>
      <div class="footer-col"><h5>Downloads</h5><ul>
        <li><a href="/downloads/onlinefdr-disclosure-worksheet.pdf" download>Disclosure worksheet (PDF)</a></li>
        <li><a href="/downloads/onlinefdr-disclosure-worksheet.docx" download>Disclosure worksheet (Word)</a></li>
        <li><a href="/downloads/onlinefdr-parenting-reflection-workbook.pdf" download>Parenting reflection workbook (PDF)</a></li>
      </ul></div>
      <div class="footer-col"><h5>Contact</h5><ul>
        <li><a href="tel:0399617544">(03) 9961 7544</a></li>
        <li><a href="mailto:hello@onlinefdr.com.au">hello@onlinefdr.com.au</a></li>
        <li><a href="/#discovery">Free Discovery Call</a></li>
        <li><a href="/book/">Book a Session</a></li>
      </ul></div>
    </div>
    <div class="footer-bottom">
      <p class="footer-copy">&copy; 2026 onlinefdr.com.au, Accredited Online Family Dispute Resolution. All rights reserved.</p>
      <div class="footer-legal">
        <a href="/about/">About Us</a>
        <a href="/privacy/">Privacy</a>
        <a href="/terms/">Terms</a>
        <a href="/complaints/">Complaints</a>
      </div>
    </div>
    <div class="footer-meta">
      <p class="footer-abn">Operated by Kevin Scrimshaw, sole trader. ABN 42 961 240 633. AGD FDRP Reg. No. F2003011.</p>
      <p class="footer-disclaimer">Information on this website is provided for general educational purposes only. Nothing on this site should be construed as legal or financial advice. For advice specific to your circumstances, consult a qualified legal or financial professional.</p>
    </div>
  </div>
</footer>"""

BASE_JS = """<script>
  const nav=document.getElementById('nav');
  window.addEventListener('scroll',()=>nav.classList.toggle('scrolled',window.scrollY>20),{passive:true});
  const toggle=document.getElementById('nav-toggle'),navLinks=document.getElementById('nav-links');
  if(toggle&&navLinks){
    toggle.addEventListener('click',()=>{const o=navLinks.classList.toggle('open');toggle.setAttribute('aria-expanded',o)});
    navLinks.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{navLinks.classList.remove('open');toggle.setAttribute('aria-expanded','false')}));
  }
  document.querySelectorAll('.nav-sub-trigger').forEach(t=>{
    const parent=t.parentElement;
    t.addEventListener('click',e=>{e.stopPropagation();const o=parent.classList.toggle('open');t.setAttribute('aria-expanded',o)});
  });
  document.addEventListener('click',e=>{
    document.querySelectorAll('.nav-has-sub.open').forEach(item=>{
      if(!item.contains(e.target)){item.classList.remove('open');item.querySelector('.nav-sub-trigger').setAttribute('aria-expanded','false')}
    });
  });
  document.querySelectorAll('.faq-q').forEach(btn=>{
    btn.addEventListener('click',()=>{
      const item=btn.closest('.faq-item'),isOpen=item.classList.contains('open');
      document.querySelectorAll('.faq-item').forEach(i=>{i.classList.remove('open');i.querySelector('.faq-q').setAttribute('aria-expanded','false')});
      if(!isOpen){item.classList.add('open');btn.setAttribute('aria-expanded','true')}
    });
  });
  const observer=new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add('visible');observer.unobserve(e.target)}}),{threshold:0.1,rootMargin:'0px 0px -48px 0px'});
  document.querySelectorAll('.reveal').forEach(el=>observer.observe(el));
</script>"""

SOCIAL_RAIL = """<aside class="social-rail" aria-label="Follow us on social media">
  <a href="https://www.facebook.com/onlinefdr/" aria-label="Follow onlinefdr.com.au on Facebook" rel="noopener" target="_blank"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true" focusable="false"><path d="M16 8.049c0-4.446-3.582-8.05-8-8.05C3.58 0-.002 3.603-.002 8.05c0 4.017 2.926 7.347 6.75 7.951v-5.625h-2.03V8.05H6.75V6.275c0-2.017 1.195-3.131 3.022-3.131.876 0 1.791.157 1.791.157v1.98h-1.009c-.993 0-1.303.621-1.303 1.258v1.51h2.218l-.354 2.326H9.25V16c3.824-.604 6.75-3.934 6.75-7.951"/></svg></a>
  <a href="https://www.instagram.com/onlinefdr.com.au/" aria-label="Follow onlinefdr.com.au on Instagram" rel="noopener" target="_blank"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true" focusable="false"><path d="M8 0C5.829 0 5.556.01 4.703.048 3.85.088 3.269.222 2.76.42a3.9 3.9 0 0 0-1.417.923A3.9 3.9 0 0 0 .42 2.76C.222 3.268.087 3.85.048 4.7.01 5.555 0 5.827 0 8.001c0 2.172.01 2.444.048 3.297.04.852.174 1.433.372 1.942.205.526.478.972.923 1.417.444.445.89.719 1.416.923.51.198 1.09.333 1.942.372C5.555 15.99 5.827 16 8 16s2.444-.01 3.298-.048c.851-.04 1.434-.174 1.943-.372a3.9 3.9 0 0 0 1.416-.923c.445-.445.718-.891.923-1.417.197-.509.332-1.09.372-1.942C15.99 10.445 16 10.173 16 8s-.01-2.445-.048-3.299c-.04-.851-.175-1.433-.372-1.941a3.9 3.9 0 0 0-.923-1.417A3.9 3.9 0 0 0 13.24.42c-.51-.198-1.092-.333-1.943-.372C10.443.01 10.172 0 7.998 0zm-.717 1.442h.718c2.136 0 2.389.007 3.232.046.78.035 1.204.166 1.486.275.373.145.64.319.92.599s.453.546.598.92c.11.281.24.705.275 1.485.039.843.047 1.096.047 3.231s-.008 2.389-.047 3.232c-.035.78-.166 1.203-.275 1.485a2.5 2.5 0 0 1-.599.919c-.28.28-.546.453-.92.598-.28.11-.704.24-1.485.276-.843.038-1.096.047-3.232.047s-2.39-.009-3.233-.047c-.78-.036-1.203-.166-1.485-.276a2.5 2.5 0 0 1-.92-.598 2.5 2.5 0 0 1-.6-.92c-.109-.281-.24-.705-.275-1.485-.038-.843-.046-1.096-.046-3.233s.008-2.388.046-3.231c.036-.78.166-1.204.276-1.486.145-.373.319-.64.599-.92s.546-.453.92-.598c.282-.11.705-.24 1.485-.276.738-.034 1.024-.044 2.515-.045zm4.988 1.328a.96.96 0 1 0 0 1.92.96.96 0 0 0 0-1.92m-4.27 1.122a4.109 4.109 0 1 0 0 8.217 4.109 4.109 0 0 0 0-8.217m0 1.441a2.667 2.667 0 1 1 0 5.334 2.667 2.667 0 0 1 0-5.334"/></svg></a>
  <a href="https://www.linkedin.com/company/onlinefdr/" aria-label="Follow onlinefdr.com.au on LinkedIn" rel="noopener" target="_blank"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true" focusable="false"><path d="M0 1.146C0 .513.526 0 1.175 0h13.65C15.474 0 16 .513 16 1.146v13.708c0 .633-.526 1.146-1.175 1.146H1.175C.526 16 0 15.487 0 14.854zm4.943 12.248V6.169H2.542v7.225zm-1.2-8.212c.837 0 1.358-.554 1.358-1.248-.015-.709-.52-1.248-1.342-1.248S2.4 3.226 2.4 3.934c0 .694.521 1.248 1.327 1.248zm4.908 8.212V9.359c0-.216.016-.432.08-.586.173-.431.568-.878 1.232-.878.869 0 1.216.662 1.216 1.634v3.865h2.401V9.25c0-2.22-1.184-3.252-2.764-3.252-1.274 0-1.845.7-2.165 1.193v.025h-.016l.016-.025V6.169h-2.4c.03.678 0 7.225 0 7.225z"/></svg></a>
</aside>"""

SOCIAL_INLINE = """<aside class="social-inline" aria-label="Follow us on social media">
  <a href="https://www.facebook.com/onlinefdr/" aria-label="Follow onlinefdr.com.au on Facebook" rel="noopener" target="_blank"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true" focusable="false"><path d="M16 8.049c0-4.446-3.582-8.05-8-8.05C3.58 0-.002 3.603-.002 8.05c0 4.017 2.926 7.347 6.75 7.951v-5.625h-2.03V8.05H6.75V6.275c0-2.017 1.195-3.131 3.022-3.131.876 0 1.791.157 1.791.157v1.98h-1.009c-.993 0-1.303.621-1.303 1.258v1.51h2.218l-.354 2.326H9.25V16c3.824-.604 6.75-3.934 6.75-7.951"/></svg></a>
  <a href="https://www.instagram.com/onlinefdr.com.au/" aria-label="Follow onlinefdr.com.au on Instagram" rel="noopener" target="_blank"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true" focusable="false"><path d="M8 0C5.829 0 5.556.01 4.703.048 3.85.088 3.269.222 2.76.42a3.9 3.9 0 0 0-1.417.923A3.9 3.9 0 0 0 .42 2.76C.222 3.268.087 3.85.048 4.7.01 5.555 0 5.827 0 8.001c0 2.172.01 2.444.048 3.297.04.852.174 1.433.372 1.942.205.526.478.972.923 1.417.444.445.89.719 1.416.923.51.198 1.09.333 1.942.372C5.555 15.99 5.827 16 8 16s2.444-.01 3.298-.048c.851-.04 1.434-.174 1.943-.372a3.9 3.9 0 0 0 1.416-.923c.445-.445.718-.891.923-1.417.197-.509.332-1.09.372-1.942C15.99 10.445 16 10.173 16 8s-.01-2.445-.048-3.299c-.04-.851-.175-1.433-.372-1.941a3.9 3.9 0 0 0-.923-1.417A3.9 3.9 0 0 0 13.24.42c-.51-.198-1.092-.333-1.943-.372C10.443.01 10.172 0 7.998 0zm-.717 1.442h.718c2.136 0 2.389.007 3.232.046.78.035 1.204.166 1.486.275.373.145.64.319.92.599s.453.546.598.92c.11.281.24.705.275 1.485.039.843.047 1.096.047 3.231s-.008 2.389-.047 3.232c-.035.78-.166 1.203-.275 1.485a2.5 2.5 0 0 1-.599.919c-.28.28-.546.453-.92.598-.28.11-.704.24-1.485.276-.843.038-1.096.047-3.232.047s-2.39-.009-3.233-.047c-.78-.036-1.203-.166-1.485-.276a2.5 2.5 0 0 1-.92-.598 2.5 2.5 0 0 1-.6-.92c-.109-.281-.24-.705-.275-1.485-.038-.843-.046-1.096-.046-3.233s.008-2.388.046-3.231c.036-.78.166-1.204.276-1.486.145-.373.319-.64.599-.92s.546-.453.92-.598c.282-.11.705-.24 1.485-.276.738-.034 1.024-.044 2.515-.045zm4.988 1.328a.96.96 0 1 0 0 1.92.96.96 0 0 0 0-1.92m-4.27 1.122a4.109 4.109 0 1 0 0 8.217 4.109 4.109 0 0 0 0-8.217m0 1.441a2.667 2.667 0 1 1 0 5.334 2.667 2.667 0 0 1 0-5.334"/></svg></a>
  <a href="https://www.linkedin.com/company/onlinefdr/" aria-label="Follow onlinefdr.com.au on LinkedIn" rel="noopener" target="_blank"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true" focusable="false"><path d="M0 1.146C0 .513.526 0 1.175 0h13.65C15.474 0 16 .513 16 1.146v13.708c0 .633-.526 1.146-1.175 1.146H1.175C.526 16 0 15.487 0 14.854zm4.943 12.248V6.169H2.542v7.225zm-1.2-8.212c.837 0 1.358-.554 1.358-1.248-.015-.709-.52-1.248-1.342-1.248S2.4 3.226 2.4 3.934c0 .694.521 1.248 1.327 1.248zm4.908 8.212V9.359c0-.216.016-.432.08-.586.173-.431.568-.878 1.232-.878.869 0 1.216.662 1.216 1.634v3.865h2.401V9.25c0-2.22-1.184-3.252-2.764-3.252-1.274 0-1.845.7-2.165 1.193v.025h-.016l.016-.025V6.169h-2.4c.03.678 0 7.225 0 7.225z"/></svg></a>
</aside>"""

def build_page(
    filename, title, meta_desc, canonical, current_page,
    schema_json, extra_css, breadcrumbs, page_html,
    show_marquee=False, extra_js="", robots="index, follow"
):
    # Nav with current page highlighted
    nav_links = NAV_LINKS.replace(
        f'href="{canonical}"',
        f'href="{canonical}" aria-current="page"'
    )
    breadcrumb_html = ""
    if breadcrumbs:
        items = []
        for label, href in breadcrumbs[:-1]:
            items.append(f'<a href="{href}">{label}</a>')
            items.append('<span class="breadcrumb-sep" aria-hidden="true">/</span>')
        items.append(f'<span aria-current="page">{breadcrumbs[-1][0]}</span>')
        breadcrumb_html = f"""<nav class="breadcrumb" aria-label="Breadcrumb">
  <div class="wrap"><div class="breadcrumb-inner">{"".join(items)}</div></div>
</nav>"""

    marquee_html = ""
    if show_marquee:
        marquee_html = f"""<div class="marquee-bar" aria-hidden="true" role="marquee">
  <div class="marquee-track">{MARQUEE_ITEMS}
  </div>
</div>"""

    schema_block = f'<script type="application/ld+json">{schema_json}</script>' if schema_json else ""

    html = f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
{GTAG}
  <title>{title}</title>
  <meta name="description" content="{meta_desc}">
  <meta name="robots" content="{robots}">
  <link rel="canonical" href="https://onlinefdr.com.au{canonical}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{meta_desc}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://onlinefdr.com.au{canonical}">
  <meta property="og:site_name" content="onlinefdr.com.au">
  <meta property="og:locale" content="en_AU">
  <meta property="og:image" content="https://onlinefdr.com.au/images/og-default.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="onlinefdr.com.au. Divorce. Done different. Accredited online Family Dispute Resolution, available nationally.">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="https://onlinefdr.com.au/images/og-default.jpg">
  <meta name="twitter:image:alt" content="onlinefdr.com.au. Divorce. Done different. Accredited online Family Dispute Resolution, available nationally.">
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" type="image/png" sizes="16x16" href="/images/favicon-16.png">
  <link rel="icon" type="image/png" sizes="32x32" href="/images/favicon-32.png">
  <link rel="icon" type="image/png" sizes="192x192" href="/images/favicon-192.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/images/apple-touch-icon.png">
  <meta name="theme-color" content="#F2EDE4">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700;800&display=swap">
  <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700;800&display=swap" rel="stylesheet" media="print" onload="this.media='all'">
  <noscript><link href="https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700;800&display=swap" rel="stylesheet"></noscript>
  {schema_block}
  <style>
{BASE_CSS}
{extra_css}
  </style>
</head>
<body>

<a href="#main" class="skip-to-content">Skip to main content</a>

{SOCIAL_RAIL}

<nav class="nav" id="nav" role="navigation" aria-label="Main navigation">
  <div class="nav-inner">
    <a href="/" class="nav-brand" aria-label="onlinefdr.com.au home">
      <svg class="nav-brand-mark" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#C4873A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">
        <path d="m11 17 2 2a1 1 0 1 0 3-3"/>
        <path d="m14 14 2.5 2.5a1 1 0 1 0 3-3l-3.88-3.88a3 3 0 0 0-4.24 0l-.88.88a1 1 0 1 1-3-3l2.81-2.81a5.79 5.79 0 0 1 7.06-.87l.47.28a2 2 0 0 0 1.42.25L21 4"/>
        <path d="m21 3 1 11h-2"/>
        <path d="M3 3 2 14l6.5 6.5a1 1 0 1 0 3-3"/>
        <path d="M3 4h8"/>
      </svg>
      <span class="nav-brand-text">
        <span class="nav-brand-name">online<span class="brand-fdr">fdr</span>.com.au</span>
        <span class="nav-brand-tag">Accredited Online FDR</span>
      </span>
    </a>
    <ul class="nav-links" id="nav-links" role="list">{nav_links}
    </ul>
    <div class="nav-cta-wrap">{NAV_CTA}</div>
    <button class="nav-toggle" id="nav-toggle" aria-label="Toggle navigation" aria-expanded="false">
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
    </button>
  </div>
</nav>

{marquee_html}

{breadcrumb_html}

<main id="main">
{page_html}
</main>

{SOCIAL_INLINE}

{ENTITY_BAR}

{FOOTER}

{BASE_JS}
{extra_js}
</body>
</html>"""
    out = f"/home/claude/{filename}"
    with open(out, 'w') as f:
        f.write(html)
    lines = html.count('\n')
    print(f"  Built {filename}: {lines} lines")
    return out

print("Generator loaded.")

# ─────────────────────────────────────────────
# HOME
# ─────────────────────────────────────────────
HOME_CSS = """
/* ── HOME HERO ── */
.hero{min-height:calc(100svh - 46px);max-height:calc(100svh - 46px);padding-top:72px;background:var(--charcoal);display:grid;grid-template-rows:1fr auto;position:relative;overflow:hidden}
.hero::before{content:'';position:absolute;inset:0;background:radial-gradient(ellipse 70% 60% at 75% 35%,rgba(196,135,58,0.1) 0%,transparent 60%),radial-gradient(ellipse 40% 70% at 5% 95%,rgba(168,92,50,0.07) 0%,transparent 50%);pointer-events:none}
.hero-inner{display:flex;flex-direction:column;padding:32px var(--pad) 32px;max-width:var(--max);margin:0 auto;width:100%;position:relative;z-index:1;justify-content:center;height:100%;overflow:hidden}
.hero-grid{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:start;min-height:0}
.hero-text{display:flex;flex-direction:column;justify-content:flex-start}
.hero-eyebrow{font-size:0.72rem;font-weight:700;letter-spacing:0.2em;text-transform:uppercase;color:var(--ochre);margin-bottom:18px;display:flex;align-items:center;gap:10px;opacity:0;animation:fadeUp 0.7s var(--ease) 0.1s forwards;flex-shrink:0}
.hero-eyebrow::before{content:'';width:24px;height:2px;background:var(--ochre);flex-shrink:0}
.hero-tagline{font-size:clamp(2.2rem,4vw,4rem);font-weight:800;line-height:1.05;letter-spacing:-0.03em;color:var(--white);margin-bottom:20px;opacity:0;animation:fadeUp 0.8s var(--ease) 0.25s forwards;text-wrap:balance}
.hero-tagline .accent{color:var(--ochre)}
.hero-sub{font-size:clamp(0.9rem,1.2vw,1rem);font-weight:400;color:rgba(253,250,246,0.6);line-height:1.6;margin-bottom:24px;opacity:0;animation:fadeUp 0.8s var(--ease) 0.4s forwards}
.hero-actions{display:flex;align-items:center;gap:14px;flex-wrap:wrap;opacity:0;animation:fadeUp 0.8s var(--ease) 0.55s forwards;margin-bottom:0}
.btn-ghost{display:inline-flex;align-items:center;gap:8px;font-family:var(--f);font-size:0.9rem;font-weight:600;color:rgba(253,250,246,0.55);text-decoration:none;transition:color 0.2s}
.btn-ghost:hover{color:var(--white)}
.btn-ghost svg{transition:transform 0.2s}
.btn-ghost:hover svg{transform:translateX(4px)}

/* Hero image */
.hero-image-panel{position:relative;opacity:0;animation:fadeUp 0.9s var(--ease) 0.4s forwards;align-self:stretch}
.hero-image-panel > .hero-img-real{position:absolute;inset:0;width:100%;height:100%;aspect-ratio:auto}
.hero-image-panel img{object-position:center 40%}
.hero-img-placeholder{background:rgba(255,255,255,0.06);border:2px dashed rgba(255,255,255,0.15);border-radius:12px;aspect-ratio:4/5;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px}
.img-placeholder-icon{width:48px;height:48px;border-radius:50%;background:rgba(196,135,58,0.15);display:flex;align-items:center;justify-content:center;color:var(--ochre)}
.img-placeholder-label{font-size:0.75rem;font-weight:600;color:rgba(255,255,255,0.25);letter-spacing:0.08em;text-transform:uppercase;text-align:center;padding:0 20px}
.hero-img-tag{position:absolute;bottom:-16px;left:50%;transform:translateX(-50%);background:var(--terra);color:var(--white);font-size:0.72rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;padding:8px 20px;border-radius:100px;white-space:nowrap;box-shadow:0 4px 16px rgba(168,92,50,0.4)}

/* Home marquee (more padding than default) */
.hero ~ .marquee-bar,
main > .marquee-bar{padding:13px 0}
.marquee-track{display:inline-flex;animation:marquee 28s linear infinite}
.marquee-track:hover{animation-play-state:paused}
.marquee-item{font-size:0.72rem;font-weight:700;letter-spacing:0.16em;text-transform:uppercase;color:var(--white);padding:0 32px;display:flex;align-items:center;gap:10px}
.marquee-sep{opacity:0.5;font-size:1rem}

/* ── SOCIAL PROOF ── */
/* ── EMPATHY ── */
.empathy{background:var(--white);padding:100px 0}
.empathy-inner{display:grid;grid-template-columns:1fr 1.15fr;gap:80px;align-items:start}
.empathy-left{position:sticky;top:100px}
.empathy-h2{font-size:clamp(1.8rem,3.2vw,2.8rem);font-weight:800;line-height:1.1;color:var(--charcoal);letter-spacing:-0.03em;margin-top:8px;margin-bottom:28px}
.empathy-h2 .accent{color:var(--terra)}
.empathy-img-placeholder{background:var(--dust);border:2px dashed var(--dust-3);border-radius:10px;aspect-ratio:4/3;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px}
.empathy-img-placeholder span{font-size:0.72rem;font-weight:600;color:var(--light-mid);letter-spacing:0.08em;text-transform:uppercase;text-align:center;padding:0 16px}
.empathy-cta{display:flex;align-items:center;gap:14px;margin-top:36px;flex-wrap:wrap}

/* ── WHY FDR ── */
.why-fdr{background:var(--dust);padding:100px 0}
.why-fdr-header{max-width:640px;margin-bottom:52px}
.why-fdr-header h2{font-size:clamp(1.8rem,3.2vw,2.8rem);font-weight:800;line-height:1.1;color:var(--charcoal);letter-spacing:-0.03em;margin-top:8px;margin-bottom:14px}
.why-fdr-header p{font-size:1rem;font-weight:400;color:var(--mid);line-height:1.75}
.compare{display:grid;grid-template-columns:1fr 1fr;grid-template-rows:auto auto auto auto auto;gap:2px;background:var(--dust-3);border-radius:10px;overflow:hidden;margin-bottom:52px}
.compare-header{padding:28px 32px 20px}
.compare-header.left{background:var(--dust-2);grid-column:1;grid-row:1}
.compare-header.right{background:var(--ochre-pale);grid-column:2;grid-row:1}
.compare-header-tag{font-size:0.65rem;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;margin-bottom:10px;display:flex;align-items:center;gap:8px}
.compare-header.left .compare-header-tag{color:var(--light-mid)}
.compare-header.right .compare-header-tag{color:var(--terra)}
.compare-header-tag::before{content:'';width:7px;height:7px;border-radius:50%;flex-shrink:0}
.compare-header.left .compare-header-tag::before{background:var(--dust-3)}
.compare-header.right .compare-header-tag::before{background:var(--terra)}
.compare-header h3{font-size:1.1rem;font-weight:700;color:var(--charcoal);line-height:1.25;letter-spacing:-0.01em}
.compare-cell{padding:14px 32px 18px;display:flex;gap:12px;align-items:flex-start}
.compare-cell.left{background:var(--dust-2)}
.compare-cell.right{background:var(--ochre-pale)}
.compare-cell svg{flex-shrink:0;margin-top:2px}
.compare-cell.left svg{color:var(--light-mid)}
.compare-cell.right svg{color:var(--terra)}
.compare-cell p{font-size:0.88rem;font-weight:400;color:var(--mid);line-height:1.55}
.compare-cell p strong{font-weight:700;color:var(--charcoal);display:block;margin-bottom:2px}
.pillars{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.pillar{background:var(--white);border:1px solid var(--dust-3);border-radius:10px;padding:32px 26px;transition:border-color 0.25s,transform 0.25s,box-shadow 0.25s;cursor:default}
.pillar:hover{border-color:var(--ochre);transform:translateY(-4px);box-shadow:0 12px 32px rgba(196,135,58,0.12)}
.pillar-num{font-size:2rem;font-weight:800;color:var(--dust-3);line-height:1;margin-bottom:14px;letter-spacing:-0.04em}
.pillar h3{font-size:1rem;font-weight:700;color:var(--charcoal);margin-bottom:10px;line-height:1.3;letter-spacing:-0.01em}
.pillar p{font-size:0.86rem;font-weight:400;color:var(--mid);line-height:1.65;margin-bottom:16px}
.pillar-link{font-size:0.78rem;font-weight:700;color:var(--terra);text-decoration:none;letter-spacing:0.04em;display:inline-flex;align-items:center;gap:6px}
.pillar-link svg{transition:transform 0.2s}
.pillar-link:hover svg{transform:translateX(4px)}

/* ── MID-PAGE CTA BAND ── */
.cta-band{background:var(--terra);padding:56px 0}
.cta-band-inner{display:flex;align-items:center;justify-content:space-between;gap:40px;flex-wrap:wrap}
.cta-band-text h3{font-size:clamp(1.4rem,2.5vw,2rem);font-weight:800;color:var(--white);letter-spacing:-0.02em;margin-bottom:8px}
.cta-band-text p{font-size:0.95rem;font-weight:400;color:rgba(253,250,246,0.7);line-height:1.6;max-width:480px}
.cta-band-btn{display:inline-flex;align-items:center;gap:10px;background:var(--white);color:var(--terra);font-family:var(--f);font-size:0.92rem;font-weight:800;letter-spacing:0.01em;padding:16px 32px;border-radius:8px;text-decoration:none;white-space:nowrap;transition:all 0.2s;flex-shrink:0}
.cta-band-btn:hover{background:var(--charcoal);color:var(--white);transform:translateY(-1px);box-shadow:0 6px 20px rgba(0,0,0,0.2)}

/* ── WHY ONLINE ── */
.why-online{background:var(--charcoal);padding:100px 0;position:relative;overflow:hidden}
.why-online::before{content:'';position:absolute;top:-20%;right:-5%;width:50%;height:140%;background:radial-gradient(ellipse at center,rgba(196,135,58,0.07) 0%,transparent 60%);pointer-events:none}
.why-online-inner{display:grid;grid-template-columns:1fr 1fr;gap:80px;align-items:center;position:relative;z-index:1}
.why-online .section-label{color:var(--ochre-lt)}
.why-online h2{font-size:clamp(1.8rem,3.2vw,2.8rem);font-weight:800;line-height:1.1;color:var(--white);letter-spacing:-0.03em;margin-top:8px;margin-bottom:18px}
.why-online h2 .accent{color:var(--ochre)}
.why-online-lead{font-size:1rem;font-weight:400;color:rgba(253,250,246,0.55);line-height:1.8;margin-bottom:28px}
.why-facts{display:flex;flex-direction:column;border-top:1px solid rgba(255,255,255,0.08)}
.why-fact{display:flex;gap:18px;align-items:flex-start;padding:20px 0;border-bottom:1px solid rgba(255,255,255,0.08)}
.why-fact-icon{width:38px;height:38px;border-radius:10px;background:rgba(196,135,58,0.12);color:var(--ochre-lt);display:flex;align-items:center;justify-content:center;flex-shrink:0}
.why-fact-text h4{font-size:0.88rem;font-weight:700;color:var(--white);margin-bottom:3px}
.why-fact-text p{font-size:0.82rem;font-weight:400;color:rgba(253,250,246,0.45);line-height:1.6}
.why-img-placeholder{background:rgba(255,255,255,0.04);border:2px dashed rgba(255,255,255,0.12);border-radius:12px;aspect-ratio:4/3;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px}
.why-stats{display:grid;grid-template-columns:1fr 1fr;gap:3px;background:rgba(255,255,255,0.06);border-radius:10px;overflow:hidden;margin-top:20px}
.why-stat{padding:28px 24px;background:rgba(255,255,255,0.03);transition:background 0.2s}
.why-stat:hover{background:rgba(255,255,255,0.06)}
.why-stat-val{font-size:clamp(1.9rem,3vw,2.4rem);font-weight:800;color:var(--white);line-height:1;margin-bottom:8px;letter-spacing:-0.03em}
.why-stat-val .unit{color:var(--ochre);font-weight:800;margin-left:4px}
.why-stat-val.text{font-size:clamp(1.6rem,2.6vw,2.1rem)}
.why-stat-label{font-size:0.74rem;font-weight:500;color:rgba(253,250,246,0.35);line-height:1.5}
.why-comparator{background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:12px;padding:32px 28px;margin-top:24px}
.why-comparator-header{display:grid;grid-template-columns:90px 1fr 1fr;gap:18px;margin-bottom:18px;padding-bottom:14px;border-bottom:1px solid rgba(255,255,255,0.08)}
.why-comparator-header > div{font-size:0.66rem;font-weight:700;letter-spacing:0.14em;text-transform:uppercase;color:rgba(253,250,246,0.4)}
.why-comparator-row{display:grid;grid-template-columns:90px 1fr 1fr;gap:18px;align-items:center;padding:18px 0}
.why-comparator-row + .why-comparator-row{border-top:1px solid rgba(255,255,255,0.06)}
.why-comparator-label{font-size:0.78rem;font-weight:700;color:var(--white);letter-spacing:0.02em}
.why-comparator-label .qual{display:block;font-size:0.66rem;font-weight:500;color:rgba(253,250,246,0.4);letter-spacing:0;margin-top:4px;text-transform:none}
.why-bar-cell{position:relative;height:36px;display:flex;align-items:center}
.why-bar{height:8px;border-radius:4px;position:relative}
.why-bar-fdr{background:var(--ochre);width:8%}
.why-bar-court{background:rgba(253,250,246,0.18);width:100%;position:relative}
.why-bar-court::after{content:"";position:absolute;right:-6px;top:50%;transform:translateY(-50%);border-left:8px solid rgba(253,250,246,0.45);border-top:6px solid transparent;border-bottom:6px solid transparent}
.why-bar-text{position:absolute;left:0;top:100%;margin-top:8px;font-size:0.72rem;font-weight:600;color:rgba(253,250,246,0.85);white-space:nowrap}
.why-bar-text.text-fdr{color:var(--ochre-lt)}
.why-comparator-foot{margin-top:18px;padding-top:14px;border-top:1px solid rgba(255,255,255,0.06);font-size:0.7rem;font-style:italic;color:rgba(253,250,246,0.35);line-height:1.55}

@media(max-width:640px){
  .why-comparator{padding:24px 18px}
  .why-comparator-header{grid-template-columns:70px 1fr 1fr;gap:10px}
  .why-comparator-row{grid-template-columns:70px 1fr 1fr;gap:10px}
  .why-bar-text{white-space:normal;line-height:1.3;padding-right:6px}
  .why-bar-cell{height:auto;min-height:36px;padding-bottom:30px}
}

/* ── PROCESS ── */
.process{background:var(--white);padding:100px 0}
.process-header{max-width:560px;margin-bottom:52px}
.process-header h2{font-size:clamp(1.8rem,3.2vw,2.8rem);font-weight:800;line-height:1.1;color:var(--charcoal);letter-spacing:-0.03em;margin-top:8px;margin-bottom:14px}
.process-header p{font-size:1rem;font-weight:400;color:var(--mid);line-height:1.75}
.process-header a{color:var(--terra);font-weight:600;text-decoration:none;border-bottom:1px solid rgba(168,92,50,0.3)}
.process-header a:hover{border-color:var(--terra)}
.process-grid{display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:start}
.process-steps{display:flex;flex-direction:column;border-left:2px solid var(--dust-3);margin-left:16px}
.process-step{display:grid;grid-template-columns:52px 1fr;gap:24px;padding:0 0 44px 36px;position:relative}
.process-step:last-child{padding-bottom:0}
.process-dot{position:absolute;left:-9px;top:6px;width:18px;height:18px;border-radius:50%;background:var(--white);border:2px solid var(--dust-3);transition:border-color 0.25s,background 0.25s}
.process-step:hover .process-dot{border-color:var(--ochre);background:var(--ochre-pale)}
.process-num{font-size:2.4rem;font-weight:800;color:var(--dust-3);line-height:1;flex-shrink:0;letter-spacing:-0.04em}
.process-content h3{font-size:1rem;font-weight:700;color:var(--charcoal);margin-bottom:6px;line-height:1.3;margin-top:6px;letter-spacing:-0.01em}
.process-content p{font-size:0.9rem;font-weight:400;color:var(--mid);line-height:1.75}
.process-tag{display:inline-flex;align-items:center;gap:6px;font-size:0.66rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:var(--terra);background:var(--ochre-pale);padding:4px 12px;border-radius:100px;margin-top:10px}
.process-img{background:var(--dust);border:2px dashed var(--dust-3);border-radius:12px;aspect-ratio:4/3;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;position:sticky;top:100px}
.process-img-icon{width:48px;height:48px;border-radius:50%;background:rgba(196,135,58,0.15);display:flex;align-items:center;justify-content:center;color:var(--ochre)}
.process-img-label{font-size:0.72rem;font-weight:600;color:var(--light-mid);letter-spacing:0.08em;text-transform:uppercase;text-align:center;padding:0 16px}

/* ── FAQ ── */
.faq-section{background:var(--dust);padding:100px 0}
.faq-header{max-width:560px;margin:0 auto 48px;text-align:center}
.faq-header h2{font-size:clamp(1.8rem,3.2vw,2.8rem);font-weight:800;line-height:1.1;color:var(--charcoal);letter-spacing:-0.03em;margin-top:8px;margin-bottom:14px}
.faq-header p{font-size:1rem;font-weight:400;color:var(--mid);line-height:1.7}
.faq-list{max-width:760px;margin:0 auto;border:1px solid var(--dust-3);border-radius:10px;overflow:hidden;background:var(--white)}
.faq-item{border-bottom:1px solid var(--dust-3)}
.faq-item:last-child{border-bottom:none}
.faq-q{width:100%;display:flex;align-items:center;justify-content:space-between;gap:20px;padding:20px 26px;background:none;border:none;text-align:left;cursor:pointer;font-family:var(--f);font-size:0.92rem;font-weight:600;color:var(--charcoal);transition:background 0.2s}
.faq-q:hover{background:var(--ochre-pale)}
.faq-q svg{flex-shrink:0;color:var(--terra);transition:transform 0.3s}
.faq-item.open .faq-q svg{transform:rotate(45deg)}
.faq-a{display:none;padding:0 26px 20px}
.faq-item.open .faq-a{display:block}
.faq-a p{font-size:0.9rem;font-weight:400;color:var(--mid);line-height:1.75}
.faq-footer{text-align:center;margin-top:28px;display:flex;flex-direction:column;align-items:center;gap:12px}
.faq-footer p{font-size:0.88rem;font-weight:400;color:var(--mid)}

/* ── AVAILABILITY STRIP ── */
.home-availability{background:var(--dust);padding:48px 0;border-top:1px solid var(--dust-2);border-bottom:1px solid var(--dust-2)}
.home-availability-eyebrow{font-size:0.72rem;font-weight:700;letter-spacing:0.16em;text-transform:uppercase;color:var(--ochre);margin-bottom:14px;display:flex;align-items:center;gap:10px}
.home-availability-eyebrow::before{content:'';width:24px;height:2px;background:var(--ochre)}
.home-availability-text{font-size:1rem;font-weight:400;color:var(--charcoal);line-height:1.8;max-width:880px;margin:0}
.home-availability-text strong{font-weight:600}
.home-availability-link{color:var(--terra);text-decoration:none;font-weight:600;white-space:nowrap;transition:color 0.2s}
.home-availability-link:hover{color:var(--charcoal)}

/* ── FINAL CTA ── */
.cta{background:var(--terra);padding:100px 0;position:relative;overflow:hidden}
.cta::before{content:'';position:absolute;top:-40%;right:-8%;width:500px;height:500px;border-radius:50%;background:rgba(255,255,255,0.06);pointer-events:none}
.cta::after{content:'';position:absolute;bottom:-30%;left:-5%;width:350px;height:350px;border-radius:50%;background:rgba(0,0,0,0.06);pointer-events:none}
.cta-inner{max-width:760px;margin:0 auto;text-align:center;position:relative;z-index:1}
.cta-eyebrow{font-size:0.68rem;font-weight:700;letter-spacing:0.2em;text-transform:uppercase;color:rgba(253,250,246,0.5);margin-bottom:20px;display:block}
.cta h2{font-size:clamp(2.2rem,5vw,4.4rem);font-weight:800;line-height:1.05;color:var(--white);letter-spacing:-0.03em;margin-bottom:20px}
.cta p{font-size:1.1rem;font-weight:400;color:rgba(253,250,246,0.72);line-height:1.75;margin-bottom:44px;max-width:580px;margin-left:auto;margin-right:auto}
.cta-actions{display:flex;align-items:center;justify-content:center;gap:16px;flex-wrap:wrap;margin-bottom:24px}
.cta-btn{display:inline-flex;align-items:center;gap:10px;background:var(--charcoal);color:var(--white);font-family:var(--f);font-size:0.95rem;font-weight:700;letter-spacing:0.01em;padding:18px 40px;border-radius:8px;text-decoration:none;transition:all 0.2s}
.cta-btn:hover{background:var(--charcoal-2);transform:translateY(-2px);box-shadow:0 8px 24px rgba(0,0,0,0.3)}
.cta-btn svg{transition:transform 0.2s}
.cta-btn:hover svg{transform:translateX(4px)}
.cta-btn-outline{display:inline-flex;align-items:center;gap:10px;background:transparent;color:var(--white);font-family:var(--f);font-size:0.95rem;font-weight:700;letter-spacing:0.01em;padding:16px 38px;border-radius:8px;text-decoration:none;border:2px solid rgba(255,255,255,0.4);transition:all 0.2s}
.cta-btn-outline:hover{background:rgba(255,255,255,0.1);border-color:rgba(255,255,255,0.7)}
.cta-note{font-size:0.76rem;font-weight:500;color:rgba(253,250,246,0.4)}

/* Hero animation keyframe */
@keyframes fadeUp{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}

@media(max-width:960px){
  .hero{min-height:0;max-height:none}
  .hero-inner{overflow:visible;padding-top:48px;padding-bottom:48px}
  .hero-grid{grid-template-columns:1fr;gap:0}
  .hero-image-panel{position:static;align-self:auto;aspect-ratio:3/2;margin-top:32px;border-radius:8px;overflow:hidden}
  .hero-image-panel > .hero-img-real{position:static;width:100%;height:100%}
  .hero-image-panel img{width:100%;height:100%;object-fit:cover;border-radius:8px}
  .empathy-inner{grid-template-columns:1fr;gap:40px}
  .empathy-left{position:static}
  .why-online-inner{grid-template-columns:1fr;gap:56px}
  .process-grid{grid-template-columns:1fr}
  .process-img{position:static}
  .pillars{grid-template-columns:1fr 1fr}
}
@media(max-width:768px){
  .compare{grid-template-columns:1fr;grid-template-rows:none}
  .compare-header.left,.compare-header.right{grid-column:1;grid-row:auto}
  .compare-cell{grid-column:1 !important;grid-row:auto !important}
  .pillars{grid-template-columns:1fr}
  .process-step{grid-template-columns:1fr;gap:8px;padding-left:32px}
  .cta-band-inner{flex-direction:column;text-align:center}
}
@media(max-width:480px){
  .hero-actions{flex-direction:row;align-items:stretch;flex-wrap:nowrap}
  .hero-actions .btn-primary{flex:1;justify-content:center;padding-left:16px;padding-right:16px}
  .why-stats{grid-template-columns:1fr}
  .cta-actions{flex-direction:column;align-items:center}
}
"""

HOME_HTML = """
  <!-- HERO -->
  <section class="hero" aria-labelledby="hero-heading">
    <div class="hero-inner">
      <p class="hero-eyebrow">Online Family Dispute Resolution &bull; Available nationally</p>
      <div class="hero-grid">
        <div class="hero-text">
          <h1 class="hero-tagline" id="hero-heading">
            The call you make<br>before you call<br><span class="accent">a lawyer.</span>
          </h1>
          <p class="hero-sub">Family dispute resolution is the structured, professionally facilitated path to working out parenting and financial matters without going to court. Significantly less costly than contested proceedings, and most families resolve their matter in a matter of weeks rather than years.</p>
          <div class="hero-actions">
            <a href="tel:0399617544" class="btn-primary" aria-label="Call us on 0 3 9 9 6 1 7 5 4 4">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="margin-right:4px"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
              Call (03) 9961 7544
            </a>
            <a href="/book/" class="btn-icon-book" aria-label="Book a free discovery call">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            </a>
          </div>
        </div>
        <div class="hero-image-panel" aria-hidden="true">
          <div class="hero-img-real"><img src="/images/home-hero.jpg" alt="A couple at opposite ends of a lounge at dusk, their dog at rest on the rug between them." fetchpriority="high"></div>
        </div>
      </div>
    </div>
  </section>

  <!-- HOME MARQUEE -->
  <div class="marquee-bar" aria-label="Accreditation and credentials" role="marquee">
    <div class="marquee-track" aria-hidden="true">
      <span class="marquee-item">AGD-Accredited FDRP <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Australian Mediation Association Member <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Section 60I Certificates (s 66H in WA) <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Conducted Securely Online <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Available Anywhere in Australia <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Free Discovery Call <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">No Obligation <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Confidential under the Family Law Act <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Both Parenting and Financial Matters <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">AGD-Accredited FDRP <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Australian Mediation Association Member <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Section 60I Certificates (s 66H in WA) <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Conducted Securely Online <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Available Anywhere in Australia <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Free Discovery Call <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">No Obligation <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Confidential under the Family Law Act <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Both Parenting and Financial Matters <span class="marquee-sep">&bull;</span></span>
    </div>
  </div>

  <!-- FUTURE: REVIEWS SCROLLER (will replace this placeholder once reviews exist) -->

  <div class="divider" aria-hidden="true"></div>

  <!-- EMPATHY -->
  <section class="empathy" aria-labelledby="empathy-heading">
    <div class="wrap">
      <div class="empathy-inner">
        <div class="empathy-left reveal">
          <span class="section-label">Where you are right now</span>
          <h2 class="empathy-h2" id="empathy-heading">This is one of the hardest things you will <span class="accent">get through.</span></h2>
          <div class="empathy-img-real"><img src="/images/home-supporting-1.jpg" alt="A woman alone at her kitchen counter at dusk, in tears on the phone to her mother." loading="lazy" decoding="async"></div>
        </div>
        <div class="empathy-right">
          <p class="body-text reveal">If you have landed here, you are in the middle of something painful. A relationship ending. Decisions about children, or property, or both. Financial uncertainty. And the weight of not knowing what comes next.</p>
          <p class="body-text reveal reveal-d1">Most people are told they need a lawyer. Sometimes that is true. For many families navigating separation, there is a step that comes first. One that is <strong>faster, less adversarial, and significantly less costly than contested proceedings.</strong></p>
          <div class="pull reveal reveal-d2">
            <p>"Family dispute resolution is not about deciding who is right. It is about finding a way forward that works, on terms you have reached yourselves."</p>
          </div>
          <p class="body-text reveal reveal-d3">That is what we do. Entirely online. Available anywhere in Australia. Ready within weeks, not months.</p>
          <div class="empathy-cta reveal">
            <a href="#discovery" class="btn-primary">Book a free call<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg></a>
            <a href="/what-is-fdr/" class="btn-secondary">What is FDR?</a>
          </div>
        </div>
      </div>
    </div>
  </section>

  <div class="divider" aria-hidden="true"></div>

  <!-- WHY FDR -->
  <section class="why-fdr" id="what-is-fdr" aria-labelledby="why-fdr-heading">
    <div class="wrap">
      <div class="why-fdr-header reveal">
        <span class="section-label">Understanding your options</span>
        <h2 id="why-fdr-heading">FDR versus court. The difference that matters.</h2>
        <p>Family Dispute Resolution is a structured, professionally facilitated process that helps separating families reach their own agreements, without a judge making decisions for them.</p>
      </div>
      <div class="compare reveal" role="table" aria-label="FDR versus going to court">
        <div class="compare-header left" role="columnheader"><p class="compare-header-tag">Going to court</p><h3>Expensive, slow, and out of your hands</h3></div>
        <div class="compare-header right" role="columnheader"><p class="compare-header-tag">Family Dispute Resolution</p><h3>Faster, calmer, and you stay in control</h3></div>
        <div class="compare-cell left" role="cell" style="grid-column:1;grid-row:2"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg><p><strong>18 to 36 months</strong>Typical timeframe from filing to final hearing.</p></div>
        <div class="compare-cell right" role="cell" style="grid-column:2;grid-row:2"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg><p><strong>Weeks, not years</strong>Most matters resolve in a matter of weeks from first enquiry.</p></div>
        <div class="compare-cell left" role="cell" style="grid-column:1;grid-row:3"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg><p><strong>Tens of thousands per party</strong>Legal fees accumulate from first instruction and compound throughout.</p></div>
        <div class="compare-cell right" role="cell" style="grid-column:2;grid-row:3"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg><p><strong>Less costly than contested proceedings</strong>Transparent fees agreed upfront. A small share of what a contested matter typically takes from both parties.</p></div>
        <div class="compare-cell left" role="cell" style="grid-column:1;grid-row:4"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg><p><strong>A judge decides</strong>You lose control. A stranger makes decisions about your children, your property, or both.</p></div>
        <div class="compare-cell right" role="cell" style="grid-column:2;grid-row:4"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg><p><strong>You reach the agreement</strong>The mediator facilitates. The decisions are yours. Both parties own the outcome.</p></div>
        <div class="compare-cell left" role="cell" style="grid-column:1;grid-row:5"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg><p><strong>Entrenches conflict</strong>The adversarial process deepens divisions and makes any ongoing relationship harder.</p></div>
        <div class="compare-cell right" role="cell" style="grid-column:2;grid-row:5"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg><p><strong>Reduces ongoing conflict</strong>Collaborative by design. Less damaging to any ongoing relationship between parties.</p></div>
      </div>
      <div class="pillars">
        <div class="pillar reveal reveal-d1">
          <div class="pillar-num" aria-hidden="true">01</div>
          <h3>Parenting and care arrangements</h3>
          <p>Child-focused parenting plans and the basis for Consent Orders. FDR helps parents reach workable arrangements that grow with their children, without a judge deciding for them.</p>
          <a href="/parenting/" class="pillar-link">Learn more <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg></a>
        </div>
        <div class="pillar reveal reveal-d2">
          <div class="pillar-num" aria-hidden="true">02</div>
          <h3>Financial and property settlement</h3>
          <p>Property, superannuation, debt, and de facto matters under the codified four-step framework in the Family Law Act. Structured mediation that meets the disclosure obligations the 2024 amendments brought in.</p>
          <a href="/financial-settlement/" class="pillar-link">Learn more <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg></a>
        </div>
        <div class="pillar reveal reveal-d3">
          <div class="pillar-num" aria-hidden="true">03</div>
          <h3>Section 60I certificates</h3>
          <p>Required before Family Court parenting applications. Issued only following a proper FDR process, in the certificate type that reflects what occurred.</p>
          <a href="/section-60i/" class="pillar-link">Learn more <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg></a>
        </div>
      </div>
    </div>
  </section>

  <!-- MID-PAGE CTA BAND -->
  <div class="cta-band" role="complementary" aria-label="Call to action">
    <div class="wrap">
      <div class="cta-band-inner">
        <div class="cta-band-text">
          <h3>Not sure where to start? Start with a conversation.</h3>
          <p>A free discovery call with an accredited FDR practitioner. No pressure, no commitment. Just a straight conversation about your options.</p>
        </div>
        <a href="#discovery" class="cta-band-btn">
          Book your free call
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
        </a>
      </div>
    </div>
  </div>

  <div class="divider" aria-hidden="true"></div>

  <!-- WHY ONLINE -->
  <section class="why-online" aria-labelledby="why-online-heading">
    <div class="wrap">
      <div class="why-online-inner">
        <div class="reveal">
          <span class="section-label">Why online</span>
          <h2 id="why-online-heading">Most people dread the day of mediation as much as the <span class="accent">process itself.</span></h2>
          <p class="why-online-lead">The drive across the city. The waiting room. Walking past the other party in a corridor. None of that has anything to do with resolving your dispute, but all of it shapes how you walk into the room. Online FDR removes that entirely.</p>
          <div class="why-facts">
            <div class="why-fact">
              <div class="why-fact-icon" aria-hidden="true"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg></div>
              <div class="why-fact-text"><h4>No logistics overhead</h4><p>No travel, no parking, no half-day written off. Join from your home, your office, or wherever you happen to be.</p></div>
            </div>
            <div class="why-fact">
              <div class="why-fact-icon" aria-hidden="true"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg></div>
              <div class="why-fact-text"><h4>Safer for high-conflict matters</h4><p>Genuine physical separation throughout. No shared waiting room. No unwanted proximity.</p></div>
            </div>
            <div class="why-fact">
              <div class="why-fact-icon" aria-hidden="true"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg></div>
              <div class="why-fact-text"><h4>The practitioner comes to you</h4><p>Available anywhere in Australia. Both parties can be in different cities or states.</p></div>
            </div>
            <div class="why-fact">
              <div class="why-fact-icon" aria-hidden="true"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg></div>
              <div class="why-fact-text"><h4>Faster than government services</h4><p>Community services can take months. We are typically available within two weeks of first enquiry.</p></div>
            </div>
            <div class="why-fact">
              <div class="why-fact-icon" aria-hidden="true"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg></div>
              <div class="why-fact-text"><h4>Real shuttle mediation</h4><p>Parties in different homes, different cities. The separation is genuine, not just different rooms.</p></div>
            </div>
          </div>
        </div>
        <div class="reveal reveal-d2">
          <div class="why-img-real"><img src="/images/home-supporting-2.jpg" alt="A woman at her desk wearing noise-cancelling headphones, composed and focused before her online mediation session." loading="lazy" decoding="async"></div>
          <div class="why-comparator">
            <div class="why-comparator-header">
              <div></div>
              <div>Time</div>
              <div>Cost</div>
            </div>
            <div class="why-comparator-row">
              <div class="why-comparator-label">
                FDR
                <span class="qual">Online via this practice</span>
              </div>
              <div class="why-bar-cell">
                <div class="why-bar why-bar-fdr"></div>
                <div class="why-bar-text text-fdr">Weeks</div>
              </div>
              <div class="why-bar-cell">
                <div class="why-bar why-bar-fdr"></div>
                <div class="why-bar-text text-fdr">A fraction of litigation</div>
              </div>
            </div>
            <div class="why-comparator-row">
              <div class="why-comparator-label">
                Court
                <span class="qual">Contested proceedings</span>
              </div>
              <div class="why-bar-cell">
                <div class="why-bar why-bar-court"></div>
                <div class="why-bar-text">18 to 36 months</div>
              </div>
              <div class="why-bar-cell">
                <div class="why-bar why-bar-court"></div>
                <div class="why-bar-text">Often six figures per party</div>
              </div>
            </div>
            <div class="why-comparator-foot">
              Court figures reflect typical fully-litigated parenting or property matters from filing to final hearing. Costs vary with complexity.
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <div class="divider" aria-hidden="true"></div>

  <!-- PROCESS -->
  <section class="process" aria-labelledby="home-process-heading">
    <div class="wrap">
      <div class="process-header reveal">
        <span class="section-label">How it works</span>
        <h2 id="home-process-heading">From first conversation to signed agreement.</h2>
        <p>Every step happens online, at a pace that suits your situation. For the full walkthrough, see <a href="/how-it-works/">How it works</a>.</p>
      </div>
      <div class="process-grid">
        <div class="process-steps">
          <div class="process-step reveal">
            <div class="process-dot" aria-hidden="true"></div>
            <div class="process-num" aria-hidden="true">01</div>
            <div class="process-content">
              <h3>Free discovery call</h3>
              <p>A no-obligation conversation. We explain how FDR works, whether it is right for your circumstances, and answer any questions before you commit to anything.</p>
              <span class="process-tag">Free &bull; No obligation</span>
            </div>
          </div>
          <div class="process-step reveal reveal-d1">
            <div class="process-dot" aria-hidden="true"></div>
            <div class="process-num" aria-hidden="true">02</div>
            <div class="process-content">
              <h3>Individual intake sessions</h3>
              <p>Each party meets privately with the practitioner. Your chance to share your perspective and what matters most before the joint session begins. For financial matters, the duty of disclosure is walked through here and the Full and Frank Disclosure worksheet is provided.</p>
              <span class="process-tag">Private &bull; Confidential &bull; Online</span>
            </div>
          </div>
          <div class="process-step reveal reveal-d2">
            <div class="process-dot" aria-hidden="true"></div>
            <div class="process-num" aria-hidden="true">03</div>
            <div class="process-content">
              <h3>Joint mediation session</h3>
              <p>A structured session facilitated by the practitioner. Four hours for parenting matters, three hours for financial. Where direct communication is not appropriate, shuttle mediation keeps parties in separate breakout rooms throughout, with the practitioner moving between them.</p>
              <span class="process-tag">Shuttle mediation available</span>
            </div>
          </div>
          <div class="process-step reveal reveal-d3">
            <div class="process-dot" aria-hidden="true"></div>
            <div class="process-num" aria-hidden="true">04</div>
            <div class="process-content">
              <h3>Agreement and documentation</h3>
              <p>Where agreement is reached, it is documented. A Parenting Plan, financial heads of agreement, or the basis for Consent Orders. Where it is not, a Section 60I certificate is issued reflecting what occurred. Documents signed electronically and delivered within 48 hours.</p>
              <span class="process-tag">Legally recognised documents</span>
            </div>
          </div>
        </div>
        <div class="process-img-real reveal reveal-d2"><img src="/images/home-supporting-3.jpg" alt="A woman on a park bench in autumn, her golden retriever at her feet, looking quietly into the distance." loading="lazy" decoding="async"></div>
      </div>
    </div>
  </section>

  <!-- FAQ -->
  <section class="faq-section" aria-labelledby="home-faq-heading">
    <div class="wrap">
      <div class="faq-header reveal">
        <span class="section-label">Common questions</span>
        <h2 id="home-faq-heading">Questions we hear every day</h2>
        <p>Straightforward answers before you commit to anything.</p>
      </div>
      <div class="faq-list reveal">
        <div class="faq-item">
          <button class="faq-q" aria-expanded="false">Do I need to attempt FDR before going to the Family Court?<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></button>
          <div class="faq-a"><p>For parenting orders, yes. Under section 60I of the Family Law Act, FDR is the step the law expects to be taken before applying for parenting orders, unless an exemption applies. For financial and property matters, the Section 60I certificate does not apply, but every initiating application requires a Genuine Steps Certificate under Schedule 1 of the FCFCOA (Family Law) Rules 2021. The Genuine Steps Certificate is signed by the party themselves and confirms a genuine attempt at dispute resolution has been made.</p></div>
        </div>
        <div class="faq-item">
          <button class="faq-q" aria-expanded="false">Is online family mediation legally valid in Australia?<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></button>
          <div class="faq-a"><p>Yes. The Family Law Act does not require FDR to be conducted in person. Online mediation by an accredited FDRP is fully legally valid. Section 60I certificates issued after online sessions carry exactly the same legal standing as those from in-person sessions, and the statutory confidentiality and inadmissibility protections under sections 10H and 10J apply equally.</p></div>
        </div>
        <div class="faq-item">
          <button class="faq-q" aria-expanded="false">What if the other party will not participate?<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></button>
          <div class="faq-a"><p>If the other party refuses to attend after being given a genuine opportunity, a Section 60I certificate under paragraph 60I(8)(a) can be issued documenting non-attendance. The matter can then proceed to court for parenting orders. Courts may take non-participation into account when making subsequent orders, including in relation to costs.</p></div>
        </div>
        <div class="faq-item">
          <button class="faq-q" aria-expanded="false">How long does the FDR process take?<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></button>
          <div class="faq-a"><p>Most matters resolve in a matter of weeks rather than months. Discovery calls are typically available within a few days of enquiry, intake within a week or two, and the first joint session within two weeks of initial contact. Higher-conflict matters take longer, but still run significantly faster than the 18 to 36 month timeline for contested family law proceedings.</p></div>
        </div>
        <div class="faq-item">
          <button class="faq-q" aria-expanded="false">Can I participate if I live in regional or rural Australia?<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></button>
          <div class="faq-a"><p>Yes. Our practice is entirely online so you can participate from anywhere in Australia. Both parties can be in different cities or states. Access to an accredited FDRP is no longer determined by postcode.</p></div>
        </div>
        <div class="faq-item">
          <button class="faq-q" aria-expanded="false">Does this apply to financial matters as well as parenting?<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></button>
          <div class="faq-a"><p>Yes. We handle parenting matters, financial and property settlement, and Section 60I certificates. Whether you are mid-separation, already divorced with ongoing parenting disputes, or dealing with financial matters only, FDR is available and appropriate. The Family Law Amendment Act 2024, in force from 10 June 2025, codified the four-step property settlement framework into the Family Law Act and imposed new statutory obligations on FDR practitioners to inform parties about their duty of disclosure.</p></div>
        </div>
      </div>
      <div class="faq-footer reveal">
        <p>More questions? Our full FAQ covers process, eligibility, and what to expect.</p>
        <a href="/faq/" class="btn-primary">View all frequently asked questions</a>
      </div>
    </div>
  </section>

  <!-- AVAILABILITY STRIP — before final CTA -->
  <section class="home-availability" aria-label="Service availability">
    <div class="wrap">
      <p class="home-availability-eyebrow">Available throughout Australia</p>
      <p class="home-availability-text">Online FDR is available in <strong>Victoria, New South Wales, Queensland, Western Australia, South Australia, Tasmania, the ACT, and the Northern Territory</strong>. Clients connect from Melbourne, Sydney, Brisbane, Perth, Adelaide, Hobart, Canberra, Darwin, and every regional centre in between. <a href="/locations/" class="home-availability-link">See state-by-state availability &rarr;</a></p>
    </div>
  </section>

  <!-- FINAL CTA -->
  <section class="cta" id="discovery" aria-labelledby="cta-heading">
    <div class="wrap">
      <div class="cta-inner">
        <span class="cta-eyebrow">Take the first step</span>
        <h2 id="cta-heading">The call you make before you call a lawyer.</h2>
        <p>A free, no-obligation conversation with an accredited FDR practitioner. Whether your matter involves children, property, or both, this is a chance to understand your options before you commit to anything.</p>
        <div class="cta-actions">
          <a href="https://calendar.app.google/zwNm4dzYnwAwhwxY8" class="cta-btn">
            Book your free discovery call
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
          </a>
          <a href="tel:0399617544" class="cta-btn-outline">
            Call (03) 9961 7544
          </a>
        </div>
        <span class="cta-note">Free &bull; Confidential &bull; No obligation &bull; Available nationally &bull; AGD Accredited</span>
      </div>
    </div>
  </section>
"""

HOME_SCHEMA = '{"@context":"https://schema.org","@graph":[{"@type":"WebSite","@id":"https://onlinefdr.com.au/#website","url":"https://onlinefdr.com.au/","name":"onlinefdr.com.au","description":"Accredited Online Family Dispute Resolution in Australia. Available nationally, conducted online, registered with the AGD.","publisher":{"@id":"https://onlinefdr.com.au/#organization"},"inLanguage":"en-AU"},{"@type":["Organization","LegalService"],"@id":"https://onlinefdr.com.au/#organization","name":"onlinefdr.com.au","alternateName":"Online FDR","url":"https://onlinefdr.com.au/","logo":"https://onlinefdr.com.au/images/logo.png","sameAs":["https://www.facebook.com/onlinefdr/","https://www.instagram.com/onlinefdr.com.au/","https://www.linkedin.com/company/onlinefdr/"],"telephone":"+61399617544","email":"hello@onlinefdr.com.au","description":"Accredited Online Family Dispute Resolution practice. Registered with the Australian Government Attorney-General\'s Department under the Family Law (Family Dispute Resolution Practitioners) Regulations 2025. Authorised to issue Section 60I certificates nationally.","areaServed":{"@type":"Country","name":"Australia"},"serviceType":["Family Dispute Resolution","Online Mediation","Section 60I Certificate Issuance","Parenting Mediation","Property Settlement Mediation"],"knowsAbout":["Family Law Act 1975","Section 60I certificates","Family Dispute Resolution","Parenting arrangements","Property settlement","Online mediation"],"founder":{"@type":"Person","name":"Kevin Scrimshaw","jobTitle":"Founder","identifier":{"@type":"PropertyValue","propertyID":"AGD FDRP Registration Number","value":"F2003011"},"hasCredential":[{"@type":"EducationalOccupationalCredential","credentialCategory":"Accreditation","name":"Accredited Family Dispute Resolution Practitioner","recognizedBy":{"@type":"GovernmentOrganization","name":"Australian Government Attorney-General\'s Department"}}]}},{"@type":"WebPage","@id":"https://onlinefdr.com.au/#webpage","url":"https://onlinefdr.com.au/","name":"Accredited Online Family Dispute Resolution in Australia","isPartOf":{"@id":"https://onlinefdr.com.au/#website"},"about":{"@id":"https://onlinefdr.com.au/#organization"},"mainEntity":{"@id":"https://onlinefdr.com.au/#faq"},"inLanguage":"en-AU"},{"@type":"FAQPage","@id":"https://onlinefdr.com.au/#faq","mainEntity":[{"@type":"Question","name":"Do I need to attempt FDR before going to the Family Court?","acceptedAnswer":{"@type":"Answer","text":"For parenting orders, yes. Under section 60I of the Family Law Act, FDR is the step the law expects to be taken before applying for parenting orders, unless an exemption applies. For financial and property matters, the Section 60I certificate does not apply, but every initiating application requires a Genuine Steps Certificate under Schedule 1 of the FCFCOA (Family Law) Rules 2021. The Genuine Steps Certificate is signed by the party themselves and confirms a genuine attempt at dispute resolution has been made."}},{"@type":"Question","name":"Is online family mediation legally valid in Australia?","acceptedAnswer":{"@type":"Answer","text":"Yes. The Family Law Act does not require FDR to be conducted in person. Online mediation by an accredited FDRP is fully legally valid. Section 60I certificates issued after online sessions carry exactly the same legal standing as those from in-person sessions, and the statutory confidentiality and inadmissibility protections under sections 10H and 10J apply equally."}},{"@type":"Question","name":"What if the other party will not participate?","acceptedAnswer":{"@type":"Answer","text":"If the other party refuses to attend after being given a genuine opportunity, a Section 60I certificate under paragraph 60I(8)(a) can be issued documenting non-attendance. The matter can then proceed to court for parenting orders. Courts may take non-participation into account when making subsequent orders, including in relation to costs."}},{"@type":"Question","name":"How long does the FDR process take?","acceptedAnswer":{"@type":"Answer","text":"Most matters resolve in a matter of weeks rather than months. Discovery calls are typically available within a few days of enquiry, intake within a week or two, and the first joint session within two weeks of initial contact. Higher-conflict matters take longer, but still run significantly faster than the 18 to 36 month timeline for contested family law proceedings."}},{"@type":"Question","name":"Can I participate if I live in regional or rural Australia?","acceptedAnswer":{"@type":"Answer","text":"Yes. Our practice is entirely online so you can participate from anywhere in Australia. Both parties can be in different cities or states. Access to an accredited FDRP is no longer determined by postcode."}},{"@type":"Question","name":"Does this apply to financial matters as well as parenting?","acceptedAnswer":{"@type":"Answer","text":"Yes. We handle parenting matters, financial and property settlement, and Section 60I certificates. Whether you are mid-separation, already divorced with ongoing parenting disputes, or dealing with financial matters only, FDR is available and appropriate. The Family Law Amendment Act 2024, in force from 10 June 2025, codified the four-step property settlement framework into the Family Law Act and imposed new statutory obligations on FDR practitioners to inform parties about their duty of disclosure."}}]}]}'

build_page(
    filename="home-v2.html",
    title="Accredited Online Family Dispute Resolution Australia",
    meta_desc="Accredited Online Family Dispute Resolution in Australia. Parenting matters, financial settlement, and Section 60I certificates. Available nationally, conducted online.",
    canonical="/",
    current_page="/",
    schema_json=HOME_SCHEMA,
    extra_css=HOME_CSS,
    breadcrumbs=[],
    page_html=HOME_HTML,
    show_marquee=False,
)
print("Home done.")

# ─────────────────────────────────────────────
# ABOUT
# ─────────────────────────────────────────────
ABOUT_CSS = """
.about-hero{background:var(--charcoal);padding:120px 0 80px;position:relative;overflow:hidden}
.about-hero::before{content:'';position:absolute;inset:0;background:radial-gradient(ellipse 70% 60% at 70% 40%,rgba(196,135,58,0.1) 0%,transparent 60%);pointer-events:none}
.about-hero-inner{position:relative;z-index:1;max-width:800px}
.about-fold-grid{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:start;position:relative;z-index:1;width:100%;min-height:0}
.about-fold-grid .about-hero-inner{max-width:none}
.about-fold-grid .about-hero h1,
.about-hero.page-fold h1{font-size:clamp(1.6rem,3.4vw,3rem) !important}
.about-fold-image-panel{position:relative;align-self:stretch;opacity:0;animation:fadeUp 0.9s var(--ease) 0.4s forwards}
.about-fold-image-panel > .about-fold-img-real{position:absolute;inset:0;width:100%;height:100%}
.about-fold-image-panel img{width:100%;height:100%;object-fit:cover;object-position:center 40%;border-radius:8px}
.about-hero-tag{font-size:0.68rem;font-weight:700;letter-spacing:0.2em;text-transform:uppercase;color:var(--ochre);margin-bottom:24px;display:flex;align-items:center;gap:10px}
.about-hero-tag::before{content:'';width:24px;height:2px;background:var(--ochre);flex-shrink:0}
.about-hero h1{font-size:clamp(2.8rem,6vw,5.5rem);font-weight:800;line-height:1.0;letter-spacing:-0.03em;color:var(--white);margin-bottom:28px}
.about-hero h1 .accent{color:var(--ochre)}
.about-hero-sub{font-size:1.15rem;font-weight:400;color:rgba(253,250,246,0.6);line-height:1.8;max-width:600px}
.belief{background:var(--terra);padding:72px 0;position:relative;overflow:hidden}
.belief::before{content:'';position:absolute;top:-40%;right:-8%;width:400px;height:400px;border-radius:50%;background:rgba(255,255,255,0.06);pointer-events:none}
.belief-inner{position:relative;z-index:1;max-width:760px}
.belief-label{font-size:0.68rem;font-weight:700;letter-spacing:0.2em;text-transform:uppercase;color:rgba(253,250,246,0.55);margin-bottom:20px;display:block}
.belief-quote{font-size:clamp(1.4rem,3vw,2.2rem);font-weight:700;line-height:1.35;color:var(--white);letter-spacing:-0.02em}
.story-section{padding:100px 0}
.story-section.dark{background:var(--charcoal)}
.story-section.light{background:var(--white)}
.story-section.mid{background:var(--dust)}
.story-grid{display:grid;grid-template-columns:1fr 1.3fr;gap:80px;align-items:start}
.story-grid.reverse{grid-template-columns:1.3fr 1fr}
.story-num{font-size:5rem;font-weight:800;color:rgba(255,255,255,0.06);line-height:1;margin-bottom:16px;letter-spacing:-0.04em}
.story-num-dark{color:var(--dust-3)}
.story-left{position:sticky;top:100px}
.story-h2{font-size:clamp(1.8rem,3.2vw,2.6rem);font-weight:800;line-height:1.1;letter-spacing:-0.02em;margin-top:8px;margin-bottom:16px}
.approach-cards{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:20px}
.approach-card{background:var(--dust);border:1px solid var(--dust-3);border-radius:10px;padding:24px 22px;transition:border-color 0.25s,transform 0.25s}
.approach-card:hover{border-color:var(--ochre);transform:translateY(-3px)}
.approach-card-icon{width:36px;height:36px;border-radius:9px;background:var(--ochre-pale);color:var(--terra);display:flex;align-items:center;justify-content:center;margin-bottom:14px}
.approach-card h4{font-size:0.92rem;font-weight:700;color:var(--charcoal);margin-bottom:6px}
.approach-card p{font-size:0.84rem;font-weight:400;color:var(--mid);line-height:1.6}
.cred-cards{display:flex;flex-direction:column;gap:14px}
.cred-card{background:var(--dust);border:1px solid var(--dust-3);border-radius:10px;padding:20px 22px;display:flex;gap:14px;align-items:flex-start;transition:border-color 0.25s}
.cred-card:hover{border-color:var(--ochre)}
.cred-icon{width:40px;height:40px;border-radius:10px;background:var(--ochre-pale);color:var(--terra);display:flex;align-items:center;justify-content:center;flex-shrink:0}
.cred-text strong{display:block;font-size:0.88rem;font-weight:700;color:var(--charcoal);margin-bottom:3px}
.cred-text span{font-size:0.8rem;font-weight:400;color:var(--mid);line-height:1.45}
.diff-points{display:flex;flex-direction:column;border-top:1px solid rgba(255,255,255,0.08)}
.diff-point{display:flex;gap:18px;padding:20px 0;border-bottom:1px solid rgba(255,255,255,0.08);align-items:flex-start}
.diff-icon{width:36px;height:36px;border-radius:9px;background:rgba(196,135,58,0.12);color:var(--ochre-lt);display:flex;align-items:center;justify-content:center;flex-shrink:0}
.diff-h4{font-size:0.88rem;font-weight:700;color:var(--white);margin-bottom:3px}
.diff-p{font-size:0.82rem;font-weight:400;color:rgba(253,250,246,0.45);line-height:1.6}
.about-img{border-radius:10px;overflow:hidden;aspect-ratio:4/3}
.about-img-tall{aspect-ratio:3/4}
@media(max-width:960px){.story-grid,.story-grid.reverse{grid-template-columns:1fr;gap:48px}.story-left{position:static}.approach-cards{grid-template-columns:1fr}.about-fold-grid{grid-template-columns:1fr;gap:0}.about-fold-image-panel{position:static;align-self:auto;aspect-ratio:2/1;margin-top:32px;border-radius:8px;overflow:hidden}.about-fold-image-panel > .about-fold-img-real{position:static;width:100%;height:100%}.about-fold-image-panel img{width:100%;height:100%;object-fit:cover;border-radius:8px}}
"""

ABOUT_HTML = """
  <section class="about-hero page-fold" aria-labelledby="about-heading">
    <div class="wrap">
      <div class="about-fold-grid">
        <div class="about-hero-inner">
          <p class="about-hero-tag">Our practice</p>
          <h1 id="about-heading">Built for the<br>people the system<br><span class="accent">wasn't reaching.</span></h1>
          <p class="about-hero-sub">onlinefdr.com.au was founded on the belief that accredited Family Dispute Resolution should be reachable by anyone in Australia, without the months of waiting and the geographic limits that keep so many separating families from the help they need.</p>
        </div>
        <div class="about-fold-image-panel" aria-hidden="true">
          <div class="about-fold-img-real"><img src="/images/about-fold.jpg" alt="A modest, lived-in kitchen in a regional Australian weatherboard home at dusk. An open laptop and a steaming mug sit on a simple timber table, a warm pendant light overhead, the room empty of people. Through the large window behind the table, a paddock with dry grass and a lone gum tree stand against a pink-and-amber dusk sky, the visual signature of accredited online FDR reaching anywhere in the country." fetchpriority="high"></div>
        </div>
      </div>
    </div>
  </section>

  <!-- ABOVE-FOLD MARQUEE -->
  <div class="marquee-bar" aria-label="Accreditation and credentials" role="marquee">
    <div class="marquee-track" aria-hidden="true">
      <span class="marquee-item">AGD-Accredited FDRP <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Australian Mediation Association Member <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Section 60I Certificates (s 66H in WA) <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Conducted Securely Online <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Available Anywhere in Australia <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Free Discovery Call <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">No Obligation <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Confidential under the Family Law Act <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Both Parenting and Financial Matters <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">AGD-Accredited FDRP <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Australian Mediation Association Member <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Section 60I Certificates (s 66H in WA) <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Conducted Securely Online <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Available Anywhere in Australia <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Free Discovery Call <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">No Obligation <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Confidential under the Family Law Act <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Both Parenting and Financial Matters <span class="marquee-sep">&bull;</span></span>
    </div>
  </div>


  <div class="divider" aria-hidden="true"></div>

  <section class="belief" aria-label="Founding belief">
    <div class="wrap">
      <div class="belief-inner">
        <span class="belief-label">Why we exist</span>
        <p class="belief-quote">"Too many separating Australians can't get to the help they need. Distance, waiting lists, and the time the system takes all stand in the way. We built this practice to bring resolution within reach."</p>
      </div>
    </div>
  </section>

  <!-- 01: THE PROBLEM -->
  <section class="story-section light" aria-labelledby="story-1-heading">
    <div class="wrap">
      <div class="story-grid">
        <div class="story-left reveal">
          <div class="story-num story-num-dark" aria-hidden="true">01</div>
          <span class="section-label">The problem we set out to solve</span>
          <h2 class="story-h2 section-h2" id="story-1-heading">The hardest part of FDR is not the conversation. It is <span class="accent">getting started.</span></h2>
          <div class="about-img-real" style="margin-top:28px"><img src="/images/about-section-01.jpg" alt="A weathered cast-iron directional signpost at a regional Australian crossroads, arms pointing to Dubbo 412 km, Broken Hill, Tamworth, Moree, and Mildura 780 km, illustrating the geographic spread of need for accessible FDR services across the country." loading="lazy" decoding="async"></div>
        </div>
        <div class="reveal reveal-d1">
          <p class="body-text">Family Dispute Resolution exists for a reason. The law requires separating parents to attempt it before going to court, and evidence consistently shows that negotiated outcomes are better for families, better for children, and far less damaging than contested proceedings.</p>
          <p class="body-text">The reality is more complicated. Government-funded FDR services are stretched. Waiting lists in major cities run to weeks. In regional and rural Australia, the wait can be months, and in some areas there is no local service at all.</p>
          <p class="body-text">Private FDR practitioners fill that gap. But the majority operate from offices in capital cities, requiring both parties to travel to the same location on the same day. For separated couples in different cities, different states, or different circumstances, that model creates its own barriers.</p>
          <div class="pull">
            <p>"The in-person model was designed around the practitioner's office. The online model is designed around the parties."</p>
          </div>
          <p class="body-text">We built onlinefdr.com.au to make accredited, professional FDR genuinely accessible. Every session is conducted online, which means no travel, no waiting rooms, no requirement to be in the same city. A family in Broken Hill, Broome, or Brisbane's outer suburbs can access the same quality of service as one in the inner city.</p>
        </div>
      </div>
    </div>
  </section>

  <div class="divider" aria-hidden="true"></div>

  <!-- 02: HOW WE WORK -->
  <section class="story-section mid" aria-labelledby="story-2-heading">
    <div class="wrap">
      <div class="story-grid reverse">
        <div class="reveal">
          <span class="section-label">02, How we work</span>
          <h2 class="story-h2 section-h2" id="story-2-heading">Structured, child-focused, and built around <span class="accent">resolution.</span></h2>
          <p class="body-text">Our practice uses a facilitative mediation model, the recognised standard for Family Dispute Resolution in Australia. Sessions are structured to give each party the space to be heard, to understand the other perspective, and to work toward an outcome that both can live with.</p>
          <p class="body-text">In parenting matters, every conversation is anchored to the needs, wellbeing, and future of the children involved. We work with parents to bring the voice of their children into the room, through what each parent knows and observes, without placing children in the process directly.</p>
          <div class="approach-cards">
            <div class="approach-card">
              <div class="approach-card-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/></svg></div>
              <h4>The child at the centre</h4>
              <p>Parenting arrangements anchored to the needs of children, not the preferences of parents.</p>
            </div>
            <div class="approach-card">
              <div class="approach-card-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg></div>
              <h4>Safe and confidential</h4>
              <p>FDR is protected by two distinct legal provisions: confidentiality (s10H Family Law Act) prevents disclosure, and inadmissibility (s10J) means that even if something is disclosed, it cannot be used as evidence in court.</p>
            </div>
            <div class="approach-card">
              <div class="approach-card-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg></div>
              <h4>Focused on outcomes</h4>
              <p>Practical, workable agreements. Not a forum for relitigating the past.</p>
            </div>
            <div class="approach-card">
              <div class="approach-card-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg></div>
              <h4>Genuinely national</h4>
              <p>Both parties can be in different cities or states. Geography is no longer a reason not to proceed.</p>
            </div>
          </div>
        </div>
        <div class="story-left reveal reveal-d2">
          <div class="about-img-real about-img-tall" style="margin-bottom:0"><img src="/images/about-supporting-1.jpg" alt="Our founder preparing for a mediation." loading="lazy" decoding="async"></div>
        </div>
      </div>
    </div>
  </section>

  <div class="divider" aria-hidden="true"></div>

  <!-- 03: CREDENTIALS PREAMBLE -->
  <section class="story-section light" aria-labelledby="story-3-heading">
    <div class="wrap">
      <div class="story-grid">
        <div class="story-left reveal">
          <div class="story-num story-num-dark" aria-hidden="true">03</div>
          <span class="section-label">Accreditation</span>
          <h2 class="story-h2 section-h2" id="story-3-heading">Properly credentialled, <span class="accent">properly accountable.</span></h2>
        </div>
        <div class="reveal reveal-d1">
          <p class="body-text" style="margin-top:0">Family Dispute Resolution is a regulated profession in Australia. Accredited FDRPs are registered with the Australian Government Attorney-General's Department and authorised to issue Section 60I certificates required before most parenting order applications.</p>
          <p class="body-text">Credentials matter. They are the difference between a qualified, accountable practitioner and someone offering a service without the training or professional obligations that protect clients.</p>
        </div>
      </div>
    </div>
  </section>

  <div class="divider" aria-hidden="true"></div>

  <!-- 03b: FOUNDER -->
  <section class="story-section light" aria-labelledby="story-3b-heading">
    <div class="wrap">
      <div class="story-grid">
        <div class="story-left reveal">
          <span class="section-label">The founder</span>
          <h2 class="story-h2 section-h2" id="story-3b-heading">Kevin Scrimshaw, founder of <span class="accent">onlinefdr.com.au.</span></h2>
          <p class="body-text" style="margin-top:16px">onlinefdr.com.au was founded by Kevin Scrimshaw, an accredited Family Dispute Resolution Practitioner registered with the Australian Government Attorney-General's Department (AGD FDRP Reg. No. F2003011) and a member of the Australian Mediation Association. Kevin leads the practice and continues to take on matters personally. His background and ongoing professional development are in mediation, conflict resolution, and family law process, not commercial litigation.</p>
          <p class="body-text">The practice operates online by design. Sessions are conducted via Google Meet. There is no shared waiting room, no commute for either party, and no geographic limit on who can be reached.</p>
          <p class="body-text">Kevin founded onlinefdr.com.au to make accredited FDR reachable for families the public system cannot get to in time, and for those who simply live too far from one to attend in person. The practice is built to extend that reach over time. Online sessions only. Every type of family dispute, every stage of separation.</p>
          <div class="cred-cards" style="margin-top:28px">
            <div class="cred-card">
              <div class="cred-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg></div>
              <div class="cred-text"><strong>AGD-Accredited FDRP</strong><span>Practitioners working under the onlinefdr.com.au brand are accredited by the Australian Government Attorney-General's Department, authorised to issue Section 60I certificates nationally.</span></div>
            </div>
            <div class="cred-card">
              <div class="cred-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="6"/><path d="M15.477 12.89L17 22l-5-3-5 3 1.523-9.11"/></svg></div>
              <div class="cred-text"><strong>Australian Mediation Association</strong><span>Members of the AMA, subject to the AMA Code of Ethics and professional conduct standards.</span></div>
            </div>
          </div>
        </div>
        <div class="reveal reveal-d1">
          <div class="principal-headshot-real" style="aspect-ratio:4/5;margin-bottom:24px"><img src="/images/about-kevin-headshot.jpg" alt="Kevin Scrimshaw, founder of onlinefdr.com.au, professional portrait." loading="lazy" decoding="async"></div>
          <div class="principal-note" style="margin-top:0">
            <p>"Most of the families who reach this practice have already waited months for an option that was meant to be available. The work is to remove those barriers, not add new ones."</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <div class="divider" aria-hidden="true"></div>

  <!-- 04: WHY ONLINE -->
  <section class="story-section dark" aria-labelledby="story-4-heading">
    <div class="wrap">
      <div class="story-grid">
        <div class="story-left reveal">
          <div class="story-num" aria-hidden="true">04</div>
          <span class="section-label section-label-light">Why online</span>
          <h2 class="story-h2 section-h2-light" id="story-4-heading">Why every session runs <span class="accent">online.</span></h2>
          <p style="font-size:1rem;font-weight:400;color:rgba(253,250,246,0.55);line-height:1.8;margin-top:16px">The decision to operate entirely online was not about convenience. It was about access. The communities that need FDR most are precisely the communities the traditional in-person model serves least well.</p>
        </div>
        <div class="diff-points reveal reveal-d1">
          <div class="diff-point">
            <div class="diff-icon"><svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg></div>
            <div><p class="diff-h4">Genuinely national</p><p class="diff-p">Available to any separating couple in Australia, regardless of where they are.</p></div>
          </div>
          <div class="diff-point">
            <div class="diff-icon"><svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg></div>
            <div><p class="diff-h4">Safer for high-conflict matters</p><p class="diff-p">Physical separation throughout. Shuttle mediation means parties are genuinely in different locations.</p></div>
          </div>
          <div class="diff-point">
            <div class="diff-icon"><svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg></div>
            <div><p class="diff-h4">Faster than the alternative</p><p class="diff-p">Typically available within two weeks of first enquiry. Government services in many areas have waiting lists of months.</p></div>
          </div>
          <div class="diff-point">
            <div class="diff-icon"><svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg></div>
            <div><p class="diff-h4">Less costly than contested proceedings</p><p class="diff-p">Contested family law proceedings commonly cost tens of thousands of dollars per party. FDR costs significantly less than that and is usually resolved in weeks.</p></div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="page-cta" id="discovery" aria-labelledby="about-cta-heading">
    <div class="wrap">
      <div class="page-cta-inner">
        <span class="page-cta-eyebrow">Take the first step</span>
        <h2 id="about-cta-heading">Ready to find out if FDR is right for your situation?</h2>
        <p>A free discovery call with an accredited practitioner. No pressure, no commitment. Just a straight conversation about your options.</p>
        <div class="page-cta-actions">
          <a href="https://calendar.app.google/zwNm4dzYnwAwhwxY8" class="btn-light">Book your free discovery call</a>
          <a href="tel:0399617544" class="btn-outline-light">Call (03) 9961 7544</a>
        </div>
        <span class="page-cta-note">Free &bull; Confidential &bull; No obligation &bull; Available nationally</span>
      </div>
    </div>
  </section>
"""

build_page(
    filename="about-v2.html",
    title="About onlinefdr.com.au | Accredited Online FDR Australia",
    meta_desc="onlinefdr.com.au was founded on the belief that accredited Family Dispute Resolution should be reachable by anyone in Australia, online and without long waits.",
    canonical="/about/",
    current_page="/about/",
    schema_json='{"@context":"https://schema.org","@graph":[{"@type":"AboutPage","@id":"https://onlinefdr.com.au/about/#aboutpage","url":"https://onlinefdr.com.au/about/","name":"About onlinefdr.com.au","about":{"@id":"https://onlinefdr.com.au/#organization"},"mainEntity":{"@id":"https://onlinefdr.com.au/#kevin-scrimshaw"}},{"@type":"Organization","@id":"https://onlinefdr.com.au/#organization","name":"onlinefdr.com.au","url":"https://onlinefdr.com.au/","logo":"https://onlinefdr.com.au/images/logo.png","sameAs":["https://www.facebook.com/onlinefdr/","https://www.instagram.com/onlinefdr.com.au/","https://www.linkedin.com/company/onlinefdr/"],"description":"Accredited online Family Dispute Resolution practice serving separating couples nationally across Australia.","founder":{"@id":"https://onlinefdr.com.au/#kevin-scrimshaw"},"areaServed":{"@type":"Country","name":"Australia"}},{"@type":"Person","@id":"https://onlinefdr.com.au/#kevin-scrimshaw","name":"Kevin Scrimshaw","jobTitle":"Founder","identifier":{"@type":"PropertyValue","propertyID":"AGD FDRP Registration Number","value":"F2003011"},"worksFor":{"@id":"https://onlinefdr.com.au/#organization"},"hasCredential":[{"@type":"EducationalOccupationalCredential","credentialCategory":"professional accreditation","name":"Accredited Family Dispute Resolution Practitioner","recognizedBy":{"@type":"GovernmentOrganization","name":"Australian Government Attorney-General\'s Department"}},{"@type":"EducationalOccupationalCredential","credentialCategory":"professional membership","name":"Member, Australian Mediation Association"}]}]}',
    extra_css=ABOUT_CSS,
    breadcrumbs=[("Home", "/"), ("About", "/about/")],
    page_html=ABOUT_HTML,
    show_marquee=False,
)

print("About done.")

# ─────────────────────────────────────────────
# SHARED: ARTICLE PAGE CSS
# ─────────────────────────────────────────────
ARTICLE_CSS = """
.article-page-header{background:var(--charcoal);padding:120px 0 72px;position:relative;overflow:hidden}
.article-page-header::before{content:'';position:absolute;inset:0;background:radial-gradient(ellipse 60% 70% at 80% 30%,rgba(196,135,58,0.09) 0%,transparent 60%);pointer-events:none}
.article-page-header-inner{position:relative;z-index:1;max-width:800px}
.article-page-header .page-label{color:var(--ochre-lt)}
.article-page-header h1{font-size:clamp(2.4rem,5.5vw,4.8rem);font-weight:800;line-height:1.0;letter-spacing:-0.03em;color:var(--white);margin-bottom:24px}
.article-page-header h1 .accent{color:var(--ochre)}
.article-page-header .page-intro{color:rgba(253,250,246,0.6)}

/* Four-step framework */
.four-steps{display:flex;flex-direction:column;gap:2px;border-radius:10px;overflow:hidden;background:var(--dust-3);margin:28px 0}
.four-step{display:grid;grid-template-columns:56px 1fr;background:var(--white)}
.four-step-num{background:var(--dust-2);display:flex;align-items:flex-start;justify-content:center;padding:22px 0;border-right:1px solid var(--dust-3)}
.four-step-num span{font-size:1.8rem;font-weight:800;color:var(--dust-3);margin-top:4px;letter-spacing:-0.03em}
.four-step-content{padding:20px 24px}
.four-step-content h4{font-size:0.92rem;font-weight:700;color:var(--charcoal);margin-bottom:6px}
.four-step-content p{font-size:0.86rem;font-weight:400;color:var(--mid);line-height:1.65;margin-bottom:0}

/* Order/agreement types */
.card-list{display:flex;flex-direction:column;gap:14px;margin:28px 0}
.card-item{border:1px solid var(--dust-3);border-radius:10px;padding:22px 24px;background:var(--white);transition:border-color 0.25s}
.card-item:hover{border-color:var(--ochre)}
.card-item-header{display:flex;align-items:center;gap:10px;margin-bottom:8px}
.card-dot{width:9px;height:9px;border-radius:50%;background:var(--terra);flex-shrink:0}
.card-item h3{font-size:0.95rem;font-weight:700;color:var(--charcoal)}
.card-item p{font-size:0.87rem;font-weight:400;color:var(--mid);line-height:1.65;margin-bottom:0}
.card-tag{display:inline-flex;font-size:0.62rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;padding:3px 10px;border-radius:100px;margin-top:8px}
.tag-amber{background:var(--ochre-pale);color:var(--ochre)}
.tag-terra{background:#FAF0EA;color:var(--terra)}
.tag-dust{background:var(--dust-2);color:var(--mid)}

/* Factor rows (best interests) */
.factor-rows{display:flex;flex-direction:column;gap:2px;border-radius:10px;overflow:hidden;background:var(--dust-3);margin:28px 0}
.factor-row{display:grid;grid-template-columns:48px 1fr;background:var(--white)}
.factor-num{background:var(--dust-2);display:flex;align-items:flex-start;justify-content:center;padding:18px 0;border-right:1px solid var(--dust-3)}
.factor-num span{font-size:1.4rem;font-weight:800;color:var(--dust-3);letter-spacing:-0.03em}
.factor-content{padding:18px 22px}
.factor-content h4{font-size:0.9rem;font-weight:700;color:var(--charcoal);margin-bottom:5px}
.factor-content p{font-size:0.84rem;font-weight:400;color:var(--mid);line-height:1.65;margin-bottom:0}

/* Consequences table */
.table-block{margin:28px 0;border:1px solid var(--dust-3);border-radius:10px;overflow:hidden}
.table-row{display:grid;grid-template-columns:1fr 1.5fr;border-bottom:1px solid var(--dust-3)}
.table-row:last-child{border-bottom:none}
.table-row.header{background:var(--charcoal)}
.table-cell{padding:14px 20px;font-size:0.85rem}
.table-row.header .table-cell{font-size:0.65rem;font-weight:700;letter-spacing:0.14em;text-transform:uppercase;color:rgba(255,255,255,0.5)}
.table-row:not(.header):nth-child(even) .table-cell{background:var(--dust-2)}
.table-row:not(.header):nth-child(odd) .table-cell{background:var(--white)}
.table-cell:first-child{font-weight:700;color:var(--charcoal);border-right:1px solid var(--dust-3)}
.table-cell:last-child{font-weight:400;color:var(--mid);line-height:1.55}

/* Time limit cards */
.time-cards{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:28px 0}
.time-card{border:1px solid var(--dust-3);border-radius:10px;padding:24px;background:var(--white)}
.time-val{font-size:clamp(2rem,4vw,3rem);font-weight:800;color:var(--charcoal);line-height:1;margin-bottom:8px;letter-spacing:-0.03em}
.time-val span{color:var(--terra);font-size:60%}
.time-label{font-size:0.78rem;font-weight:700;color:var(--charcoal);margin-bottom:6px}
.time-note{font-size:0.8rem;font-weight:400;color:var(--mid);line-height:1.55}

/* Super info */
.info-box{background:var(--dust);border:1px solid var(--dust-3);border-radius:10px;padding:28px 26px;margin:28px 0}
.info-box h3{font-size:1rem;font-weight:700;color:var(--charcoal);margin-bottom:16px}
.info-items{display:flex;flex-direction:column;gap:14px}
.info-item{display:flex;gap:12px;align-items:flex-start}
.info-icon{width:32px;height:32px;border-radius:8px;background:var(--ochre-pale);color:var(--terra);display:flex;align-items:center;justify-content:center;flex-shrink:0}
.info-item h4{font-size:0.86rem;font-weight:700;color:var(--charcoal);margin-bottom:3px}
.info-item p{font-size:0.82rem;font-weight:400;color:var(--mid);line-height:1.6;margin-bottom:0}

/* Sidebar image card (tight, no padding) */
.sidebar-card-img{padding:0;overflow:hidden}
.sidebar-card-img .img-placeholder{border:none;border-radius:0;width:100%}

/* Article body lists */
.article-body ul{margin:0 0 18px 22px;padding:0}
.article-body ul li{font-size:1rem;font-weight:400;color:var(--mid);line-height:1.85;margin-bottom:6px;padding-left:4px}
.article-body ul li::marker{color:var(--terra)}

/* Process steps (in article) */
.proc-steps{display:flex;flex-direction:column;border-left:2px solid var(--dust-3);margin:28px 0 28px 16px}
.proc-step{display:grid;grid-template-columns:44px 1fr;gap:20px;padding:0 0 40px 36px;position:relative}
.proc-step:last-child{padding-bottom:0}
.proc-dot{position:absolute;left:-9px;top:4px;width:17px;height:17px;border-radius:50%;background:var(--white);border:2px solid var(--dust-3);transition:border-color 0.2s,background 0.2s}
.proc-step:hover .proc-dot{border-color:var(--ochre);background:var(--ochre-pale)}
.proc-num{font-size:2.2rem;font-weight:800;color:var(--dust-3);line-height:1;flex-shrink:0;letter-spacing:-0.04em}
.proc-content h3{font-size:0.95rem;font-weight:700;color:var(--charcoal);margin-bottom:6px;margin-top:4px}
.proc-content p{font-size:0.88rem;font-weight:400;color:var(--mid);line-height:1.75;margin-bottom:0}
.proc-tag{display:inline-flex;font-size:0.64rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:var(--terra);background:var(--ochre-pale);padding:4px 10px;border-radius:100px;margin-top:10px}

@media(max-width:768px){
  .four-step{grid-template-columns:44px 1fr}
  .table-row{grid-template-columns:1fr}
  .table-cell:first-child{border-right:none;border-bottom:1px solid var(--dust-3)}
  .time-cards{grid-template-columns:1fr}
  .proc-step{grid-template-columns:1fr;gap:6px;padding-left:28px}
}
"""



# ─────────────────────────────────────────────
# PARENTING ORDERS (Children & Parenting)
# ─────────────────────────────────────────────
PO_HTML = """
  <header class="article-page-header page-fold">
    <div class="wrap">
      <div class="parenting-fold-grid">
        <div class="article-page-header-inner">
          <span class="page-label">Parenting</span>
          <h1><span class="accent">Parenting arrangements</span> after separation in Australia.</h1>
          <p class="page-intro">When parents separate, Australian family law offers three distinct paths for setting parenting arrangements. They are not equally desirable. This page explains each one in the order that is generally best for children and parents, and the trade-offs that come with each. References to "parents" throughout cover married, separated, divorced, and de facto parents. The Family Law Act applies equally to all.</p>
        </div>
        <div class="parenting-fold-image-panel" aria-hidden="true">
          <div class="parenting-fold-img-real"><img src="/images/parenting-fold.jpg" alt="A mother and father at the front door of a weatherboard home, handing off their young son for the changeover. The boy is wearing a backpack and holding a football, mid-step between his parents." fetchpriority="high"></div>
        </div>
      </div>
    </div>
  </header>

  <!-- ABOVE-FOLD MARQUEE -->
  <div class="marquee-bar" aria-label="Accreditation and credentials" role="marquee">
    <div class="marquee-track" aria-hidden="true">
      <span class="marquee-item">AGD-Accredited FDRP <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Australian Mediation Association Member <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Section 60I Certificates (s 66H in WA) <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Conducted Securely Online <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Available Anywhere in Australia <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Free Discovery Call <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">No Obligation <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Confidential under the Family Law Act <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Both Parenting and Financial Matters <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">AGD-Accredited FDRP <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Australian Mediation Association Member <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Section 60I Certificates (s 66H in WA) <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Conducted Securely Online <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Available Anywhere in Australia <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Free Discovery Call <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">No Obligation <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Confidential under the Family Law Act <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Both Parenting and Financial Matters <span class="marquee-sep">&bull;</span></span>
    </div>
  </div>


  <div class="wrap article-wrap">
    <div class="article-grid">
      <article class="article-body">

        <h2 id="three-paths">Three paths at a glance</h2>
        <p>Most separating parents do not need a court order. Most do not even need a lawyer to draft anything formal. The three paths below run from the most flexible and least adversarial to the most formal and most contested. Where it is safe and possible, the preference is always to stay at the top of this list.</p>
        <p>The colloquial term "Parenting Agreement" is sometimes used. The legal term in the Family Law Act 1975 is "Parenting Plan" (section 63C). This page uses the legal term throughout.</p>

        <div class="table-block" role="table" aria-label="Three paths for parenting arrangements">
          <div class="table-row header" role="row"><div class="table-cell" role="columnheader">Path</div><div class="table-cell" role="columnheader">What it is, and when to choose it</div></div>
          <div class="table-row" role="row"><div class="table-cell" role="cell"><strong>1. Parenting Plan</strong></div><div class="table-cell" role="cell">A written agreement between parents, signed and dated. Recognised under section 63C of the Family Law Act. Not court-approved. Easily updated by mutual agreement. <strong>Best when</strong> both parents can communicate, agreement is genuinely mutual, and flexibility matters more than enforceability.</div></div>
          <div class="table-row" role="row"><div class="table-cell" role="cell"><strong>2. Consent Orders</strong></div><div class="table-cell" role="cell">A court order made by agreement. Parents file an Application for Consent Orders and the court reviews and approves without a hearing. Legally enforceable. <strong>Best when</strong> both parents agree on the arrangements but want certainty, formal protection, and a higher bar against future change.</div></div>
          <div class="table-row" role="row"><div class="table-cell" role="cell"><strong>3. Contested Parenting Orders</strong></div><div class="table-cell" role="cell">A court order made after a hearing, where the judge decides. Used when parents cannot agree. The longest, most expensive, and most adversarial path. <strong>Best when</strong> agreement is genuinely impossible, or where there are serious safety concerns that require the court to step in.</div></div>
        </div>

        <div class="notice notice-amber">
          <p class="notice-label">Preparing for the joint session</p>
          <p>Parents who arrive at mediation having thought through what they actually want, what is working, and where they already agree tend to have shorter, calmer, and more productive sessions. The <a href="/downloads/onlinefdr-parenting-reflection-workbook.pdf">Pre-Mediation Parenting Reflection Workbook</a> is a private thinking document, not a form. Nothing in it needs to be filled out, signed, or returned. It is for each parent, separately, in their own time, ahead of the joint session.</p>
        </div>

        <div class="download-row">
          <div class="download-row-text">
            <h3>Pre-Mediation Parenting Reflection Workbook</h3>
            <p>A private thinking document for each parent to work through before the joint session. Covers time with the children, special days, major decisions, day-to-day life, money for the children, household practicalities, and how to handle change. Designed to surface what you already think, separately, so the joint session moves faster.</p>
          </div>
          <div class="download-row-buttons">
            <a href="/downloads/onlinefdr-parenting-reflection-workbook.pdf" class="btn-primary" download>Download PDF</a>
          </div>
        </div>

        <div class="img-real" style="aspect-ratio:16/9;margin:32px 0"><img src="/images/parenting-hero.jpg" alt="A father and his young son riding bicycles together along a leafy suburban Melbourne street on a bright spring morning, both wearing helmets, both smiling. The boy rides a small red kids' bike, the father rides a charcoal mountain bike." loading="lazy" decoding="async"></div>

        <h2 id="parenting-plan">1. Parenting Plan <span class="accent">(the flexible first option)</span></h2>
        <p>A Parenting Plan is a written agreement between parents about parenting arrangements. The term used in the Family Law Act 1975 is "Parenting Plan" (section 63C). For most amicable separations, this is the right place to land.</p>

        <p>To be recognised under section 63C, a Parenting Plan must be:</p>
        <ul>
          <li>In writing</li>
          <li>Signed and dated by both parents</li>
          <li>Made free of threat, duress, or coercion</li>
        </ul>

        <p>That is the legal threshold. There is no required format, no court filing, no lawyer required, and no fee. The plan can cover where the child lives, how time is divided, parental responsibility for major long-term decisions, communication, holidays, dispute-resolution procedures, and anything else relevant to the care, welfare, or development of the child.</p>

        <div class="notice notice-amber">
          <p class="notice-label">Why parents choose this path first</p>
          <p>A Parenting Plan can be updated at any time by mutual written agreement, as your children grow and circumstances change. There is no court application, no significant-change-in-circumstances threshold to meet, and no filing fee. This flexibility is the strongest reason to keep arrangements at the Plan level wherever both parents continue to communicate and act in good faith.</p>
        </div>

        <p><strong>What a Parenting Plan cannot do.</strong> A Parenting Plan is not legally enforceable in the way a court order is. If the other parent stops following the agreed arrangements, you cannot apply to the court for a contravention order on the basis of the plan alone. The plan is recognised by the Act and a court is likely to consider its terms in any later proceedings, but it does not, by itself, give you a path to enforcement.</p>

        <p>For most families this limitation is theoretical. For some, particularly where there is a history of one party not following through, the lack of enforceability is the reason to formalise the agreement as Consent Orders instead.</p>

        <h2 id="consent-orders">2. Consent Orders <span class="accent">(when you want it locked in)</span></h2>
        <p>Consent Orders are court orders made by agreement. Both parents agree on the terms, file an Application for Consent Orders with the Federal Circuit and Family Court of Australia, and a Judicial Registrar reviews the application. Where the proposed orders are in the best interests of the children, the Registrar makes the orders without a hearing.</p>

        <p>Once made, Consent Orders have the same legal force as orders made after a contested hearing. Breaching them carries real consequences. Changing them is deliberately harder than changing a Parenting Plan.</p>

        <p>The Consent Orders path makes sense when:</p>
        <ul>
          <li>Both parents agree on the arrangements but want them legally enforceable</li>
          <li>One or both parents want the structure and certainty of a court order without the cost and conflict of a contested hearing</li>
          <li>The matter is complex enough that formal documentation will reduce future disputes</li>
          <li>There is a realistic concern that one party may not honour an informal agreement</li>
        </ul>

        <p>A filing fee applies, and there may be additional legal costs if you have a lawyer draft the orders. The process from filing to approval typically takes a few weeks if the application is complete and the proposed orders are clearly in the child's best interests. There is no hearing for either parent to attend.</p>

        <div class="notice notice-terra">
          <p class="notice-label">A common misconception</p>
          <p>Consent Orders do not, by themselves, function as a recovery order. If the other parent withholds the child in breach of Consent Orders, you cannot rely on the Orders alone to require police action. You will still need to apply to the court for a recovery order. The advantage of having Consent Orders in this scenario is that the court already has parenting orders in place to enforce, which significantly speeds up the recovery process. Without any orders at all, you would be applying for parenting orders and a recovery order at the same time, which is slower and more complex.</p>
        </div>

        <h2 id="contested">3. Contested Parenting Orders <span class="accent">(the path of last resort)</span></h2>
        <p>Where parents cannot agree, the Federal Circuit and Family Court can make parenting orders after a hearing. The judge considers evidence from both sides, often with a family report and sometimes with an Independent Children's Lawyer, and makes final orders based on the child's best interests.</p>

        <p>This path is the most legally rigorous but also the most expensive, the most adversarial, and the slowest. Contested parenting matters can commonly take 18 to 36 months from filing to final hearing. Legal costs can typically reach tens of thousands of dollars per party. The toll on parents and children, beyond the cost, is significant.</p>

        <p>Before a contested application can be filed, parents must in most cases attempt Family Dispute Resolution and obtain a <a href="/section-60i/">Section 60I certificate</a> from an accredited FDR practitioner. Exemptions apply in limited circumstances, including family violence and urgent matters.</p>

        <div class="notice notice-terra">
          <p class="notice-label">If you or your children are not safe</p>
          <p>If you are experiencing family violence, or are concerned about the safety of a child, support is available. The <a href="/get-help/">Get Help</a> page lists national crisis and family violence services that operate independently of this practice. In immediate danger, call Triple Zero (000).</p>
        </div>

        <div class="proc-steps">
          <div class="proc-step"><div class="proc-dot"></div><div class="proc-num">1</div><div class="proc-content"><h3>Attempt Family Dispute Resolution</h3><p>Parties make a genuine attempt at FDR and obtain a <a href="/section-60i/">Section 60I certificate</a> before applying for contested parenting orders. The step the law expects in most cases. Exemptions apply for family violence, child abuse, urgent matters, and where the matter is genuinely not appropriate for FDR.</p><span class="proc-tag">Pre-action step</span></div></div>
          <div class="proc-step"><div class="proc-dot"></div><div class="proc-num">2</div><div class="proc-content"><h3>File an Initiating Application</h3><p>The applicant files with the court, setting out the orders sought. The other party files a Response. Both parties file financial statements and other required documents.</p></div></div>
          <div class="proc-step"><div class="proc-dot"></div><div class="proc-num">3</div><div class="proc-content"><h3>First return date and case management</h3><p>The matter is listed for a directions hearing. The court manages progression: ordering family reports, appointing an Independent Children's Lawyer where appropriate, and directing parties toward mediation or hearing.</p></div></div>
          <div class="proc-step"><div class="proc-dot"></div><div class="proc-num">4</div><div class="proc-content"><h3>Interim orders</h3><p>Where parties cannot agree on arrangements while the matter is proceeding, the court can make interim parenting orders. These can remain in place for many months while the matter is finalised.</p></div></div>
          <div class="proc-step"><div class="proc-dot"></div><div class="proc-num">5</div><div class="proc-content"><h3>Family report</h3><p>A family consultant may prepare a family report involving interviews with both parents and children. These reports carry significant weight in contested proceedings.</p></div></div>
          <div class="proc-step"><div class="proc-dot"></div><div class="proc-num">6</div><div class="proc-content"><h3>Final hearing</h3><p>Both parties give evidence and are cross-examined. The judge applies the best-interests framework in section 60CC of the Family Law Act and makes final orders.</p><span class="proc-tag">18 to 36 months typical</span></div></div>
        </div>

        <h2 id="best-interests">The best-interests framework that applies to all three paths</h2>
        <p>Whether parents are agreeing privately to a Parenting Plan, asking the court to approve Consent Orders, or in a contested hearing, the same legal framework governs what the arrangements should look like. Section 60CC of the Family Law Act, as amended in May 2024, requires that the child's best interests are the paramount consideration. The court works through six general factors to assess what those best interests require. The 2024 amendments also removed the presumption of equal shared parental responsibility, simplified the best-interests test, and strengthened the focus on safety where family violence is present.</p>

        <div class="img-real" style="aspect-ratio:16/9;margin:32px 0"><img src="/images/parenting-supporting-1.jpg" alt="A mother and her young son sharing a weeknight dinner at the dining table at home. Sensible meat-and-three-veg meal, warm pendant light overhead, the boy mid-conversation, the mother listening." loading="lazy" decoding="async"></div>

        <div class="factor-rows">
          <div class="factor-row"><div class="factor-num"><span>1</span></div><div class="factor-content"><h4>Safety of the child and carers</h4><p>What arrangements promote safety from family violence, abuse, neglect, or other harm. Where genuine risk exists, the obligation to protect the child outweighs the benefit of maintaining a relationship with both parents. The Family Law Amendment Act 2024, in force from 10 June 2025, expanded the definition of family violence in section 4AB to expressly include economic and financial abuse.</p></div></div>
          <div class="factor-row"><div class="factor-num"><span>2</span></div><div class="factor-content"><h4>The child's own views</h4><p>Any views expressed by the child, considered in light of their age, maturity, and the circumstances in which those views were formed. Weight given to a child's views generally increases with age and maturity.</p></div></div>
          <div class="factor-row"><div class="factor-num"><span>3</span></div><div class="factor-content"><h4>Developmental, psychological, emotional and cultural needs</h4><p>What this particular child, at this stage of life, needs to thrive. Courts look at the child as an individual, not a generic child of their age.</p></div></div>
          <div class="factor-row"><div class="factor-num"><span>4</span></div><div class="factor-content"><h4>Each parent's capacity to meet those needs</h4><p>The practical capacity of each parent to provide for the child's identified needs. An assessment of capability, not character. Available time, stability, and the quality of the parent-child relationship.</p></div></div>
          <div class="factor-row"><div class="factor-num"><span>5</span></div><div class="factor-content"><h4>Benefit of the child's relationships with parents and significant others</h4><p>The benefit to the child of being able to have a relationship with both parents, and other people who are significant to them, where it is safe to do so. Since May 2024, the presumption of equal shared parental responsibility no longer applies, and this factor does not have elevated status relative to other considerations.</p></div></div>
          <div class="factor-row"><div class="factor-num"><span>6</span></div><div class="factor-content"><h4>Anything else relevant to this child's circumstances</h4><p>A catch-all allowing the court to consider any factor relevant to the particular family. No two families are the same, and rigid formulas fail children whose circumstances fall outside standard patterns.</p></div></div>
        </div>

        <h2 id="breach">When a parenting order is breached</h2>
        <p>This section is about Consent Orders and contested Parenting Orders. A Parenting Plan is not enforceable in the same way and the framework below does not apply to plans.</p>

        <p>A common misconception is that breaching a parenting order triggers automatic police intervention. It does not. The affected parent must apply to the court for a contravention order. The court then determines whether a breach occurred, whether the breaching party had a reasonable excuse, and what consequence is appropriate.</p>

        <div class="table-block" role="table" aria-label="Consequences of breaching a parenting order">
          <div class="table-row header" role="row"><div class="table-cell" role="columnheader">Consequence</div><div class="table-cell" role="columnheader">When it applies</div></div>
          <div class="table-row" role="row"><div class="table-cell" role="cell">Make-up time</div><div class="table-cell" role="cell">Additional time ordered with the parent denied contact. Most common for less serious breaches.</div></div>
          <div class="table-row" role="row"><div class="table-cell" role="cell">Fine</div><div class="table-cell" role="cell">Financial penalty. Amount varies with severity and frequency of the breach.</div></div>
          <div class="table-row" role="row"><div class="table-cell" role="cell">Community service</div><div class="table-cell" role="cell">Court-ordered community service as an alternative to or in addition to financial penalty.</div></div>
          <div class="table-row" role="row"><div class="table-cell" role="cell">Variation of orders</div><div class="table-cell" role="cell">The court changes the parenting orders in response to the breach, which may reduce the breaching parent's time or responsibility.</div></div>
          <div class="table-row" role="row"><div class="table-cell" role="cell">Costs order</div><div class="table-cell" role="cell">The breaching party is ordered to pay the other party's legal costs for the contravention application.</div></div>
          <div class="table-row" role="row"><div class="table-cell" role="cell">Imprisonment</div><div class="table-cell" role="cell">Reserved for serious, wilful, repeated breaches. The court must be satisfied no other consequence is adequate.</div></div>
        </div>

        <h2 id="recovery">Recovery orders</h2>
        <p>A recovery order is a separate court order that authorises police or other officers to find, recover, and deliver a child to a person entitled to care of the child. A recovery order is sought when a child has been unlawfully withheld or taken.</p>

        <p>The court can make a recovery order with or without an existing parenting order, though existing orders typically speed up the process. This is one of the practical reasons parents with a real risk of a child being withheld choose Consent Orders rather than relying on a Parenting Plan.</p>

        <ul>
          <li>If you have <strong>Consent Orders or contested parenting orders</strong> and the other parent withholds the child in breach, you can apply to the court for a recovery order. Having the parenting orders already in place generally makes this faster.</li>
          <li>If you have <strong>only a Parenting Plan</strong> (or no formal arrangements), you can still apply for a recovery order, but you must apply for parenting orders at the same time. The court is unlikely to make a recovery order without parenting orders that define the care arrangements.</li>
          <li>The court is <strong>not a child-recovery agency</strong>. Where the court makes a recovery order, it is the responsibility of the applicant and police to act on it. State or territory police typically execute recovery orders, with the Australian Federal Police involved in interstate or international matters.</li>
        </ul>

        <h2 id="changing">Changing arrangements over time</h2>
        <p>Children grow. Circumstances change. The right arrangement at age four is rarely the right arrangement at age fourteen. How easy it is to change the arrangements depends on which path you are on.</p>

        <div class="table-block" role="table" aria-label="How to change parenting arrangements">
          <div class="table-row header" role="row"><div class="table-cell" role="columnheader">If you have...</div><div class="table-cell" role="columnheader">To change it, you need...</div></div>
          <div class="table-row" role="row"><div class="table-cell" role="cell">A Parenting Plan</div><div class="table-cell" role="cell">A new written agreement, signed and dated by both parents. No court application, no fee. As simple as the original plan.</div></div>
          <div class="table-row" role="row"><div class="table-cell" role="cell">Consent Orders (both parents agree on the change)</div><div class="table-cell" role="cell">A new Application for Consent Orders, or in some cases, a new Parenting Plan that varies the Consent Orders. Either way, both parents must agree.</div></div>
          <div class="table-row" role="row"><div class="table-cell" role="cell">Consent Orders or contested orders (the other parent does not agree)</div><div class="table-cell" role="cell">A court application. The court applies the Rice and Asplund principle, requiring a significant change in circumstances since the orders were made before it will revisit final parenting orders. The threshold is deliberately high.</div></div>
        </div>

        <p>This is one of the strongest reasons to keep arrangements at the Parenting Plan level wherever both parents continue to communicate well. Court-made parenting orders, including Consent Orders, are designed to provide stability, which means they are designed to be difficult to change. Where genuine flexibility matters more than enforceability, a Parenting Plan is almost always the right answer.</p>

        <h2 id="grandparents">Grandparents and other significant persons</h2>
        <p>Parenting arrangements are not limited to the legal parents. Section 65C of the Family Law Act gives standing to apply for parenting orders to a grandparent or any other person concerned with the care, welfare, or development of the child. In practice, applications from non-parents are most common from grandparents who have been substantially involved in raising the child, or from step-parents in long-established relationships.</p>

        <p>The same best-interests framework in section 60CC applies. The court does not give automatic preference to biological parents over non-parents where the non-parent has been a primary caregiver. The arrangements that promote the child's best interests are the arrangements the court will make.</p>

        <p>Where grandparents or other significant persons want to be included in a Parenting Plan or Consent Orders, this can usually be addressed during FDR alongside the parents' agreements about parenting arrangements.</p>

        <h2 id="lawyer">When you genuinely need a lawyer</h2>
        <p>FDR practitioners are not lawyers and do not give legal advice. There are situations where independent legal advice is not optional. You should obtain legal advice:</p>
        <ul>
          <li>Before signing Consent Orders, so you understand what you are agreeing to and how it will be enforced</li>
          <li>Before commencing any contested court proceedings</li>
          <li>If you are served with an application for parenting orders</li>
          <li>If you are considering applying for a recovery order, particularly if there is no parenting order in place</li>
          <li>If there are urgent safety concerns about your child, including suspected abduction or relocation without consent</li>
        </ul>
        <p>Legal Aid may be available in family law matters depending on your circumstances and state or territory.</p>

        <div class="notice notice-terra">
          <p class="notice-label">Our role</p>
          <p>We are accredited Family Dispute Resolution Practitioners. Our role is to help separating parents reach their own agreements, which most commonly means working through a Parenting Plan or the basis for Consent Orders. We can also issue <a href="/section-60i/">Section 60I certificates</a> where the process has been properly completed. If your situation has moved beyond the point where FDR is appropriate, or if you need legal representation, we will tell you that directly.</p>
        </div>

      </article>

      <aside class="sidebar">
        <div class="sidebar-card sidebar-card-img">
          <div class="img-real" style="aspect-ratio:4/5"><img src="/images/parenting-supporting-2.jpg" alt="A five-year-old boy sitting at a small wooden desk in his bedroom, quietly absorbed in colouring a picture book. Soft afternoon light, a warm desk lamp, a teddy and books beside him." loading="lazy" decoding="async"></div>
        </div>
        <div class="sidebar-card">
          <h4>Where to start</h4>
          <p>A free discovery call to talk through which path is right for your situation. No pressure, no commitment.</p>
          <a href="/#discovery" class="btn-primary">Book a free discovery call</a>
        </div>
        <div class="sidebar-card sidebar-card-download">
          <h4>Pre-Mediation Parenting Reflection Workbook</h4>
          <p>A private thinking document, not a form. Nothing to fill out, sign, or return. For each parent to work through separately before the joint session.</p>
          <a href="/downloads/onlinefdr-parenting-reflection-workbook.pdf" class="btn-primary" download>Download PDF</a>
        </div>
        <nav class="sidebar-card sidebar-nav">
          <h5>On this page</h5>
          <ul>
            <li><a href="#three-paths"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>Three paths at a glance</a></li>
            <li class="sidebar-nav-download"><a href="/downloads/onlinefdr-parenting-reflection-workbook.pdf" download><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>Reflection workbook (PDF)</a></li>
            <li><a href="#parenting-plan"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>1. Parenting Plan</a></li>
            <li><a href="#consent-orders"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>2. Consent Orders</a></li>
            <li><a href="#contested"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>3. Contested Orders</a></li>
            <li><a href="#best-interests"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>The best-interests framework</a></li>
            <li><a href="#breach"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>When an order is breached</a></li>
            <li><a href="#recovery"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>Recovery orders</a></li>
            <li><a href="#changing"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>Changing arrangements</a></li>
            <li><a href="#grandparents"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>Grandparents and others</a></li>
            <li><a href="#lawyer"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>When you need a lawyer</a></li>
          </ul>
        </nav>
        <div class="sidebar-card">
          <h4>Related pages</h4>
          <ul class="related-links">
            <li><a href="/what-is-fdr/">What is FDR? <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg></a></li>
            <li><a href="/how-it-works/">How it works <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg></a></li>
            <li><a href="/section-60i/">Section 60I certificates <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg></a></li>
            <li><a href="/financial-settlement/">Financial settlement <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg></a></li>
          </ul>
        </div>
      </aside>
    </div>
  </div>

  <section class="page-faq" aria-labelledby="po-faq-heading">
    <div class="wrap">
      <div class="page-faq-header reveal">
        <span class="section-label">Common questions</span>
        <h2 id="po-faq-heading">Questions about children and parenting arrangements</h2>
      </div>
      <div class="faq-list reveal" style="max-width:760px">
        <div class="faq-item"><button class="faq-q" aria-expanded="false">What is the difference between a Parenting Plan and Consent Orders?<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></button><div class="faq-a"><p>A Parenting Plan is a written agreement between parents that is not court-approved and is not legally enforceable. Consent Orders are court orders made by agreement, approved by the Federal Circuit and Family Court, and have the same legal force as orders made after a contested hearing. Parenting Plans are more flexible and easier to change. Consent Orders are more rigid and harder to change, but they are enforceable.</p></div></div>
        <div class="faq-item"><button class="faq-q" aria-expanded="false">If we have Consent Orders, can the police enforce them automatically?<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></button><div class="faq-a"><p>No. State or territory police have no automatic power over parenting orders. If the other parent withholds the child in breach of Consent Orders, you must apply to the court for a contravention order, and separately for a recovery order if you need the child physically returned. Having Consent Orders in place makes this process faster than starting from a Parenting Plan, but the orders themselves do not function as a recovery instrument.</p></div></div>
        <div class="faq-item"><button class="faq-q" aria-expanded="false">Can we change our Parenting Plan as the children grow?<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></button><div class="faq-a"><p>Yes. This is one of the main practical advantages of a Parenting Plan. As long as both parents agree, you can update or replace the plan at any time with a new written agreement that is signed and dated. No court application, no fee, no significant-change-in-circumstances threshold. This flexibility is the reason most amicable separations stay at the Parenting Plan level.</p></div></div>
        <div class="faq-item"><button class="faq-q" aria-expanded="false">Can we change Consent Orders if we both agree?<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></button><div class="faq-a"><p>Yes. Where both parents agree to a change, new Consent Orders can be applied for, or in some cases a Parenting Plan can vary the Consent Orders. The significant-change-in-circumstances threshold applies where one parent wants to change the orders without the other parent's agreement. Where both agree, the change is straightforward.</p></div></div>
        <div class="faq-item"><button class="faq-q" aria-expanded="false">Do we still need to attempt FDR if we already agree?<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></button><div class="faq-a"><p>If you are agreeing privately to a Parenting Plan, there is no requirement to involve an FDR practitioner. If you are applying for Consent Orders, FDR is not required because the matter is not in dispute. FDR is the step the law expects before applying for contested parenting orders, with limited exemptions for family violence, urgent matters, and a few other circumstances.</p></div></div>
        <div class="faq-item"><button class="faq-q" aria-expanded="false">Do de facto parents have the same rights as married parents in parenting matters?<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></button><div class="faq-a"><p>Yes. The Family Law Act applies equally to all parents in parenting matters, regardless of marital status. Married, divorced, separated, and de facto parents all have the same rights and obligations in relation to their children. The same three paths apply (Parenting Plan, Consent Orders, contested orders), the same best-interests framework in section 60CC applies, and Section 60I certificates are required in the same circumstances before applying for contested parenting orders.</p></div></div>
        <div class="faq-item"><button class="faq-q" aria-expanded="false">Can grandparents apply for parenting orders?<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></button><div class="faq-a"><p>Yes. Section 65C of the Family Law Act expressly gives grandparents standing to apply for parenting orders, alongside any other person concerned with the care, welfare, or development of the child. The court applies the same best-interests framework regardless of whether the applicant is a parent, a grandparent, a step-parent, or another significant person. Grandparents who have been substantially involved in raising a child can also be included in a Parenting Plan or Consent Orders by agreement.</p></div></div>
        <div class="faq-item"><button class="faq-q" aria-expanded="false">Do I need a lawyer to apply for parenting orders?<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></button><div class="faq-a"><p>Not legally required, but strongly recommended. Parenting order proceedings are procedurally complex and the consequences are significant. Even for Consent Orders, getting legal advice on the proposed terms before signing is sensible. For contested proceedings, legal representation is close to essential. Legal Aid may be available depending on your circumstances and state or territory.</p></div></div>
      </div>
    </div>
  </section>

  <section class="page-cta" id="discovery" aria-labelledby="po-cta-heading">
    <div class="wrap">
      <div class="page-cta-inner">
        <span class="page-cta-eyebrow">Where most families should start</span>
        <h2 id="po-cta-heading">A Parenting Plan is reachable for most separating couples.</h2>
        <p>FDR is the structured way to get there. A free discovery call to talk through whether it is right for your situation.</p>
        <div class="page-cta-actions">
          <a href="https://calendar.app.google/zwNm4dzYnwAwhwxY8" class="btn-light">Book your free discovery call</a>
          <a href="tel:0399617544" class="btn-outline-light">Call (03) 9961 7544</a>
        </div>
        <span class="page-cta-note">Free &bull; Confidential &bull; No obligation &bull; Available nationally</span>
      </div>
    </div>
  </section>
"""

PO_CSS = """
.parenting-fold-grid{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:start;position:relative;z-index:1;width:100%;min-height:0}
.parenting-fold-image-panel{position:relative;align-self:stretch;opacity:0;animation:fadeUp 0.9s var(--ease) 0.4s forwards}
.parenting-fold-image-panel > .parenting-fold-img-real{position:absolute;inset:0;width:100%;height:100%}
.parenting-fold-image-panel img{width:100%;height:100%;object-fit:cover;object-position:center 40%;border-radius:8px}
.article-page-header.page-fold .article-page-header-inner{max-width:none}
@media(max-width:960px){
  .parenting-fold-grid{grid-template-columns:1fr;gap:0}
  .parenting-fold-image-panel{position:static;align-self:auto;aspect-ratio:2/1;margin-top:32px;border-radius:8px;overflow:hidden}
  .parenting-fold-image-panel > .parenting-fold-img-real{position:static;width:100%;height:100%}
  .parenting-fold-image-panel img{width:100%;height:100%;object-fit:cover;border-radius:8px}
}
"""

build_page(
    filename="parenting-v2.html",
    title="Parenting Arrangements After Separation | onlinefdr.com.au",
    meta_desc="Three paths for parenting arrangements under the Family Law Act: Parenting Plan, Consent Orders, and contested Parenting Orders. With the 2024 best-interests framework.",
    canonical="/parenting/",
    current_page="/parenting/",
    schema_json='{"@context":"https://schema.org","@graph":[{"@type":"WebPage","@id":"https://onlinefdr.com.au/parenting/#webpage","url":"https://onlinefdr.com.au/parenting/","name":"Parenting arrangements after separation in Australia","description":"Three paths for parenting arrangements after separation under the Family Law Act: Parenting Plan, Consent Orders, and contested Parenting Orders. The 2024 amendments to section 60CC and the best-interests framework. Recovery orders, contravention, changing arrangements, and the role of grandparents and other significant persons.","about":{"@id":"https://onlinefdr.com.au/#organization"},"mainEntity":{"@id":"https://onlinefdr.com.au/parenting/#faq"}},{"@type":"FAQPage","@id":"https://onlinefdr.com.au/parenting/#faq","mainEntity":[{"@type":"Question","name":"What is the difference between a Parenting Plan and Consent Orders?","acceptedAnswer":{"@type":"Answer","text":"A Parenting Plan is a written agreement between parents that is not court-approved and is not legally enforceable. Consent Orders are court orders made by agreement, approved by the Federal Circuit and Family Court, and have the same legal force as orders made after a contested hearing. Parenting Plans are more flexible and easier to change. Consent Orders are more rigid and harder to change, but they are enforceable."}},{"@type":"Question","name":"If we have Consent Orders, can the police enforce them automatically?","acceptedAnswer":{"@type":"Answer","text":"No. State or territory police have no automatic power over parenting orders. If the other parent withholds the child in breach of Consent Orders, you must apply to the court for a contravention order, and separately for a recovery order if you need the child physically returned. Having Consent Orders in place makes this process faster than starting from a Parenting Plan, but the orders themselves do not function as a recovery instrument."}},{"@type":"Question","name":"Can we change our Parenting Plan as the children grow?","acceptedAnswer":{"@type":"Answer","text":"Yes. This is one of the main practical advantages of a Parenting Plan. As long as both parents agree, you can update or replace the plan at any time with a new written agreement that is signed and dated. No court application, no fee, no significant-change-in-circumstances threshold. This flexibility is the reason most amicable separations stay at the Parenting Plan level."}},{"@type":"Question","name":"Can we change Consent Orders if we both agree?","acceptedAnswer":{"@type":"Answer","text":"Yes. Where both parents agree to a change, new Consent Orders can be applied for, or in some cases a Parenting Plan can vary the Consent Orders. The significant-change-in-circumstances threshold applies where one parent wants to change the orders without the other parent\'s agreement. Where both agree, the change is straightforward."}},{"@type":"Question","name":"Do we still need to attempt FDR if we already agree?","acceptedAnswer":{"@type":"Answer","text":"If you are agreeing privately to a Parenting Plan, there is no requirement to involve an FDR practitioner. If you are applying for Consent Orders, FDR is not required because the matter is not in dispute. FDR is the step the law expects before applying for contested parenting orders, with limited exemptions for family violence, urgent matters, and a few other circumstances."}},{"@type":"Question","name":"Do de facto parents have the same rights as married parents in parenting matters?","acceptedAnswer":{"@type":"Answer","text":"Yes. The Family Law Act applies equally to all parents in parenting matters, regardless of marital status. Married, divorced, separated, and de facto parents all have the same rights and obligations in relation to their children. The same three paths apply (Parenting Plan, Consent Orders, contested orders), the same best-interests framework in section 60CC applies, and Section 60I certificates are required in the same circumstances before applying for contested parenting orders."}},{"@type":"Question","name":"Can grandparents apply for parenting orders?","acceptedAnswer":{"@type":"Answer","text":"Yes. Section 65C of the Family Law Act expressly gives grandparents standing to apply for parenting orders, alongside any other person concerned with the care, welfare, or development of the child. The court applies the same best-interests framework regardless of whether the applicant is a parent, a grandparent, a step-parent, or another significant person. Grandparents who have been substantially involved in raising a child can also be included in a Parenting Plan or Consent Orders by agreement."}},{"@type":"Question","name":"Do I need a lawyer to apply for parenting orders?","acceptedAnswer":{"@type":"Answer","text":"Not legally required, but strongly recommended. Parenting order proceedings are procedurally complex and the consequences are significant. Even for Consent Orders, getting legal advice on the proposed terms before signing is sensible. For contested proceedings, legal representation is close to essential. Legal Aid may be available depending on your circumstances and state or territory."}}]}]}',
    extra_css=ARTICLE_CSS + PO_CSS,
    breadcrumbs=[("Home", "/"), ("Parenting", "/parenting/")],
    page_html=PO_HTML,
)
print("Parenting done.")

# ─────────────────────────────────────────────
# FINANCIAL SETTLEMENT
# ─────────────────────────────────────────────
FS_HTML = """
  <header class="article-page-header page-fold">
    <div class="wrap">
      <div class="fs-fold-grid">
        <div class="article-page-header-inner">
          <span class="page-label">Financial settlements</span>
          <h1><span class="accent">Financial settlements</span><br>after separation<br>in Australia.</h1>
          <p class="page-intro">Dividing property, superannuation, and debt is one of the most significant financial decisions most people will ever make. This page explains how financial settlements work in Australia, what changed under the Family Law Amendment Act 2024, and how FDR helps you reach a fair outcome without contested court proceedings.</p>
        </div>
        <div class="fs-fold-image-panel" aria-hidden="true">
          <div class="fs-fold-img-real"><img src="/images/financial-settlement-fold.jpg" alt="Two neighbouring Australian weatherboard and brick homes at dusk, separated by a narrow shared path with children's chalk drawings on the concrete, suggesting two households now sharing the care of children." fetchpriority="high"></div>
        </div>
      </div>
    </div>
  </header>

  <!-- ABOVE-FOLD MARQUEE -->
  <div class="marquee-bar" aria-label="Accreditation and credentials" role="marquee">
    <div class="marquee-track" aria-hidden="true">
      <span class="marquee-item">AGD-Accredited FDRP <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Australian Mediation Association Member <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Section 60I Certificates (s 66H in WA) <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Conducted Securely Online <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Available Anywhere in Australia <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Free Discovery Call <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">No Obligation <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Confidential under the Family Law Act <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Both Parenting and Financial Matters <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">AGD-Accredited FDRP <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Australian Mediation Association Member <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Section 60I Certificates (s 66H in WA) <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Conducted Securely Online <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Available Anywhere in Australia <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Free Discovery Call <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">No Obligation <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Confidential under the Family Law Act <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Both Parenting and Financial Matters <span class="marquee-sep">&bull;</span></span>
    </div>
  </div>


  <div class="wrap article-wrap">
    <div class="article-grid">
      <article class="article-body">

        <h2 id="why-informal-risky">Why informal arrangements are risky</h2>
        <p>Many separating couples divide their assets informally. They transfer the house, split the savings, and move on, assuming the matter is settled. Without a formal agreement, it is not.</p>
        <p>Without Consent Orders or a Binding Financial Agreement in place, either party retains the legal right to make a property settlement claim in the future, potentially years later, after you have rebuilt your finances or accumulated new assets. The informal arrangement provides no legal protection.</p>

        <div class="notice notice-amber">
          <p class="notice-label">Time limits apply</p>
          <p><strong>Married couples</strong> must apply for property orders within 12 months of a divorce becoming final. <strong>De facto couples</strong> must apply within two years of the end of the relationship. After these limits, court permission is required and is not guaranteed.</p>
        </div>

        <h2 id="four-step-framework">The four-step framework, now codified in legislation</h2>
        <p>There is no automatic 50/50 split in Australian family law. From 10 June 2025, the Family Law Amendment Act 2024 wrote the established four-step framework directly into the Family Law Act, in sections 79 (for married couples) and 90SM (for de facto couples). What was previously judge-made common law is now legislation.</p>
        <p>The framework applies to all separating couples, whether their settlement is decided by a court or negotiated privately, and the same logic governs FDR conversations about property and finance.</p>

        <div class="four-steps">
          <div class="four-step"><div class="four-step-num"><span>1</span></div><div class="four-step-content"><h4>Identify and value the asset pool</h4><p>All assets, liabilities, and financial resources of both parties. Real property, superannuation, investments, bank accounts, business interests, vehicles, and debts, whether held jointly, solely, in Australia, or overseas. Full and frank disclosure of every asset and liability is a statutory obligation.</p></div></div>
          <div class="four-step"><div class="four-step-num"><span>2</span></div><div class="four-step-content"><h4>Assess contributions</h4><p>Both financial and non-financial contributions. Income earned, property brought in, inheritances received, homemaking, caring for children, and supporting the other party's career. Where family violence has affected one party's ability to make contributions, the court can now take that into account explicitly.</p></div></div>
          <div class="four-step"><div class="four-step-num"><span>3</span></div><div class="four-step-content"><h4>Consider current and future circumstances</h4><p>Previously called "future needs," this step now uses updated language under the amended Act. It covers earning capacity, age, health, care responsibilities for children, the housing needs of any children, and the long-term financial impact of the relationship and any family violence on each party's career or earning potential.</p></div></div>
          <div class="four-step"><div class="four-step-num"><span>4</span></div><div class="four-step-content"><h4>Decide whether it is just and equitable to alter property interests</h4><p>A final check. The court is not required to make an order simply because parties are before it. Orders are only made if it would be just and equitable to alter the existing property interests, which prevents outcomes that are technically supported by the formula but genuinely unfair in context.</p></div></div>
        </div>

        <div class="notice notice-terra">
          <p class="notice-label">Wastage of property</p>
          <p>The Act now expressly allows the court to consider any significant or material wastage of property or financial resources caused intentionally or recklessly by a party. Gambling losses, dissipation of assets after separation, and deliberate destruction of value can all be brought into the contributions assessment. This was previously addressed through case law and is now written into the legislation.</p>
        </div>

        <h2 id="family-violence">Family violence in financial settlements</h2>
        <p>One of the most significant changes under the 2024 Act is the explicit role of family violence in property and financial matters. The principles set out in Kennon v Kennon, which recognised the economic effect of family violence on a party's ability to contribute and on their future circumstances, are now codified into the Family Law Act.</p>
        <p>The Act also expanded the definition of family violence in section 4AB to more clearly recognise economic or financial abuse, including:</p>
        <ul>
          <li>Unreasonably denying a partner financial autonomy</li>
          <li>Unreasonably withholding financial support</li>
          <li>Coercing a partner into taking on debt or incurring debt in their name</li>
          <li>Dowry-related abuse</li>
          <li>Controlling a partner's access to employment, income, or financial assets</li>
        </ul>
        <p>Where these patterns are present, they are no longer peripheral to a property settlement. They sit at the centre of the contributions assessment and the assessment of current and future circumstances. They are also a consideration in spousal maintenance applications.</p>

        <div class="notice notice-terra">
          <p class="notice-label">If family violence is part of your situation</p>
          <p>FDR is not appropriate in every case involving family violence, and a careful screening conversation comes first. Where FDR can proceed safely, shuttle mediation through separate Google Meet breakout rooms, additional safety arrangements, and other process adjustments are available. Where it cannot proceed safely, you will be advised accordingly.</p>
        </div>

        <h2 id="disclosure">Your duty of full and frank disclosure</h2>
        <p>Before the 2024 amendments, the duty of full and frank financial disclosure sat in the Federal Circuit and Family Court Rules. From 10 June 2025, it is written into the Family Law Act itself, in sections 71B (married couples) and 90RI (de facto couples).</p>
        <p>The duty begins the moment a party is preparing to start property or financial proceedings, not when proceedings are filed. It continues until the matter is finally resolved. It covers all relevant information and documents: bank statements, tax returns, payslips, business records, superannuation statements, and details of any trusts or companies.</p>
        <p>Non-compliance has real consequences. The court can take non-disclosure into account when dividing property, make costs orders against the non-disclosing party, stay or dismiss proceedings, or in extreme cases find a party in contempt.</p>

        <div class="notice notice-terra">
          <p class="notice-label">FDR practitioner obligation</p>
          <p>The same amendments place a new obligation on FDR practitioners to inform parties of their duty of disclosure, explain when the duty applies, set out the potential consequences of non-compliance, and encourage compliance. This is built into our intake and pre-mediation process. You will be given clear written information about disclosure before any financial mediation begins, including the <a href="/downloads/onlinefdr-disclosure-worksheet.pdf">Full and Frank Disclosure worksheet</a> to complete before your first joint financial session.</p>
        </div>

        <div class="download-row">
          <div class="download-row-text">
            <h3>Full and Frank Disclosure worksheet</h3>
            <p>The practical preparation document for financial FDR. Plain-English explanation of your statutory duty, a structured worksheet covering every category of income, asset, liability, superannuation, and financial resource, and a supporting-documents checklist. Each party completes their own copy before the joint session.</p>
          </div>
          <div class="download-row-buttons">
            <a href="/downloads/onlinefdr-disclosure-worksheet.pdf" class="btn-primary" download>Download PDF</a>
            <a href="/downloads/onlinefdr-disclosure-worksheet.docx" class="btn-outline" download>Download Word</a>
          </div>
        </div>

        <div class="img-real" style="aspect-ratio:16/9;margin:32px 0"><img src="/images/financial-hero.jpg" alt="A man standing at the kitchen island in his modern apartment at dusk, leaning forward on both hands over a spread of twenty or thirty financial documents and an open laptop, working out where to start." loading="lazy" decoding="async"></div>

        <h2 id="superannuation">How superannuation is treated in a <span class="accent">settlement</span></h2>
        <p>Superannuation is treated as property under the Family Law Act and can be divided as part of a financial settlement. A superannuation split does not involve early withdrawal. Instead, part of one party's superannuation interest is transferred to the other party's fund, remaining preserved until retirement.</p>

        <div class="info-box">
          <h3>Key things to understand about superannuation splitting</h3>
          <div class="info-items">
            <div class="info-item"><div class="info-icon"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg></div><div><h4>Requires a formal agreement or order</h4><p>Superannuation cannot be split informally. A splitting agreement or court order must be in place and the fund trustee must be notified.</p></div></div>
            <div class="info-item"><div class="info-icon"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg></div><div><h4>Defined benefit funds are more complex</h4><p>Public sector defined benefit schemes require specialist valuation and different procedural steps. Seek advice before agreeing to split these.</p></div></div>
            <div class="info-item"><div class="info-icon"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg></div><div><h4>Super and the rest of the asset pool interact</h4><p>The superannuation split does not have to mirror the overall property split. What matters is that the overall settlement, viewed holistically, is just and equitable.</p></div></div>
          </div>
        </div>

        <h2 id="de-facto">De facto relationships</h2>
        <p>De facto couples have substantially the same property settlement rights as married couples. The same four-step framework applies, mirrored in section 90SM of the Family Law Act. A de facto relationship is covered by the Act if it lasted at least two years, the couple has a child together, or one party made substantial contributions.</p>

        <div class="notice notice-amber">
          <p class="notice-label">Time limit for de facto couples</p>
          <p>De facto couples must apply within <strong>two years of the end of the relationship</strong>. This is shorter than the limit for married couples and is a common source of missed claims.</p>
        </div>

        <h2 id="spousal-maintenance">Spousal maintenance</h2>
        <p>Spousal maintenance is a separate but related question to property division. It is financial support paid by one former partner to the other where one party cannot adequately support themselves and the other has the capacity to pay. It can be ordered as periodic payments, a lump sum, or both.</p>
        <p>The 2024 Act updated the factors the court considers under sections 75(2) and 90SF(3). The renamed list of "considerations relating to current and future circumstances" now explicitly includes the effect of any family violence one party has subjected or exposed the other to, alongside the established considerations of age, health, earning capacity, care of children, and the standard of living that is reasonable in the circumstances.</p>
        <p>Spousal maintenance can be addressed in the same FDR conversation as property division, or as a standalone issue. It can be formalised through Consent Orders or a Binding Financial Agreement.</p>

        <h2 id="consent-orders-bfas">Consent Orders versus <span class="accent">Binding Financial Agreements</span></h2>
        <div class="card-list">
          <div class="card-item">
            <div class="card-item-header"><div class="card-dot"></div><h3>Consent Orders</h3></div>
            <p>A financial agreement submitted to the court for approval. Legally binding once approved by a registrar. Does not require a hearing. For most post-separation financial settlements, this is the more straightforward and reliably enforceable path.</p>
            <span class="card-tag tag-terra">Recommended for most</span>
          </div>
          <div class="card-item">
            <div class="card-item-header"><div class="card-dot"></div><h3>Binding Financial Agreements (BFAs)</h3></div>
            <p>A private contract that does not involve the court, but requires both parties to obtain independent legal advice before signing, and their lawyers must certify that advice was given. More involved to prepare than Consent Orders, and more vulnerable to being set aside if a court later finds the agreement was unjust or that proper advice was not given.</p>
            <span class="card-tag tag-amber">More complex, narrower use case</span>
          </div>
        </div>

        <div class="notice notice-terra">
          <p class="notice-label">BFAs: a note</p>
          <p>BFAs have their place, particularly for protecting pre-relationship assets or for second relationships. For most post-separation financial settlements, Consent Orders are simpler and more reliably enforceable. The right choice depends on the structure of the asset pool and the goals of both parties, and is a conversation worth having before drafting anything.</p>
        </div>

        <div class="img-real" style="aspect-ratio:16/9;margin:32px 0"><img src="/images/financial-supporting-1.jpg" alt="A woman working on her financial paperwork late at night, seated on a borrowed sofa in her new home. A laptop, a spread of documents, and a mug on the coffee table in front of her. Children's books at the side of the sofa." loading="lazy" decoding="async"></div>

        <h2 id="companion-animals">Companion animals</h2>
        <p>The 2024 Act introduced a new framework for dealing with family pets in property settlements. A "companion animal" is now a specific category of property: an animal kept primarily for companionship, excluding assistance animals, working animals, and animals used for business purposes.</p>
        <p>The court can order sole ownership to one party, transfer to a third party with consent, or sale. The court considers caregiving history, the financial cost of providing for the animal, any history of family violence or animal abuse, the attachment of each party and any children to the animal, and the willingness and ability of each party to care for it. The court cannot order shared ownership or shared care of a companion animal.</p>

        <h2 id="before-applying">Before applying to court</h2>
        <p>Going to court is not the first step. Schedule 1 Part 1 of the Federal Circuit and Family Court of Australia (Family Law) Rules 2021 sets out pre-action procedures that parties must follow before filing a financial application. The intent is that parties make a genuine attempt to resolve the dispute first.</p>
        <p>The procedures include making a genuine attempt at dispute resolution, exchanging documents relevant to the duty of disclosure, giving the other party written notice of any intention to start proceedings, and only filing if reasonable attempts to settle have been exhausted.</p>

        <h3 id="genuine-steps-certificate">The Genuine Steps Certificate</h3>
        <p>A Genuine Steps Certificate is the document the court uses to confirm that a party has complied with the pre-action procedures. It is signed by the party themselves, not by a lawyer and not by a mediator. The Applicant completes Parts A, B, and D of the prescribed form; a Respondent completes Parts A, C, and D. Each party signs a Statement of Truth confirming that the contents are accurate. The certificate is filed alongside the Initiating Application or Response to Initiating Application. Where a party is legally represented, the lawyer typically files the certificate as part of the wider application package, but the certifying signature remains the party's.</p>
        <p>Where pre-action procedures have not been followed, the certificate is used to set out the basis for an exemption (for example, family violence, urgency, or where a party would be unduly prejudiced by following the procedures). The court may stay proceedings, impose costs, or draw adverse inferences against a party who has not made a genuine attempt to resolve the dispute.</p>

        <h3 id="fdr-supports-genuine-steps">How FDR supports your Genuine Steps Certificate</h3>
        <p>Where financial FDR is attempted, the practitioner provides a Letter of Attendance and Genuine Effort at the conclusion of the process. The letter confirms the dates of attendance, the practitioner's assessment of whether each party made a genuine effort, and the outcome. The letter is not a court-issued document. It is supporting evidence that a party can attach to or refer to in their own Genuine Steps Certificate.</p>

                <h2 id="time-limits">Time limits</h2>
        <div class="time-cards">
          <div class="time-card"><div class="time-val">12<span> months</span></div><div class="time-label">Married couples</div><div class="time-note">From the date the divorce becomes final. Not from the date of separation. After this, court permission is required.</div></div>
          <div class="time-card"><div class="time-val">2<span> years</span></div><div class="time-label">De facto couples</div><div class="time-note">From the date the relationship ended. After this, court permission is required and is not guaranteed.</div></div>
        </div>

        <div class="pull">
          <p>"Property and financial settlements run on a clock. The framework is now in legislation, the disclosure duty is statutory, and the time limits are strict. Getting it right, in writing, is the work."</p>
        </div>

      </article>

      <aside class="sidebar">
        <div class="sidebar-card">
          <h4>Ready to talk through your financial situation?</h4>
          <p>A free discovery call to discuss where you stand and whether FDR is right for your circumstances.</p>
          <a href="/#discovery" class="btn-primary">Book a free discovery call</a>
        </div>
        <div class="sidebar-card sidebar-card-download">
          <h4>Full and Frank Disclosure worksheet</h4>
          <p>Pre-mediation preparation document. Plain-English explanation of your disclosure duty and a structured worksheet to complete before your first joint financial session.</p>
          <a href="/downloads/onlinefdr-disclosure-worksheet.pdf" class="btn-primary" download>Download PDF</a>
          <a href="/downloads/onlinefdr-disclosure-worksheet.docx" class="btn-outline" download>Download Word version</a>
        </div>
        <div class="sidebar-card sidebar-card-img">
          <div class="img-real" style="aspect-ratio:4/5"><img src="/images/financial-supporting-2.jpg" alt="A man at a kitchen table reviewing a bank statement on his laptop." loading="lazy" decoding="async"></div>
        </div>
        <nav class="sidebar-card sidebar-nav">
          <h5>On this page</h5>
          <ul>
            <li><a href="#why-informal-risky"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>Why informal is risky</a></li>
            <li><a href="#four-step-framework"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>Four-step framework</a></li>
            <li><a href="#family-violence"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>Family violence</a></li>
            <li><a href="#disclosure"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>Disclosure duty</a></li>
            <li class="sidebar-nav-download"><a href="/downloads/onlinefdr-disclosure-worksheet.pdf" download><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>Disclosure worksheet (PDF)</a></li>
            <li><a href="#superannuation"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>Superannuation</a></li>
            <li><a href="#de-facto"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>De facto relationships</a></li>
            <li><a href="#spousal-maintenance"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>Spousal maintenance</a></li>
            <li><a href="#consent-orders-bfas"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>Consent Orders vs BFAs</a></li>
            <li><a href="#companion-animals"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>Companion animals</a></li>
            <li><a href="#time-limits"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>Time limits</a></li>
          </ul>
        </nav>
        <div class="sidebar-card">
          <h4>Related pages</h4>
          <ul class="related-links">
            <li><a href="/section-60i/">Section 60I certificates <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg></a></li>
            <li><a href="/parenting/">Parenting <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg></a></li>
            <li><a href="/what-is-fdr/">What is FDR <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg></a></li>
          </ul>
        </div>
      </aside>
    </div>
  </div>

  <section class="page-faq" aria-labelledby="fs-faq-heading">
    <div class="wrap">
      <div class="page-faq-header reveal">
        <span class="section-label">Common questions</span>
        <h2 id="fs-faq-heading">Financial settlement questions answered</h2>
      </div>
      <div class="faq-list reveal" style="max-width:760px">
        <div class="faq-item"><button class="faq-q" aria-expanded="false">How is property divided after separation in Australia?<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></button><div class="faq-a"><p>There is no automatic 50/50 split. Since 10 June 2025, the Family Law Act uses a codified four-step framework: identify and value the asset pool, assess contributions, consider current and future circumstances, and determine whether it would be just and equitable to alter property interests at all. The result depends on the specific facts of each case.</p></div></div>
        <div class="faq-item"><button class="faq-q" aria-expanded="false">What changed in property settlement law in 2025?<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></button><div class="faq-a"><p>The Family Law Amendment Act 2024 commenced on 10 June 2025 and made significant changes to how property and financial matters are decided. The four-step framework was written directly into the Family Law Act, family violence and economic abuse became explicit considerations in contributions and current and future circumstances, the duty of disclosure was elevated from court rules into the Act itself, wastage of property was expressly codified, and a new framework was introduced for dealing with companion animals.</p></div></div>
        <div class="faq-item"><button class="faq-q" aria-expanded="false">Does family violence affect a property settlement?<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></button><div class="faq-a"><p>Yes. Under the Family Law Amendment Act 2024, in force from 10 June 2025, family violence is now an explicit consideration at multiple points in the four-step framework. The court can take into account how family violence affected a party's ability to contribute financially or non-financially, and how it affects their current and future circumstances. Economic and financial abuse, including denying financial autonomy, coercing debt, dowry abuse, and controlling access to employment, is expressly recognised as family violence under section 4AB.</p></div></div>
        <div class="faq-item"><button class="faq-q" aria-expanded="false">Does financial settlement apply to de facto couples?<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></button><div class="faq-a"><p>Yes. De facto couples have substantially the same property settlement rights as married couples, provided the relationship lasted at least two years, the couple has a child together, or one party made substantial contributions. The same four-step framework applies under section 90SM of the Family Law Act. De facto couples must apply within two years of the end of the relationship.</p></div></div>
        <div class="faq-item"><button class="faq-q" aria-expanded="false">Can superannuation be split after separation?<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></button><div class="faq-a"><p>Yes. Superannuation is treated as property and can be split. A split does not involve early withdrawal. Part of one party's superannuation is transferred to the other party's fund, remaining preserved until retirement. A formal agreement or order is required and the fund trustee must be notified.</p></div></div>
        <div class="faq-item"><button class="faq-q" aria-expanded="false">What is the duty of disclosure?<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></button><div class="faq-a"><p>Both parties to a property or financial matter have a statutory duty to give full and frank disclosure of all information and documents relevant to their financial position. This includes bank statements, tax returns, payslips, business records, superannuation statements, and details of any trusts or companies. Since 10 June 2025, this duty sits in the Family Law Act itself, applies from the moment a party is preparing to start proceedings, and continues until the matter is resolved. Non-compliance can result in costs orders, adjusted property division, or in extreme cases contempt findings.</p></div></div>
        <div class="faq-item"><button class="faq-q" aria-expanded="false">Do I need to wait 12 months before sorting out property settlement?<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></button><div class="faq-a"><p>No. Property settlement and divorce are separate legal processes. You can negotiate and formalise financial arrangements at any time after separation, without waiting for a divorce. In fact, waiting can be risky. The time limit for married couples runs from when the divorce is finalised, not the date of separation, but starting the conversation early generally results in better outcomes and less compounding conflict.</p></div></div>
        <div class="faq-item"><button class="faq-q" aria-expanded="false">What happens to a family pet in a property settlement?<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></button><div class="faq-a"><p>Under the Family Law Amendment Act 2024, in force from 10 June 2025, the court can make orders about a companion animal, considering caregiving history, the cost of care, any history of family violence or animal abuse, the attachment of each party and any children to the animal, and the willingness and ability of each party to care for it. The court can order sole ownership to one party, transfer to a third party with consent, or sale. The court cannot order shared ownership or shared care of a companion animal.</p></div></div>
      </div>
    </div>
  </section>

  <section class="page-cta" id="discovery" aria-labelledby="fs-cta-heading">
    <div class="wrap">
      <div class="page-cta-inner">
        <span class="page-cta-eyebrow">Before it becomes a legal battle</span>
        <h2 id="fs-cta-heading">The call you make before you call a lawyer.</h2>
        <p>A free discovery call to discuss your financial situation, understand your options, and find out whether FDR is right for your circumstances.</p>
        <div class="page-cta-actions">
          <a href="https://calendar.app.google/zwNm4dzYnwAwhwxY8" class="btn-light">Book your free discovery call</a>
          <a href="tel:0399617544" class="btn-outline-light">Call (03) 9961 7544</a>
        </div>
        <span class="page-cta-note">Free &bull; Confidential &bull; No obligation &bull; Available nationally</span>
      </div>
    </div>
  </section>
"""

FS_CSS = """
.fs-fold-grid{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:start;position:relative;z-index:1;width:100%;min-height:0}
.fs-fold-image-panel{position:relative;align-self:stretch;opacity:0;animation:fadeUp 0.9s var(--ease) 0.4s forwards}
.fs-fold-image-panel > .fs-fold-img-real{position:absolute;inset:0;width:100%;height:100%}
.fs-fold-image-panel img{width:100%;height:100%;object-fit:cover;object-position:center 40%;border-radius:8px}
@media(max-width:960px){
  .fs-fold-grid{grid-template-columns:1fr;gap:0}
  .fs-fold-image-panel{position:static;align-self:auto;aspect-ratio:1/1;margin-top:32px;border-radius:8px;overflow:hidden}
  .fs-fold-image-panel > .fs-fold-img-real{position:static;width:100%;height:100%}
  .fs-fold-image-panel img{width:100%;height:100%;object-fit:cover;border-radius:8px}
}
"""

build_page(
    filename="financial-settlement-v2.html",
    title="Financial Settlements After Separation | onlinefdr.com.au",
    meta_desc="How property, superannuation, and debt are divided after separation in Australia. The codified four-step framework, BFAs versus Consent Orders, and time limits.",
    canonical="/financial-settlement/",
    current_page="/financial-settlement/",
    schema_json='{"@context":"https://schema.org","@type":"WebPage","@id":"https://onlinefdr.com.au/financial-settlement/#webpage","url":"https://onlinefdr.com.au/financial-settlement/","name":"Financial Settlements After Separation in Australia","description":"How property, superannuation, and debt are divided after separation under the Family Law Act. The codified four-step framework following the Family Law Amendment Act 2024, family violence and disclosure obligations under sections 71B, 90RI, and 90YJA, companion animals, superannuation splitting, de facto rights, BFAs versus Consent Orders, and time limits.","about":{"@id":"https://onlinefdr.com.au/#organization"},"isPartOf":{"@id":"https://onlinefdr.com.au/#website"},"inLanguage":"en-AU"}',
    extra_css=ARTICLE_CSS + FS_CSS,
    breadcrumbs=[("Home", "/"), ("Financial Settlements", "/financial-settlement/")],
    page_html=FS_HTML,
)
print("Financial Settlement done.")

# ─────────────────────────────────────────────
# SECTION 60I
# ─────────────────────────────────────────────
S60I_HTML = """
  <header class="article-page-header page-fold">
    <div class="wrap">
      <div class="s60i-fold-grid">
        <div class="article-page-header-inner">
          <span class="page-label">Section 60I certificates</span>
          <h1>Section 60I certificates, <span class="accent">properly explained.</span></h1>
          <p class="page-intro">A Section 60I certificate documents the outcome of a genuine attempt at Family Dispute Resolution. It is not a product, and not a shortcut to court. This page explains what the certificate is, what it certifies, the five types under section 60I(8), and what the 2025 regulatory updates changed.</p>
        </div>
        <div class="s60i-fold-image-panel" aria-hidden="true">
          <div class="s60i-fold-img-real"><img src="/images/section-60i-fold.jpg" alt="A woman seated alone on a long timber bench in a quiet courthouse foyer, hands clasped in her lap, looking down. Tall windows line the wall behind her and a polished stone corridor recedes into the distance, suggesting the apprehension of waiting for a court matter." fetchpriority="high"></div>
        </div>
      </div>
    </div>
  </header>

  <!-- ABOVE-FOLD MARQUEE -->
  <div class="marquee-bar" aria-label="Accreditation and credentials" role="marquee">
    <div class="marquee-track" aria-hidden="true">
      <span class="marquee-item">AGD-Accredited FDRP <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Australian Mediation Association Member <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Section 60I Certificates (s 66H in WA) <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Conducted Securely Online <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Available Anywhere in Australia <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Free Discovery Call <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">No Obligation <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Confidential under the Family Law Act <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Both Parenting and Financial Matters <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">AGD-Accredited FDRP <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Australian Mediation Association Member <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Section 60I Certificates (s 66H in WA) <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Conducted Securely Online <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Available Anywhere in Australia <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Free Discovery Call <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">No Obligation <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Confidential under the Family Law Act <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Both Parenting and Financial Matters <span class="marquee-sep">&bull;</span></span>
    </div>
  </div>


  <div class="wrap article-wrap">
    <div class="article-grid">
      <article class="article-body">

        <h2 id="what-is-it">What is a Section 60I certificate?</h2>
        <p>A Section 60I certificate is a document issued by an accredited Family Dispute Resolution Practitioner under section 60I(8) of the Family Law Act 1975. Before applying for parenting orders in the Federal Circuit and Family Court of Australia, a party must in most cases file a Section 60I certificate. Without it, the court will not accept the application unless an exemption applies.</p>
        <p>The certificate is not a product to be ordered. It is the formal outcome of a proper FDR process, and it is issued only after the practitioner has conducted the required intake assessment and, where appropriate, the FDR sessions themselves. The type of certificate issued depends on what occurred during that process. The practitioner decides, not the parties.</p>

        <div class="notice notice-terra">
          <p class="notice-label">This is not a rubber stamp</p>
          <p>A Section 60I certificate cannot be issued on request or as a shortcut to court. It requires a proper FDR process, including individual intake sessions with each party. The type of certificate issued is determined by what the process reveals, not by what either party wants. Issuing a certificate without a genuine process is a breach of the practitioner's statutory obligations.</p>
        </div>

        <h2 id="why-it-exists">Why the certificate exists</h2>
        <p>The certificate requirement exists because contested family law proceedings are expensive, slow, and adversarial. Parliament decided that separating families should be required to attempt a structured, professionally facilitated resolution process before the courts become involved. The certificate is the evidence that this attempt was made, or that there was a proper reason it could not be.</p>
        <p>The requirement is not purely procedural. It reflects a clear policy intent: most parenting disputes can and should be resolved without a judge making decisions about a family's children. The certificate ensures that parties have genuinely tried, or that genuine reasons exist for why they could not.</p>
        <p>From June 2025, under the Family Law Amendment Act 2024, the court has express power to reject a parenting application for filing if a Section 60I certificate is required and has not been filed. Skipping the certificate is no longer a procedural oversight that can be corrected later; it can stop the application reaching the court at all.</p>

        <h2 id="vs-genuine-steps">Section 60I vs Genuine Steps Certificate</h2>
        <p>Two different certificates govern access to the family court system. They are often confused, but they do different jobs and are issued by different people.</p>
        <p>A Section 60I certificate is issued by an accredited Family Dispute Resolution Practitioner under section 60I(8) of the Family Law Act 1975 and Regulation 24 of the Family Law (Family Dispute Resolution Practitioners) Regulations 2025. It applies only to parenting applications under Part VII of the Family Law Act. The practitioner determines which type of certificate to issue based on what occurred in the FDR process.</p>
        <p>A Genuine Steps Certificate is signed by the party themselves under Schedule 1 of the Federal Circuit and Family Court of Australia (Family Law) Rules 2021. It is required for every initiating application and response, parenting and financial. Schedule 1 Part 1 governs financial proceedings; Part 2 governs parenting proceedings. Where a matter involves both, both Parts apply. The certificate is filed with the application. Where a party is legally represented, the lawyer typically files the certificate alongside the rest of the application package, but the certifying signature remains the party's.</p>

        <h3 id="vs-practice">What this means in practice</h3>
        <p>For a parenting application, a party files both: an FDRP-issued Section 60I certificate and a party-signed Genuine Steps Certificate. For a financial application, a party files only the Genuine Steps Certificate. For a combined parenting and financial application, all three documents apply.</p>
        <p>Where financial FDR has been attempted, the practitioner cannot issue a Section 60I certificate for the financial matter. That certificate is reserved for parenting under Part VII. Instead, the practitioner provides a Letter of Attendance and Genuine Effort confirming the dates of attendance, whether each party made a genuine effort, and the outcome. The letter is supporting evidence the party can attach to or refer to in their Genuine Steps Certificate.</p>
        <p>In Western Australia, the equivalent of a Section 60I certificate for parenting matters before the Family Court of Western Australia under state jurisdiction (unmarried parents) is a Section 66H certificate, issued under section 66H of the Family Court Act 1997 (WA).</p>

        <h2 id="five-types">The five certificate types under section 60I(8)</h2>
        <p>Section 60I(8) of the Family Law Act sets out five paragraphs under which a certificate can be issued. Each documents a different outcome. The practitioner issues the type that accurately reflects what occurred, and only that type. The 2025 regulations also updated the certificate template itself, which is set out in Schedule 1 of the Family Law (Family Dispute Resolution Practitioners) Regulations 2025.</p>

        <div class="card-list">
          <div class="card-item">
            <div class="card-item-header"><div class="card-dot"></div><h3>60I(8)(a): the other party did not attend</h3></div>
            <p>Issued when the person seeking the certificate was prepared to attend FDR, but the other party refused or failed to attend. The non-attendance is recorded. A court may take this into account when making orders about referrals to FDR, and when considering whether to award costs.</p>
            <span class="card-tag tag-terra">Other party did not attend</span>
          </div>
          <div class="card-item">
            <div class="card-item-header"><div class="card-dot"></div><h3>60I(8)(aa): FDR was not appropriate to conduct</h3></div>
            <p>Issued when the practitioner, after intake assessment, determines that conducting FDR would not be appropriate. The most common reasons are family violence, safety concerns, significant power imbalances, or inability to negotiate freely. Section 50 of the Family Law (Family Dispute Resolution Practitioners) Regulations 2025, which incorporates the matters listed in regulation 20(2), sets out what the practitioner must consider for the purposes of paragraph 60I(8)(aa).</p>
            <span class="card-tag tag-amber">Not appropriate to conduct</span>
          </div>
          <div class="card-item">
            <div class="card-item-header"><div class="card-dot"></div><h3>60I(8)(b): attended and made a genuine effort</h3></div>
            <p>Issued when both parties attended and all attendees made a genuine effort to resolve the dispute. The certificate does not record whether agreement was reached. Parties who reach full agreement typically do not file applications for contested orders and would not file the certificate; this type is most often filed when parties resolved some matters but go to court on others, or when no agreement was reached despite genuine effort.</p>
            <span class="card-tag tag-dust">Attended, genuine effort</span>
          </div>
          <div class="card-item">
            <div class="card-item-header"><div class="card-dot"></div><h3>60I(8)(c): attended but did not make a genuine effort</h3></div>
            <p>Issued when one or more attendees did not make a genuine effort to resolve the dispute. The assessment is made by the practitioner. A court may take this into account in subsequent proceedings, including when deciding costs orders.</p>
            <span class="card-tag tag-terra">Did not make a genuine effort</span>
          </div>
          <div class="card-item">
            <div class="card-item-header"><div class="card-dot"></div><h3>60I(8)(d): FDR began but was not appropriate to continue</h3></div>
            <p>Issued when FDR commenced but the practitioner determined, after sessions began, that it would not be appropriate to continue. This typically reflects safety concerns or other prescribed matters that emerged during the process rather than at intake.</p>
            <span class="card-tag tag-amber">Not appropriate to continue</span>
          </div>
        </div>

        <div class="notice notice-amber">
          <p class="notice-label">There is no "partial agreement" certificate</p>
          <p>A common misconception is that there is a certificate type for parties who reached agreement on some issues but not others. There is not. Section 60I(8) certifies whether a party attended and whether each party made a genuine effort. Whether agreement was reached is not what the certificate documents. Parties who reach partial agreement can record it in a Parenting Plan and bring the unresolved issues to court alongside a certificate under 60I(8)(b) or (8)(c).</p>
        </div>

        <div class="img-real" style="aspect-ratio:16/9;margin:32px 0"><img src="/images/section60i-hero.jpg" alt="A lone figure in a dark suit, briefcase in hand, climbing the wide granite steps toward the entrance of an imposing modernist family court building under cold overcast light." loading="lazy" decoding="async"></div>

        <h2 id="practitioner-role">The practitioner's role</h2>
        <p>Issuing a Section 60I certificate is a professional decision, not an administrative one. The Family Law Act and the Family Law (Family Dispute Resolution Practitioners) Regulations 2025 require the practitioner to make an independent assessment of what occurred in the process and to issue the certificate type that accurately reflects that assessment.</p>
        <p>This means the practitioner is required to exercise professional discretion when deciding:</p>
        <ul>
          <li>Whether a party made a genuine effort to resolve the dispute</li>
          <li>Whether FDR was, or became, inappropriate in the circumstances</li>
          <li>Which paragraph of section 60I(8) applies to the matter</li>
        </ul>
        <p>The practitioner's assessment is not subject to negotiation by the parties. Neither party can request a particular type of certificate, and the practitioner cannot agree to issue one type when the assessment supports another. The decision rests with the practitioner and is made in accordance with the practitioner's professional and statutory obligations.</p>

        <div class="notice notice-terra">
          <p class="notice-label">What changed on 1 April 2025</p>
          <p>The Family Law (Family Dispute Resolution Practitioners) Regulations 2025 commenced on 1 April 2025, replacing the 2008 Regulations. Schedule 1 of the new regulations contains an updated Section 60I certificate template, which all FDR practitioners are required to use for certificates issued from that date. The new template is issued to a single person rather than to the couple, scopes the certificate to the specific matters in dispute that the parenting order would deal with, and requires the practitioner to record their name, registration number, and the date of the last attempted or actual attendance at FDR. Certificates issued in the 12 months before 1 April 2025 using the old template continue to be accepted by the court.</p>
        </div>

        <h2 id="validity-and-issuance">Validity and who receives the certificate</h2>
        <p>Each party can request a certificate. Each party receives their own certificate, issued in their name. Under the 2025 regulations, the certificate is now addressed to a single person rather than to the couple jointly.</p>
        <p>A certificate must not be issued more than 12 months after the person's last attendance, or attempted attendance, at FDR. Once issued, a certificate is generally relied on by the court for filings made within 12 months. If proceedings are not commenced within that window, a fresh attempt at FDR is required.</p>

        <div class="notice notice-amber">
          <p class="notice-label">A note for Western Australia</p>
          <p>Western Australia has its own Family Court that exercises both Commonwealth and state jurisdiction. Section 60I certificates apply where the matter is filed in the Family Court of WA exercising Commonwealth jurisdiction (typically where the parties were married). Section 66H certificates under the Family Court Act 1997 (WA) apply where the FCWA exercises state jurisdiction (typically never-married parents in WA). Accredited FDR practitioners issue both where required. Clients in WA are welcome; the process is the same.</p>
        </div>

        <div class="img-real" style="aspect-ratio:16/9;margin:32px 0"><img src="/images/section60i-supporting-1.jpg" alt="Wide view of an Australian family courtroom from the judge's bench. Two bar tables face each other across an empty floor, three figures at each table, all with heads bowed. Cold fluorescent overhead light, pale timber panelling, charcoal carpet." loading="lazy" decoding="async"></div>

        <h2 id="exemptions">Exemptions from the FDR requirement</h2>
        <p>Certain circumstances exempt a party from the requirement to obtain a Section 60I certificate before applying for parenting orders. Exemptions are not automatic and must be established to the court's satisfaction. From June 2025, under the Family Law Amendment Act 2024, the court has express power to reject a parenting application for filing if a certificate is required and has not been filed.</p>
        <p>The exemptions include circumstances where there are reasonable grounds to believe a party has engaged in family violence or child abuse, where there is a risk of family violence or child abuse if there is a delay, where the application falls within one of the urgency-related grounds set out in s60I(9) such as risk of family violence or child abuse if there is a delay in applying, where a party is unable to participate effectively due to incapacity or remoteness, and where the application is for Consent Orders or in response to another party's application.</p>
        <p>Where there are reasonable grounds to believe family violence or child abuse, the court applies the exemption carefully. It recognises both the genuine need to protect victims and the potential for the exemption to be misused. The 2025 regulations require the FDR practitioner to consider prescribed matters at intake to identify these risks early, and where appropriate to issue a certificate under 60I(8)(aa) rather than conducting FDR that is not safe to proceed.</p>

        <div class="notice notice-terra">
          <p class="notice-label">If you or your children are not safe</p>
          <p>If you are experiencing family violence, or are concerned about the safety of a child, support is available. The <a href="/get-help/">Get Help</a> page lists national crisis and family violence services that operate independently of this practice. In immediate danger, call Triple Zero (000).</p>
        </div>

        <h2 id="after-issued">What happens after the certificate is issued</h2>
        <p>Once a Section 60I certificate is filed alongside an application for parenting orders, the matter enters the court system. The certificate documents what occurred in the FDR process without disclosing the content of discussions, which remain confidential.</p>
        <p>The type of certificate filed can affect the court's assessment of each party's conduct. A party who receives a certificate under 60I(8)(c) (did not make a genuine effort), or whose non-attendance led to a certificate under 60I(8)(a), may find their conduct noted and potentially reflected in costs orders under section 114UB of the Family Law Act.</p>

        <div class="notice notice-amber">
          <p class="notice-label">Confidentiality and inadmissibility</p>
          <p>FDR is protected by two distinct provisions of the Family Law Act. Confidentiality under section 10H prevents the practitioner from disclosing what was said in the process, with limited exceptions, and parties agree contractually under our terms to maintain the same confidentiality. Inadmissibility under section 10J goes further: even if confidentiality is breached and something is disclosed, that information cannot be admitted as evidence in court proceedings. The certificate documents the outcome of the process, not its content.</p>
        </div>

      </article>

      <aside class="sidebar">
        <div class="sidebar-card">
          <h4>Considering FDR for a parenting matter?</h4>
          <p>Start with a free discovery call. We will explain the process, walk through whether FDR is appropriate, and answer questions about Section 60I.</p>
          <a href="/#discovery" class="btn-primary">Book a free discovery call</a>
        </div>
        <div class="sidebar-card sidebar-card-img">
          <div class="img-real" style="aspect-ratio:4/5"><img src="/images/section60i-supporting-2.jpg" alt="A man in a suit standing composed on the steps of the Federal Court of Australia, briefcase in hand, his solicitor in robes a few steps behind." loading="lazy" decoding="async"></div>
        </div>
        <nav class="sidebar-card sidebar-nav">
          <h5>On this page</h5>
          <ul>
            <li><a href="#what-is-it"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>What is a Section 60I certificate</a></li>
            <li><a href="#why-it-exists"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>Why the certificate exists</a></li>
            <li><a href="#five-types"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>The five certificate types</a></li>
            <li><a href="#practitioner-role"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>The practitioner's role</a></li>
            <li><a href="#validity-and-issuance"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>Validity and issuance</a></li>
            <li><a href="#exemptions"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>Exemptions</a></li>
            <li><a href="#after-issued"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>After the certificate is issued</a></li>
          </ul>
        </nav>
        <div class="sidebar-card">
          <h4>Related pages</h4>
          <ul class="related-links">
            <li><a href="/parenting/">Parenting <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg></a></li>
            <li><a href="/financial-settlement/">Financial settlements <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg></a></li>
            <li><a href="/what-is-fdr/">What is FDR <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg></a></li>
          </ul>
        </div>
      </aside>
    </div>
  </div>

  <section class="page-faq" aria-labelledby="s60i-faq-heading">
    <div class="wrap">
      <div class="page-faq-header reveal">
        <span class="section-label">Common questions</span>
        <h2 id="s60i-faq-heading">Section 60I questions answered</h2>
      </div>
      <div class="faq-list reveal" style="max-width:760px">
        <div class="faq-item"><button class="faq-q" aria-expanded="false">How long is a Section 60I certificate valid?<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></button><div class="faq-a"><p>A certificate must not be issued more than 12 months after a party's last attendance, or attempted attendance, at FDR. Once issued, it is generally relied on by the court for filings made within 12 months. If proceedings are not commenced within that window, a fresh attempt at FDR is required.</p></div></div>
        <div class="faq-item"><button class="faq-q" aria-expanded="false">Do both parties get a certificate?<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></button><div class="faq-a"><p>Under the 2025 regulations, each party can request their own certificate, and each certificate is issued in that single person's name. There is no requirement for both parties to receive a certificate, and only the person who requests one is given one.</p></div></div>
        <div class="faq-item"><button class="faq-q" aria-expanded="false">Can the FDR practitioner refuse to issue a certificate?<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></button><div class="faq-a"><p>The practitioner cannot issue a certificate where a proper FDR process has not occurred. Where intake and (where appropriate) FDR sessions have occurred, the practitioner issues the certificate type that accurately reflects what happened. The practitioner does not choose whether to issue, but does decide which paragraph of section 60I(8) applies. That decision is the practitioner's professional judgment and is not negotiable.</p></div></div>
        <div class="faq-item"><button class="faq-q" aria-expanded="false">What if I disagree with the type of certificate issued?<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></button><div class="faq-a"><p>The certificate type reflects the practitioner's professional assessment of what occurred. It is not a negotiation. If a party believes the practitioner has acted improperly in making that assessment, the appropriate avenue is to raise a complaint through the practitioner's approved complaints body, not to seek a different certificate.</p></div></div>
        <div class="faq-item"><button class="faq-q" aria-expanded="false">Is a Section 60I certificate required for financial matters?<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></button><div class="faq-a"><p>No. Section 60I certificates apply only to parenting applications under Part VII of the Family Law Act. They do not apply to financial or property matters. However, the court does require a Genuine Steps Certificate for every initiating application and response, including financial. A Genuine Steps Certificate is signed by the party themselves under Schedule 1 of the Federal Circuit and Family Court of Australia (Family Law) Rules 2021 and confirms that the party has complied with the pre-action procedures. Where financial FDR has been attempted, the practitioner provides a Letter of Attendance and Genuine Effort that the party can attach to or refer to in their Genuine Steps Certificate.</p></div></div>
        <div class="faq-item"><button class="faq-q" aria-expanded="false">What if I have a family violence order against the other party?<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></button><div class="faq-a"><p>Reasonable grounds to believe there has been, or there is a risk of, family violence is one of the grounds for exemption from the FDR requirement. A party may be able to apply for parenting orders without first obtaining a Section 60I certificate. Legal advice is appropriate about whether the exemption applies to specific circumstances. Where FDR is attempted in a matter involving family violence, the practitioner may determine the matter is not appropriate to conduct or continue, and issue a certificate under 60I(8)(aa) or 60I(8)(d). Safety always takes priority over procedural requirements.</p></div></div>
        <div class="faq-item"><button class="faq-q" aria-expanded="false">Does the certificate reveal what was said in mediation?<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></button><div class="faq-a"><p>No. FDR is protected by two distinct provisions of the Family Law Act. Confidentiality under section 10H prevents disclosure of what was said. Inadmissibility under section 10J means that even if disclosed, it cannot be admitted as evidence in court. The certificate documents the outcome of the process, such as whether each party attended and whether each made a genuine effort, without revealing what was discussed.</p></div></div>
      </div>
    </div>
  </section>

  <section class="page-cta" id="discovery" aria-labelledby="s60i-cta-heading">
    <div class="wrap">
      <div class="page-cta-inner">
        <span class="page-cta-eyebrow">A proper process, not a shortcut</span>
        <h2 id="s60i-cta-heading">Talk through your matter before deciding the next step.</h2>
        <p>A free discovery call to understand whether FDR is appropriate for your circumstances and to walk through what the Section 60I process involves.</p>
        <div class="page-cta-actions">
          <a href="https://calendar.app.google/zwNm4dzYnwAwhwxY8" class="btn-light">Book your free discovery call</a>
          <a href="tel:0399617544" class="btn-outline-light">Call (03) 9961 7544</a>
        </div>
        <span class="page-cta-note">Free &bull; Confidential &bull; No obligation &bull; Available nationally</span>
      </div>
    </div>
  </section>
"""

S60I_CSS = """
.s60i-fold-grid{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:start;position:relative;z-index:1;width:100%;min-height:0}
.s60i-fold-image-panel{position:relative;align-self:stretch;opacity:0;animation:fadeUp 0.9s var(--ease) 0.4s forwards}
.s60i-fold-image-panel > .s60i-fold-img-real{position:absolute;inset:0;width:100%;height:100%}
.s60i-fold-image-panel img{width:100%;height:100%;object-fit:cover;object-position:center 40%;border-radius:8px}
@media(max-width:960px){
  .s60i-fold-grid{grid-template-columns:1fr;gap:0}
  .s60i-fold-image-panel{position:static;align-self:auto;aspect-ratio:3/2;margin-top:32px;border-radius:8px;overflow:hidden}
  .s60i-fold-image-panel > .s60i-fold-img-real{position:static;width:100%;height:100%}
  .s60i-fold-image-panel img{width:100%;height:100%;object-fit:cover;border-radius:8px}
}
"""

build_page(
    filename="section-60i-v2.html",
    title="Section 60I Certificates Explained | onlinefdr.com.au",
    meta_desc="What a Section 60I certificate is under the Family Law Act 1975, the five certificate types under section 60I(8), exemptions, and the practitioner's role in issuing.",
    canonical="/section-60i/",
    current_page="/section-60i/",
    schema_json='{"@context":"https://schema.org","@graph":[{"@type":"WebPage","@id":"https://onlinefdr.com.au/section-60i/#webpage","url":"https://onlinefdr.com.au/section-60i/","name":"Section 60I Certificates Explained","description":"What a Section 60I certificate is under the Family Law Act 1975, the five certificate types under section 60I(8), the 2025 regulatory updates, exemptions, and the practitioner\'s role in issuing.","about":{"@id":"https://onlinefdr.com.au/#organization"},"isPartOf":{"@id":"https://onlinefdr.com.au/#website"},"mainEntity":{"@id":"https://onlinefdr.com.au/section-60i/#faq"},"inLanguage":"en-AU"},{"@type":"FAQPage","@id":"https://onlinefdr.com.au/section-60i/#faq","mainEntity":[{"@type":"Question","name":"How long is a Section 60I certificate valid?","acceptedAnswer":{"@type":"Answer","text":"A certificate must not be issued more than 12 months after a party\'s last attendance, or attempted attendance, at FDR. Once issued, it is generally relied on by the court for filings made within 12 months. If proceedings are not commenced within that window, a fresh attempt at FDR is required."}},{"@type":"Question","name":"Do both parties get a certificate?","acceptedAnswer":{"@type":"Answer","text":"Under the 2025 regulations, each party can request their own certificate, and each certificate is issued in that single person\'s name. There is no requirement for both parties to receive a certificate, and only the person who requests one is given one."}},{"@type":"Question","name":"Can the FDR practitioner refuse to issue a certificate?","acceptedAnswer":{"@type":"Answer","text":"The practitioner cannot issue a certificate where a proper FDR process has not occurred. Where intake and (where appropriate) FDR sessions have occurred, the practitioner issues the certificate type that accurately reflects what happened. The practitioner does not choose whether to issue, but does decide which paragraph of section 60I(8) applies. That decision is the practitioner\'s professional judgment and is not negotiable."}},{"@type":"Question","name":"What if I disagree with the type of certificate issued?","acceptedAnswer":{"@type":"Answer","text":"The certificate type reflects the practitioner\'s professional assessment of what occurred. It is not a negotiation. If a party believes the practitioner has acted improperly in making that assessment, the appropriate avenue is to raise a complaint through the practitioner\'s approved complaints body, not to seek a different certificate."}},{"@type":"Question","name":"Is a Section 60I certificate required for financial matters?","acceptedAnswer":{"@type":"Answer","text":"No. Section 60I certificates apply only to parenting applications under Part VII of the Family Law Act. They do not apply to financial or property matters. However, the court does require a Genuine Steps Certificate for every initiating application and response, including financial. A Genuine Steps Certificate is signed by the party themselves under Schedule 1 of the Federal Circuit and Family Court of Australia (Family Law) Rules 2021 and confirms that the party has complied with the pre-action procedures. Where financial FDR has been attempted, the practitioner provides a Letter of Attendance and Genuine Effort that the party can attach to or refer to in their Genuine Steps Certificate."}},{"@type":"Question","name":"What if I have a family violence order against the other party?","acceptedAnswer":{"@type":"Answer","text":"Reasonable grounds to believe there has been, or there is a risk of, family violence is one of the grounds for exemption from the FDR requirement. A party may be able to apply for parenting orders without first obtaining a Section 60I certificate. Legal advice is appropriate about whether the exemption applies to specific circumstances. Where FDR is attempted in a matter involving family violence, the practitioner may determine the matter is not appropriate to conduct or continue, and issue a certificate under 60I(8)(aa) or 60I(8)(d). Safety always takes priority over procedural requirements."}},{"@type":"Question","name":"Does the certificate reveal what was said in mediation?","acceptedAnswer":{"@type":"Answer","text":"No. FDR is protected by two distinct provisions of the Family Law Act. Confidentiality under section 10H prevents disclosure of what was said. Inadmissibility under section 10J means that even if disclosed, it cannot be admitted as evidence in court. The certificate documents the outcome of the process, such as whether each party attended and whether each made a genuine effort, without revealing what was discussed."}}]}]}',
    extra_css=ARTICLE_CSS + S60I_CSS,
    breadcrumbs=[("Home", "/"), ("Section 60I Certificate", "/section-60i/")],
    page_html=S60I_HTML,
)
print("Section 60I done.")

# ─────────────────────────────────────────────
# JOIN THE TEAM
# ─────────────────────────────────────────────
JTT_CSS = """
.jtt-header{background:var(--charcoal);padding:120px 0 72px;position:relative;overflow:hidden}
.jtt-header::before{content:'';position:absolute;inset:0;background:radial-gradient(ellipse 60% 70% at 80% 30%,rgba(196,135,58,0.09) 0%,transparent 60%);pointer-events:none}
.jtt-header-grid{display:grid;grid-template-columns:1fr 1fr;gap:72px;align-items:start;position:relative;z-index:1}
.jtt-header h1{font-size:clamp(2.4rem,5vw,4.4rem);font-weight:800;line-height:1.0;letter-spacing:-0.03em;color:var(--white);margin-bottom:20px}
.jtt-header h1 .accent{color:var(--ochre)}
.jtt-header-sub{font-size:1.05rem;font-weight:400;color:rgba(253,250,246,0.6);line-height:1.8;margin-bottom:0}
.req-panel{background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);border-radius:10px;padding:24px 22px}
.req-panel h2{font-size:0.88rem;font-weight:700;color:var(--white);margin-bottom:16px}
.req-list{list-style:none;display:flex;flex-direction:column;gap:12px}
.req-item{display:flex;gap:10px;align-items:flex-start;font-size:0.84rem;font-weight:400;color:rgba(253,250,246,0.55);line-height:1.5}
.req-item svg{color:var(--ochre);flex-shrink:0;margin-top:1px}
.req-item strong{font-weight:700;color:var(--white);display:block;margin-bottom:2px}
.form-wrap{padding:64px 0 100px;max-width:800px}
.form-section-header{margin:52px 0 24px;padding-bottom:14px;border-bottom:1px solid var(--dust-3)}
.form-section-header:first-of-type{margin-top:0}
.form-section-num{font-size:0.62rem;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;color:var(--light-mid);margin-bottom:4px;display:block}
.form-section-title{font-size:1.3rem;font-weight:800;color:var(--charcoal);letter-spacing:-0.02em}
.field-row{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-bottom:18px}
.field-row.thirds{grid-template-columns:1fr 1fr 1fr}
.field-group{display:flex;flex-direction:column;gap:5px;margin-bottom:0}
.field-group.standalone{margin-bottom:18px}
label{font-size:0.8rem;font-weight:700;color:var(--charcoal);letter-spacing:0.01em}
label .req{color:var(--terra);margin-left:2px}
label .opt{font-size:0.72rem;font-weight:400;color:var(--light-mid);margin-left:6px}
.field-hint{font-size:0.74rem;font-weight:400;color:var(--light-mid);line-height:1.4;margin-top:2px}
input[type="text"],input[type="email"],input[type="tel"],input[type="url"],input[type="date"],select,textarea{font-family:var(--f);font-size:0.9rem;font-weight:400;color:var(--charcoal);background:var(--white);border:1px solid var(--dust-3);border-radius:6px;padding:11px 14px;width:100%;transition:border-color 0.2s,box-shadow 0.2s;-webkit-appearance:none;appearance:none}
input:focus,select:focus,textarea:focus{outline:none;border-color:var(--ochre);box-shadow:0 0 0 3px rgba(196,135,58,0.1)}
input.err,select.err,textarea.err{border-color:var(--terra)}
.field-err{font-size:0.74rem;color:var(--terra);margin-top:4px;display:none}
.field-err.show{display:block}
select{background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8' viewBox='0 0 12 8'%3E%3Cpath d='M1 1l5 5 5-5' stroke='%23A09690' stroke-width='1.5' fill='none' stroke-linecap='round'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:right 14px center;padding-right:36px;cursor:pointer}
textarea{resize:vertical;min-height:100px;line-height:1.6}
.check-group{display:flex;flex-direction:column;gap:10px;margin-top:4px}
.check-group.inline{flex-direction:row;flex-wrap:wrap;gap:8px}
.check-label{display:flex;align-items:flex-start;gap:10px;cursor:pointer;font-size:0.86rem;font-weight:400;color:var(--mid);line-height:1.4}
.check-label input[type="checkbox"],.check-label input[type="radio"]{width:17px;height:17px;min-width:17px;border:1.5px solid var(--dust-3);border-radius:4px;background:var(--white);cursor:pointer;margin-top:2px;padding:0;-webkit-appearance:none;appearance:none;transition:all 0.15s;display:flex;align-items:center;justify-content:center}
.check-label input[type="radio"]{border-radius:50%}
.check-label input[type="checkbox"]:checked,.check-label input[type="radio"]:checked{background:var(--terra);border-color:var(--terra)}
.check-label input[type="checkbox"]:checked::after{content:'';display:block;width:5px;height:8px;border:2px solid white;border-top:none;border-left:none;transform:rotate(45deg) translate(1px,-1px);margin-left:4px}
.check-label input[type="radio"]:checked::after{content:'';display:block;width:7px;height:7px;border-radius:50%;background:white;margin:auto}
.check-label:hover input{border-color:var(--ochre)}
.mandatory-field{background:var(--ochre-pale);border:1px solid rgba(196,135,58,0.3);border-radius:8px;padding:18px 20px;margin-bottom:16px}
.mandatory-field .check-label{font-size:0.86rem;color:var(--charcoal);font-weight:400}
.mandatory-field .check-label strong{font-weight:700}
.file-upload{position:relative}
.file-upload input[type="file"]{position:absolute;inset:0;opacity:0;cursor:pointer;width:100%;height:100%}
.file-display{border:1.5px dashed var(--dust-3);border-radius:6px;padding:18px 20px;display:flex;align-items:center;gap:12px;background:var(--white);cursor:pointer;transition:border-color 0.2s,background 0.2s}
.file-upload:hover .file-display,.file-upload.has-file .file-display{border-color:var(--ochre);background:var(--ochre-pale)}
.file-icon{width:32px;height:32px;border-radius:8px;background:var(--dust-2);display:flex;align-items:center;justify-content:center;color:var(--mid);flex-shrink:0}
.file-text strong{display:block;font-size:0.84rem;font-weight:700;color:var(--charcoal);margin-bottom:2px}
.file-text span{font-size:0.76rem;font-weight:400;color:var(--light-mid)}
.file-name{font-size:0.82rem;font-weight:600;color:var(--terra)}
.word-count{font-size:0.7rem;color:var(--light-mid);text-align:right;margin-top:4px}
.word-count.over{color:var(--terra)}
.form-divider{border:none;border-top:1px solid var(--dust-3);margin:8px 0 24px}
.form-submit{margin-top:40px;padding-top:32px;border-top:1px solid var(--dust-3)}
.form-submit-note{font-size:0.8rem;font-weight:400;color:var(--light-mid);line-height:1.65;margin-bottom:22px}
.form-submit-note a{color:var(--terra);text-decoration:none}
.btn-submit{display:inline-flex;align-items:center;gap:10px;background:var(--terra);color:var(--white);font-family:var(--f);font-size:0.95rem;font-weight:700;padding:17px 40px;border-radius:8px;border:2px solid var(--terra);cursor:pointer;transition:all 0.2s}
.btn-submit:hover{background:var(--terra-lt);border-color:var(--terra-lt)}
.btn-submit:disabled{opacity:0.5;cursor:not-allowed}
.form-success{display:none;text-align:center;padding:56px 28px;background:var(--ochre-pale);border:1px solid rgba(196,135,58,0.3);border-radius:12px}
.form-success.show{display:block}
.form-success-icon{width:52px;height:52px;background:var(--terra);border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 auto 20px;color:white}
.form-success h2{font-size:1.6rem;font-weight:800;color:var(--charcoal);letter-spacing:-0.02em;margin-bottom:10px}
.form-success p{font-size:0.95rem;font-weight:400;color:var(--mid);line-height:1.7}
@media(max-width:960px){.jtt-header-grid{grid-template-columns:1fr;gap:40px}}
@media(max-width:768px){.field-row,.field-row.thirds{grid-template-columns:1fr}}
"""

JTT_JS = """<script>
  document.querySelectorAll('input[name="online_experience"]').forEach(r=>{
    r.addEventListener('change',()=>{
      document.getElementById('platforms-field').style.display=r.value==='yes'?'block':'none';
    });
  });
  document.querySelectorAll('input[name="registration_clear"]').forEach(r=>{
    r.addEventListener('change',()=>{
      document.getElementById('complaints-field').style.display=r.value==='yes'?'block':'none';
    });
  });
  const fi=document.getElementById('pi-cert');
  if(fi){
    const uw=document.getElementById('upload-wrap'),ul=document.getElementById('upload-label');
    fi.addEventListener('change',()=>{if(fi.files.length){uw.classList.add('has-file');ul.innerHTML='<span class="file-name">'+fi.files[0].name+'</span>';}});
  }
  function wordCount(taId,cntId,limit){
    const ta=document.getElementById(taId),cnt=document.getElementById(cntId);
    if(!ta||!cnt)return;
    ta.addEventListener('input',()=>{const w=ta.value.trim()===''?0:ta.value.trim().split(/\\s+/).length;cnt.textContent=w+' / '+limit+' words';cnt.classList.toggle('over',w>limit)});
  }
  wordCount('background','bg-count',300);
  wordCount('motivation','mot-count',200);
  const form=document.getElementById('jtt-form'),submitBtn=document.getElementById('jtt-submit');
  if(form&&submitBtn){
    form.addEventListener('submit',function(e){
      e.preventDefault();
      submitBtn.disabled=true;
      submitBtn.textContent='Submitting...';
      if(typeof grecaptcha!=='undefined'){
        grecaptcha.ready(()=>{
          grecaptcha.execute('YOUR_RECAPTCHA_SITE_KEY',{action:'submit'}).then(token=>{
            fetch('/api/practitioner-application',{method:'POST',body:new FormData(form)})
              .then(r=>{if(r.ok){form.style.display='none';document.getElementById('form-success').classList.add('show')}else{submitBtn.disabled=false;submitBtn.textContent='Submit application'}})
              .catch(()=>{submitBtn.disabled=false;submitBtn.textContent='Submit application'});
          });
        });
      } else {
        form.style.display='none';document.getElementById('form-success').classList.add('show');
      }
    });
  }
</script>"""

JTT_HTML = """
  <div class="jtt-header page-fold">
    <div class="wrap">
      <div class="jtt-header-grid">
        <div>
          <span class="page-label" style="color:var(--ochre-lt)">Practitioner network</span>
          <h1>Join the online<span class="brand-fdr">fdr</span>.com.au network</h1>
          <p class="jtt-header-sub">We are building a national network of accredited online FDR practitioners to handle overflow referrals. If you hold current AGD registration, carry professional indemnity insurance, and are looking to take on additional matters, we want to hear from you.</p>
          <p class="jtt-header-sub" style="margin-top:16px">This is a contractor arrangement with revenue sharing on referred matters. We are selective. Quality, reliability, and a genuine commitment to client outcomes are what we look for.</p>
        </div>
        <div class="req-panel">
          <h2>Before you apply</h2>
          <ul class="req-list">
            <li class="req-item"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg><div><strong>Current AGD registration</strong>Applications without a valid AGD FDRP registration number will not be considered.</div></li>
            <li class="req-item"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg><div><strong>Current professional indemnity insurance</strong>Current certificate of currency required at time of application.</div></li>
            <li class="req-item"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg><div><strong>Onboarding observation period</strong>24 hours of co-mediation observation prior to taking independent referrals. An investment in the quality of our client experience.</div></li>
            <li class="req-item"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg><div><strong>Private workspace</strong>Suitable for confidential online sessions.</div></li>
            <li class="req-item"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg><div><strong>Interview</strong>Shortlisted applicants invited to a video interview before any offer is made.</div></li>
          </ul>
        </div>
      </div>
    </div>
  </div>

  <!-- ABOVE-FOLD MARQUEE -->
  <div class="marquee-bar" aria-label="Accreditation and credentials" role="marquee">
    <div class="marquee-track" aria-hidden="true">
      <span class="marquee-item">AGD-Accredited FDRP <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Australian Mediation Association Member <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Section 60I Certificates (s 66H in WA) <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Conducted Securely Online <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Available Anywhere in Australia <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Free Discovery Call <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">No Obligation <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Confidential under the Family Law Act <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Both Parenting and Financial Matters <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">AGD-Accredited FDRP <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Australian Mediation Association Member <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Section 60I Certificates (s 66H in WA) <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Conducted Securely Online <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Available Anywhere in Australia <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Free Discovery Call <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">No Obligation <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Confidential under the Family Law Act <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Both Parenting and Financial Matters <span class="marquee-sep">&bull;</span></span>
    </div>
  </div>


  <section class="wrap form-wrap" aria-labelledby="jtt-form-heading">
    <div id="form-success" class="form-success" role="status">
      <div class="form-success-icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg></div>
      <h2>Application received</h2>
      <p>Thank you for your interest in joining the onlinefdr.com.au network. We review all applications personally and will be in touch within five business days if we would like to proceed to interview.</p>
    </div>

    <form id="jtt-form" novalidate>

      <div class="form-section-header">
        <span class="form-section-num">01</span>
        <h2 class="form-section-title" id="jtt-form-heading">Professional credentials</h2>
      </div>

      <div class="field-row">
        <div class="field-group"><label for="full-name">Full legal name <span class="req">*</span></label><input type="text" id="full-name" name="full_name" required placeholder="As it appears on your AGD registration"></div>
        <div class="field-group"><label for="email">Email address <span class="req">*</span></label><input type="email" id="email" name="email" required placeholder="you@example.com"></div>
      </div>
      <div class="field-row">
        <div class="field-group"><label for="mobile">Mobile number <span class="req">*</span></label><input type="tel" id="mobile" name="mobile" required placeholder="04XX XXX XXX"></div>
        <div class="field-group"><label for="linkedin">LinkedIn profile URL <span class="opt">(optional)</span></label><input type="url" id="linkedin" name="linkedin" placeholder="https://linkedin.com/in/yourname"></div>
      </div>
      <hr class="form-divider">
      <div class="field-row">
        <div class="field-group"><label for="agd-num">AGD FDRP registration number <span class="req">*</span></label><input type="text" id="agd-num" name="agd_number" required placeholder="Your registration number"><p class="field-hint">Applications without a valid registration number cannot be considered.</p></div>
        <div class="field-group"><label for="agd-expiry">Registration expiry date <span class="req">*</span></label><input type="date" id="agd-expiry" name="agd_expiry" required></div>
      </div>
      <div class="field-row thirds">
        <div class="field-group"><label for="pi-provider">PI insurance provider <span class="req">*</span></label><input type="text" id="pi-provider" name="pi_provider" required placeholder="Insurance company"></div>
        <div class="field-group"><label for="pi-policy">PI policy number <span class="req">*</span></label><input type="text" id="pi-policy" name="pi_policy" required placeholder="Policy number"></div>
        <div class="field-group"><label for="pi-expiry">PI insurance expiry <span class="req">*</span></label><input type="date" id="pi-expiry" name="pi_expiry" required></div>
      </div>
      <div class="field-group standalone">
        <label>Certificate of currency <span class="req">*</span></label>
        <div class="file-upload" id="upload-wrap">
          <input type="file" id="pi-cert" name="pi_certificate" accept=".pdf,.jpg,.jpeg,.png" required>
          <div class="file-display">
            <div class="file-icon"><svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg></div>
            <div class="file-text"><strong id="upload-label">Upload current certificate of currency</strong><span>PDF, JPG or PNG, max 5MB</span></div>
          </div>
        </div>
      </div>

      <div class="form-section-header">
        <span class="form-section-num">02</span>
        <h2 class="form-section-title">Experience</h2>
      </div>

      <div class="field-row">
        <div class="field-group"><label for="years">Years practising as an accredited FDRP <span class="req">*</span></label><select id="years" name="years_practising" required><option value="" disabled selected>Select</option><option value="less-than-1">Less than 1 year</option><option value="1-2">1 to 2 years</option><option value="3-5">3 to 5 years</option><option value="6-10">6 to 10 years</option><option value="10+">More than 10 years</option></select></div>
        <div class="field-group"><label for="matters">Approximate matters conducted <span class="req">*</span></label><select id="matters" name="matters_conducted" required><option value="" disabled selected>Select</option><option value="1-10">1 to 10</option><option value="11-25">11 to 25</option><option value="26-50">26 to 50</option><option value="51-100">51 to 100</option><option value="100+">More than 100</option></select></div>
      </div>
      <div class="field-group standalone">
        <label>Primary matter types <span class="req">*</span></label>
        <div class="check-group inline">
          <label class="check-label"><input type="checkbox" name="matter_types" value="parenting"><span>Parenting</span></label>
          <label class="check-label"><input type="checkbox" name="matter_types" value="financial"><span>Financial</span></label>
          <label class="check-label"><input type="checkbox" name="matter_types" value="combined"><span>Combined</span></label>
          <label class="check-label"><input type="checkbox" name="matter_types" value="s60i-only"><span>Section 60I only</span></label>
        </div>
      </div>
      <div class="field-group standalone">
        <label>Have you conducted online FDR sessions? <span class="req">*</span></label>
        <div class="check-group">
          <label class="check-label"><input type="radio" name="online_experience" value="yes" required><span>Yes</span></label>
          <label class="check-label"><input type="radio" name="online_experience" value="no"><span>No, but I am set up and ready to do so</span></label>
        </div>
      </div>
      <div class="field-group standalone" id="platforms-field" style="display:none">
        <label for="platforms">Which platforms have you used? <span class="opt">(optional)</span></label>
        <input type="text" id="platforms" name="platforms" placeholder="e.g. Google Meet, Zoom, Teams">
      </div>

      <div class="form-section-header">
        <span class="form-section-num">03</span>
        <h2 class="form-section-title">Availability and capacity</h2>
      </div>

      <div class="field-row">
        <div class="field-group"><label for="state">State or territory <span class="req">*</span></label><select id="state" name="state" required><option value="" disabled selected>Select</option><option value="NSW">New South Wales</option><option value="VIC">Victoria</option><option value="QLD">Queensland</option><option value="WA">Western Australia</option><option value="SA">South Australia</option><option value="TAS">Tasmania</option><option value="ACT">Australian Capital Territory</option><option value="NT">Northern Territory</option></select></div>
        <div class="field-group"><label for="capacity">Additional matters per month <span class="req">*</span></label><select id="capacity" name="capacity" required><option value="" disabled selected>Select</option><option value="1-2">1 to 2</option><option value="3-5">3 to 5</option><option value="6-10">6 to 10</option><option value="10+">More than 10</option></select></div>
      </div>
      <div class="field-group standalone">
        <label>Typical availability <span class="req">*</span></label>
        <div class="check-group inline">
          <label class="check-label"><input type="checkbox" name="availability" value="weekday-daytime"><span>Weekday daytime</span></label>
          <label class="check-label"><input type="checkbox" name="availability" value="weekday-evenings"><span>Weekday evenings</span></label>
          <label class="check-label"><input type="checkbox" name="availability" value="weekends"><span>Weekends</span></label>
        </div>
      </div>

      <div class="form-section-header">
        <span class="form-section-num">04</span>
        <h2 class="form-section-title">Fit and motivation</h2>
      </div>

      <div class="field-group standalone">
        <label for="background">Brief professional background <span class="req">*</span></label>
        <textarea id="background" name="background" rows="5" required placeholder="Your background, qualifications, and current practice context. 300 words maximum."></textarea>
        <div class="word-count" id="bg-count">0 / 300 words</div>
      </div>
      <div class="field-group standalone">
        <label for="motivation">Why are you interested in joining the network? <span class="req">*</span></label>
        <textarea id="motivation" name="motivation" rows="4" required placeholder="200 words maximum."></textarea>
        <div class="word-count" id="mot-count">0 / 200 words</div>
      </div>
      <div class="field-group standalone">
        <label>Is FDR your primary professional activity? <span class="req">*</span></label>
        <div class="check-group">
          <label class="check-label"><input type="radio" name="primary_activity" value="yes" required><span>Yes, FDR is my primary practice</span></label>
          <label class="check-label"><input type="radio" name="primary_activity" value="part"><span>FDR is part of a broader practice</span></label>
          <label class="check-label"><input type="radio" name="primary_activity" value="no"><span>No, I am looking to expand into FDR</span></label>
        </div>
      </div>

      <div class="form-section-header">
        <span class="form-section-num">05</span>
        <h2 class="form-section-title">Practical and compliance</h2>
      </div>

      <div class="field-group standalone">
        <label>Current Working With Children Check or equivalent? <span class="req">*</span></label>
        <div class="check-group">
          <label class="check-label"><input type="radio" name="wwcc" value="yes" required><span>Yes</span></label>
          <label class="check-label"><input type="radio" name="wwcc" value="no"><span>No</span></label>
          <label class="check-label"><input type="radio" name="wwcc" value="na"><span>Not applicable to my practice</span></label>
        </div>
        <p class="field-hint">May be required depending on matter type. Does not automatically affect eligibility.</p>
      </div>
      <div class="field-group standalone">
        <label>Access to a private, distraction-free workspace for online sessions? <span class="req">*</span></label>
        <div class="check-group">
          <label class="check-label"><input type="radio" name="workspace" value="yes" required><span>Yes, I have a suitable private workspace</span></label>
          <label class="check-label"><input type="radio" name="workspace" value="no"><span>No</span></label>
        </div>
      </div>
      <div class="field-group standalone">
        <label>Any current complaints, investigations, or conditions on your AGD registration? <span class="req">*</span></label>
        <div class="check-group">
          <label class="check-label"><input type="radio" name="registration_clear" value="no" required><span>No</span></label>
          <label class="check-label"><input type="radio" name="registration_clear" value="yes"><span>Yes, please provide details below</span></label>
        </div>
      </div>
      <div class="field-group standalone" id="complaints-field" style="display:none">
        <label for="complaints">Please provide details</label>
        <textarea id="complaints" name="complaints_detail" rows="3" placeholder="Describe any complaints, investigations, or conditions currently in place."></textarea>
        <p class="field-hint">Disclosure does not automatically result in rejection. Applications are assessed on their individual merits.</p>
      </div>
      <div class="field-group standalone">
        <label for="how-heard">How did you hear about onlinefdr.com.au?</label>
        <select id="how-heard" name="how_heard"><option value="" disabled selected>Select</option><option value="google">Google search</option><option value="colleague">Colleague referral</option><option value="social">Social media</option><option value="ama">Australian Mediation Association</option><option value="other">Other</option></select>
      </div>

      <div class="form-section-header">
        <span class="form-section-num">06</span>
        <h2 class="form-section-title">Declarations</h2>
      </div>

      <div class="mandatory-field">
        <label class="check-label"><input type="checkbox" name="onboarding_agreed" required><span>I understand that joining the onlinefdr.com.au network requires completion of <strong>24 hours of co-mediation observation</strong> prior to taking independent referrals, and I agree to complete this onboarding requirement before accepting referred matters.</span></label>
      </div>
      <div class="mandatory-field">
        <label class="check-label"><input type="checkbox" name="workspace_declared" required><span>I confirm that I have access to a <strong>private, confidential workspace</strong> suitable for conducting online FDR sessions, and that I will maintain these standards for all referred matters.</span></label>
      </div>
      <div class="mandatory-field">
        <label class="check-label"><input type="checkbox" name="accuracy_confirmed" required><span>I confirm that all information in this application is <strong>accurate and complete</strong>, and I understand that providing false or misleading information will result in immediate disqualification and may be reported to the AGD.</span></label>
      </div>

      <div class="form-submit">
        <p class="form-submit-note">By submitting this application you confirm you have read and agreed to the declarations above. Your information will be held securely. See our <a href="/privacy/">Privacy Policy</a> for details.</p>
        <button type="submit" class="btn-submit" id="jtt-submit">Submit application <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg></button>
      </div>

    </form>
  </section>
"""

build_page(
    filename="join-the-team-v2.html",
    title="Join the Practitioner Network | onlinefdr.com.au",
    meta_desc="Accredited FDR practitioners: join the onlinefdr.com.au network and take on overflow referrals from a nationally positioned online practice.",
    canonical="/join-the-team/",
    current_page="/join-the-team/",
    schema_json='{"@context":"https://schema.org","@type":"WebPage","@id":"https://onlinefdr.com.au/join-the-team/#webpage","url":"https://onlinefdr.com.au/join-the-team/","name":"Join the Practitioner Network","description":"Application page for accredited Family Dispute Resolution Practitioners looking to join the onlinefdr.com.au national practitioner network. Requires current AGD registration and professional indemnity insurance.","about":{"@id":"https://onlinefdr.com.au/#organization"}}',
    extra_css=JTT_CSS,
    breadcrumbs=[("Home", "/"), ("Join the Team", "/join-the-team/")],
    page_html=JTT_HTML,
    robots="noindex, nofollow",
    show_marquee=False,
    extra_js=JTT_JS,
)
print("Join the Team done.")

# ─────────────────────────────────────────────
# HOW IT WORKS
# ─────────────────────────────────────────────
HIW_CSS = """
.hiw-header{background:var(--charcoal);padding:120px 0 80px;position:relative;overflow:hidden}
.hiw-header::before{content:'';position:absolute;inset:0;background:radial-gradient(ellipse 60% 70% at 80% 30%,rgba(196,135,58,0.09) 0%,transparent 60%);pointer-events:none}
.hiw-fold-grid{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:start;position:relative;z-index:1;width:100%;min-height:0}
.hiw-header-inner{position:relative;z-index:1}
.hiw-header h1{font-size:clamp(2.8rem,6vw,5.2rem);font-weight:800;line-height:1.0;letter-spacing:-0.03em;color:var(--white);margin-bottom:24px}
.hiw-header h1 .accent{color:var(--ochre)}
.hiw-header-sub{font-size:1.15rem;font-weight:400;color:rgba(253,250,246,0.6);line-height:1.8}
.hiw-fold-image-panel{position:relative;align-self:stretch;opacity:0;animation:fadeUp 0.9s var(--ease) 0.4s forwards}
.hiw-fold-image-panel > .hiw-fold-img-real{position:absolute;inset:0;width:100%;height:100%}
.hiw-fold-image-panel img{width:100%;height:100%;object-fit:cover;object-position:center 40%;border-radius:8px}

/* PROCESS TIMELINE */
.process-section{padding:100px 0;background:var(--dust)}
.process-intro{max-width:640px;margin-bottom:72px}
.process-intro h2{font-size:clamp(1.8rem,3.2vw,2.6rem);font-weight:800;line-height:1.1;letter-spacing:-0.03em;color:var(--charcoal);margin-bottom:14px}
.process-intro p{font-size:1rem;font-weight:400;color:var(--mid);line-height:1.8}
.timeline{display:flex;flex-direction:column;gap:0;position:relative}
.timeline::before{content:'';position:absolute;left:28px;top:0;bottom:0;width:2px;background:linear-gradient(to bottom,var(--ochre) 0%,var(--dust-3) 100%)}
.tl-item{display:grid;grid-template-columns:56px 1fr;gap:40px;padding-bottom:60px;position:relative}
.tl-item:last-child{padding-bottom:0}
.tl-dot-wrap{display:flex;justify-content:center;position:relative;z-index:1;padding-top:4px}
.tl-dot{width:18px;height:18px;border-radius:50%;border:2.5px solid var(--ochre);background:var(--dust);transition:background 0.25s}
.tl-item:hover .tl-dot{background:var(--ochre)}
.tl-content{padding-bottom:0}
.tl-step-num{font-size:0.62rem;font-weight:700;letter-spacing:0.2em;text-transform:uppercase;color:var(--ochre);margin-bottom:8px;display:block}
.tl-content h3{font-size:clamp(1.2rem,2.2vw,1.7rem);font-weight:800;line-height:1.1;letter-spacing:-0.02em;color:var(--charcoal);margin-bottom:14px}
.tl-content p{font-size:0.98rem;font-weight:400;color:var(--mid);line-height:1.85;margin-bottom:12px}
.tl-content p:last-of-type{margin-bottom:0}
.tl-content p strong{font-weight:700;color:var(--charcoal)}
.tl-meta{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px}
.tl-tag{display:inline-flex;align-items:center;gap:5px;font-size:0.68rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;padding:5px 12px;border-radius:100px}
.tl-tag-time{background:var(--ochre-pale);color:var(--ochre)}
.tl-tag-note{background:var(--dust-2);color:var(--mid)}
.tl-tag-terra{background:#FAF0EA;color:var(--terra)}
.tl-img{margin:20px 0 0;border-radius:8px;overflow:hidden}

/* WHAT TO EXPECT */
.expect-section{padding:80px 0;background:var(--white)}
.expect-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:44px}
.expect-card{border:1px solid var(--dust-3);border-radius:10px;padding:28px 26px;background:var(--dust);transition:border-color 0.25s,transform 0.25s}
.expect-card:hover{border-color:var(--ochre);transform:translateY(-2px)}
.expect-icon{width:40px;height:40px;border-radius:10px;background:var(--ochre-pale);color:var(--terra);display:flex;align-items:center;justify-content:center;margin-bottom:16px}
.expect-card h3{font-size:1rem;font-weight:800;color:var(--charcoal);margin-bottom:8px;letter-spacing:-0.01em}
.expect-card p{font-size:0.88rem;font-weight:400;color:var(--mid);line-height:1.7;margin-bottom:0}

/* TYPICAL TIMEFRAMES */
.timeframes-section{padding:80px 0;background:var(--charcoal);position:relative;overflow:hidden}
.timeframes-section::before{content:'';position:absolute;top:-30%;right:-5%;width:500px;height:500px;border-radius:50%;background:rgba(196,135,58,0.06);pointer-events:none}
.timeframes-header{max-width:580px;margin-bottom:56px;position:relative;z-index:1}
.timeframes-header h2{font-size:clamp(1.8rem,3.2vw,2.6rem);font-weight:800;line-height:1.1;letter-spacing:-0.03em;color:var(--white);margin-bottom:12px}
.timeframes-header p{font-size:0.95rem;font-weight:400;color:rgba(253,250,246,0.5);line-height:1.7}
.timeframes-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:2px;border-radius:12px;overflow:hidden;position:relative;z-index:1}
.tf-card{background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.08);padding:32px 28px;transition:background 0.25s}
.tf-card:hover{background:rgba(255,255,255,0.08)}
.tf-label{font-size:0.62rem;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;color:rgba(253,250,246,0.3);margin-bottom:10px;display:block}
.tf-type{font-size:1rem;font-weight:800;color:var(--white);margin-bottom:20px;letter-spacing:-0.01em}
.tf-row{display:flex;justify-content:space-between;align-items:baseline;padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.06)}
.tf-row:last-child{border-bottom:none;padding-bottom:0}
.tf-row-label{font-size:0.78rem;font-weight:400;color:rgba(253,250,246,0.38)}
.tf-row-val{font-size:0.82rem;font-weight:700;color:var(--ochre-lt)}
.tf-note{font-size:0.76rem;font-weight:400;color:rgba(253,250,246,0.22);line-height:1.5;margin-top:14px}

/* SHUTTLE */
.shuttle-section{padding:80px 0;background:var(--dust)}
.shuttle-inner{display:grid;grid-template-columns:1fr 1fr;gap:80px;align-items:start}
.shuttle-img{border-radius:10px;overflow:hidden}

/* PRINCIPAL NOTE */
.principal-note{background:var(--ochre-pale);border:1px solid rgba(196,135,58,0.25);border-radius:12px;padding:32px 36px;margin-top:32px}
.principal-note p{font-size:1.05rem;font-weight:500;color:var(--charcoal);line-height:1.75;font-style:normal}
.principal-note p strong{font-weight:700}

@media(max-width:960px){
  .hiw-fold-grid{grid-template-columns:1fr;gap:0}
  .hiw-fold-image-panel{position:static;align-self:auto;aspect-ratio:3/2;margin-top:32px;border-radius:8px;overflow:hidden}
  .hiw-fold-image-panel > .hiw-fold-img-real{position:static;width:100%;height:100%}
  .hiw-fold-image-panel img{width:100%;height:100%;object-fit:cover;border-radius:8px}
  .expect-grid,.timeframes-grid,.shuttle-inner{grid-template-columns:1fr}
  .timeline::before{left:20px}
  .tl-item{grid-template-columns:40px 1fr;gap:24px}
}
"""

HIW_HTML = """
  <header class="hiw-header page-fold" aria-labelledby="hiw-heading">
    <div class="wrap">
      <div class="hiw-fold-grid">
        <div class="hiw-header-inner">
          <span class="page-label" style="color:var(--ochre-lt)">The process</span>
          <h1 id="hiw-heading">How online FDR <span class="accent">actually works.</span></h1>
          <p class="hiw-header-sub">From first call to a signed agreement. A plain-language walkthrough of every step, how long each takes, and what to expect from a practitioner who stays in the room until the job is done.</p>
        </div>
        <div class="hiw-fold-image-panel" aria-hidden="true">
          <div class="hiw-fold-img-real"><img src="/images/how-it-works-fold.jpg" alt="A practitioner's view over their shoulder of a laptop on a home-office desk, with both parties visible side by side on a video call, each wearing noise-cancelling headphones." fetchpriority="high"></div>
        </div>
      </div>
    </div>
  </header>

  <!-- ABOVE-FOLD MARQUEE -->
  <div class="marquee-bar" aria-label="Accreditation and credentials" role="marquee">
    <div class="marquee-track" aria-hidden="true">
      <span class="marquee-item">AGD-Accredited FDRP <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Australian Mediation Association Member <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Section 60I Certificates (s 66H in WA) <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Conducted Securely Online <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Available Anywhere in Australia <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Free Discovery Call <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">No Obligation <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Confidential under the Family Law Act <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Both Parenting and Financial Matters <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">AGD-Accredited FDRP <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Australian Mediation Association Member <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Section 60I Certificates (s 66H in WA) <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Conducted Securely Online <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Available Anywhere in Australia <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Free Discovery Call <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">No Obligation <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Confidential under the Family Law Act <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Both Parenting and Financial Matters <span class="marquee-sep">&bull;</span></span>
    </div>
  </div>


  <!-- PROCESS TIMELINE -->
  <section class="process-section" aria-labelledby="process-heading">
    <div class="wrap">
      <div class="process-intro reveal">
        <span class="section-label">Step by step</span>
        <h2 id="process-heading">The FDR process, from start to finish</h2>
        <p>Every matter moves through the same sequence of steps. The number of sessions varies depending on complexity and how far apart the parties begin. What does not vary is the commitment to getting there.</p>
      </div>

      <div class="timeline">

        <div class="tl-item reveal">
          <div class="tl-dot-wrap"><div class="tl-dot"></div></div>
          <div class="tl-content">
            <span class="tl-step-num">Step 01</span>
            <h3 id="step-discovery">Free discovery call</h3>
            <p>A discovery call with your mediator to talk through your situation and confirm that FDR is appropriate for your circumstances. This is not a sales call. If FDR is not right for you, we will say so and point you in the right direction.</p>
            <p>If you decide to proceed, you will each receive a booking link for your individual intake session.</p>
            <div class="tl-meta">
              <span class="tl-tag tl-tag-note">Free, no obligation</span>
            </div>
          </div>
        </div>

        <div class="tl-item reveal">
          <div class="tl-dot-wrap"><div class="tl-dot"></div></div>
          <div class="tl-content">
            <span class="tl-step-num">Step 02</span>
            <h3 id="step-intake">Individual intake sessions</h3>
            <p>Each party meets separately with the mediator for a one-hour session. This is your opportunity to speak candidly about your situation, your concerns, and what matters most to you, without the other party present.</p>
            <p>The intake session also allows the mediator to assess whether the matter is suitable for joint FDR, and to identify any issues that may need to be managed in the joint process. For financial matters, the mediator will walk through the duty of full and frank disclosure with you, in line with the statutory obligation under sections 71B, 90RI, and 90YJA of the Family Law Act.</p>
            <p>If financial matters are in scope, you will be given the <a href="/downloads/onlinefdr-disclosure-worksheet.pdf">Full and Frank Disclosure worksheet</a> to complete before the first joint financial session.</p>
            <div class="tl-meta">
              <span class="tl-tag tl-tag-time">1 hour each party</span>
              <span class="tl-tag tl-tag-note">Held separately</span>
              <span class="tl-tag tl-tag-note">Conducted online</span>
            </div>
          </div>
        </div>

        <div class="tl-item reveal">
          <div class="tl-dot-wrap"><div class="tl-dot"></div></div>
          <div class="tl-content">
            <span class="tl-step-num">Step 03</span>
            <h3 id="step-joint">Joint mediation session</h3>
            <p>Both parties join the same video call with the mediator. Session length depends on the matter type. Parenting matters and financial settlement are addressed in their own sessions.</p>
            <p><strong>Parenting matters:</strong> Joint sessions for parenting matters run for four hours. This length allows the discussion to move properly through the framework of issues that parenting arrangements need to cover, without artificial time pressure forcing premature compromise.</p>
            <p><strong>Financial settlement:</strong> Joint sessions for financial matters run for three hours. Couples without children can often reach agreement in a single session, provided both parties arrive with the Full and Frank Disclosure worksheet completed. Matters involving property, superannuation, and business interests typically need more time.</p>
            <div class="tl-meta">
              <span class="tl-tag tl-tag-time">4hrs parenting / 3hrs financial</span>
              <span class="tl-tag tl-tag-note">Both parties together</span>
            </div>
          </div>
        </div>

        <div class="tl-item reveal">
          <div class="tl-dot-wrap"><div class="tl-dot"></div></div>
          <div class="tl-content">
            <span class="tl-step-num">Step 04</span>
            <h3 id="step-between">Between sessions, if needed</h3>
            <p>Most matters that need more than one session resolve in two to three joint sessions in total. Higher-conflict matters can take more. Where the first session does not reach full agreement, subsequent sessions are booked and parties are often given specific tasks to complete in between, so each session moves forward rather than retreading what has already been covered.</p>
            <p>Multi-session matters are still significantly less expensive and less drawn out than litigation. The commitment is to keep working.</p>

            <div class="tl-meta" style="margin-top:20px">
              <span class="tl-tag tl-tag-note">Most matters: 2 to 3 joint sessions</span>
              <span class="tl-tag tl-tag-terra">Higher conflict: more, still less than court</span>
            </div>
          </div>
        </div>

        <div class="tl-item reveal">
          <div class="tl-dot-wrap"><div class="tl-dot"></div></div>
          <div class="tl-content">
            <span class="tl-step-num">Step 05</span>
            <h3 id="step-outcome">Agreement or certificate</h3>
            <p>When agreement is reached, the mediator documents the agreed terms. For parenting matters, this is typically a Parenting Plan or the basis for Consent Orders. For financial matters, it is typically a heads of agreement that lawyers can convert into Consent Orders, or the basis for a Binding Financial Agreement where that is the more appropriate path.</p>
            <p>If agreement is not reached, the practitioner documents what occurred. For parenting matters, this takes the form of a <a href="/section-60i/">Section 60I certificate</a>, issued by the practitioner in accordance with section 60I(8) of the Family Law Act 1975. For financial matters, the practitioner provides a Letter of Attendance and Genuine Effort, which the party can use to support their own Genuine Steps Certificate. Both documents reflect the practitioner's professional assessment of attendance and genuine effort. A certificate or letter is the outcome of last resort, not the goal of the process.</p>
            <div class="tl-meta">
              <span class="tl-tag tl-tag-terra">Goal: agreement</span>
              <span class="tl-tag tl-tag-note">Certificate or letter if needed</span>
            </div>
          </div>
        </div>

      </div>
    </div>
  </section>

  <!-- IMAGE BREAK -->
  <section style="background:var(--dust);padding:0 0 80px">
    <div class="wrap">
      <div class="img-real" style="aspect-ratio:21/9"><img src="/images/how-it-works-hero.jpg" alt="A practitioner's view over their shoulder of a laptop on a home-office desk, with both parties visible side by side on a video call, each wearing noise-cancelling headphones." loading="lazy" decoding="async"></div>
    </div>
  </section>

  <!-- WHAT TO EXPECT -->
  <section class="expect-section" aria-labelledby="expect-heading">
    <div class="wrap">
      <div class="reveal">
        <span class="section-label">What to expect</span>
        <h2 class="section-h2" id="expect-heading">What the process feels like</h2>
        <p class="body-text" style="max-width:600px">FDR is structured, but it is not a formal proceeding. Most people are surprised by how different it is from what they expected.</p>
      </div>
      <div class="expect-grid">
        <div class="expect-card reveal">
          <div class="expect-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg></div>
          <h3>You will be heard</h3>
          <p>The intake session exists specifically so you can speak without the other party present. Your perspective, concerns, and priorities are understood before the joint process begins.</p>
        </div>
        <div class="expect-card reveal reveal-d1">
          <div class="expect-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg></div>
          <h3>Confidential and inadmissible</h3>
          <p>FDR is protected by two distinct provisions of the Family Law Act. Confidentiality (section 10H) prevents disclosure of what was said. Inadmissibility (section 10J) means that even if disclosed, it cannot be admitted as evidence in court. Both protections apply.</p>
        </div>
        <div class="expect-card reveal">
          <div class="expect-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg></div>
          <h3>Sessions have structure</h3>
          <p>Your mediator sets the agenda and manages the process. Sessions do not become a forum for relitigating the relationship. The focus stays on what needs to be resolved.</p>
        </div>
        <div class="expect-card reveal reveal-d1">
          <div class="expect-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg></div>
          <h3>Progress is real</h3>
          <p>Sessions are designed to move. If something cannot be resolved, it is set aside and returned to. Between sessions, both parties may be given tasks to complete so the next session can cover new ground.</p>
        </div>
        <div class="expect-card reveal">
          <div class="expect-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg></div>
          <h3>You do not need to be in the same location</h3>
          <p>Both parties join via Google Meet from wherever they are. Different cities, different states. The only requirement is a private, quiet space and a reliable internet connection.</p>
        </div>
        <div class="expect-card reveal reveal-d1">
          <div class="expect-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg></div>
          <h3>Significantly less costly than litigation</h3>
          <p>Even matters that need multiple sessions across both parenting and financial issues come in well below the cost of contested family law proceedings, which can typically run to tens of thousands of dollars per party.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- IMAGE BREAK -->
  <section style="background:var(--white);padding:0 0 40px">
    <div class="wrap">
      <div class="img-real" style="aspect-ratio:21/9"><img src="/images/how-it-works-supporting-1.jpg" alt="A woman in her mid-30s sitting on the sofa late in the evening, working through a spread of financial paperwork laid across the coffee table in front of her, her laptop open beside the documents. A pile of children's books on the side table." loading="lazy" decoding="async"></div>
    </div>
  </section>

  <!-- TIMEFRAMES -->
  <section class="timeframes-section" aria-labelledby="timeframes-heading">
    <div class="wrap">
      <div class="timeframes-header reveal">
        <span class="section-label section-label-light">Typical timeframes</span>
        <h2 id="timeframes-heading">How long does it take?</h2>
        <p>Every matter is different. These are realistic ranges based on typical cases. Higher conflict, greater financial complexity, and the number of issues in dispute all affect how many sessions are needed.</p>
      </div>
      <div class="timeframes-grid reveal">
        <div class="tf-card">
          <span class="tf-label">Scenario</span>
          <div class="tf-type">Financial only, no children</div>
          <div class="tf-row"><span class="tf-row-label">Intake sessions</span><span class="tf-row-val">1hr each party</span></div>
          <div class="tf-row"><span class="tf-row-label">Joint sessions</span><span class="tf-row-val">1 to 2 x 3hrs</span></div>
          <div class="tf-row"><span class="tf-row-label">Total time (per person)</span><span class="tf-row-val">~4 to 7hrs</span></div>
          <p class="tf-note">Requires both parties to arrive with the Full and Frank Disclosure worksheet completed and supporting documents gathered.</p>
        </div>
        <div class="tf-card">
          <span class="tf-label">Scenario</span>
          <div class="tf-type">Parenting and financial</div>
          <div class="tf-row"><span class="tf-row-label">Intake sessions</span><span class="tf-row-val">1hr each party</span></div>
          <div class="tf-row"><span class="tf-row-label">Joint sessions</span><span class="tf-row-val">1 x 4hrs + 1 x 3hrs</span></div>
          <div class="tf-row"><span class="tf-row-label">Total time (per person)</span><span class="tf-row-val">~8hrs</span></div>
          <p class="tf-note">One four-hour session for parenting, one three-hour session for financial. Low to moderate conflict.</p>
        </div>
        <div class="tf-card">
          <span class="tf-label">Scenario</span>
          <div class="tf-type">Complex or high conflict</div>
          <div class="tf-row"><span class="tf-row-label">Intake sessions</span><span class="tf-row-val">1hr each party</span></div>
          <div class="tf-row"><span class="tf-row-label">Joint sessions</span><span class="tf-row-val">2 to 3 sessions per area</span></div>
          <div class="tf-row"><span class="tf-row-label">Total time (per person)</span><span class="tf-row-val">13hrs+</span></div>
          <p class="tf-note">Still significantly less than the time and cost of contested proceedings.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- SHUTTLE -->
  <section class="shuttle-section" aria-labelledby="shuttle-heading">
    <div class="wrap">
      <div class="shuttle-inner">
        <div class="reveal">
          <span class="section-label">Shuttle mediation</span>
          <h2 class="section-h2" id="shuttle-heading">When parties need to be <span class="accent">kept separate.</span></h2>
          <p class="body-text">Shuttle mediation means the mediator moves between parties separately rather than having them in the same virtual room. It is available when a significant power imbalance, safety concern, or level of conflict makes joint sessions unproductive or inappropriate.</p>
          <p class="body-text">Shuttle is not the default. Joint sessions allow parties to hear each other directly, which often unlocks movement that shuttle cannot. Shuttle also significantly increases the time required, and with it the cost. Your mediator will advise if and when shuttle is the better approach for your situation.</p>
          <p class="body-text">In an online environment, shuttle is conducted using breakout rooms inside a single Google Meet session. The mediator moves between rooms; parties remain in their own room and cannot see or hear each other. This is more practical online than in person, where shuttle requires the mediator to physically move between separate rooms while the parties remain in the same building.</p>
          <div class="notice notice-amber" style="margin-top:28px">
            <p class="notice-label">A note on safety</p>
            <p>If there are family violence concerns, please raise these during the discovery call or your intake session. The Family Law Amendment Act 2024, in force from 10 June 2025, expanded the definition of family violence in section 4AB to expressly include economic and financial abuse. Your safety is assessed as part of the intake process, and shuttle or other arrangements can be put in place before the joint process begins.</p>
          </div>
        </div>
        <div class="reveal reveal-d1">
          <div class="img-real" style="aspect-ratio:4/3;margin-bottom:24px"><img src="/images/how-it-works-supporting-2.jpg" alt="A practitioner at his home-office desk wearing noise-cancelling headphones, mid-conversation with one party visible on the laptop screen. A clipboard with handwritten notes and a warm desk lamp sit on the desk beside the laptop." loading="lazy" decoding="async"></div>
          <div class="info-box" style="margin:0">
            <h3>What you will need for online sessions</h3>
            <div class="info-items">
              <div class="info-item"><div class="info-icon"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg></div><div><h4>A device with camera and microphone</h4><p>Laptop, desktop, or tablet. Phone is not recommended for sessions of this length.</p></div></div>
              <div class="info-item"><div class="info-icon"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.55a11 11 0 0 1 14.08 0"/><path d="M1.42 9a16 16 0 0 1 21.16 0"/><path d="M8.53 16.11a6 6 0 0 1 6.95 0"/><line x1="12" y1="20" x2="12.01" y2="20"/></svg></div><div><h4>Reliable internet connection</h4><p>A stable connection throughout. A wired connection is more reliable than Wi-Fi for long sessions.</p></div></div>
              <div class="info-item"><div class="info-icon"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg></div><div><h4>A private, quiet space</h4><p>Somewhere you will not be interrupted for the duration of the session. Sessions are confidential.</p></div></div>
              <div class="info-item"><div class="info-icon"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg></div><div><h4>For financial matters: the Full and Frank Disclosure worksheet</h4><p>Completed and supporting documents gathered before the first joint financial session. Provided to you at intake.</p></div></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- FAQ -->
  <section class="page-faq" aria-labelledby="hiw-faq-heading">
    <div class="wrap">
      <div class="page-faq-header reveal">
        <span class="section-label">Common questions</span>
        <h2 id="hiw-faq-heading">Questions about the process</h2>
        <p>The questions we hear most often before people book their discovery call.</p>
      </div>
      <div class="faq-list reveal" style="max-width:760px">
        <div class="faq-item"><button class="faq-q" aria-expanded="false">Do both parties have to agree to participate?<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></button><div class="faq-a"><p>Yes. FDR requires the genuine participation of both parties. We cannot compel participation. If the other party declines to attend, a Section 60I certificate under paragraph 60I(8)(a) can be issued reflecting their non-attendance, which allows the matter to proceed to court for parenting orders. If only one party contacts us, we will explain the process and suggest ways to approach the other party about participating.</p></div></div>
        <div class="faq-item"><button class="faq-q" aria-expanded="false">Can I have a lawyer present during sessions?<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></button><div class="faq-a"><p>Generally, lawyers do not attend FDR sessions. You are encouraged to seek legal advice before and after sessions, and to consult a lawyer before signing any agreement. Having lawyers present in sessions tends to change the dynamic in ways that can make agreement harder to reach, not easier. If you have specific concerns about this, raise them in the discovery call.</p></div></div>
        <div class="faq-item"><button class="faq-q" aria-expanded="false">What if we cannot agree on everything?<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></button><div class="faq-a"><p>Partial agreement is a real and useful outcome. Any agreements reached during the process can be recorded in a Parenting Plan or heads of agreement. For matters that need to proceed to court on the remaining issues, parties can request a Section 60I certificate that allows the parenting matter to be filed. Court then deals only with what remains in dispute, not with the matters already settled in FDR.</p></div></div>
        <div class="faq-item"><button class="faq-q" aria-expanded="false">What financial documents do I need to prepare?<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></button><div class="faq-a"><p>For financial settlement, both parties complete the <a href="/downloads/onlinefdr-disclosure-worksheet.pdf">Full and Frank Disclosure worksheet</a> ahead of the first joint financial session. The worksheet covers income, assets, liabilities, superannuation, financial resources, and any property disposals since separation. Supporting documents include three years of tax returns, twelve months of bank and credit card statements, recent superannuation statements, and statements for any loans or mortgages. The duty of full and frank disclosure is now a statutory obligation under sections 71B and 90RI of the Family Law Act. The worksheet is provided to you at the intake session.</p></div></div>
        <div class="faq-item"><button class="faq-q" aria-expanded="false">How quickly can we start?<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></button><div class="faq-a"><p>Discovery calls are typically available within a few days of enquiry. Intake sessions follow shortly after. For most matters, the first joint session can be scheduled within two weeks of initial contact. This is significantly faster than government FDR services in most areas, where waiting times can run to several months.</p></div></div>
        <div class="faq-item"><button class="faq-q" aria-expanded="false">How long does a typical matter take from start to finish?<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></button><div class="faq-a"><p>For most matters, the full process runs from first contact to final agreement in a matter of weeks rather than months. Discovery call within a few days, intake sessions within a week or two, joint sessions in the weeks following. Most matters that need more than one joint session resolve in two to three joint sessions in total. Higher-conflict matters can take longer but still run significantly faster than the 18 to 36 month timeline for contested family law proceedings.</p></div></div>
      </div>
    </div>
  </section>

  <section class="page-cta" id="discovery" aria-labelledby="hiw-cta-heading">
    <div class="wrap">
      <div class="page-cta-inner">
        <span class="page-cta-eyebrow">Ready to start?</span>
        <h2 id="hiw-cta-heading">The call you make before you call a lawyer.</h2>
        <p>A free discovery call. Find out whether FDR is right for your situation, what the process looks like for your circumstances, and how quickly you can start.</p>
        <div class="page-cta-actions">
          <a href="https://calendar.app.google/zwNm4dzYnwAwhwxY8" class="btn-light">Book your free discovery call</a>
          <a href="tel:0399617544" class="btn-outline-light">Call (03) 9961 7544</a>
        </div>
        <span class="page-cta-note">Free &bull; Confidential &bull; No obligation &bull; Available nationally</span>
      </div>
    </div>
  </section>
"""

build_page(
    filename="how-it-works-v2.html",
    title="How Online FDR Works | onlinefdr.com.au",
    meta_desc="A plain-language walkthrough of the online FDR process. Discovery call, intake sessions, joint mediation, typical timeframes, and what to expect from start to finish.",
    canonical="/how-it-works/",
    current_page="/how-it-works/",
    schema_json='{"@context":"https://schema.org","@graph":[{"@type":"WebPage","@id":"https://onlinefdr.com.au/how-it-works/#webpage","url":"https://onlinefdr.com.au/how-it-works/","name":"How Online FDR Works","description":"Step-by-step walkthrough of the online Family Dispute Resolution process: discovery call, individual intake, joint sessions for parenting (four hours) and financial matters (three hours), typical timeframes, shuttle mediation, and what to expect from start to finish.","about":{"@id":"https://onlinefdr.com.au/#organization"},"mainEntity":{"@id":"https://onlinefdr.com.au/how-it-works/#faq"}},{"@type":"FAQPage","@id":"https://onlinefdr.com.au/how-it-works/#faq","mainEntity":[{"@type":"Question","name":"Do both parties have to agree to participate?","acceptedAnswer":{"@type":"Answer","text":"Yes. FDR requires the genuine participation of both parties. We cannot compel participation. If the other party declines to attend, a Section 60I certificate under paragraph 60I(8)(a) can be issued reflecting their non-attendance, which allows the matter to proceed to court for parenting orders. If only one party contacts us, we will explain the process and suggest ways to approach the other party about participating."}},{"@type":"Question","name":"Can I have a lawyer present during sessions?","acceptedAnswer":{"@type":"Answer","text":"Generally, lawyers do not attend FDR sessions. You are encouraged to seek legal advice before and after sessions, and to consult a lawyer before signing any agreement. Having lawyers present in sessions tends to change the dynamic in ways that can make agreement harder to reach, not easier. If you have specific concerns about this, raise them in the discovery call."}},{"@type":"Question","name":"What if we cannot agree on everything?","acceptedAnswer":{"@type":"Answer","text":"Partial agreement is a real and useful outcome. Any agreements reached during the process can be recorded in a Parenting Plan or heads of agreement. For matters that need to proceed to court on the remaining issues, parties can request a Section 60I certificate that allows the parenting matter to be filed. Court then deals only with what remains in dispute, not with the matters already settled in FDR."}},{"@type":"Question","name":"What financial documents do I need to prepare?","acceptedAnswer":{"@type":"Answer","text":"For financial settlement, both parties complete the Full and Frank Disclosure worksheet ahead of the first joint financial session. The worksheet covers income, assets, liabilities, superannuation, financial resources, and any property disposals since separation. Supporting documents include three years of tax returns, twelve months of bank and credit card statements, recent superannuation statements, and statements for any loans or mortgages. The duty of full and frank disclosure is now a statutory obligation under sections 71B and 90RI of the Family Law Act. The worksheet is provided to you at the intake session."}},{"@type":"Question","name":"How quickly can we start?","acceptedAnswer":{"@type":"Answer","text":"Discovery calls are typically available within a few days of enquiry. Intake sessions follow shortly after. For most matters, the first joint session can be scheduled within two weeks of initial contact. This is significantly faster than government FDR services in most areas, where waiting times can run to several months."}},{"@type":"Question","name":"How long does a typical matter take from start to finish?","acceptedAnswer":{"@type":"Answer","text":"For most matters, the full process runs from first contact to final agreement in a matter of weeks rather than months. Discovery call within a few days, intake sessions within a week or two, joint sessions in the weeks following. Most matters that need more than one joint session resolve in two to three joint sessions in total. Higher-conflict matters can take longer but still run significantly faster than the 18 to 36 month timeline for contested family law proceedings."}}]}]}',
    extra_css=HIW_CSS,
    breadcrumbs=[("Home", "/"), ("How It Works", "/how-it-works/")],
    page_html=HIW_HTML,
    show_marquee=False,
)
print("How It Works done.")

# ─────────────────────────────────────────────
# WHAT IS FDR
# ─────────────────────────────────────────────
WIFDR_CSS = """
.wifdr-hero{background:var(--charcoal);padding:120px 0 80px;position:relative;overflow:hidden}
.wifdr-hero::before{content:'';position:absolute;inset:0;background:radial-gradient(ellipse 65% 60% at 75% 35%,rgba(196,135,58,0.1) 0%,transparent 60%);pointer-events:none}
.wifdr-hero-grid{display:grid;grid-template-columns:1.1fr 0.9fr;gap:72px;align-items:center;position:relative;z-index:1}
.wifdr-hero h1{font-size:clamp(2.8rem,6vw,5.2rem);font-weight:800;line-height:1.0;letter-spacing:-0.03em;color:var(--white);margin-bottom:24px}
.wifdr-hero h1 .accent{color:var(--ochre)}
.wifdr-hero-sub{font-size:1.1rem;font-weight:400;color:rgba(253,250,246,0.6);line-height:1.8;margin-bottom:32px}
.wifdr-hero-stats{display:grid;grid-template-columns:1fr 1fr;gap:2px;border-radius:10px;overflow:hidden}
.hero-stat{background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.08);padding:22px 20px}
.hero-stat-val{font-size:clamp(1.9rem,3vw,2.4rem);font-weight:800;color:var(--white);line-height:1;margin-bottom:6px;letter-spacing:-0.03em}
.hero-stat-val .unit{color:var(--ochre);font-weight:800;margin-left:4px}
.hero-stat-val.text{font-size:clamp(1.6rem,2.6vw,2.1rem)}
.hero-stat-label{font-size:0.74rem;font-weight:500;color:rgba(253,250,246,0.4);line-height:1.4}

/* DEFINITION */
.definition-section{padding:80px 0;background:var(--white)}
.definition-grid{display:grid;grid-template-columns:1fr 1fr;gap:80px;align-items:start}
.definition-text h2{font-size:clamp(1.8rem,3vw,2.6rem);font-weight:800;line-height:1.1;letter-spacing:-0.03em;color:var(--charcoal);margin-bottom:20px}
.definition-text h2 .accent{color:var(--terra)}

/* HOW IT WORKS SUMMARY */
.how-summary-section{padding:80px 0;background:var(--dust)}
.how-summary-steps{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:44px}
.how-summary-step{background:var(--white);border:1px solid var(--dust-3);border-radius:10px;padding:24px 22px;transition:border-color 0.25s}
.how-summary-step:hover{border-color:var(--ochre)}
.how-summary-num{width:32px;height:32px;border-radius:8px;background:var(--ochre-pale);color:var(--terra);display:flex;align-items:center;justify-content:center;font-size:0.95rem;font-weight:800;margin-bottom:14px}
.how-summary-step h3{font-size:0.92rem;font-weight:800;color:var(--charcoal);margin-bottom:8px;letter-spacing:-0.01em}
.how-summary-step p{font-size:0.84rem;font-weight:400;color:var(--mid);line-height:1.65;margin-bottom:0}

/* CONFIDENTIALITY */
.confidentiality-section{padding:80px 0;background:var(--white)}

/* VS SECTION */
.vs-section{padding:80px 0;background:var(--dust)}
.vs-header{max-width:600px;margin-bottom:52px}
.vs-grid{display:grid;grid-template-columns:1fr 80px 1fr;gap:0;align-items:start}
.vs-col{background:var(--white);border:1px solid var(--dust-3);border-radius:10px;padding:32px 28px}
.vs-col.fdr{border-color:var(--ochre);border-width:2px}
.vs-col-label{font-size:0.62rem;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;margin-bottom:8px;display:block}
.vs-col.fdr .vs-col-label{color:var(--terra)}
.vs-col.court .vs-col-label{color:var(--light-mid)}
.vs-col h3{font-size:1.1rem;font-weight:800;color:var(--charcoal);margin-bottom:24px;letter-spacing:-0.02em}
.vs-rows{display:flex;flex-direction:column;gap:0;border-top:1px solid var(--dust-3)}
.vs-row{display:flex;align-items:flex-start;gap:12px;padding:14px 0;border-bottom:1px solid var(--dust-3)}
.vs-row:last-child{border-bottom:none}
.vs-icon{width:22px;height:22px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:1px}
.vs-icon.yes{background:var(--ochre-pale);color:var(--terra)}
.vs-icon.no{background:#FEF2F2;color:#DC2626}
.vs-row-text{font-size:0.88rem;font-weight:400;color:var(--mid);line-height:1.55}
.vs-row-text strong{font-weight:700;color:var(--charcoal)}
.vs-mid{display:flex;align-items:center;justify-content:center;padding-top:72px}
.vs-badge{width:60px;height:60px;border-radius:50%;background:var(--charcoal);color:var(--white);display:flex;align-items:center;justify-content:center;font-size:0.8rem;font-weight:800;letter-spacing:0.04em}

/* WHO IS IT FOR */
.who-section{padding:80px 0;background:var(--white)}
.who-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;margin-top:44px}
.who-card{border:1px solid var(--dust-3);border-radius:10px;padding:28px 24px;background:var(--dust);transition:border-color 0.25s,transform 0.25s}
.who-card:hover{border-color:var(--ochre);transform:translateY(-2px)}
.who-card-icon{width:40px;height:40px;border-radius:10px;background:var(--ochre-pale);color:var(--terra);display:flex;align-items:center;justify-content:center;margin-bottom:16px}
.who-card h3{font-size:0.95rem;font-weight:800;color:var(--charcoal);margin-bottom:8px;letter-spacing:-0.01em}
.who-card p{font-size:0.86rem;font-weight:400;color:var(--mid);line-height:1.7;margin-bottom:0}

/* NOT FOR */
.notfor-section{padding:72px 0;background:var(--charcoal)}
.notfor-inner{display:grid;grid-template-columns:1fr 1fr;gap:64px;align-items:start}
.notfor-list{display:flex;flex-direction:column;gap:2px;margin-top:24px;border-radius:10px;overflow:hidden}
.notfor-item{display:flex;align-items:flex-start;gap:14px;padding:18px 20px;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.08)}
.notfor-icon{width:28px;height:28px;border-radius:7px;background:rgba(220,38,38,0.15);color:#F87171;display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:1px}
.notfor-item h4{font-size:0.88rem;font-weight:700;color:var(--white);margin-bottom:3px}
.notfor-item p{font-size:0.82rem;font-weight:400;color:rgba(253,250,246,0.45);line-height:1.55;margin-bottom:0}
.notfor-note{margin-top:20px;padding:20px 22px;background:rgba(196,135,58,0.1);border:1px solid rgba(196,135,58,0.2);border-radius:8px}
.notfor-note p{font-size:0.88rem;font-weight:400;color:rgba(253,250,246,0.6);line-height:1.7;margin-bottom:0}
.notfor-note strong{color:var(--ochre-lt)}

/* LEGAL BASIS */
.legal-section{padding:80px 0;background:var(--dust)}

@media(max-width:960px){
  .wifdr-hero-grid,.definition-grid,.vs-grid,.notfor-inner{grid-template-columns:1fr;gap:48px}
  .vs-mid{padding:16px 0}
  .who-grid{grid-template-columns:1fr 1fr}
  .how-summary-steps{grid-template-columns:1fr 1fr}
}
@media(max-width:640px){
  .who-grid{grid-template-columns:1fr}
  .wifdr-hero-stats{grid-template-columns:1fr 1fr}
  .how-summary-steps{grid-template-columns:1fr}
}
"""

WIFDR_HTML = """
  <header class="wifdr-hero page-fold" aria-labelledby="wifdr-heading">
    <div class="wrap">
      <div class="wifdr-hero-grid">
        <div>
          <span class="page-label" style="color:var(--ochre-lt)">The basics</span>
          <h1 id="wifdr-heading">What is <span class="accent">Family</span> <span class="accent">Dispute</span> <span class="accent">Resolution?</span></h1>
          <p class="wifdr-hero-sub">Family Dispute Resolution is a structured, professionally facilitated process that helps separating couples reach their own agreements on parenting and financial matters. It is conducted by an accredited practitioner under the Family Law Act 1975 and is confidential and inadmissible by statute. This page explains what FDR is, how it works in practice, and where it fits in the Australian family law system.</p>
          <div style="display:flex;gap:12px;flex-wrap:wrap">
            <a href="https://calendar.app.google/zwNm4dzYnwAwhwxY8" class="btn-light">Book a free discovery call</a>
            <a href="/how-it-works/" class="btn-outline-light">How it works</a>
          </div>
        </div>
        <div class="why-comparator">
          <div class="why-comparator-header">
            <div></div>
            <div>Time</div>
            <div>Cost</div>
          </div>
          <div class="why-comparator-row">
            <div class="why-comparator-label">
              FDR
              <span class="qual">Online via this practice</span>
            </div>
            <div class="why-bar-cell">
              <div class="why-bar why-bar-fdr"></div>
              <div class="why-bar-text text-fdr">Weeks</div>
            </div>
            <div class="why-bar-cell">
              <div class="why-bar why-bar-fdr"></div>
              <div class="why-bar-text text-fdr">A fraction of litigation</div>
            </div>
          </div>
          <div class="why-comparator-row">
            <div class="why-comparator-label">
              Court
              <span class="qual">Contested proceedings</span>
            </div>
            <div class="why-bar-cell">
              <div class="why-bar why-bar-court"></div>
              <div class="why-bar-text">18 to 36 months</div>
            </div>
            <div class="why-bar-cell">
              <div class="why-bar why-bar-court"></div>
              <div class="why-bar-text">Often six figures per party</div>
            </div>
          </div>
          <div class="why-comparator-foot">
            Court figures reflect typical fully-litigated parenting or property matters from filing to final hearing. Costs vary with complexity.
          </div>
        </div>
      </div>
    </div>
  </header>

  <!-- ABOVE-FOLD MARQUEE -->
  <div class="marquee-bar" aria-label="Accreditation and credentials" role="marquee">
    <div class="marquee-track" aria-hidden="true">
      <span class="marquee-item">AGD-Accredited FDRP <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Australian Mediation Association Member <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Section 60I Certificates (s 66H in WA) <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Conducted Securely Online <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Available Anywhere in Australia <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Free Discovery Call <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">No Obligation <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Confidential under the Family Law Act <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Both Parenting and Financial Matters <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">AGD-Accredited FDRP <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Australian Mediation Association Member <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Section 60I Certificates (s 66H in WA) <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Conducted Securely Online <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Available Anywhere in Australia <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Free Discovery Call <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">No Obligation <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Confidential under the Family Law Act <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Both Parenting and Financial Matters <span class="marquee-sep">&bull;</span></span>
    </div>
  </div>


  <!-- DEFINITION -->
  <section class="definition-section" aria-labelledby="definition-heading">
    <div class="wrap">
      <div class="definition-grid">
        <div class="definition-text reveal">
          <span class="section-label">What it actually is</span>
          <h2 id="definition-heading">A structured conversation, with a <span class="accent">professional in the room.</span></h2>
          <p class="body-text">Family Dispute Resolution is a form of mediation, specifically designed for separating couples dealing with parenting and financial matters. A trained, accredited practitioner facilitates structured conversations between both parties, helping them work through their situation and reach agreements they have made themselves.</p>
          <p class="body-text">The practitioner does not make decisions. They are not a judge, and nothing decided in FDR is imposed on either party. Their role is to create a structured space where both people can hear each other, understand each other's position, and work toward outcomes that both can live with.</p>
          <p class="body-text">Because the agreements come from both parties rather than being imposed by a court, they are generally more workable, more durable, and far less damaging to the ongoing relationship between former partners and co-parents.</p>
        </div>
        <div class="reveal reveal-d1">
          <div class="pull" style="margin-top:0">
            <p>"The agreements that come out of FDR are the ones the parties built themselves. They tend to last."</p>
          </div>
          <div class="img-real" style="aspect-ratio:4/3;margin-top:24px"><img src="/images/what-is-fdr-hero.jpg" alt="Over-the-shoulder view from the practitioner's desk: a laptop screen showing the two parties joined to a video session from separate locations, both wearing headphones." loading="lazy" decoding="async"></div>
        </div>
      </div>
    </div>
  </section>

  <div class="divider" aria-hidden="true"></div>

  <!-- HOW A TYPICAL ENGAGEMENT WORKS -->
  <section class="how-summary-section" aria-labelledby="how-summary-heading">
    <div class="wrap">
      <div class="reveal" style="max-width:760px">
        <span class="section-label">How it works in practice</span>
        <h2 class="section-h2" id="how-summary-heading">From first call to <span class="accent">final agreement.</span></h2>
        <p class="body-text">A typical FDR engagement runs in four stages. Timing varies with matter complexity, but most matters move from first call to written agreement in a matter of weeks rather than months.</p>
      </div>
      <div class="how-summary-steps">
        <div class="how-summary-step reveal">
          <div class="how-summary-num">1</div>
          <h3>Free discovery call</h3>
          <p>A discovery call with the practitioner to understand the matter, check whether FDR is appropriate, and answer your questions about the process.</p>
        </div>
        <div class="how-summary-step reveal reveal-d1">
          <div class="how-summary-num">2</div>
          <h3>Individual intake sessions</h3>
          <p>The practitioner meets with each party separately. This is where screening for safety, suitability, and willingness occurs. The matter does not proceed to joint sessions if it is not appropriate.</p>
        </div>
        <div class="how-summary-step reveal reveal-d2">
          <div class="how-summary-num">3</div>
          <h3>Joint sessions</h3>
          <p>Both parties join via Google Meet, from wherever they are. Shuttle mediation (parties in separate sessions seeing only the practitioner) is available where it is the safer or more productive approach.</p>
        </div>
        <div class="how-summary-step reveal">
          <div class="how-summary-num">4</div>
          <h3>Agreement or certificate</h3>
          <p>Where agreement is reached, it is documented as a Parenting Plan, the basis for Consent Orders, or a heads of agreement for financial matters. Where it is not, a Section 60I certificate is issued.</p>
        </div>
      </div>
      <p class="body-text" style="margin-top:24px;text-align:center">For the full process detail, see the <a href="/how-it-works/">How it works</a> page.</p>
    </div>
  </section>

  <div class="divider" aria-hidden="true"></div>

  <!-- FDR VS COURT -->
  <section class="vs-section" aria-labelledby="vs-heading">
    <div class="wrap">
      <div class="vs-header reveal">
        <span class="section-label">FDR vs litigation</span>
        <h2 class="section-h2" id="vs-heading">Why most couples choose <span class="accent">FDR</span> <span class="accent">first.</span></h2>
        <p class="body-text" style="max-width:560px">Contested family law proceedings are slow, expensive, and adversarial by design. FDR is the opposite of all three. The comparison is not close.</p>
      </div>
      <div class="vs-grid reveal">
        <div class="vs-col fdr" role="region" aria-label="FDR comparison">
          <span class="vs-col-label">Family Dispute Resolution</span>
          <h3>online<span class="brand-fdr">fdr</span>.com.au</h3>
          <div class="vs-rows">
            <div class="vs-row"><div class="vs-icon yes"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg></div><div class="vs-row-text"><strong>Weeks, not years.</strong> Most matters are resolved in a matter of weeks from first contact.</div></div>
            <div class="vs-row"><div class="vs-icon yes"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg></div><div class="vs-row-text"><strong>You keep control.</strong> Both parties make the decisions. Nothing is imposed on you.</div></div>
            <div class="vs-row"><div class="vs-icon yes"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg></div><div class="vs-row-text"><strong>Confidential and inadmissible.</strong> What is said in FDR cannot be disclosed (s10H) and cannot be admitted as evidence in court (s10J), even if disclosed.</div></div>
            <div class="vs-row"><div class="vs-icon yes"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg></div><div class="vs-row-text"><strong>Significantly less costly.</strong> Costs a small share of what contested proceedings typically take from both parties.</div></div>
            <div class="vs-row"><div class="vs-icon yes"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg></div><div class="vs-row-text"><strong>Less damaging to ongoing relationships.</strong> Avoids the adversarial structure that often hardens positions and prolongs disputes.</div></div>
            <div class="vs-row"><div class="vs-icon yes"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg></div><div class="vs-row-text"><strong>Available nationally.</strong> Online, from wherever both parties are.</div></div>
          </div>
        </div>
        <div class="vs-mid" aria-hidden="true"><div class="vs-badge">VS</div></div>
        <div class="vs-col court" role="region" aria-label="Litigation comparison">
          <span class="vs-col-label">Contested court proceedings</span>
          <h3>Family Court litigation</h3>
          <div class="vs-rows">
            <div class="vs-row"><div class="vs-icon no"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg></div><div class="vs-row-text"><strong>18 to 36 months</strong> from filing to final hearing. Often longer for complex matters.</div></div>
            <div class="vs-row"><div class="vs-icon no"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg></div><div class="vs-row-text">A judge makes decisions about your children and finances. <strong>You have limited control.</strong></div></div>
            <div class="vs-row"><div class="vs-icon no"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg></div><div class="vs-row-text">Court proceedings are on the public record. <strong>Not confidential.</strong></div></div>
            <div class="vs-row"><div class="vs-icon no"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg></div><div class="vs-row-text">Legal costs can typically reach <strong>tens of thousands of dollars per party.</strong></div></div>
            <div class="vs-row"><div class="vs-icon no"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg></div><div class="vs-row-text">Adversarial proceedings often harden positions and prolong conflict. <strong>Ongoing relationships are damaged.</strong></div></div>
            <div class="vs-row"><div class="vs-icon no"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg></div><div class="vs-row-text">Requires FDR to be attempted first in most parenting matters. <strong>Court is the last step, not the first.</strong></div></div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <div class="divider" aria-hidden="true"></div>

  <!-- CONFIDENTIALITY AND INADMISSIBILITY -->
  <section class="confidentiality-section" aria-labelledby="confidentiality-heading">
    <div class="wrap">
      <div class="article-grid">
        <article class="article-body reveal">
          <h2 id="confidentiality-heading">Confidentiality and inadmissibility</h2>
          <p>FDR is protected by two distinct provisions of the Family Law Act. Together, they create a stronger protection for what is said in mediation than exists in almost any other formal process.</p>
          <p><strong>Confidentiality (section 10H)</strong> prevents the practitioner from disclosing what was said during FDR, with limited exceptions for child safety, threats to life, and similar matters. Parties agree contractually under our terms to maintain the same confidentiality. The practitioner cannot be compelled to give evidence about communications made in FDR.</p>
          <p><strong>Inadmissibility (section 10J)</strong> goes further. Even if confidentiality is breached and something is disclosed, that information cannot be admitted as evidence in court proceedings. This is unusual. Most professional confidentiality protects against disclosure but not against admissibility once disclosure occurs. FDR protects against both.</p>
          <p>This matters because it means parties can speak frankly in FDR without worrying that what they say will be used against them later. The protection applies whether or not agreement is reached, and whether or not the matter ends up in court.</p>
        </article>
        <aside class="sidebar">
          <div class="sidebar-card">
            <h4>The protection in one line</h4>
            <p>What is said in FDR stays out of court. That is the legal protection that lets the conversation happen at all.</p>
          </div>
        </aside>
      </div>
    </div>
  </section>

  <div class="divider" aria-hidden="true"></div>

  <!-- WHO IS IT FOR -->
  <section class="who-section" aria-labelledby="who-heading">
    <div class="wrap">
      <div class="reveal">
        <span class="section-label">Who it is for</span>
        <h2 class="section-h2" id="who-heading">FDR works for most <span class="accent">separating</span> <span class="accent">couples.</span></h2>
        <p class="body-text" style="max-width:600px">You do not need to be on good terms. You do not need to agree on everything before you start. You need to be willing to try.</p>
      </div>
      <div class="who-grid">
        <div class="who-card reveal">
          <div class="who-card-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/></svg></div>
          <h3>Parents separating</h3>
          <p>Couples with children who need to work out parenting arrangements, responsibilities, and financial settlement. FDR is the step the law expects to be taken before applying for parenting orders.</p>
        </div>
        <div class="who-card reveal reveal-d1">
          <div class="who-card-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg></div>
          <h3>Couples without children</h3>
          <p>Financial and property matters without parenting complexity. Often resolved efficiently when both parties arrive prepared and have completed pre-mediation disclosure.</p>
        </div>
        <div class="who-card reveal reveal-d2">
          <div class="who-card-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg></div>
          <h3>Couples in different locations</h3>
          <p>Different cities, different states. Online FDR removes geography as a barrier. Both parties join via Google Meet from wherever they are.</p>
        </div>
        <div class="who-card reveal">
          <div class="who-card-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg></div>
          <h3>High-conflict matters</h3>
          <p>FDR is not only for couples who get along. Shuttle mediation is available when parties need to remain separate. The process is designed to work even when direct communication has broken down.</p>
        </div>
        <div class="who-card reveal reveal-d1">
          <div class="who-card-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg></div>
          <h3>Post-order matters</h3>
          <p>Couples who already have parenting orders but want to revisit arrangements as circumstances change. Where both parties agree to vary, FDR is a sensible path to new agreements without returning to court. Where one party seeks to vary without the other's agreement, the threshold for the court is higher.</p>
        </div>
        <div class="who-card reveal reveal-d2">
          <div class="who-card-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="6"/><path d="M15.477 12.89L17 22l-5-3-5 3 1.523-9.11"/></svg></div>
          <h3>De facto couples</h3>
          <p>De facto couples have substantially the same property and parenting rights as married couples. FDR applies equally. The process and outcomes are the same.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- NOT APPROPRIATE -->
  <section class="notfor-section" aria-labelledby="notfor-heading">
    <div class="wrap">
      <div class="notfor-inner">
        <div class="reveal">
          <span class="section-label section-label-light">When FDR is not appropriate</span>
          <h2 class="section-h2 section-h2-light" id="notfor-heading">Some situations require a <span class="accent">different path.</span></h2>
          <p style="font-size:0.98rem;font-weight:400;color:rgba(253,250,246,0.55);line-height:1.8;margin-top:14px;max-width:440px">FDR is not suitable in all circumstances. The safety of both parties and any children involved is assessed as part of the intake process. Where FDR is not appropriate, we will say so directly and point you toward the right support.</p>
          <div class="notfor-note">
            <p><strong>If you are not sure whether FDR is right for your situation,</strong> the free discovery call is the right starting point. A practitioner will assess your circumstances and be direct about whether this process is suitable.</p>
          </div>
        </div>
        <div class="notfor-list reveal reveal-d1">
          <div class="notfor-item">
            <div class="notfor-icon"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg></div>
            <div><h4>Active family violence</h4><p>Where one party is at genuine risk of harm from the other. Safety is assessed at intake. The Family Law Amendment Act 2024, in force from 10 June 2025, expanded the definition of family violence in section 4AB to expressly include economic and financial abuse. Exemptions from the FDR requirement may apply.</p></div>
          </div>
          <div class="notfor-item">
            <div class="notfor-icon"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg></div>
            <div><h4>Child safety concerns</h4><p>Where a child is at immediate risk. Court intervention may be required urgently. Contact police or child protection services in the first instance.</p></div>
          </div>
          <div class="notfor-item">
            <div class="notfor-icon"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg></div>
            <div><h4>One party is unwilling to participate</h4><p>FDR requires genuine participation from both parties. If one party refuses to engage, a certificate under section 60I(8)(a) may be issued reflecting non-attendance.</p></div>
          </div>
          <div class="notfor-item">
            <div class="notfor-icon"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg></div>
            <div><h4>Urgent court matters</h4><p>Where an application for urgent orders is required, such as a recovery order for a child who has been wrongfully taken. FDR exemptions apply in urgent situations.</p></div>
          </div>
          <div class="notfor-item">
            <div class="notfor-icon"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg></div>
            <div><h4>A party lacks capacity to participate</h4><p>Where mental health, substance use, or another condition means a party cannot genuinely engage with the process.</p></div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- IMAGE BREAK -->
  <section style="background:var(--dust);padding:80px 0 0">
    <div class="wrap">
      <div class="img-real" style="aspect-ratio:21/9"><img src="/images/what-is-fdr-supporting-1.jpg" alt="A father at an AFL match at the MCG with his young son leaning into him, the boy looking up at his dad while the father gazes thoughtfully into the middle distance." loading="lazy" decoding="async"></div>
    </div>
  </section>

  <!-- LEGAL BASIS -->
  <section class="legal-section" aria-labelledby="legal-heading">
    <div class="wrap">
      <div class="article-grid">
        <article class="article-body reveal">
          <h2 id="legal-basis">The legal basis for FDR</h2>
          <p>Family Dispute Resolution is established in the Family Law Act 1975 (Cth). Accredited FDR Practitioners are registered with the Australian Government Attorney-General's Department under the Family Law (Family Dispute Resolution Practitioners) Regulations 2025, which commenced on 1 April 2025 and replaced the 2008 regulations.</p>
          <p>Family Dispute Resolution sits within a structured legal framework that includes the Section 60I certificate requirement for parenting matters, the confidentiality and inadmissibility protections under sections 10H and 10J, and the practitioner's statutory obligations on screening, disclosure, and certificate issuance.</p>

          <h2 id="parenting-and-60i">FDR and parenting matters</h2>
          <p>Before applying for parenting orders in the Federal Circuit and Family Court, a party must in most cases file a Section 60I certificate issued by an accredited FDR practitioner. This is a statutory requirement under section 60I of the Family Law Act. The certificate documents that a genuine attempt at FDR was made, or that there is a proper reason it could not be.</p>
          <p>The requirement exists because Parliament determined that most parenting disputes should be resolved without a judge making decisions about families. FDR is the mechanism for that. Exemptions apply in cases involving family violence, child abuse, urgency, and certain other circumstances.</p>

          <div class="img-real" style="aspect-ratio:16/9;margin:28px 0"><img src="/images/what-is-fdr-supporting-2.jpg" alt="A father at the front door of a suburban home, releasing his young son to the boy's mother who kneels in the doorway to welcome him in. The boy carries a football and a small backpack." loading="lazy" decoding="async"></div>

          <h2 id="financial-fdr">FDR and financial matters</h2>
          <p>The Section 60I requirement is specific to parenting matters. For financial and property settlement, the Section 60I certificate does not apply. However, every initiating application requires a Genuine Steps Certificate under Schedule 1 of the Federal Circuit and Family Court of Australia (Family Law) Rules 2021. The Genuine Steps Certificate is signed by the party themselves and confirms compliance with the pre-action procedures, including a genuine attempt at dispute resolution. Where financial FDR is attempted with this practice, the practitioner provides a Letter of Attendance and Genuine Effort confirming the dates of attendance, the assessment of each party's effort, and the outcome. The letter is supporting evidence the party can attach to or refer to in their own Genuine Steps Certificate.</p>
          <p>Financial FDR operates under the same statutory protections as parenting FDR. Confidentiality (section 10H) and inadmissibility (section 10J) both apply.</p>
          <p>The Family Law Amendment Act 2024, which commenced on 10 June 2025, codified the four-step framework for property settlement directly into the Family Law Act and elevated the duty of full and frank financial disclosure from the court rules into the Act itself. As part of those changes, FDR practitioners have a statutory obligation under sections 71B, 90RI, and 90YJA to inform parties about their duty of disclosure, explain when it applies, and encourage compliance. This is built into our intake process for financial matters.</p>

          <h2 id="who-can-conduct">Who can conduct FDR</h2>
          <p>Not all mediators are Family Dispute Resolution Practitioners. FDR in the legal sense requires an accredited practitioner registered with the AGD. Only an accredited FDRP can issue a Section 60I certificate, and the confidentiality and inadmissibility protections under sections 10H and 10J apply specifically to FDR conducted by an accredited practitioner. Mediators without this accreditation may offer useful services, but they cannot provide the legal outcomes that family law requires.</p>
          <p>For the named practitioner behind this practice, see the <a href="/about/">About page</a>.</p>
        </article>

        <aside class="sidebar">
          <div class="notice notice-amber" style="margin:0">
            <p class="notice-label">Who can issue a Section 60I certificate</p>
            <p>Only an accredited FDRP registered with the AGD can issue a Section 60I certificate. The certificate cannot be issued on request. It can only be issued after a proper FDR process has been conducted. See our <a href="/section-60i/">guide to Section 60I certificates</a> for a full explanation.</p>
          </div>
          <div class="sidebar-card">
            <h4>Ready to find out if FDR is right for you?</h4>
            <p>A free discovery call with an accredited practitioner. No pressure, no commitment.</p>
            <a href="https://calendar.app.google/zwNm4dzYnwAwhwxY8" class="btn-primary">Book a free discovery call</a>
          </div>
          <nav class="sidebar-card sidebar-nav">
            <h5>Related pages</h5>
            <ul>
              <li><a href="/how-it-works/"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>How it works</a></li>
              <li><a href="/parenting/"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>Parenting arrangements</a></li>
              <li><a href="/financial-settlement/"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>Financial settlements</a></li>
              <li><a href="/section-60i/"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>Section 60I certificates</a></li>
              <li><a href="/about/"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>About</a></li>
              <li><a href="/faq/"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>FAQ</a></li>
            </ul>
          </nav>
        </aside>
      </div>
    </div>
  </section>

  <section class="page-faq" aria-labelledby="wifdr-faq-heading">
    <div class="wrap">
      <div class="page-faq-header reveal">
        <span class="section-label">Common questions</span>
        <h2 id="wifdr-faq-heading">Questions about FDR</h2>
        <p>The questions people most commonly ask before their first call.</p>
      </div>
      <div class="faq-list reveal" style="max-width:760px">
        <div class="faq-item"><button class="faq-q" aria-expanded="false">Is FDR the same as mediation?<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></button><div class="faq-a"><p>FDR is a form of mediation, but not all mediation is FDR. Family Dispute Resolution is a specific legal term under the Family Law Act, conducted by an accredited practitioner registered with the AGD. Only an accredited FDRP can issue a Section 60I certificate, and the statutory confidentiality and inadmissibility protections under sections 10H and 10J apply specifically to FDR. A general mediator without this accreditation cannot provide the legal outcomes that family law requires.</p></div></div>
        <div class="faq-item"><button class="faq-q" aria-expanded="false">How is FDR different from family counselling?<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></button><div class="faq-a"><p>Family counselling focuses on relationship dynamics, communication, and emotional adjustment, with a therapeutic goal. FDR is a structured dispute resolution process aimed at reaching practical agreements on parenting or financial matters. The two can be complementary, but they are different professions with different goals. FDR practitioners are accredited under the Family Law Act; family counsellors are accredited separately.</p></div></div>
        <div class="faq-item"><button class="faq-q" aria-expanded="false">Can FDR be done online?<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></button><div class="faq-a"><p>Yes. Online FDR is a recognised mode of conducting Family Dispute Resolution under the Family Law Act. The statutory protections and the certificate-issuing process apply equally whether the practitioner meets parties in person or via video conference. Online FDR is particularly useful for parties in different locations, for matters involving safety concerns where physical separation is preferred, and for parties who would otherwise face significant travel or scheduling barriers.</p></div></div>
        <div class="faq-item"><button class="faq-q" aria-expanded="false">Do I need a lawyer before doing FDR?<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></button><div class="faq-a"><p>You do not need a lawyer to participate in FDR. Seeking legal advice before signing any agreement is sensible, so you understand what you are agreeing to. Lawyers do not typically attend FDR sessions. Their role is to advise, not to participate in the mediation itself.</p></div></div>
        <div class="faq-item"><button class="faq-q" aria-expanded="false">Who pays for FDR?<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></button><div class="faq-a"><p>Each party typically pays their own share of the FDR practitioner's fee. The precise arrangement is set out at intake. Government-funded FDR services are also available through Family Relationship Centres and not-for-profit providers; means-tested fees apply. The discovery call is the right place to discuss what makes sense for your circumstances.</p></div></div>
        <div class="faq-item"><button class="faq-q" aria-expanded="false">What's the difference between FDR and a Parenting Plan?<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></button><div class="faq-a"><p>They are different things. FDR is the process. A Parenting Plan is one of the documents that can come out of the process. A Parenting Plan is a written agreement between parents about parenting arrangements, signed and dated by both parents. It is not legally enforceable in the same way as a court order, but courts give it significant weight if a parenting matter later comes before them. The other typical FDR outputs are the basis for Consent Orders, a heads of agreement for financial matters, or a Section 60I certificate where no agreement was reached.</p></div></div>
        <div class="faq-item"><button class="faq-q" aria-expanded="false">What if there has been family violence?<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></button><div class="faq-a"><p>A history of family violence does not automatically make FDR inappropriate, but it does require careful assessment. The Family Law Amendment Act 2024, in force from 10 June 2025, expanded the definition of family violence in section 4AB to expressly include economic and financial abuse. Safety is evaluated as part of the intake process. Where genuine risk is identified, shuttle mediation or an exemption from the FDR requirement may apply. If you have concerns about your safety, raise them during the discovery call. Everything discussed is confidential.</p></div></div>
        <div class="faq-item"><button class="faq-q" aria-expanded="false">Can FDR cover both parenting and financial matters?<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></button><div class="faq-a"><p>Yes. Most couples with children need to resolve both parenting arrangements and financial settlement. These are typically addressed in separate sessions, since they involve different legal frameworks and different preparation requirements. Parenting is often addressed first, as the arrangements for children are usually the most pressing concern. Financial matters follow, or can run concurrently depending on the circumstances.</p></div></div>
        <div class="faq-item"><button class="faq-q" aria-expanded="false">What happens if FDR does not result in agreement?<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></button><div class="faq-a"><p>If agreement is not reached, parties can request a Section 60I certificate, which documents what occurred in the process. The certificate type reflects the practitioner's professional assessment of what happened, including whether each party attended and whether each made a genuine effort. The certificate allows the matter to proceed to court for parenting orders. Any agreements reached on particular issues during the process can be recorded separately, often in a Parenting Plan or heads of agreement.</p></div></div>
      </div>
    </div>
  </section>

  <section class="page-cta" id="discovery" aria-labelledby="wifdr-cta-heading">
    <div class="wrap">
      <div class="page-cta-inner">
        <span class="page-cta-eyebrow">Before you call a lawyer</span>
        <h2 id="wifdr-cta-heading">Find out whether FDR is right for your situation.</h2>
        <p>A free discovery call with an accredited practitioner. No pressure, no commitment, no obligation to proceed.</p>
        <div class="page-cta-actions">
          <a href="https://calendar.app.google/zwNm4dzYnwAwhwxY8" class="btn-light">Book your free discovery call</a>
          <a href="tel:0399617544" class="btn-outline-light">Call (03) 9961 7544</a>
        </div>
        <span class="page-cta-note">Free &bull; Confidential &bull; No obligation &bull; Available nationally</span>
      </div>
    </div>
  </section>
"""

build_page(
    filename="what-is-fdr-v2.html",
    title="What is Family Dispute Resolution? | onlinefdr.com.au",
    meta_desc="Family Dispute Resolution explained for separating couples in Australia. What FDR is under the Family Law Act 1975, how it works, and the confidentiality protections.",
    canonical="/what-is-fdr/",
    current_page="/what-is-fdr/",
    schema_json='{"@context":"https://schema.org","@graph":[{"@type":"WebPage","@id":"https://onlinefdr.com.au/what-is-fdr/#webpage","url":"https://onlinefdr.com.au/what-is-fdr/","name":"What is Family Dispute Resolution? FDR explained for separating couples in Australia","description":"Family Dispute Resolution explained: a structured mediation process under the Family Law Act 1975 for separating couples in Australia. Covers what FDR is, how a typical engagement works, the statutory confidentiality and inadmissibility protections, the 2024 and 2025 legislative updates, and where FDR fits in the family law system.","about":{"@id":"https://onlinefdr.com.au/#organization"},"mainEntity":{"@id":"https://onlinefdr.com.au/what-is-fdr/#faq"}},{"@type":"FAQPage","@id":"https://onlinefdr.com.au/what-is-fdr/#faq","mainEntity":[{"@type":"Question","name":"Is FDR the same as mediation?","acceptedAnswer":{"@type":"Answer","text":"FDR is a form of mediation, but not all mediation is FDR. Family Dispute Resolution is a specific legal term under the Family Law Act, conducted by an accredited practitioner registered with the AGD. Only an accredited FDRP can issue a Section 60I certificate, and the statutory confidentiality and inadmissibility protections under sections 10H and 10J apply specifically to FDR. A general mediator without this accreditation cannot provide the legal outcomes that family law requires."}},{"@type":"Question","name":"How is FDR different from family counselling?","acceptedAnswer":{"@type":"Answer","text":"Family counselling focuses on relationship dynamics, communication, and emotional adjustment, with a therapeutic goal. FDR is a structured dispute resolution process aimed at reaching practical agreements on parenting or financial matters. The two can be complementary, but they are different professions with different goals. FDR practitioners are accredited under the Family Law Act; family counsellors are accredited separately."}},{"@type":"Question","name":"Can FDR be done online?","acceptedAnswer":{"@type":"Answer","text":"Yes. Online FDR is a recognised mode of conducting Family Dispute Resolution under the Family Law Act. The statutory protections and the certificate-issuing process apply equally whether the practitioner meets parties in person or via video conference. Online FDR is particularly useful for parties in different locations, for matters involving safety concerns where physical separation is preferred, and for parties who would otherwise face significant travel or scheduling barriers."}},{"@type":"Question","name":"Do I need a lawyer before doing FDR?","acceptedAnswer":{"@type":"Answer","text":"You do not need a lawyer to participate in FDR. Seeking legal advice before signing any agreement is sensible, so you understand what you are agreeing to. Lawyers do not typically attend FDR sessions. Their role is to advise, not to participate in the mediation itself."}},{"@type":"Question","name":"Who pays for FDR?","acceptedAnswer":{"@type":"Answer","text":"Each party typically pays their own share of the FDR practitioner\'s fee. The precise arrangement is set out at intake. Government-funded FDR services are also available through Family Relationship Centres and not-for-profit providers; means-tested fees apply. The discovery call is the right place to discuss what makes sense for your circumstances."}},{"@type":"Question","name":"What is the difference between FDR and a parenting plan?","acceptedAnswer":{"@type":"Answer","text":"They are different things. FDR is the process. A parenting plan is one of the documents that can come out of the process. A parenting plan is a written agreement between parents about parenting arrangements, signed and dated by both parents. It is not legally enforceable in the same way as a court order, but courts give it significant weight if a parenting matter later comes before them. The other typical FDR outputs are the basis for consent orders, a heads of agreement for financial matters, or a Section 60I certificate where no agreement was reached."}},{"@type":"Question","name":"What if there has been family violence?","acceptedAnswer":{"@type":"Answer","text":"A history of family violence does not automatically make FDR inappropriate, but it does require careful assessment. The Family Law Amendment Act 2024, in force from 10 June 2025, expanded the definition of family violence in section 4AB to expressly include economic and financial abuse. Safety is evaluated as part of the intake process. Where genuine risk is identified, shuttle mediation or an exemption from the FDR requirement may apply. If you have concerns about your safety, raise them during the discovery call. Everything discussed is confidential."}},{"@type":"Question","name":"Can FDR cover both parenting and financial matters?","acceptedAnswer":{"@type":"Answer","text":"Yes. Most couples with children need to resolve both parenting arrangements and financial settlement. These are typically addressed in separate sessions, since they involve different legal frameworks and different preparation requirements. Parenting is often addressed first, as the arrangements for children are usually the most pressing concern. Financial matters follow, or can run concurrently depending on the circumstances."}},{"@type":"Question","name":"What happens if FDR does not result in agreement?","acceptedAnswer":{"@type":"Answer","text":"If agreement is not reached, parties can request a Section 60I certificate, which documents what occurred in the process. The certificate type reflects the practitioner\'s professional assessment of what happened, including whether each party attended and whether each made a genuine effort. The certificate allows the matter to proceed to court for parenting orders. Any agreements reached on particular issues during the process can be recorded separately, often in a parenting plan or heads of agreement."}}]}]}',
    extra_css=WIFDR_CSS,
    breadcrumbs=[("Home", "/"), ("What is FDR?", "/what-is-fdr/")],
    page_html=WIFDR_HTML,
    show_marquee=False,
)
print("What is FDR done.")

# ─────────────────────────────────────────────
# FAQ — Full AEO/SEO anchor page
# ─────────────────────────────────────────────
FAQ_CSS = """
.faq-hero{background:var(--charcoal);padding:120px 0 72px;position:relative;overflow:hidden}
.faq-hero::before{content:'';position:absolute;inset:0;background:radial-gradient(ellipse 60% 70% at 80% 30%,rgba(196,135,58,0.09) 0%,transparent 60%);pointer-events:none}
.faq-fold-grid{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:start;position:relative;z-index:1;width:100%;min-height:0}
.faq-fold-grid .faq-hero-inner{max-width:none}
.faq-fold-image-panel{position:relative;align-self:stretch;opacity:0;animation:fadeUp 0.9s var(--ease) 0.4s forwards}
.faq-fold-image-panel > .faq-fold-img-real{position:absolute;inset:0;width:100%;height:100%}
.faq-fold-image-panel img{width:100%;height:100%;object-fit:cover;object-position:center 50%;border-radius:8px}
.faq-hero-inner{position:relative;z-index:1;max-width:760px}
.faq-hero h1{font-size:clamp(2.8rem,6vw,5rem);font-weight:800;line-height:1.0;letter-spacing:-0.03em;color:var(--white);margin-bottom:20px}
.faq-hero h1 .accent{color:var(--ochre)}
.faq-hero-sub{font-size:1.1rem;font-weight:400;color:rgba(253,250,246,0.6);line-height:1.8;max-width:600px}

/* PAGE LAYOUT */
.faq-page-wrap{padding:72px 0 100px}
.faq-page-grid{display:grid;grid-template-columns:220px 1fr;gap:64px;align-items:start}

/* STICKY NAV */
.faq-toc{position:sticky;top:92px}
.faq-toc-label{font-size:0.62rem;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;color:var(--light-mid);margin-bottom:16px;display:block}
.faq-toc-list{list-style:none;display:flex;flex-direction:column;gap:2px}
.faq-toc-item a{display:flex;align-items:center;gap:8px;font-size:0.8rem;font-weight:600;color:var(--mid);text-decoration:none;padding:7px 12px;border-radius:6px;transition:all 0.2s;line-height:1.35}
.faq-toc-item a:hover{color:var(--charcoal);background:var(--dust-2)}
.faq-toc-item a.active{color:var(--terra);background:var(--ochre-pale)}
.faq-toc-dot{width:6px;height:6px;border-radius:50%;background:var(--dust-3);flex-shrink:0;transition:background 0.2s}
.faq-toc-item a.active .faq-toc-dot{background:var(--terra)}
.faq-toc-count{margin-left:auto;font-size:0.65rem;font-weight:700;color:var(--light-mid);background:var(--dust-2);padding:2px 7px;border-radius:100px}

/* FAQ SECTIONS */
.faq-sections{display:flex;flex-direction:column;gap:64px}
.faq-section-block{}
.faq-section-anchor{display:block;height:0;visibility:hidden;margin-top:-92px;padding-top:92px}
.faq-section-header{margin-bottom:28px;padding-bottom:18px;border-bottom:2px solid var(--dust-3)}
.faq-section-header h2{font-size:clamp(1.4rem,2.4vw,1.9rem);font-weight:800;line-height:1.1;letter-spacing:-0.02em;color:var(--charcoal);margin-bottom:6px}
.faq-section-header h2 .accent{color:var(--terra)}
.faq-section-header p{font-size:0.88rem;font-weight:400;color:var(--light-mid);line-height:1.5}
.faq-section-count{font-size:0.62rem;font-weight:700;letter-spacing:0.14em;text-transform:uppercase;color:var(--terra);margin-bottom:10px;display:block}

/* FAQ ITEMS — enhanced for this page */
.faq-full-list{border:1px solid var(--dust-3);border-radius:10px;overflow:hidden;background:var(--white)}
.faq-full-item{border-bottom:1px solid var(--dust-3)}
.faq-full-item:last-child{border-bottom:none}
.faq-full-q{width:100%;display:flex;align-items:flex-start;justify-content:space-between;gap:20px;padding:20px 26px;background:none;border:none;text-align:left;cursor:pointer;font-family:var(--f);font-size:0.92rem;font-weight:600;color:var(--charcoal);transition:background 0.2s;line-height:1.45}
.faq-full-q:hover{background:var(--ochre-pale)}
.faq-full-q svg{flex-shrink:0;color:var(--terra);transition:transform 0.3s;margin-top:2px}
.faq-full-item.open .faq-full-q{background:var(--ochre-pale)}
.faq-full-item.open .faq-full-q svg{transform:rotate(45deg)}
.faq-full-a{display:none;padding:0 26px 22px}
.faq-full-item.open .faq-full-a{display:block}
.faq-full-a p{font-size:0.9rem;font-weight:400;color:var(--mid);line-height:1.8;margin-bottom:12px}
.faq-full-a p:last-child{margin-bottom:0}
.faq-full-a p strong{font-weight:700;color:var(--charcoal)}
.faq-full-a a{color:var(--terra);font-weight:600;text-decoration:none;border-bottom:1px solid rgba(168,92,50,0.3);transition:border-color 0.2s}
.faq-full-a a:hover{border-color:var(--terra)}
.faq-full-a .notice{margin:14px 0 4px}

/* SEARCH (static style, no JS logic needed for launch) */
.faq-search-wrap{margin-bottom:36px}
.faq-search{position:relative}
.faq-search input{font-family:var(--f);font-size:0.95rem;font-weight:400;color:var(--charcoal);background:var(--white);border:1px solid var(--dust-3);border-radius:8px;padding:14px 48px 14px 18px;width:100%;transition:border-color 0.2s,box-shadow 0.2s}
.faq-search input:focus{outline:none;border-color:var(--ochre);box-shadow:0 0 0 3px rgba(196,135,58,0.1)}
.faq-search input::placeholder{color:var(--light-mid)}
.faq-search-icon{position:absolute;right:16px;top:50%;transform:translateY(-50%);color:var(--light-mid);pointer-events:none}

/* CTA CARD in content */
.faq-cta-inline{background:var(--terra);border-radius:10px;padding:28px 28px;margin:0;display:flex;align-items:center;justify-content:space-between;gap:24px;flex-wrap:wrap}
.faq-cta-inline p{font-size:0.95rem;font-weight:500;color:rgba(253,250,246,0.85);line-height:1.5;margin:0;max-width:420px}
.faq-cta-inline p strong{color:var(--white)}

@media(max-width:960px){
  .faq-page-grid{grid-template-columns:1fr}
  .faq-toc{display:none}
  .faq-fold-grid{grid-template-columns:1fr;gap:0}
  .faq-fold-image-panel{position:static;align-self:auto;aspect-ratio:2/1;margin-top:32px;border-radius:8px;overflow:hidden}
  .faq-fold-image-panel > .faq-fold-img-real{position:static;width:100%;height:100%}
  .faq-fold-image-panel img{width:100%;height:100%;object-fit:cover;border-radius:8px}
}
"""

FAQ_JS = """<script>
// Accordion for full FAQ items
document.querySelectorAll('.faq-full-q').forEach(btn=>{
  btn.addEventListener('click',()=>{
    const item=btn.closest('.faq-full-item');
    const isOpen=item.classList.contains('open');
    // optionally close others in same section
    item.closest('.faq-full-list').querySelectorAll('.faq-full-item').forEach(i=>{
      i.classList.remove('open');
      i.querySelector('.faq-full-q').setAttribute('aria-expanded','false');
    });
    if(!isOpen){item.classList.add('open');btn.setAttribute('aria-expanded','true');}
  });
});

// TOC active state on scroll
const sections=document.querySelectorAll('.faq-section-anchor');
const tocLinks=document.querySelectorAll('.faq-toc-item a');
const onScroll=()=>{
  let current='';
  sections.forEach(s=>{
    if(window.scrollY>=(s.parentElement.offsetTop-120))current=s.id;
  });
  tocLinks.forEach(a=>{
    a.classList.toggle('active',a.getAttribute('href')==='#'+current);
  });
};
window.addEventListener('scroll',onScroll,{passive:true});
onScroll();
</script>"""

def faq_item(q, a, schema=True):
    schema_attrs = ' itemscope itemprop="mainEntity" itemtype="https://schema.org/Question"' if schema else ''
    ans_attrs = ' itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer"' if schema else ''
    q_prop = ' itemprop="name"' if schema else ''
    a_prop = ' itemprop="text"' if schema else ''
    icon = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>'
    return f"""        <div class="faq-full-item"{schema_attrs}>
          <button class="faq-full-q" aria-expanded="false"{q_prop}>{q}{icon}</button>
          <div class="faq-full-a"{ans_attrs}><p{a_prop}>{a}</p></div>
        </div>"""

SECTIONS = [
  {
    "id": "what-is-fdr",
    "title": "What is FDR?",
    "accent": "FDR?",
    "desc": "The basics of Family Dispute Resolution for people who are new to the process.",
    "count": 7,
    "items": [
      ("What is Family Dispute Resolution?",
       "Family Dispute Resolution is a structured, professionally facilitated process that helps separating couples reach their own agreements about parenting and financial matters. A trained, accredited practitioner facilitates conversations between both parties, helping them work toward outcomes they have made themselves. The practitioner does not make decisions. Their role is to create a structured space where both people can hear each other and find workable solutions."),
      ("Is FDR the same as mediation?",
       "FDR is a specific form of mediation defined under the Family Law Act 1975 (Cth). Not all mediation is FDR. Only an accredited Family Dispute Resolution Practitioner registered with the Australian Government Attorney-General's Department can conduct FDR and issue a Section 60I certificate. A general mediator without this accreditation cannot provide the legal outcomes that family law requires."),
      ("Is FDR compulsory?",
       "For parenting matters, in most cases yes. Before applying for parenting orders in the Federal Circuit and Family Court, parties must in most cases attempt FDR and obtain a Section 60I certificate from an accredited FDRP. Exemptions to the Section 60I requirement exist for urgent matters, family violence, child safety concerns, and a small number of other circumstances, but these are not automatic. For financial and property matters, the Section 60I certificate does not apply. However, every initiating application requires a Genuine Steps Certificate under Schedule 1 of the Federal Circuit and Family Court of Australia (Family Law) Rules 2021. The Genuine Steps Certificate is signed by the party themselves and confirms that the pre-action procedures have been followed, including a genuine attempt at dispute resolution. Where financial FDR has been attempted, this practice provides a Letter of Attendance and Genuine Effort that the party can use to support their Genuine Steps Certificate."),
      ("What can FDR be used for?",
       "FDR can be used to resolve parenting arrangements (where children live, how time is shared, parental responsibility), financial and property settlement (division of assets, superannuation, debt), or both. It can also be used post-separation when circumstances change and existing arrangements need to be revisited, without returning to court."),
      ("What is the difference between FDR and going to court?",
       "FDR is confidential, party-controlled, and typically resolved in weeks. Court proceedings are on the public record, decided by a judge, and can commonly take 18 to 36 months from filing to final hearing. Legal costs in contested proceedings can typically reach tens of thousands of dollars per party. FDR produces agreements the parties made themselves, which are generally more durable and workable than orders imposed by a court."),
      ("Does FDR actually work?",
       "FDR is the path most separating couples are advised to try first, and it resolves a substantial share of matters short of court. Outcomes are stronger when both parties participate genuinely, arrive prepared, and approach the process with a willingness to find workable solutions. FDR is not a guarantee of agreement, but it is the most cost-effective and least damaging path to try before considering litigation."),
      ("What happens if FDR does not result in agreement?",
       "If agreement cannot be reached on all issues, parties can request a Section 60I certificate, which documents what occurred. The certificate type reflects the practitioner's professional assessment of what happened, including whether each party attended and whether each made a genuine effort. The certificate allows the matter to proceed to court for parenting orders. Any agreements reached on some issues during the process are preserved in a Parenting Plan or heads of agreement. A certificate is an outcome of last resort, not the goal of the process. Our commitment is to keep working toward agreement for as long as it remains a genuine possibility."),
    ]
  },
  {
    "id": "the-process",
    "title": "The process",
    "accent": "process",
    "desc": "What happens at each stage, from first contact to final agreement.",
    "count": 8,
    "items": [
      ("How does the FDR process work?",
       "The process moves through four stages. First, a free discovery call to confirm FDR is appropriate. Second, individual intake sessions of one hour each, conducted separately. Third, one or more joint mediation sessions: four hours for parenting matters and three hours for financial matters. Fourth, if agreement is reached, the terms are documented in a Parenting Plan or heads of agreement. If not, a Section 60I certificate may be issued. See our <a href='/how-it-works/'>How It Works</a> page for a full walkthrough."),
      ("What happens in the intake session?",
       "Each party meets separately with the mediator for one hour. This is your opportunity to speak candidly about your situation, your concerns, and what matters most to you, without the other party present. The intake session also allows the mediator to assess whether the matter is suitable for joint FDR and to identify any issues that may affect the process, including safety considerations."),
      ("How long does a joint session run?",
       "Joint mediation sessions run for four hours for parenting matters and three hours for financial matters. For parenting matters, many couples with lower levels of conflict can work through arrangements in a single session. Financial settlement typically requires its own session. Higher-conflict matters, or those involving greater complexity, may need two or three sessions for each area."),
      ("How many sessions will we need?",
       "It depends on the complexity of the matter and the distance between the parties at the start. Most matters that need more than one joint session resolve in two to three joint sessions in total. A couple without children resolving a straightforward financial settlement may complete the process in a single three-hour joint session, provided both arrive with the Full and Frank Disclosure worksheet completed. A matter involving both parenting and financial settlement across a significant conflict might require more sessions across both areas. Even at the higher end, this remains significantly less costly than contested proceedings."),
      ("What happens between sessions?",
       "Sometimes parties are given specific tasks to complete before the next session, to ensure progress continues rather than covering the same ground again. This might include gathering financial documents, obtaining property valuations, or reflecting on specific proposals. The mediator will be direct about what is needed and why."),
      ("How quickly can we start?",
       "Discovery calls are typically available within a few days of initial contact. Intake sessions follow shortly after. For most matters, the first joint session can be scheduled within two weeks of first contact. This is significantly faster than government-funded FDR services in most parts of Australia, where waiting times commonly run to several months."),
      ("Do both parties have to agree to participate?",
       "Yes. FDR requires the genuine participation of both parties. If only one party contacts us, we will explain the process and can suggest ways to approach the other party about participating. If the other party declines or fails to attend, a Section 60I certificate under paragraph 60I(8)(a) can be issued reflecting their non-attendance, which allows the matter to proceed to court for parenting orders."),
      ("Can I have a support person with me during sessions?",
       "This can be discussed and arranged in appropriate circumstances. Raise it during the discovery call or intake session. The mediator will assess whether having a support person present is workable given the specific dynamics of the matter. The goal is to preserve the conditions in which both parties can communicate effectively."),
    ]
  },
  {
    "id": "parenting",
    "title": "Parenting matters",
    "accent": "matters",
    "desc": "Questions about parenting arrangements, parental responsibility, and agreements for children.",
    "count": 9,
    "items": [
      ("What parenting issues can FDR help resolve?",
       "FDR can help resolve where children live, how time is divided between parents, parental responsibility (who makes major decisions about schooling, health, and religion), communication arrangements between parents, handover arrangements, holiday and special occasion schedules, and how future disagreements will be managed."),
      ("Is there a presumption of equal shared parenting time?",
       "No. There has never been a legal presumption of equal time, and the May 2024 amendments to the Family Law Act removed the previous presumption of equal shared parental responsibility. Courts now assess both time and responsibility based on the individual circumstances of each family. The question is always what arrangements best serve the child's needs, not what each parent is entitled to."),
      ("What is parental responsibility?",
       "Parental responsibility is the legal authority to make major long-term decisions about a child's life, including schooling, healthcare, religion, significant changes to living arrangements, and changes of name. It is separate from where the child lives and how much time they spend with each parent. Since May 2024, courts assess parental responsibility on the merits of each case rather than applying a default presumption."),
      ("What is a Parenting Plan?",
       "A Parenting Plan is a written agreement between parents about parenting arrangements. It is recognised under section 63C of the Family Law Act. It must be in writing, signed and dated by both parents, and made free of threat, duress, or coercion. A Parenting Plan provides flexibility to adjust arrangements as children grow and circumstances change, and can alter the effect of earlier Consent Orders by mutual agreement. It does not require court approval and can be updated when both parties agree. It is the most common outcome of parenting FDR. The colloquial term 'Parenting Agreement' is sometimes used; the legal term is Parenting Plan."),
      ("What is the difference between a Parenting Plan and Consent Orders?",
       "A Parenting Plan is a written agreement that is not a court order and is not legally enforceable through the court system. Consent Orders are court orders made by agreement and approved by a Judicial Registrar, carrying the same legal force as orders made after a contested hearing. Consent Orders for parenting are typically used where one party needs the enforceability of a court order. Parenting Plans are more flexible and better suited to many families, as they can be updated by mutual agreement without returning to court."),
      ("Does the child get a say in the arrangements?",
       "Children do not participate in FDR directly. Their perspectives are brought into the process through what each parent knows and observes about their children's needs, wishes, and day-to-day experience. In court proceedings, a child's views may be heard through an Independent Children's Lawyer or a family consultant's report. In FDR, the mediator helps both parents to consider and give appropriate weight to their children's perspectives."),
      ("Do I need a Section 60I certificate before applying for parenting orders?",
       "Yes, in most cases, and a parenting application also requires a Genuine Steps Certificate. Before applying for parenting orders in the Federal Circuit and Family Court, you must attempt FDR with an accredited FDRP and obtain a Section 60I certificate. From June 2025, the court can reject a parenting application for filing where a valid certificate or exemption is not provided. Separately, every initiating application also requires a Genuine Steps Certificate under Schedule 1 of the Federal Circuit and Family Court of Australia (Family Law) Rules 2021. The Genuine Steps Certificate is signed by the party themselves and confirms compliance with the pre-action procedures. Exemptions to the Section 60I requirement exist for matters involving family violence, child abuse, or urgent situations requiring immediate court intervention."),
      ("Can parenting arrangements be changed after they are agreed?",
       "Yes. Parenting Plans can be changed by mutual agreement at any time, simply by both parents agreeing to new terms. This flexibility is one of the main reasons Parenting Plans are more common than Consent Orders for many families. If you have Consent Orders, changing them without the other party's agreement requires returning to court. The court applies the Rice and Asplund principle, requiring a significant change in circumstances before it will revisit final parenting orders. The threshold is deliberately high."),
      ("What if one parent wants to relocate with the children?",
       "Relocation is one of the most complex issues in family law. If relocation would significantly affect the children's relationship with the other parent, it generally requires either the other parent's agreement or a court order. FDR can be an effective forum for working through relocation proposals, as it allows both parties to explore the implications and consider options in a structured environment before positions become entrenched."),
    ]
  },
  {
    "id": "financial",
    "title": "Financial and property matters",
    "accent": "property matters",
    "desc": "Questions about dividing assets, superannuation, debt, and formalising financial agreements.",
    "count": 8,
    "items": [
      ("Is there an automatic 50/50 split of assets?",
       "No. Australian family law does not apply an automatic equal split. The Family Law Act uses a four-step framework: identify and value all assets and liabilities, assess each party's contributions (financial and non-financial), consider each party's future needs, and determine whether the proposed outcome is just and equitable. The Family Law Amendment Act 2024, which commenced on 10 June 2025, codified this four-step framework directly into the Act. The result depends entirely on the specific circumstances of the relationship."),
      ("Does property settlement apply to de facto couples?",
       "Yes. De facto couples have substantially the same property and financial settlement rights as married couples under the Family Law Act. The same four-step framework applies. A de facto relationship is covered if it lasted at least two years, the couple has a child together, or one party made substantial contributions. De facto couples must apply within two years of the end of the relationship."),
      ("Can superannuation be divided as part of settlement?",
       "Yes. Superannuation is treated as property under the Family Law Act and can be split as part of financial settlement. A superannuation split does not involve early withdrawal. Part of one party's superannuation interest is transferred to the other party's fund, remaining preserved until retirement. A formal agreement or court order is required, and the fund trustee must be notified."),
      ("What is the time limit for making a financial settlement claim?",
       "<strong>Married couples</strong> must apply for property orders within 12 months of the divorce becoming final. <strong>De facto couples</strong> must apply within two years of the end of the relationship. After these limits, court permission is required and is not guaranteed. Property settlement and divorce are separate processes. You do not need to wait for a divorce to formalise financial arrangements."),
      ("What is the difference between Consent Orders and a Binding Financial Agreement?",
       "Consent Orders are submitted to the court for approval and are legally binding once approved by a registrar. They do not require a hearing. Binding Financial Agreements (BFAs) are private contracts that do not involve the court, but require both parties to obtain independent legal advice before signing. BFAs are generally more expensive to prepare and more vulnerable to being set aside if a court later finds the agreement was unjust. For most post-separation financial settlements, Consent Orders are simpler, less expensive, and more reliably enforceable."),
      ("Do I need a Section 60I certificate for financial settlement?",
       "No, but financial applications still require a Genuine Steps Certificate. The Section 60I certificate applies only to parenting applications under Part VII of the Family Law Act. For financial applications, a party signs and files a Genuine Steps Certificate under Schedule 1 of the Federal Circuit and Family Court of Australia (Family Law) Rules 2021. The Genuine Steps Certificate is signed by the party themselves, not by a lawyer and not by a mediator, and confirms compliance with the pre-action procedures. Where financial FDR has been attempted with this practice, the practitioner provides a Letter of Attendance and Genuine Effort confirming attendance, the assessment of each party's effort, and the outcome. The party can attach or refer to that letter in their own Genuine Steps Certificate. The same statutory confidentiality and inadmissibility protections under sections 10H and 10J of the Family Law Act apply to financial FDR as they do to parenting FDR."),
      ("What financial documents do I need to bring to FDR?",
       "Both parties complete the <a href='/downloads/onlinefdr-disclosure-worksheet.pdf'>Full and Frank Disclosure worksheet</a> ahead of the first joint financial session. The worksheet covers income, assets, liabilities, superannuation, financial resources, and any property disposals since separation. Supporting documents include three years of tax returns, twelve months of bank and credit card statements, recent superannuation statements, and statements for any loans or mortgages. The duty of full and frank disclosure is now a statutory obligation under sections 71B and 90RI of the Family Law Act. The worksheet is provided to you at the intake session."),
      ("What if my ex is hiding assets?",
       "Full and frank financial disclosure is a statutory obligation under sections 71B, 90RI, and 90YJA of the Family Law Act, brought in by the 2024 amendments. The 2024 amendments also place a parallel obligation on FDR practitioners to inform parties about their duty of disclosure, explain when it applies, and encourage compliance. In FDR, the process relies on both parties providing honest disclosure. If you have reason to believe the other party is not disclosing all assets, raise this with your mediator. In court proceedings, non-disclosure can result in costs orders, the matter being stayed or dismissed, or the court drawing adverse inferences. If non-disclosure is a genuine concern, you should seek legal advice before or alongside the FDR process."),
    ]
  },
  {
    "id": "section-60i",
    "title": "Section 60I certificates",
    "accent": "60I certificates",
    "desc": "Everything about the certificate required before most family court applications.",
    "count": 6,
    "items": [
      ("What is a Section 60I certificate?",
       "A Section 60I certificate is a document issued by an accredited Family Dispute Resolution Practitioner after a proper FDR process. It is required before applying for parenting orders in the Federal Circuit and Family Court. The certificate documents the outcome of the FDR process without disclosing what was discussed, which is protected by both confidentiality (s10H Family Law Act) and inadmissibility (s10J). Section 60I certificates apply to parenting matters only. For financial matters, the Section 60I certificate does not apply, but a Genuine Steps Certificate (signed by the party themselves under Schedule 1 of the FCFCOA (Family Law) Rules 2021) is required for every initiating application. Where financial FDR has been attempted, this practice provides a Letter of Attendance and Genuine Effort to support the party's Genuine Steps Certificate."),
      ("What are the five types of Section 60I certificate?",
       "There are five certificate types under section 60I(8) of the Family Law Act, each documenting a different outcome: <strong>60I(8)(a):</strong> the other party did not attend FDR. <strong>60I(8)(aa):</strong> the practitioner assessed FDR as not appropriate to be conducted. <strong>60I(8)(b):</strong> both parties attended and made a genuine effort. <strong>60I(8)(c):</strong> one or more attendees did not make a genuine effort. <strong>60I(8)(d):</strong> FDR began but became inappropriate to continue. The type of certificate issued reflects the practitioner's professional assessment of what occurred and can affect how the court views the conduct of each party."),
      ("Can I request a Section 60I certificate without going through FDR?",
       "No. A Section 60I certificate cannot be issued on request. It can only be issued by an accredited FDRP after a proper FDR process has been conducted, including individual intake sessions with each party. The certificate documents what occurred in that process. It is not a rubber stamp and cannot be used as a shortcut to court."),
      ("When is a Section 60I certificate not required?",
       "Exemptions apply where there are reasonable grounds to believe a party has engaged in family violence or child abuse, where the application falls within one of the urgency-related grounds set out in s60I(9), where a party is unable to participate due to incapacity, or where a party is in a location where FDR is not reasonably available. Exemptions are not automatic and must be established to the court's satisfaction. From June 2025, under the Family Law Amendment Act 2024, the court has express power to reject a parenting application for filing if a Section 60I certificate is required and has not been filed."),
      ("Does a Section 60I certificate reveal what was said in FDR?",
       "No. FDR is protected by two distinct provisions of the Family Law Act. Confidentiality (s10H) prevents the practitioner from disclosing what was said, with limited exceptions, and parties agree contractually under our terms to maintain the same confidentiality. Inadmissibility (s10J) goes further: even if confidentiality is breached and something is disclosed, that information still cannot be admitted as evidence in court. The certificate documents only the outcome of the process, not its content."),
      ("How long does it take to get a Section 60I certificate?",
       "Certificates are typically requested at the conclusion of the FDR process or where it becomes clear the process cannot continue. For matters where both parties participate, the certificate can usually be issued within a short time of the final session. From first contact to certificate, most matters move through the process in a matter of weeks rather than months, depending on scheduling and the number of sessions required. A certificate must not be issued more than 12 months after the person's last attendance, or attempted attendance, at FDR, and is generally relied on by the court for filings made within 12 months of issue."),
    ]
  },
  {
    "id": "online-fdr",
    "title": "Online FDR",
    "accent": "FDR",
    "desc": "How online FDR works, what you need, and why it works as well as in-person.",
    "count": 5,
    "items": [
      ("Is online FDR as effective as in-person?",
       "Yes. Research and practice experience consistently show that online FDR produces comparable outcomes to in-person sessions. The online format offers meaningful advantages: parties in different cities or states can participate without travel, physical separation reduces the anxiety of sharing a physical space, and shuttle mediation is easier to manage. For many families, online FDR is not just a practical alternative to in-person, it is the more suitable format."),
      ("What do I need for an online FDR session?",
       "A device with a camera and microphone (laptop or desktop is recommended over phone for sessions of this length), a reliable internet connection, and a private, quiet space where you will not be interrupted for the duration of the session. Sessions are conducted via Google Meet. You do not need to install any software beyond a current web browser."),
      ("What if I have technical problems during a session?",
       "Your mediator will have a contingency plan for technical issues. If connection is lost, the session can be paused and rejoined. If a significant technical issue cannot be resolved, the session can be rescheduled. Raise any concerns about your technical setup during the discovery call or intake session so they can be addressed before the joint process begins."),
      ("Can both parties be in different states or territories?",
       "Yes. This is one of the primary reasons online FDR exists. Both parties can participate from wherever they are in Australia. The process and legal outcomes are identical regardless of location. A couple where one party is in Perth and the other in Brisbane can complete the entire FDR process online without either party travelling."),
      ("Is online FDR available to people in regional and rural areas?",
       "Yes, and this is one of the most important things online FDR makes possible. Government-funded FDR services in regional and rural Australia often have significant waiting times, and some areas have no local service at all. Online FDR removes geography as a barrier. Appointments are typically available within two weeks of first contact, regardless of where either party is located."),
    ]
  },
  {
    "id": "practical",
    "title": "Practical questions",
    "accent": "questions",
    "desc": "The logistics and practicalities of participating in FDR.",
    "count": 6,
    "items": [
      ("Do I need a lawyer to participate in FDR?",
       "No. You do not need a lawyer to participate in FDR, and lawyers do not typically attend sessions. You are strongly encouraged to seek independent legal advice before and after sessions, and before signing any agreement, so you fully understand what you are agreeing to. Your mediator is not a lawyer and will not give legal advice, but they will be direct about when legal advice is important."),
      ("What if there has been family violence in our relationship?",
       "A history of family violence does not automatically make FDR inappropriate, but it requires careful assessment. The Family Law Amendment Act 2024, in force from 10 June 2025, expanded the definition of family violence in section 4AB to expressly include economic and financial abuse. Safety is evaluated as part of the intake process. Where genuine risk is identified, shuttle mediation, additional safety arrangements, or an exemption from the FDR requirement may apply. Raise any concerns about your safety during the discovery call. Everything discussed is confidential, and your safety takes priority over any procedural requirement."),
      ("What if my ex refuses to participate?",
       "You cannot force the other party to participate. If the other party declines to attend after being given a genuine opportunity to do so, a Section 60I certificate under paragraph 60I(8)(a) can be issued reflecting their non-attendance. This certificate allows you to proceed to court for parenting orders. Courts may take non-participation into account when making subsequent orders, including in relation to costs. If you are having difficulty getting the other party to engage, raise this during the discovery call. We can discuss realistic options."),
      ("What if English is not my first language?",
       "Interpreting services can be arranged for FDR sessions. Raise this requirement during the discovery call so arrangements can be confirmed before your intake session. Both parties should be able to participate fully and understand everything that is discussed. The cost of interpreter services may be an additional consideration to discuss."),
      ("Is everything discussed in FDR confidential?",
       "Yes, and the protection is stronger than most people realise. FDR is covered by two distinct provisions of the Family Law Act. Confidentiality (s10H) prevents the practitioner from disclosing what was said in the process, with limited exceptions, and both parties agree contractually under our terms to maintain the same confidentiality. Inadmissibility (s10J) is a separate and additional protection: even if confidentiality is breached and something is disclosed, that information cannot be admitted as evidence in court. The narrow exceptions include disclosures indicating a risk of harm to a child or another person."),
      ("What if we reach an agreement and one party later changes their mind?",
       "This depends on how the agreement was formalised. A Parenting Plan can be changed by mutual agreement at any time. A Consent Order, whether for parenting or financial matters, is legally binding once approved by the court and changing it without both parties' agreement requires a court application that meets the Rice and Asplund significant-change-of-circumstances threshold. If one party seeks to walk away from an agreement made in FDR before it has been formalised, seek legal advice immediately about your options for preserving the agreed terms."),
    ]
  },
  {
    "id": "accreditation",
    "title": "Accreditation and qualifications",
    "accent": "qualifications",
    "desc": "What accreditation means, why it matters, and what our credentials are.",
    "count": 4,
    "items": [
      ("What is an accredited FDRP?",
       "An accredited Family Dispute Resolution Practitioner is a mediator who has completed the specific training and assessment requirements set by the Australian Government Attorney-General's Department and holds current registration with the AGD. Only an accredited FDRP can issue a Section 60I certificate. Accreditation requires ongoing professional development, adherence to a code of practice, and professional indemnity insurance."),
      ("Why does accreditation matter?",
       "Accreditation is the difference between a qualified, accountable practitioner and someone offering a service without the training, professional obligations, or legal authority that protect clients. An accredited FDRP is subject to professional conduct standards, complaints processes, and the legal framework of the Family Law Act. Only they can issue the certificate required before court proceedings can begin."),
      ("What credentials does onlinefdr.com.au hold?",
       "Practitioners working under the onlinefdr.com.au brand hold current registration with the Australian Government Attorney-General's Department as accredited Family Dispute Resolution Practitioners under the Family Law (Family Dispute Resolution Practitioners) Regulations 2025, and are members of relevant professional bodies including the Australian Mediation Association (AMA). These credentials reflect both legal accreditation and active participation in the professional community. For more about the founder of the practice, see the <a href='/about/'>About page</a>."),
      ("How do I verify an FDRP's accreditation?",
       "Accredited FDRPs are registered with the Australian Government Attorney-General's Department. You can ask any practitioner for their AGD registration number and verify it directly with the AGD. You should always confirm accreditation before engaging a practitioner for FDR, particularly if the outcome you need is a Section 60I certificate."),
    ]
  },
]

# Build TOC
toc_items = ""
for s in SECTIONS:
    toc_items += f"""      <li class="faq-toc-item">
        <a href="#{s['id']}"><span class="faq-toc-dot"></span>{s['title']}<span class="faq-toc-count">{s['count']}</span></a>
      </li>\n"""

# Build schema FAQ list
schema_items = []
for s in SECTIONS:
    for q, a in s['items']:
        import re
        clean_a = re.sub(r'<[^>]+>', '', a).replace('"', '\\"').replace('\n', ' ')
        schema_items.append(f'{{"@type":"Question","name":"{q}","acceptedAnswer":{{"@type":"Answer","text":"{clean_a}"}}}}')

# Wrap in @graph that also references the home Organization entity
faq_webpage = '{"@type":"WebPage","@id":"https://onlinefdr.com.au/faq/#webpage","url":"https://onlinefdr.com.au/faq/","name":"FAQ — Family Dispute Resolution Questions Answered","description":"Plain answers to every common question about Family Dispute Resolution in Australia. Covers what FDR is, the process, parenting matters, financial and property settlement, Section 60I certificates, online FDR, practical questions, and accreditation.","about":{"@id":"https://onlinefdr.com.au/#organization"},"isPartOf":{"@id":"https://onlinefdr.com.au/#website"},"mainEntity":{"@id":"https://onlinefdr.com.au/faq/#faq"},"inLanguage":"en-AU"}'
faq_faqpage = '{"@type":"FAQPage","@id":"https://onlinefdr.com.au/faq/#faq","mainEntity":[' + ','.join(schema_items) + ']}'
schema_json = '{"@context":"https://schema.org","@graph":[' + faq_webpage + ',' + faq_faqpage + ']}'

# Build section HTML
sections_html = ""
for s in SECTIONS:
    items_html = ""
    for q, a in s['items']:
        items_html += faq_item(q, f'<p>{a}</p>' if not a.startswith('<') else a) + "\n"
    # replace the <p> wrapping since faq_item already adds it
    # Actually build without wrapping
    sections_html += f"""
        <div class="faq-section-block">
          <span class="faq-section-anchor" id="{s['id']}"></span>
          <div class="faq-section-header">
            <span class="faq-section-count">{s['count']} questions</span>
            <h2>{s['title'].replace(s['accent'], f'<span class="accent">{s["accent"]}</span>', 1)}</h2>
            <p>{s['desc']}</p>
          </div>
          <div class="faq-full-list" role="list">
{items_html}          </div>
        </div>"""

FAQ_HTML = f"""
  <header class="faq-hero page-fold" aria-labelledby="faq-main-heading">
    <div class="wrap">
      <div class="faq-fold-grid">
        <div class="faq-hero-inner">
          <span class="page-label" style="color:var(--ochre-lt)">Everything you need to know</span>
          <h1 id="faq-main-heading">Frequently asked <span class="accent">questions.</span></h1>
          <p class="faq-hero-sub">Plain answers to the questions separating couples ask most. From first contact to final agreement, and everything in between.</p>
        </div>
        <div class="faq-fold-image-panel" aria-hidden="true">
          <div class="faq-fold-img-real"><img src="/images/faq-fold.jpg" alt="A wooden writing desk in soft warm light, with a brass desk lamp illuminating an open leather-bound notebook and a fountain pen resting across blank pages, a closed silver laptop and a white ceramic coffee cup to one side. The quiet act of working through questions." fetchpriority="high"></div>
        </div>
      </div>
    </div>
  </header>

  <!-- ABOVE-FOLD MARQUEE -->
  <div class="marquee-bar" aria-label="Accreditation and credentials" role="marquee">
    <div class="marquee-track" aria-hidden="true">
      <span class="marquee-item">AGD-Accredited FDRP <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Australian Mediation Association Member <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Section 60I Certificates (s 66H in WA) <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Conducted Securely Online <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Available Anywhere in Australia <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Free Discovery Call <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">No Obligation <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Confidential under the Family Law Act <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Both Parenting and Financial Matters <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">AGD-Accredited FDRP <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Australian Mediation Association Member <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Section 60I Certificates (s 66H in WA) <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Conducted Securely Online <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Available Anywhere in Australia <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Free Discovery Call <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">No Obligation <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Confidential under the Family Law Act <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Both Parenting and Financial Matters <span class="marquee-sep">&bull;</span></span>
    </div>
  </div>


  <div class="wrap faq-page-wrap">
    <div class="faq-page-grid">

      <nav class="faq-toc" aria-label="FAQ sections">
        <span class="faq-toc-label">Jump to section</span>
        <ul class="faq-toc-list">
{toc_items}        </ul>
      </nav>

      <div>
        <div class="faq-search-wrap">
          <div class="faq-search">
            <input type="search" placeholder="Search questions..." aria-label="Search FAQ">
            <svg class="faq-search-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
          </div>
        </div>

        <div class="faq-sections">
{sections_html}
          <div class="faq-cta-inline">
            <p><strong>Still have a question?</strong> A free discovery call with an accredited practitioner. Ask anything.</p>
            <a href="https://calendar.app.google/zwNm4dzYnwAwhwxY8" class="btn-light" style="white-space:nowrap">Book a free call</a>
          </div>
        </div>
      </div>

    </div>
  </div>
"""

build_page(
    filename="faq-v2.html",
    title="FAQ | Family Dispute Resolution Questions | onlinefdr.com.au",
    meta_desc="Plain answers to every question separating couples ask about FDR. Parenting, financial settlement, Section 60I certificates, online sessions, accreditation, and more.",
    canonical="/faq/",
    current_page="/faq/",
    schema_json=schema_json,
    extra_css=FAQ_CSS,
    breadcrumbs=[("Home", "/"), ("FAQ", "/faq/")],
    page_html=FAQ_HTML,
    show_marquee=False,
    extra_js=FAQ_JS,
)
print("FAQ done.")

# ─────────────────────────────────────────────
# COMPLAINTS
# ─────────────────────────────────────────────
COMPLAINTS_CSS = """
.complaints-header{background:var(--charcoal);padding:120px 0 72px;position:relative;overflow:hidden}
.complaints-header::before{content:'';position:absolute;inset:0;background:radial-gradient(ellipse 60% 70% at 80% 30%,rgba(196,135,58,0.07) 0%,transparent 60%);pointer-events:none}
.complaints-header-inner{position:relative;z-index:1;max-width:680px}
.complaints-header h1{font-size:clamp(2.4rem,5vw,4.2rem);font-weight:800;line-height:1.0;letter-spacing:-0.03em;color:var(--white);margin-bottom:20px}
.complaints-header-sub{font-size:1rem;font-weight:400;color:rgba(253,250,246,0.55);line-height:1.8;max-width:560px}

.complaints-wrap{padding:72px 0 100px}
.complaints-grid{display:grid;grid-template-columns:1fr 360px;gap:64px;align-items:start}

/* FORM */
.complaints-form-wrap{background:var(--white);border:1px solid var(--dust-3);border-radius:12px;padding:40px 36px}
.complaints-form-wrap h2{font-size:1.4rem;font-weight:800;color:var(--charcoal);letter-spacing:-0.02em;margin-bottom:8px}
.complaints-form-wrap .form-sub{font-size:0.88rem;font-weight:400;color:var(--mid);line-height:1.65;margin-bottom:32px}

/* Inline responses */
.inline-response{display:none;border-radius:8px;padding:22px 24px;margin-top:4px}
.inline-response.show{display:block}
.inline-response.notgrounds{background:var(--ochre-pale);border:1px solid rgba(196,135,58,0.3)}
.inline-response.notgrounds p{font-size:0.9rem;font-weight:400;color:var(--charcoal);line-height:1.7;margin:0}
.inline-response.notgrounds strong{font-weight:700}
.inline-response.success{background:#F0FDF4;border:1px solid #86EFAC}
.inline-response.success p{font-size:0.9rem;font-weight:400;color:#166534;line-height:1.7;margin:0}
.inline-response.success strong{font-weight:700}

/* Fields — reuse base styles from JTT */
.cf-field{display:flex;flex-direction:column;gap:5px;margin-bottom:18px}
.cf-field label{font-size:0.8rem;font-weight:700;color:var(--charcoal)}
.cf-field label .req{color:var(--terra);margin-left:2px}
.cf-hint{font-size:0.74rem;color:var(--light-mid);line-height:1.4;margin-top:2px}

/* Sidebar info */
.complaints-info{display:flex;flex-direction:column;gap:20px}
.complaints-info-card{background:var(--white);border:1px solid var(--dust-3);border-radius:10px;padding:28px 24px}
.complaints-info-card h3{font-size:1rem;font-weight:800;color:var(--charcoal);margin-bottom:14px;letter-spacing:-0.01em}
.complaints-info-card p{font-size:0.86rem;font-weight:400;color:var(--mid);line-height:1.7;margin-bottom:10px}
.complaints-info-card p:last-child{margin-bottom:0}
.complaints-info-card p strong{font-weight:700;color:var(--charcoal)}
.grounds-list{list-style:none;display:flex;flex-direction:column;gap:8px;margin-top:4px}
.grounds-item{display:flex;align-items:flex-start;gap:9px;font-size:0.84rem;font-weight:400;color:var(--mid);line-height:1.45}
.grounds-icon{width:18px;height:18px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:1px}
.grounds-icon.yes{background:var(--ochre-pale);color:var(--terra)}
.grounds-icon.no{background:#FEF2F2;color:#DC2626}

@media(max-width:960px){
  .complaints-grid{grid-template-columns:1fr}
  .complaints-form-wrap{padding:28px 22px}
}
"""

COMPLAINTS_JS = """<script>
const NOT_GROUNDS = ['no-agreement','outcome','other-party','certificate-type'];

const reasonSel = document.getElementById('complaint-reason');
const detailWrap = document.getElementById('detail-wrap');
const notGroundsMsg = document.getElementById('not-grounds-msg');
const form = document.getElementById('complaints-form');
const successMsg = document.getElementById('success-msg');
const submitBtn = document.getElementById('complaints-submit');

reasonSel.addEventListener('change', function() {
  const val = this.value;
  if (!val) {
    detailWrap.style.display = 'none';
    notGroundsMsg.classList.remove('show');
    return;
  }
  if (NOT_GROUNDS.includes(val)) {
    detailWrap.style.display = 'none';
    notGroundsMsg.classList.add('show');
  } else {
    detailWrap.style.display = 'block';
    notGroundsMsg.classList.remove('show');
  }
});

form.addEventListener('submit', function(e) {
  e.preventDefault();
  const val = reasonSel.value;
  if (!val || NOT_GROUNDS.includes(val)) return;
  submitBtn.disabled = true;
  submitBtn.textContent = 'Submitting...';
  const data = new FormData(form);
  fetch('/', {
    method: 'POST',
    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
    body: new URLSearchParams(data).toString()
  }).then(() => {
    form.style.display = 'none';
    successMsg.classList.add('show');
  }).catch(() => {
    submitBtn.disabled = false;
    submitBtn.textContent = 'Submit complaint';
  });
});
</script>"""

COMPLAINTS_HTML = """
  <header class="complaints-header page-fold" aria-labelledby="complaints-heading">
    <div class="wrap">
      <div class="complaints-header-inner">
        <span class="page-label" style="color:var(--ochre-lt)">Feedback and complaints</span>
        <h1 id="complaints-heading">Complaints process</h1>
        <p class="complaints-header-sub">We are committed to conducting every matter with professionalism, impartiality, and care. If you have a concern about the conduct of your process, this page explains how to raise it.</p>
      </div>
    </div>
  </header>

  <!-- ABOVE-FOLD MARQUEE -->
  <div class="marquee-bar" aria-label="Accreditation and credentials" role="marquee">
    <div class="marquee-track" aria-hidden="true">
      <span class="marquee-item">AGD-Accredited FDRP <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Australian Mediation Association Member <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Section 60I Certificates (s 66H in WA) <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Conducted Securely Online <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Available Anywhere in Australia <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Free Discovery Call <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">No Obligation <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Confidential under the Family Law Act <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Both Parenting and Financial Matters <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">AGD-Accredited FDRP <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Australian Mediation Association Member <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Section 60I Certificates (s 66H in WA) <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Conducted Securely Online <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Available Anywhere in Australia <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Free Discovery Call <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">No Obligation <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Confidential under the Family Law Act <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Both Parenting and Financial Matters <span class="marquee-sep">&bull;</span></span>
    </div>
  </div>


  <div class="wrap complaints-wrap">
    <div class="complaints-grid">

      <div>
        <div class="complaints-form-wrap">
          <h2>Raise a concern</h2>
          <p class="form-sub">Select the nature of your concern below. We will respond within two business days for matters within the scope of our complaints process.</p>

          <div id="success-msg" class="inline-response success" role="status">
            <p><strong>Thank you for raising this.</strong> The practitioner responsible for your matter will contact you within two business days to discuss your concern.</p>
          </div>

          <form id="complaints-form" name="complaints" method="POST" data-netlify="true" netlify-honeypot="bot-field" novalidate>
            <input type="hidden" name="form-name" value="complaints">
            <input type="hidden" name="bot-field" style="display:none">

            <div class="cf-field">
              <label for="complaint-reason">Nature of concern <span class="req">*</span></label>
              <select id="complaint-reason" name="reason" required>
                <option value="" disabled selected>Select the nature of your concern</option>
                <optgroup label="Conduct concerns">
                  <option value="confidentiality">Breach of confidentiality</option>
                  <option value="impartiality">Concerns about impartiality or bias</option>
                  <option value="safety">Safety concerns not appropriately managed</option>
                  <option value="conduct">Unprofessional conduct during a session</option>
                  <option value="certificate">Certificate not issued when process was completed</option>
                  <option value="other-conduct">Other conduct concern</option>
                </optgroup>
                <optgroup label="Other feedback">
                  <option value="no-agreement">Agreement was not reached</option>
                  <option value="outcome">I am unhappy with the outcome</option>
                  <option value="other-party">Concern about the other party's conduct</option>
                  <option value="certificate-type">The certificate type that was issued</option>
                </optgroup>
              </select>
            </div>

            <div class="inline-response notgrounds" id="not-grounds-msg" role="alert">
              <p><strong>This is not within the scope of our complaints process.</strong> The outcome of FDR, including whether agreement is reached, the certificate type issued, or the conduct of the other party, is not something we are able to address through a complaint. If you have a concern about the conduct of the process itself, please select the relevant option above. If you would like to discuss your matter further, you are welcome to <a href="/#discovery">book a call</a>.</p>
            </div>

            <div id="detail-wrap" style="display:none">
              <div class="cf-field">
                <label for="complaint-name">Your full name <span class="req">*</span></label>
                <input type="text" id="complaint-name" name="name" required placeholder="Your name">
              </div>
              <div class="cf-field">
                <label for="complaint-email">Email address <span class="req">*</span></label>
                <input type="email" id="complaint-email" name="email" required placeholder="you@example.com">
              </div>
              <div class="cf-field">
                <label for="complaint-ref">Matter reference <span style="font-size:0.72rem;font-weight:400;color:var(--light-mid);margin-left:6px">(optional)</span></label>
                <input type="text" id="complaint-ref" name="reference" placeholder="If known">
                <span class="cf-hint">Helps us locate your matter quickly. Leave blank if you do not have one.</span>
              </div>
              <div class="cf-field">
                <label for="complaint-detail">Brief description <span class="req">*</span></label>
                <textarea id="complaint-detail" name="detail" rows="5" required placeholder="Please describe your concern. You do not need to include the full details of your matter at this stage. Our mediator will contact you to discuss further."></textarea>
              </div>
              <div style="margin-top:24px;padding-top:20px;border-top:1px solid var(--dust-3)">
                <p style="font-size:0.78rem;font-weight:400;color:var(--light-mid);line-height:1.65;margin-bottom:16px">Your information will be handled confidentially. By submitting this form you confirm that the details provided are accurate to the best of your knowledge.</p>
                <button type="submit" class="btn-submit" id="complaints-submit">Submit complaint <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg></button>
              </div>
            </div>

          </form>
        </div>
      </div>

      <aside class="complaints-info">
        <div class="complaints-info-card">
          <h3>What is within scope</h3>
          <p>A complaint can be raised about the conduct of your practitioner. This includes:</p>
          <ul class="grounds-list">
            <li class="grounds-item"><div class="grounds-icon yes"><svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg></div>Breach of confidentiality</li>
            <li class="grounds-item"><div class="grounds-icon yes"><svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg></div>Failure to maintain impartiality</li>
            <li class="grounds-item"><div class="grounds-icon yes"><svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg></div>Safety concerns not appropriately managed</li>
            <li class="grounds-item"><div class="grounds-icon yes"><svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg></div>Unprofessional conduct during a session</li>
            <li class="grounds-item"><div class="grounds-icon yes"><svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg></div>Certificate not issued when process was completed</li>
          </ul>
        </div>
        <div class="complaints-info-card">
          <h3>What is not within scope</h3>
          <ul class="grounds-list">
            <li class="grounds-item"><div class="grounds-icon no"><svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg></div>Agreement was not reached</li>
            <li class="grounds-item"><div class="grounds-icon no"><svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg></div>Unhappiness with the outcome</li>
            <li class="grounds-item"><div class="grounds-icon no"><svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg></div>The other party's conduct</li>
            <li class="grounds-item"><div class="grounds-icon no"><svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg></div>The certificate type issued</li>
          </ul>
        </div>
        <div class="complaints-info-card">
          <h3>Our commitment</h3>
          <p>We will acknowledge every complaint within one business day and respond substantively within two business days.</p>
          <p>All complaints are handled confidentially within onlinefdr.com.au. Where a complaint cannot be resolved to your satisfaction internally, you can escalate the matter to our approved external complaints body, the Australian Mediation Association (AMA), at <a href="https://ama.asn.au/mediation-complaints/" style="color:var(--terra);text-decoration:none;font-weight:600">ama.asn.au/mediation-complaints</a>. The AMA handles complaints about accredited FDR practitioners independently of the practice.</p>
          <p><strong>Prefer to call?</strong> You can reach us on <a href="tel:0399617544" style="color:var(--terra);text-decoration:none;font-weight:600">(03) 9961 7544</a> during business hours.</p>
        </div>
      </aside>

    </div>
  </div>
"""

build_page(
    filename="complaints-v2.html",
    title="Complaints Process | onlinefdr.com.au",
    meta_desc="How to raise a concern about your FDR process. Complaints form, scope of complaints, and our commitment to responding within two business days.",
    canonical="/complaints/",
    current_page="/complaints/",
    schema_json='{"@context":"https://schema.org","@type":"WebPage","@id":"https://onlinefdr.com.au/complaints/#webpage","url":"https://onlinefdr.com.au/complaints/","name":"Complaints Process","description":"How to raise a concern about the conduct of your FDR practitioner. Includes the complaints form, what is and is not within scope, and the commitment to acknowledge complaints within one business day and respond substantively within two.","about":{"@id":"https://onlinefdr.com.au/#organization"}}',
    extra_css=COMPLAINTS_CSS,
    breadcrumbs=[("Home", "/"), ("Complaints", "/complaints/")],
    page_html=COMPLAINTS_HTML,
    robots="noindex, nofollow",
    show_marquee=False,
    extra_js=COMPLAINTS_JS,
)
print("Complaints done.")

# ─────────────────────────────────────────────
# PRIVACY POLICY
# ─────────────────────────────────────────────
LEGAL_CSS = """
.legal-header{background:var(--charcoal);padding:120px 0 64px;position:relative;overflow:hidden}
.legal-header::before{content:'';position:absolute;inset:0;background:radial-gradient(ellipse 50% 60% at 80% 30%,rgba(196,135,58,0.07) 0%,transparent 60%);pointer-events:none}
.legal-header-inner{position:relative;z-index:1;max-width:680px}
.legal-header h1{font-size:clamp(2.4rem,5vw,4rem);font-weight:800;line-height:1.0;letter-spacing:-0.03em;color:var(--white);margin-bottom:16px}
.legal-header-meta{font-size:0.78rem;font-weight:500;color:rgba(253,250,246,0.3);margin-top:16px}

.legal-wrap{padding:72px 0 100px}
.legal-grid{display:grid;grid-template-columns:200px 1fr;gap:64px;align-items:start}
.legal-toc{position:sticky;top:92px}
.legal-toc-label{font-size:0.62rem;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;color:var(--light-mid);margin-bottom:14px;display:block}
.legal-toc ul{list-style:none;display:flex;flex-direction:column;gap:2px}
.legal-toc ul li a{display:block;font-size:0.78rem;font-weight:500;color:var(--mid);text-decoration:none;padding:6px 10px;border-radius:5px;transition:all 0.2s;line-height:1.4}
.legal-toc ul li a:hover{color:var(--charcoal);background:var(--dust-2)}

.legal-body{max-width:720px}
.legal-body h2{font-size:1.25rem;font-weight:800;color:var(--charcoal);letter-spacing:-0.02em;margin:48px 0 14px;padding-top:16px;border-top:1px solid var(--dust-3)}
.legal-body h2:first-child{margin-top:0;padding-top:0;border-top:none}
.legal-body h3{font-size:0.95rem;font-weight:700;color:var(--charcoal);margin:24px 0 8px}
.legal-body p{font-size:0.92rem;font-weight:400;color:var(--mid);line-height:1.85;margin-bottom:14px}
.legal-body p:last-child{margin-bottom:0}
.legal-body p strong{font-weight:700;color:var(--charcoal)}
.legal-body a{color:var(--terra);font-weight:600;text-decoration:none;border-bottom:1px solid rgba(168,92,50,0.3);transition:border-color 0.2s}
.legal-body a:hover{border-color:var(--terra)}
.legal-body ul{list-style:none;display:flex;flex-direction:column;gap:8px;margin:12px 0 14px}
.legal-body ul li{display:flex;align-items:flex-start;gap:10px;font-size:0.9rem;font-weight:400;color:var(--mid);line-height:1.65}
.legal-body ul li::before{content:'';width:6px;height:6px;border-radius:50%;background:var(--ochre);flex-shrink:0;margin-top:8px}
.legal-body .notice{margin:20px 0}

@media(max-width:960px){
  .legal-grid{grid-template-columns:1fr}
  .legal-toc{display:none}
}
"""

PRIVACY_HTML = """
  <header class="legal-header page-fold" aria-labelledby="privacy-heading">
    <div class="wrap">
      <div class="legal-header-inner">
        <span class="page-label" style="color:var(--ochre-lt)">Legal</span>
        <h1 id="privacy-heading">Privacy Policy</h1>
        <p class="legal-header-meta">Last updated: May 2026 &bull; Effective: May 2026</p>
      </div>
    </div>
  </header>

  <!-- ABOVE-FOLD MARQUEE -->
  <div class="marquee-bar" aria-label="Accreditation and credentials" role="marquee">
    <div class="marquee-track" aria-hidden="true">
      <span class="marquee-item">AGD-Accredited FDRP <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Australian Mediation Association Member <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Section 60I Certificates (s 66H in WA) <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Conducted Securely Online <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Available Anywhere in Australia <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Free Discovery Call <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">No Obligation <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Confidential under the Family Law Act <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Both Parenting and Financial Matters <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">AGD-Accredited FDRP <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Australian Mediation Association Member <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Section 60I Certificates (s 66H in WA) <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Conducted Securely Online <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Available Anywhere in Australia <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Free Discovery Call <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">No Obligation <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Confidential under the Family Law Act <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Both Parenting and Financial Matters <span class="marquee-sep">&bull;</span></span>
    </div>
  </div>


  <div class="wrap legal-wrap">
    <div class="legal-grid">
      <nav class="legal-toc" aria-label="Privacy policy sections">
        <span class="legal-toc-label">Contents</span>
        <ul>
          <li><a href="#who-we-are">Who we are</a></li>
          <li><a href="#what-we-collect">What we collect</a></li>
          <li><a href="#how-we-use">How we use it</a></li>
          <li><a href="#fdr-confidentiality">FDR confidentiality</a></li>
          <li><a href="#disclosure">Disclosure</a></li>
          <li><a href="#storage">Storage and security</a></li>
          <li><a href="#overseas">Overseas data storage</a></li>
          <li><a href="#recording">Recording and AI notes</a></li>
          <li><a href="#third-parties">Third-party services</a></li>
          <li><a href="#your-rights">Your rights</a></li>
          <li><a href="#cookies">Cookies</a></li>
          <li><a href="#contact">Contact us</a></li>
          <li><a href="#changelog">Change log</a></li>
        </ul>
      </nav>

      <article class="legal-body">

        <div class="notice notice-amber">
          <p class="notice-label">Plain language summary</p>
          <p>We collect only what we need to conduct your FDR process. We do not sell your information. We do not share it with third parties except where required to operate the service or where the law compels us. Everything said in your FDR sessions is legally confidential and governed by the Family Law Act, not just this policy.</p>
        </div>

        <h2 id="who-we-are">Who we are</h2>
        <p>onlinefdr.com.au is an accredited online Family Dispute Resolution practice registered with the Australian Government Attorney-General's Department. We operate under the Family Law Act 1975 (Cth) and the Australian Privacy Act 1988 (Cth).</p>
        <p>References to "we", "us", and "our" in this policy refer to the practice operating under the onlinefdr.com.au brand. References to "you" refer to any person who contacts us, uses our website, or participates in our FDR services.</p>
        <p><strong>Contact:</strong> <a href="mailto:hello@onlinefdr.com.au">hello@onlinefdr.com.au</a> &bull; <a href="tel:0399617544">(03) 9961 7544</a></p>

        <h2 id="what-we-collect">What information we collect</h2>
        <h3>When you contact us or book a call</h3>
        <ul>
          <li>Your name and contact details (email address, phone number)</li>
          <li>Brief information about your matter that you choose to share</li>
          <li>Booking information via Google Appointment Scheduling</li>
        </ul>

        <h3>During the FDR process</h3>
        <ul>
          <li>Information provided during intake sessions and joint sessions</li>
          <li>Documents shared as part of financial disclosure</li>
          <li>Notes made by the practitioner in the course of the process</li>
          <li>Your AGD registration details if you apply to join our practitioner network</li>
        </ul>

        <h3>When you use our website</h3>
        <ul>
          <li>Standard web server logs (IP address, browser type, pages visited)</li>
          <li>Information submitted through website forms (contact, complaints, practitioner applications)</li>
          <li>Cookie data as described in the Cookies section below</li>
        </ul>

        <h2 id="how-we-use">How we use your information</h2>
        <p>We use personal information only for the purposes for which it was collected:</p>
        <ul>
          <li>To conduct your FDR process, including intake, joint sessions, and issuing certificates or documenting agreements</li>
          <li>To communicate with you about your matter, appointments, and next steps</li>
          <li>To manage bookings via Google Appointment Scheduling</li>
          <li>To respond to enquiries, complaints, and practitioner applications</li>
          <li>To meet our obligations as an AGD-registered FDRP, including record-keeping requirements</li>
          <li>To improve our services and website</li>
        </ul>
        <p>We do not use your personal information for marketing purposes without your explicit consent. We do not sell, rent, or trade your information to third parties.</p>

        <h2 id="fdr-confidentiality">FDR confidentiality, inadmissibility, and the Family Law Act</h2>
        <p>Information disclosed during FDR sessions is subject to two distinct and separate legal protections under the Family Law Act 1975 (Cth), which operate alongside this Privacy Policy and prevail to the extent of any inconsistency.</p>
        <p><strong>Confidentiality (s10H):</strong> The practitioner is statutorily prohibited from disclosing communications made in the course of the FDR process, with limited exceptions. Parties agree contractually under our terms to maintain the same confidentiality. The practitioner cannot be compelled to give evidence about what was said in sessions.</p>
        <p><strong>Inadmissibility (s10J):</strong> Even if confidentiality is breached and something from FDR is disclosed, that information cannot be admitted as evidence in court proceedings. This is a separate and additional protection that operates independently of confidentiality. A breach of confidentiality does not give the other party a litigation advantage.</p>
        <p>Together these protections allow both parties to participate and negotiate in FDR candidly, without fear that what they say will be used against them in subsequent proceedings.</p>
        <p>The narrow exceptions where disclosure may be required include:</p>
        <ul>
          <li>Where a disclosure indicates a risk of harm to a child or another person</li>
          <li>Where a court order compels disclosure in defined circumstances</li>
          <li>Where both parties consent to disclosure</li>
        </ul>
        <p>These exceptions are defined by the Family Law Act and are not a matter of our discretion.</p>

        <h2 id="disclosure">When we disclose information</h2>
        <p>We do not disclose your personal information to third parties except in the following circumstances:</p>
        <ul>
          <li><strong>Service providers:</strong> We use Google Workspace and Google Appointment Scheduling for communications and bookings, and Stripe for payment processing. These providers process data on our behalf and are bound by their own privacy policies.</li>
          <li><strong>Legal obligations:</strong> Where we are required by law to disclose information, including under the Family Law Act exceptions described above.</li>
          <li><strong>AGD compliance:</strong> Where required to comply with our obligations as an AGD-registered FDRP, including any regulatory requirements relating to our registration.</li>
          <li><strong>Safety:</strong> Where we have reasonable grounds to believe disclosure is necessary to prevent a serious threat to the life, health, or safety of any person.</li>
        </ul>
        <p>We will not disclose your information to any other party without your explicit written consent.</p>

        <h2 id="storage">Storage and security</h2>
        <p>Your information is stored on secure systems. We take reasonable steps to protect personal information from misuse, interference, loss, and unauthorised access. Our communications infrastructure is operated through Google Workspace, which provides enterprise-grade security.</p>
        <p><strong>Retention.</strong> We retain personal information for as long as necessary to fulfil the purposes for which it was collected, and for as long as required by law. As an AGD-registered FDR practitioner, we are required to retain FDR records for a minimum period under the Family Law (Family Dispute Resolution Practitioners) Regulations 2025. Where the regulations require a longer retention period than would otherwise apply, the longer period prevails.</p>
        <p>When personal information is no longer required and is no longer subject to a retention obligation, it is securely deleted or de-identified.</p>

        <h2 id="overseas">Overseas data storage</h2>
        <p>Some of the third-party services we use are operated from outside Australia, or may transfer data outside Australia for the purposes of backup, replication, or processing. This disclosure is provided to meet our obligations under Australian Privacy Principle 8 (cross-border disclosure of personal information).</p>
        <ul>
          <li><strong>Google Workspace and Google Appointment Scheduling:</strong> Primary storage region is Australia. Data may be transferred to the United States or other Google regions for backup, replication, or platform operation.</li>
          <li><strong>Google Gemini:</strong> Processing of intake recordings and transcripts may occur on Google infrastructure located outside Australia.</li>
          <li><strong>Stripe:</strong> United States-based payment processor. Stripe complies with applicable cross-border data protection frameworks.</li>
          <li><strong>Netlify:</strong> United States-based website hosting provider.</li>
        </ul>
        <p>We take reasonable steps to ensure that any overseas recipients of personal information do not breach the Australian Privacy Principles in relation to your information. By using our services, you consent to the cross-border disclosures described above.</p>

        <h2 id="recording">Recording and AI-assisted note-taking</h2>
        <p>Intake sessions are recorded and processed by an AI assistant for the practitioner's note-taking purposes. Joint mediation sessions are not recorded.</p>
        <ul>
          <li><strong>Intake sessions only.</strong> Each party's individual intake session (held separately, with each party privately, before any joint session) is audio-recorded with the assistance of Google Gemini, which transcribes and annotates the session for the practitioner's professional notes. This is part of your practitioner's record-keeping and supports the quality and accuracy of the FDR process. Joint sessions, where both parties are present, are not recorded.</li>
          <li><strong>Express consent required.</strong> Before any intake session begins, your practitioner will ask for your express consent to record. You may refuse, in which case the practitioner will take handwritten or typed notes only. Refusing to be recorded does not affect your ability to participate in FDR.</li>
          <li><strong>Access.</strong> Recordings and AI-generated transcripts are accessible only to your practitioner. They are stored within Google Workspace under the practitioner's account and are subject to the same security and retention rules as other client records.</li>
          <li><strong>Confidentiality.</strong> Recordings and transcripts are covered by the same statutory confidentiality and inadmissibility protections as the rest of the FDR process under sections 10H and 10J of the Family Law Act 1975 (Cth).</li>
          <li><strong>No training use.</strong> We do not consent to recordings or transcripts being used by Google or any third party to train AI models. Google Workspace business accounts do not, by default, use customer content for model training.</li>
          <li><strong>Retention.</strong> Recordings and transcripts are retained in accordance with our standard retention rules described in the Storage and security section above.</li>
        </ul>

        <h2 id="third-parties">Third-party services we use</h2>
        <ul>
          <li><strong>Google Appointment Scheduling:</strong> Booking and scheduling. See Google's Privacy Policy at policies.google.com.</li>
          <li><strong>Google Workspace:</strong> Email, calendar, and document storage. See Google's Privacy Policy at google.com/privacy.</li>
          <li><strong>Google Meet:</strong> Video conferencing for sessions. Subject to Google's Privacy Policy.</li>
          <li><strong>Google Gemini:</strong> AI-assisted transcription and annotation of intake sessions only (with your express consent). Subject to Google's Privacy Policy.</li>
          <li><strong>Stripe:</strong> Payment processing, including Buy Now Pay Later providers (Afterpay, Klarna, Affirm, Zip). See Stripe's Privacy Policy at stripe.com/privacy.</li>
          <li><strong>Netlify:</strong> Website hosting and form submissions. See Netlify's Privacy Policy at netlify.com.</li>
          <li><strong>Dialpad:</strong> Phone service for our business landline. See Dialpad's Privacy Policy at dialpad.com.</li>
        </ul>
        <p>We have selected these services carefully. We do not use advertising platforms, tracking pixels, or third-party analytics services that profile users for commercial purposes.</p>

        <h2 id="your-rights">Your rights</h2>
        <p>Under the Australian Privacy Act 1988 (Cth), you have the right to:</p>
        <ul>
          <li>Request access to the personal information we hold about you</li>
          <li>Request correction of personal information that is inaccurate, incomplete, or out of date</li>
          <li>Make a complaint about how we have handled your personal information</li>
        </ul>
        <p>To make an access or correction request, contact us at <a href="mailto:hello@onlinefdr.com.au">hello@onlinefdr.com.au</a>. We will respond within 30 days.</p>
        <p>If you are not satisfied with our response, you may make a complaint to the Office of the Australian Information Commissioner (OAIC) at <a href="https://www.oaic.gov.au" target="_blank" rel="noopener noreferrer">oaic.gov.au</a>.</p>

        <div class="notice notice-amber">
          <p class="notice-label">Note on FDR records</p>
          <p>Access to records of FDR sessions is subject to the confidentiality provisions of the Family Law Act, which may limit what we can provide in response to an access request. We will advise you of any applicable limitations when responding to your request.</p>
        </div>

        <h2 id="cookies">Cookies</h2>
        <p>Our website uses minimal cookies. We do not use advertising cookies or third-party tracking cookies. The cookies we use are limited to:</p>
        <ul>
          <li><strong>Session cookies:</strong> Temporary cookies that expire when you close your browser, used to maintain basic website functionality.</li>
          <li><strong>Google Appointment Scheduling:</strong> If you use our booking system, Google may set cookies as part of their booking functionality.</li>
        </ul>
        <p>You can control cookies through your browser settings. Disabling cookies may affect the functionality of our booking system.</p>

        <h2 id="contact">Contact and complaints</h2>
        <p>For privacy enquiries or to exercise your rights, contact us:</p>
        <ul>
          <li>Email: <a href="mailto:hello@onlinefdr.com.au">hello@onlinefdr.com.au</a></li>
          <li>Phone: <a href="tel:0399617544">(03) 9961 7544</a></li>
        </ul>
        <p>If you have a complaint about our handling of your personal information, please contact us in the first instance. If we are unable to resolve your complaint, you may refer it to the Office of the Australian Information Commissioner at <a href="https://www.oaic.gov.au" target="_blank" rel="noopener noreferrer">oaic.gov.au</a>.</p>
        <p>This policy was last updated in May 2026. We may update it from time to time. The current version will always be available at this address.</p>

        <h2 id="changelog">Change log</h2>
        <p>Substantive changes to this Privacy Policy are recorded here. Minor formatting or typographical corrections may be made without entry.</p>
        <ul class="changelog-list">
          <li><strong>May 2026 &mdash; Initial version.</strong> Privacy Policy published at launch.</li>
        </ul>

      </article>
    </div>
  </div>
"""

build_page(
    filename="privacy-v2.html",
    title="Privacy Policy | onlinefdr.com.au",
    meta_desc="Privacy policy for onlinefdr.com.au. How we collect, use, store, and protect your personal information, and the confidentiality protections that apply to FDR sessions.",
    canonical="/privacy/",
    current_page="/privacy/",
    schema_json='{"@context":"https://schema.org","@type":"WebPage","@id":"https://onlinefdr.com.au/privacy/#webpage","url":"https://onlinefdr.com.au/privacy/","name":"Privacy Policy","description":"Privacy policy explaining how onlinefdr.com.au collects, uses, stores, and protects your personal information. Includes FDR confidentiality and inadmissibility under the Family Law Act, overseas data storage disclosure under Australian Privacy Principle 8, intake recording and AI-assisted notes, retention obligations under the FDR Practitioner Regulations 2025, and your rights under the Australian Privacy Act 1988.","about":{"@id":"https://onlinefdr.com.au/#organization"}}',
    extra_css=LEGAL_CSS,
    breadcrumbs=[("Home", "/"), ("Privacy Policy", "/privacy/")],
    page_html=PRIVACY_HTML,
    robots="noindex, nofollow",
    show_marquee=False,
)
print("Privacy done.")

# ─────────────────────────────────────────────
# TERMS OF SERVICE
# ─────────────────────────────────────────────
TERMS_HTML = """
  <header class="legal-header page-fold" aria-labelledby="terms-heading">
    <div class="wrap">
      <div class="legal-header-inner">
        <span class="page-label" style="color:var(--ochre-lt)">Legal</span>
        <h1 id="terms-heading">Terms of Service</h1>
        <p class="legal-header-meta">Last updated: May 2026 &bull; Effective: May 2026</p>
      </div>
    </div>
  </header>

  <!-- ABOVE-FOLD MARQUEE -->
  <div class="marquee-bar" aria-label="Accreditation and credentials" role="marquee">
    <div class="marquee-track" aria-hidden="true">
      <span class="marquee-item">AGD-Accredited FDRP <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Australian Mediation Association Member <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Section 60I Certificates (s 66H in WA) <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Conducted Securely Online <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Available Anywhere in Australia <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Free Discovery Call <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">No Obligation <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Confidential under the Family Law Act <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Both Parenting and Financial Matters <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">AGD-Accredited FDRP <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Australian Mediation Association Member <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Section 60I Certificates (s 66H in WA) <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Conducted Securely Online <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Available Anywhere in Australia <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Free Discovery Call <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">No Obligation <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Confidential under the Family Law Act <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Both Parenting and Financial Matters <span class="marquee-sep">&bull;</span></span>
    </div>
  </div>


  <div class="wrap legal-wrap">
    <div class="legal-grid">
      <nav class="legal-toc" aria-label="Terms sections">
        <span class="legal-toc-label">Contents</span>
        <ul>
          <li><a href="#about">About these terms</a></li>
          <li><a href="#services">Our services</a></li>
          <li><a href="#eligibility">Eligibility</a></li>
          <li><a href="#bookings">Bookings and sessions</a></li>
          <li><a href="#fees">Fees and payment</a></li>
          <li><a href="#cancellation">Cancellation</a></li>
          <li><a href="#confidentiality">Confidentiality</a></li>
          <li><a href="#not-legal-advice">Not legal advice</a></li>
          <li><a href="#conduct">Conduct in sessions</a></li>
          <li><a href="#conflicts">Conflicts of interest</a></li>
          <li><a href="#withdrawal">Practitioner withdrawal</a></li>
          <li><a href="#liability">Limitation of liability</a></li>
          <li><a href="#website">Website use</a></li>
          <li><a href="#governing-law">Governing law</a></li>
          <li><a href="#contact">Contact</a></li>
          <li><a href="#changelog">Change log</a></li>
        </ul>
      </nav>

      <article class="legal-body">

        <div class="notice notice-amber">
          <p class="notice-label">Plain language summary</p>
          <p>These terms govern how we work with you. The important points: FDR is confidential, we are not your lawyers, both parties must participate genuinely, payment must be received at least 24 hours before each session or the session is automatically cancelled, and three non-payment cancellations terminates the engagement.</p>
        </div>

        <h2 id="about">About these terms</h2>
        <p>These Terms of Service govern your use of the onlinefdr.com.au website and your engagement with our Family Dispute Resolution services. By booking a session, submitting an enquiry, or using our website, you agree to these terms.</p>
        <p>These terms should be read together with our <a href="/privacy/">Privacy Policy</a>. If you have any questions before booking, contact us at <a href="mailto:hello@onlinefdr.com.au">hello@onlinefdr.com.au</a> or <a href="tel:0399617544">(03) 9961 7544</a>.</p>

        <h2 id="services">Our services</h2>
        <p>onlinefdr.com.au provides accredited Family Dispute Resolution services conducted online via Google Meet. Our services include:</p>
        <ul>
          <li>Free discovery calls to assess whether FDR is appropriate for your circumstances</li>
          <li>Individual intake sessions (one hour per party)</li>
          <li>Joint mediation sessions (four hours for parenting matters, three hours for financial matters)</li>
          <li>Documentation of agreed terms</li>
          <li>Section 60I certificates where appropriate</li>
        </ul>
        <p>Practitioners working under the onlinefdr.com.au brand hold current registration with the Australian Government Attorney-General's Department as accredited Family Dispute Resolution Practitioners.</p>
        <p><strong>No outcome is guaranteed.</strong> FDR is a process for assisting parties to reach their own agreements. We do not guarantee that agreement will be reached, that a particular outcome will be achieved, or that any agreement reached will be honoured by the other party.</p>
        <p><strong>Section 60I certificates and Letters of Attendance.</strong> For parenting matters, Section 60I certificates are issued at the practitioner's professional discretion in accordance with section 60I(8) of the Family Law Act 1975 and Regulation 24 of the Family Law (Family Dispute Resolution Practitioners) Regulations 2025. The type of certificate (i.e. which paragraph of section 60I(8) applies) is determined by the practitioner's assessment of what occurred in the FDR process, including whether each party made a genuine effort and whether FDR was appropriate in the circumstances. The certificate type is not negotiable; parties cannot request a particular type. For financial matters, the practitioner issues a Letter of Attendance and Genuine Effort confirming the dates of attendance, the practitioner's assessment of whether each party made a genuine effort, and the outcome. The letter is supporting evidence the party can use in their own Genuine Steps Certificate, which is the certificate the party themselves signs and files under Schedule 1 of the Federal Circuit and Family Court of Australia (Family Law) Rules 2021.</p>

        <h2 id="eligibility">Eligibility and suitability</h2>
        <p>FDR is not appropriate in all circumstances. As part of the intake process, we assess whether the matter is suitable for FDR. We reserve the right to decline to provide services, or to cease providing services, where we determine that FDR is not appropriate for the matter. This includes where:</p>
        <ul>
          <li>There are safety concerns for either party or any children involved</li>
          <li>A significant power imbalance exists that cannot be adequately managed in the process</li>
          <li>One party is unable to participate genuinely due to incapacity</li>
          <li>The matter requires urgent court intervention</li>
        </ul>
        <p>Where we determine FDR is not appropriate, we will advise you and, where possible, point you toward appropriate alternatives.</p>

        <h2 id="bookings">Bookings and sessions</h2>
        <p>Sessions are booked through our online booking system (Google Appointment Scheduling). By making a booking, you confirm that you have read and agree to these terms.</p>
        <p><strong>Discovery calls</strong> are free and non-binding. They do not constitute the commencement of a formal FDR process.</p>
        <p><strong>Intake sessions</strong> are conducted individually with each party. Both parties must complete an intake session before a joint session can be scheduled. The intake session is a required step in the FDR process and is not optional.</p>
        <p><strong>Joint sessions</strong> run for four hours for parenting matters and three hours for financial matters. Both parties must be available for the full duration. Arriving significantly late to a session may result in the session being rescheduled at the party's cost.</p>
        <p>Sessions are conducted via Google Meet. Both parties are responsible for ensuring they have a suitable device, reliable internet connection, and a private space for the duration of the session.</p>

        <h2 id="fees">Fees and payment</h2>
        <p>Our fees are confirmed at the time of booking. We do not publish fees on our website. Fees are discussed and confirmed during the discovery call and are fixed for the duration of your matter unless otherwise agreed in writing.</p>
        <p>The discovery call is provided at no charge. Intake sessions and joint sessions are charged at the rates confirmed at the time of booking.</p>
        <p>Where a matter requires additional sessions beyond those initially anticipated, each additional session is charged at the same rate as the initial sessions unless otherwise agreed.</p>
        <p><strong>Strict prepayment.</strong> Payment must be received at least 24 hours before the scheduled session, or the session is automatically cancelled. This applies to all intake and joint sessions.</p>
        <p><strong>Three-cancellation rule.</strong> Three non-payment cancellations of scheduled sessions terminates the engagement. The three-cancellation rule applies to the party causing the cancellations only. Where the engagement is terminated under this clause, any prepaid fees for sessions not yet held are refunded in full to the paying party. Where a party's repeated non-payment results in the matter not being able to proceed, a Section 60I certificate may be issued reflecting that the party did not make a genuine effort to resolve the dispute, in accordance with section 60I(8) of the Family Law Act.</p>

        <h2 id="cancellation">Cancellation and rescheduling</h2>
        <p><strong>Rescheduling before payment is due.</strong> If you need to reschedule a session, do so before the 24-hour prepayment deadline. Once payment has been made for a session, rescheduling is at the practitioner's discretion and subject to availability.</p>
        <p><strong>Non-attendance.</strong> Where a party does not attend a paid scheduled session without notice, the full session fee is forfeited. A Section 60I certificate reflecting non-attendance may be issued.</p>
        <p><strong>Practitioner cancellation.</strong> In the unlikely event that we need to cancel a session, we will provide as much notice as possible and reschedule at no additional cost to either party. Where rescheduling is not possible, fees paid for the cancelled session will be refunded.</p>

        <h2 id="confidentiality">Confidentiality and inadmissibility</h2>
        <p>FDR sessions are protected by two distinct legal provisions under the Family Law Act 1975 (Cth):</p>
        <ul>
          <li><strong>Confidentiality (s10H):</strong> The practitioner is statutorily prohibited from disclosing communications made during the FDR process, with limited exceptions. By agreeing to these Terms, both parties agree contractually to maintain the same confidentiality. The practitioner cannot be compelled to give evidence about what was said in sessions.</li>
          <li><strong>Inadmissibility (s10J):</strong> Even if confidentiality is breached and something from FDR is disclosed, that information cannot be admitted as evidence in court proceedings. This protection operates independently of confidentiality and cannot be waived by a breach of it.</li>
        </ul>
        <p>By participating in FDR, both parties agree to maintain confidentiality of the process and its content. Narrow exceptions apply as defined by the Family Law Act, including where disclosure is necessary to prevent harm to a child or another person.</p>
        <p>Session notes made by the practitioner are their professional records and are not provided to either party unless required by law.</p>

        <h2 id="not-legal-advice">We are not your lawyers</h2>
        <p>onlinefdr.com.au provides Family Dispute Resolution services only. The practitioner acts as a neutral facilitator. We do not provide legal advice or legal representation, and engaging us does not create a solicitor-client relationship.</p>
        <p>Specifically, the practitioner does not:</p>
        <ul>
          <li>Provide legal advice on your rights, obligations, or the merits of your matter</li>
          <li>Draft, file, or prepare legal documents on your behalf</li>
          <li>Appear in court or in any legal proceedings on your behalf</li>
          <li>Negotiate on a party's behalf, including with the other party, their lawyer, or any third party</li>
        </ul>
        <p>Any documents produced during the FDR process (for example, a Parenting Plan or a record of issues discussed) are not legal advice and are not legally binding unless they are subsequently formalised through the appropriate legal process by you and the other party with your own independent advisors.</p>
        <p>We strongly encourage both parties to obtain independent legal advice before, during, and after the FDR process, and before signing any agreement. Understanding your legal rights and obligations is essential to making informed decisions. The content on our website is provided for general information only and is not a substitute for legal advice in your specific circumstances.</p>
        <p>If you need legal advice, contact a family lawyer or Legal Aid in your state or territory.</p>

        <h2 id="conduct">Conduct during sessions</h2>
        <p>Both parties are expected to participate in sessions in good faith and to treat the practitioner and each other with respect. The practitioner may terminate a session, and may withdraw from the engagement under the section below on <a href="#withdrawal">practitioner withdrawal</a>, where:</p>
        <ul>
          <li>A party's conduct makes it impossible to continue the session productively</li>
          <li>A party makes threats or engages in abusive behaviour toward the practitioner or the other party</li>
          <li>Continuing the session would pose a risk to the safety of any person</li>
        </ul>
        <p>Where a session is terminated due to a party's conduct, the full session fee remains payable by that party. A Section 60I certificate may be issued reflecting the circumstances of the termination.</p>
        <p><strong>Recording by parties.</strong> Sessions may not be recorded by either party without the prior written consent of the practitioner and the other party.</p>
        <p><strong>Recording by the practitioner.</strong> Intake sessions are audio-recorded by the practitioner with AI-assisted transcription for note-taking purposes. Joint sessions are not recorded. Each party's express consent will be sought before any intake recording begins, and refusal is accepted without prejudice to the engagement. Full details are in our <a href="/privacy/#recording">Privacy Policy</a>.</p>

        <h2 id="conflicts">Conflicts of interest</h2>
        <p>The practitioner is required to act as a neutral and impartial facilitator. A conflict of interest arises where the practitioner has any relationship, interest, or association that could reasonably be perceived to affect their impartiality. This includes:</p>
        <ul>
          <li>A prior professional relationship with a party (for example, having previously provided services to one of the parties)</li>
          <li>Personal connections to a party (family, friendship, or other relationships of a personal nature)</li>
          <li>Close associates with a stake in the outcome of the matter</li>
          <li>Any other matter where the practitioner's professional judgement could reasonably be impaired</li>
        </ul>
        <p>Where a conflict of interest is identified, the practitioner will disclose the conflict to all parties, withdraw from the matter, refund any fees paid for sessions not yet held, and where practical refer the parties to another accredited FDR practitioner.</p>

        <h2 id="withdrawal">Practitioner withdrawal</h2>
        <p>The practitioner reserves the right to withdraw from an engagement at their professional discretion. Reasons for withdrawal include:</p>
        <ul>
          <li>Bad faith or dishonesty by a party, including non-disclosure of material information</li>
          <li>Safety concerns relating to a party, a child, or the practitioner</li>
          <li>Practitioner incapacity</li>
          <li>A conflict of interest identified after the engagement has commenced</li>
          <li>Any other matter where continuing the engagement would breach the practitioner's professional or statutory obligations</li>
        </ul>
        <p>Where the practitioner withdraws, fees paid for sessions not yet held will be refunded. Where appropriate, a Section 60I certificate will be issued reflecting the circumstances (for example, a certificate that a party did not make a genuine effort to resolve the dispute, or that FDR was not appropriate in the circumstances).</p>

        <h2 id="liability">Limitation of liability</h2>
        <p>We carry professional indemnity insurance appropriate to our practice, as required of all accredited Family Dispute Resolution Practitioners.</p>
        <p>To the extent permitted by law, our liability to you in connection with our services is limited to the fees paid for the session or sessions to which the claim relates.</p>
        <p>We are not liable for any indirect, consequential, or special loss arising from your participation in FDR, including any loss arising from an outcome you are unhappy with, a breakdown in negotiations, or any decision made by either party in the course of or following the FDR process.</p>
        <p>Nothing in these terms excludes, restricts, or modifies any right or guarantee you may have under Australian Consumer Law that cannot be excluded, restricted, or modified.</p>

        <h2 id="website">Website use</h2>
        <p>The content on onlinefdr.com.au is provided for general information purposes. While we take care to keep it accurate and current, we make no warranty as to its completeness or accuracy. The law changes, and content may not always reflect the most recent legal developments.</p>
        <p>You must not use our website in any way that breaches any applicable law, infringes the rights of any person, or interferes with the operation of the site.</p>

        <h2 id="governing-law">Governing law</h2>
        <p>These terms are governed by the laws of Victoria, Australia. Any disputes arising from these terms or your use of our services are subject to the exclusive jurisdiction of the courts of Victoria, except where the Family Law Act 1975 (Cth) or another Commonwealth law provides otherwise.</p>

        <h2 id="contact">Contact</h2>
        <p>Questions about these terms can be directed to:</p>
        <ul>
          <li>Email: <a href="mailto:hello@onlinefdr.com.au">hello@onlinefdr.com.au</a></li>
          <li>Phone: <a href="tel:0399617544">(03) 9961 7544</a></li>
        </ul>
        <p>These terms were last updated in May 2026. We may update them from time to time. Continued use of our services following any update constitutes acceptance of the revised terms. The current version will always be available at this address.</p>

        <h2 id="changelog">Change log</h2>
        <p>Substantive changes to these Terms of Service are recorded here. Minor formatting or typographical corrections may be made without entry.</p>
        <ul class="changelog-list">
          <li><strong>May 2026 &mdash; Initial version.</strong> Terms of Service published at launch.</li>
        </ul>

      </article>
    </div>
  </div>
"""

build_page(
    filename="terms-v2.html",
    title="Terms of Service | onlinefdr.com.au",
    meta_desc="Terms of service for onlinefdr.com.au. Bookings, fees, cancellation policy, confidentiality, conduct in sessions, and limitation of liability.",
    canonical="/terms/",
    current_page="/terms/",
    schema_json='{"@context":"https://schema.org","@type":"WebPage","@id":"https://onlinefdr.com.au/terms/#webpage","url":"https://onlinefdr.com.au/terms/","name":"Terms of Service","description":"Terms governing engagement with onlinefdr.com.au Family Dispute Resolution services. Bookings, fees, prepayment, cancellation, confidentiality under the Family Law Act, conduct in sessions, conflicts of interest, and limitation of liability.","about":{"@id":"https://onlinefdr.com.au/#organization"}}',
    extra_css=LEGAL_CSS,
    breadcrumbs=[("Home", "/"), ("Terms of Service", "/terms/")],
    page_html=TERMS_HTML,
    robots="noindex, nofollow",
    show_marquee=False,
)
print("Terms done.")

# ─────────────────────────────────────────────
# BOOK
# ─────────────────────────────────────────────
BOOK_CSS = """
.book-header{background:var(--charcoal);padding:96px 0 64px;position:relative;overflow:hidden}
.book-header::before{content:'';position:absolute;inset:0;background:radial-gradient(ellipse 60% 50% at 75% 30%,rgba(196,135,58,0.08) 0%,transparent 60%);pointer-events:none}
.book-fold-grid{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:start;position:relative;z-index:1;width:100%;min-height:0}
.book-fold-grid .book-header-inner{max-width:none}
.book-fold-image-panel{position:relative;align-self:stretch;opacity:0;animation:fadeUp 0.9s var(--ease) 0.4s forwards}
.book-fold-image-panel > .book-fold-img-real{position:absolute;inset:0;width:100%;height:100%}
.book-fold-image-panel img{width:100%;height:100%;object-fit:cover;object-position:center 50%;border-radius:8px}
.book-header-inner{position:relative;z-index:1;max-width:780px}
.book-header .page-label{color:var(--ochre-lt)}
.book-header h1{font-size:clamp(2.4rem,5vw,4.4rem);font-weight:800;line-height:1.05;letter-spacing:-0.025em;color:var(--white);margin:24px 0 24px}
.book-header h1 .accent{color:var(--ochre)}
.book-header .page-intro{font-size:1.05rem;font-weight:400;color:rgba(253,250,246,0.7);line-height:1.75;max-width:680px}

.book-wrap{padding:64px 0 96px}
.book-intro{max-width:820px;margin:0 auto 48px;font-size:1rem;line-height:1.8;color:var(--charcoal-2)}
.book-intro p{margin:0 0 16px}
.book-intro p:last-child{margin-bottom:0}

.book-cards{display:flex;flex-direction:column;gap:24px;margin-bottom:64px}
.book-card{background:var(--white);border:1px solid var(--dust-2);border-radius:8px;padding:36px 36px;position:relative}
.book-card-head{display:flex;flex-direction:column;gap:8px;margin-bottom:18px}
.book-card-step{font-size:0.66rem;font-weight:700;letter-spacing:0.2em;text-transform:uppercase;color:var(--mid)}
.book-card.discovery .book-card-step{color:var(--terra)}
.book-card.intake .book-card-step{color:var(--ochre)}
.book-card.joint .book-card-step{color:var(--charcoal-2)}
.book-card h2{font-size:1.55rem;font-weight:700;line-height:1.2;letter-spacing:-0.015em;color:var(--charcoal);margin:0}
.book-card-meta{display:flex;flex-wrap:wrap;gap:18px 24px;font-size:0.85rem;color:var(--mid);font-weight:500;margin-bottom:18px}
.book-card-meta span{display:inline-flex;align-items:center;gap:6px}
.book-card-meta svg{flex-shrink:0;color:var(--mid)}
.book-card p{font-size:0.98rem;line-height:1.75;color:var(--charcoal-2);margin:0 0 14px}
.book-card p:last-of-type{margin-bottom:0}
.book-card-emph{background:var(--dust);padding:14px 18px;border-radius:4px;border-left:3px solid var(--ochre);margin:18px 0}
.book-card-emph p{margin:0;font-size:0.94rem;line-height:1.65}
.book-card-cta{margin-top:24px}
.book-card-cta .btn-cta{display:inline-flex;align-items:center;gap:10px;background:var(--charcoal);color:var(--white);padding:14px 26px;border-radius:6px;text-decoration:none;font-weight:600;font-size:0.95rem;transition:background 0.2s}
.book-card.discovery .btn-cta{background:var(--terra)}
.book-card.intake .btn-cta{background:var(--ochre)}
.book-card .btn-cta:hover{background:var(--charcoal)}
.book-card .btn-cta svg{flex-shrink:0}
.book-card-note{display:inline-flex;align-items:center;gap:8px;padding:10px 16px;background:var(--dust);border-radius:4px;font-size:0.88rem;color:var(--charcoal-2);font-weight:500;margin-top:24px}
.book-card-note svg{color:var(--mid);flex-shrink:0}

.hours-section{margin-bottom:56px}
.hours-section h3{font-size:1.2rem;font-weight:700;letter-spacing:-0.01em;color:var(--charcoal);margin:0 0 18px;display:flex;align-items:center;gap:10px}
.hours-section h3 svg{color:var(--terra)}
.hours-grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:32px;align-items:stretch}
@media(max-width:760px){.hours-grid{grid-template-columns:1fr;gap:24px}}
.hours-grid-left{min-width:0;display:flex;flex-direction:column}
.hours-table{width:100%;max-width:520px;border-collapse:collapse;background:var(--white);border:1px solid var(--dust-2);border-radius:6px;overflow:hidden}
.hours-table tr{border-bottom:1px solid var(--dust-2)}
.hours-table tr:last-child{border-bottom:none}
.hours-table td{padding:12px 20px;font-size:0.93rem;line-height:1.5}
.hours-table td:first-child{font-weight:600;color:var(--charcoal);width:42%}
.hours-table td:last-child{color:var(--charcoal-2)}
.hours-table tr.closed td:last-child{color:var(--mid);font-style:normal}
.hours-notes{margin-top:18px;font-size:0.88rem;line-height:1.7;color:var(--charcoal-2);max-width:680px}
.hours-notes p{margin:0 0 8px}
.hours-notes p:last-child{margin-bottom:0}
.hours-image{margin:0;background:var(--dust);border:1px solid var(--dust-2);border-radius:8px;overflow:hidden;position:relative;height:100%}
.hours-image-inner{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;color:var(--light-mid)}
.hours-image-inner svg{opacity:0.55}
@media(max-width:760px){.hours-image{aspect-ratio:1/1;height:auto;max-width:340px;margin-left:auto;margin-right:auto}}

.payment-section{background:var(--dust);border-radius:8px;padding:32px 36px;margin-bottom:48px}
.payment-section h3{font-size:1.2rem;font-weight:700;letter-spacing:-0.01em;color:var(--charcoal);margin:0 0 14px}
.payment-section > p{font-size:0.95rem;line-height:1.75;color:var(--charcoal-2);margin:0 0 14px;max-width:780px}
.payment-section > p:last-of-type{margin-bottom:22px}
.payment-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(110px,1fr));gap:10px;margin-top:8px}
.payment-brand-tile{background:var(--white);border:1px solid var(--dust-2);border-radius:5px;height:50px;display:flex;align-items:center;justify-content:center;padding:8px}
.payment-brand-logo{display:inline-flex;align-items:center;justify-content:center;height:34px}
.payment-brand-logo img{height:18px;width:auto;display:block;object-fit:contain}

.book-fallback{margin-top:0;padding-top:32px;border-top:1px solid var(--dust-2);text-align:center}
.book-fallback p{font-size:0.95rem;color:var(--charcoal-2);line-height:1.7;margin:0}
.book-fallback a{color:var(--terra);text-decoration:none;font-weight:600}
.book-fallback a:hover{text-decoration:underline}

/* Live calendar inside the hours-image slot — auto-rolls each month via JS */
.hours-cal{background:var(--white);border:1px solid var(--dust-2);border-radius:8px;padding:22px 22px 18px;height:100%;display:flex;flex-direction:column;box-sizing:border-box}
.hours-cal-head{display:flex;align-items:baseline;justify-content:space-between;margin-bottom:14px}
.hours-cal-month{font-size:1.05rem;font-weight:700;letter-spacing:-0.01em;color:var(--charcoal);margin:0}
.hours-cal-tz{font-size:0.7rem;font-weight:600;letter-spacing:0.12em;text-transform:uppercase;color:var(--light-mid)}
.hours-cal-grid{display:grid;grid-template-columns:repeat(7,1fr);gap:4px;flex:1}
.hours-cal-dow{font-size:0.66rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:var(--light-mid);text-align:center;padding:6px 0 8px}
.hours-cal-cell{aspect-ratio:1/1;display:flex;align-items:center;justify-content:center;font-size:0.85rem;font-weight:500;color:var(--charcoal-2);border-radius:50%;position:relative}
.hours-cal-cell.is-muted{color:var(--dust-3)}
.hours-cal-cell.is-weekend{color:var(--dust-3)}
.hours-cal-cell.is-today{background:var(--ochre);color:var(--white);font-weight:700}
.hours-cal-foot{margin-top:14px;padding-top:14px;border-top:1px solid var(--dust-2);font-size:0.78rem;color:var(--light-mid);line-height:1.5;text-align:center}
.hours-cal-foot strong{color:var(--charcoal);font-weight:600}
@media(max-width:760px){.hours-cal{aspect-ratio:auto;min-height:340px;max-width:340px;margin-left:auto;margin-right:auto}}

@media(max-width:960px){
  .book-fold-grid{grid-template-columns:1fr;gap:0}
  .book-fold-image-panel{position:static;align-self:auto;aspect-ratio:2/1;margin-top:32px;border-radius:8px;overflow:hidden}
  .book-fold-image-panel > .book-fold-img-real{position:static;width:100%;height:100%}
  .book-fold-image-panel img{width:100%;height:100%;object-fit:cover;border-radius:8px}
}
@media(max-width:640px){
  .book-card{padding:28px 22px}
  .payment-section{padding:24px 20px}
  .hours-table td{padding:10px 14px}
}
"""

BOOK_HTML = """
  <header class="book-header page-fold" aria-labelledby="book-heading">
    <div class="wrap">
      <div class="book-fold-grid">
        <div class="book-header-inner">
          <span class="page-label">Booking</span>
          <h1 id="book-heading">Book a <span class="accent">session.</span></h1>
          <p class="page-intro">Three different conversations happen at three different stages of working with us. Pick the one that matches where you are.</p>
        </div>
        <div class="book-fold-image-panel" aria-hidden="true">
          <div class="book-fold-img-real"><img src="/images/book-fold.jpg" alt="A pale oak desk in soft morning light with a smartphone, an open leather-bound diary on a clean weekly spread, a slim black pen resting across the page, and a small white ceramic cup of dark coffee. The quiet moment of taking the small decisive step of making a booking." fetchpriority="high"></div>
        </div>
      </div>
    </div>
  </header>

  <!-- ABOVE-FOLD MARQUEE -->
  <div class="marquee-bar" aria-label="Accreditation and credentials" role="marquee">
    <div class="marquee-track" aria-hidden="true">
      <span class="marquee-item">AGD-Accredited FDRP <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Australian Mediation Association Member <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Section 60I Certificates (s 66H in WA) <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Conducted Securely Online <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Available Anywhere in Australia <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Free Discovery Call <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">No Obligation <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Confidential under the Family Law Act <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Both Parenting and Financial Matters <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">AGD-Accredited FDRP <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Australian Mediation Association Member <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Section 60I Certificates (s 66H in WA) <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Conducted Securely Online <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Available Anywhere in Australia <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Free Discovery Call <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">No Obligation <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Confidential under the Family Law Act <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Both Parenting and Financial Matters <span class="marquee-sep">&bull;</span></span>
    </div>
  </div>


  <div class="wrap book-wrap">
    <div class="book-intro">
      <p>Most people start with a free discovery call. It is short, no-obligation, and the right place to confirm that Family Dispute Resolution is the right path for your circumstances before committing to anything.</p>
      <p>If you have already had a discovery call and have agreed to proceed, the next step is your private intake session. Each party attends their own intake session separately with your practitioner so both sessions are complete. Details are below.</p>
    </div>

    <div class="book-cards">

      <article class="book-card discovery">
        <div class="book-card-head">
          <span class="book-card-step">Step 1</span>
          <h2>Free discovery call</h2>
        </div>
        <div class="book-card-meta">
          <span><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>Online via Google Meet</span>
        </div>
        <p>A short, no-obligation conversation to confirm that FDR is the right path for your situation. We ask a few brief questions about your circumstances, answer any questions you have about how the process works, and give you a clear picture of what is involved.</p>
        <p>You leave the call with a clear understanding of whether FDR is appropriate for your matter and what the next steps would look like. <strong>No payment required.</strong></p>
        <div class="book-card-cta">
          <a href="https://calendar.app.google/zwNm4dzYnwAwhwxY8" class="btn-cta" target="_blank" rel="noopener noreferrer">
            Book a discovery call
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
          </a>
        </div>
      </article>

      <article class="book-card intake">
        <div class="book-card-head">
          <span class="book-card-step">Step 2</span>
          <h2>Private &amp; confidential 1:1 intake session</h2>
        </div>
        <div class="book-card-meta">
          <span><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>1 hour</span>
          <span><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>Online via Google Meet</span>
          <span><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>Held privately with each party</span>
        </div>
        <p>The intake session is private and confidential. Attended by you alone with the practitioner. The other party attends their own intake session separately. Both intake sessions are required before any joint session can be scheduled.</p>
        <p>This is your chance to speak candidly about your situation, what you need from the process, and what you hope to achieve. The practitioner uses this session to assess whether the matter is suitable for joint mediation, and to identify any safety concerns or substantive matters that may need to be in the room.</p>
        <div class="book-card-emph">
          <p><strong>The session fee is confirmed during your discovery call and is shown at the time of booking.</strong> Payment is taken at booking and secures your time slot.</p>
        </div>
        <div class="book-card-cta">
          <a href="https://calendar.app.google/vKZbYJmLo8JtHoiA6" class="btn-cta" target="_blank" rel="noopener noreferrer">
            Book an intake session
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
          </a>
        </div>
      </article>

      <article class="book-card joint">
        <div class="book-card-head">
          <span class="book-card-step">Step 3</span>
          <h2>Joint mediation sessions</h2>
        </div>
        <div class="book-card-meta">
          <span><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>4hrs parenting / 3hrs financial</span>
          <span><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>Online via Google Meet</span>
          <span><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>Both parties attend together</span>
        </div>
        <p>Joint sessions are scheduled directly between you, the other party, and your practitioner once both intake sessions are complete. They are not booked through this page.</p>
        <p>Once a time is agreed, your practitioner sends each party a private payment link by email. Each party pays their own share separately. The session is confirmed once both parties have settled their payment.</p>
        <p>Parenting sessions run for four hours and financial sessions run for three hours. Payment is taken in advance for the full scheduled hours. If the session finishes early, the unused time is refunded automatically. You only ever pay for the time actually used.</p>
        <div class="book-card-note">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
          Arranged with your practitioner after intake.
        </div>
      </article>

    </div>

    <section class="hours-section" aria-labelledby="hours-heading">
      <h3 id="hours-heading">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
        Office hours (AEST)
      </h3>
      <div class="hours-grid">
        <div class="hours-grid-left">
          <table class="hours-table" aria-label="Office hours">
            <tbody>
              <tr><td>Monday</td><td>10am &ndash; 7pm</td></tr>
              <tr><td>Tuesday</td><td>10am &ndash; 7pm</td></tr>
              <tr><td>Wednesday</td><td>10am &ndash; 7pm</td></tr>
              <tr><td>Thursday</td><td>10am &ndash; 7pm</td></tr>
              <tr><td>Friday</td><td>10am &ndash; 7pm</td></tr>
              <tr><td>Saturday</td><td>By appointment</td></tr>
              <tr class="closed"><td>Sunday</td><td>n/a</td></tr>
            </tbody>
          </table>
          <div class="hours-notes">
            <p>All intake bookings are GMT+10 (AEST). The booking system converts to your local time zone automatically.</p>
            <p>Saturday sessions are not bookable online and incur a 15% surcharge. Contact us via email or phone to arrange.</p>
          </div>
        </div>
        <figure class="hours-cal" role="img" aria-label="Calendar showing current month with today highlighted">
          <div class="hours-cal-head">
            <h4 class="hours-cal-month" id="hours-cal-month-label">&nbsp;</h4>
            <span class="hours-cal-tz">AEST</span>
          </div>
          <div class="hours-cal-grid" id="hours-cal-grid">
            <div class="hours-cal-dow">Mon</div>
            <div class="hours-cal-dow">Tue</div>
            <div class="hours-cal-dow">Wed</div>
            <div class="hours-cal-dow">Thu</div>
            <div class="hours-cal-dow">Fri</div>
            <div class="hours-cal-dow">Sat</div>
            <div class="hours-cal-dow">Sun</div>
          </div>
          <div class="hours-cal-foot">Bookings available <strong>Monday&ndash;Friday</strong></div>
        </figure>
      </div>
    </section>

    <section class="payment-section" aria-labelledby="payment-heading">
      <h3 id="payment-heading">Payment options</h3>
      <p>Payment is processed securely by Stripe. We accept Visa, Mastercard, American Express, Apple Pay, and Google Pay (if available).</p>
      <p>Buy Now Pay Later (BNPL) is available at checkout for intake sessions and joint sessions in Australia (Afterpay, Klarna, Affirm, and Zip). BNPL lets you pay across instalments. Eligibility and instalment terms are set by each provider. Some providers may not be available for all bookings.</p>
      <div class="payment-grid" aria-label="Accepted payment methods">
        <div class="payment-brand-tile"><span class="payment-brand-logo"><img src="/images/payment/visa.png" alt="Visa" loading="lazy"></span></div>
        <div class="payment-brand-tile"><span class="payment-brand-logo"><img src="/images/payment/mastercard.png" alt="Mastercard" loading="lazy"></span></div>
        <div class="payment-brand-tile"><span class="payment-brand-logo"><img src="/images/payment/amex.png" alt="American Express" loading="lazy"></span></div>
        <div class="payment-brand-tile"><span class="payment-brand-logo"><img src="/images/payment/applepay.png" alt="Apple Pay" loading="lazy"></span></div>
        <div class="payment-brand-tile"><span class="payment-brand-logo"><img src="/images/payment/googlepay.png" alt="Google Pay" loading="lazy"></span></div>
        <div class="payment-brand-tile"><span class="payment-brand-logo"><img src="/images/payment/afterpay.png" alt="Afterpay" loading="lazy"></span></div>
        <div class="payment-brand-tile"><span class="payment-brand-logo"><img src="/images/payment/klarna.png" alt="Klarna" loading="lazy"></span></div>
        <div class="payment-brand-tile"><span class="payment-brand-logo"><img src="/images/payment/affirm.png" alt="Affirm" loading="lazy"></span></div>
        <div class="payment-brand-tile"><span class="payment-brand-logo"><img src="/images/payment/zip.png" alt="Zip" loading="lazy"></span></div>
      </div>
    </section>

    <div class="book-fallback">
      <p><strong>Prefer to talk first?</strong> Reach us at <a href="mailto:hello@onlinefdr.com.au">hello@onlinefdr.com.au</a> or <a href="tel:0399617544">(03) 9961 7544</a>. We respond to enquiries within one business day.</p>
    </div>
  </div>
"""

BOOK_JS = """<script>
(function(){
  var grid = document.getElementById('hours-cal-grid');
  var label = document.getElementById('hours-cal-month-label');
  if (!grid || !label) return;
  var now = new Date();
  var year = now.getFullYear();
  var month = now.getMonth(); // 0-indexed
  var today = now.getDate();
  var MONTHS = ['January','February','March','April','May','June','July','August','September','October','November','December'];
  label.textContent = MONTHS[month] + ' ' + year;
  // Day-of-week of the 1st. JS getDay returns 0=Sun..6=Sat. We display Mon-first, so map to 0=Mon..6=Sun.
  var first = new Date(year, month, 1);
  var startDow = (first.getDay() + 6) % 7;
  // Number of days in this month
  var daysInMonth = new Date(year, month + 1, 0).getDate();
  // Number of days in previous month, used to fill leading blanks
  var daysInPrev = new Date(year, month, 0).getDate();
  // Build 42 cells (6 rows x 7 cols) covering prev-tail + current month + next-head
  var cells = [];
  for (var i = 0; i < startDow; i++) {
    cells.push({ day: daysInPrev - startDow + 1 + i, muted: true, weekend: false, today: false });
  }
  for (var d = 1; d <= daysInMonth; d++) {
    var dow = (new Date(year, month, d).getDay() + 6) % 7; // 0=Mon..6=Sun
    cells.push({ day: d, muted: false, weekend: dow >= 5, today: d === today });
  }
  var nextDay = 1;
  while (cells.length < 42) {
    var dow2 = (cells.length % 7);
    cells.push({ day: nextDay++, muted: true, weekend: dow2 >= 5, today: false });
  }
  // Trim trailing full-week row if not needed (only 5 rows of real data)
  if (cells.length === 42 && cells[35].muted && cells[41].muted) {
    // If the last row is entirely next-month, drop it
    var lastRowAllMuted = true;
    for (var k = 35; k < 42; k++) if (!cells[k].muted) lastRowAllMuted = false;
    if (lastRowAllMuted) cells = cells.slice(0, 35);
  }
  var frag = document.createDocumentFragment();
  cells.forEach(function(c){
    var el = document.createElement('div');
    var classes = ['hours-cal-cell'];
    if (c.muted) classes.push('is-muted');
    else if (c.weekend) classes.push('is-weekend');
    if (c.today) classes.push('is-today');
    el.className = classes.join(' ');
    el.textContent = c.day;
    if (c.today) el.setAttribute('aria-label', 'Today, ' + c.day + ' ' + MONTHS[month] + ' ' + year);
    frag.appendChild(el);
  });
  grid.appendChild(frag);
})();
</script>"""

build_page(
    filename="book-v2.html",
    title="Book Online FDR | Discovery Call or Intake | onlinefdr.com.au",
    meta_desc="Book a free discovery call to find out if FDR is right for you, or book an intake session to begin the process. Online, anywhere in Australia.",
    canonical="/book/",
    current_page="/book/",
    schema_json='{"@context":"https://schema.org","@type":"WebPage","@id":"https://onlinefdr.com.au/book/#webpage","url":"https://onlinefdr.com.au/book/","name":"Book Online FDR","description":"Three booking pathways for online Family Dispute Resolution: free discovery call, 1-hour individual intake session, or arranged joint mediation (four hours for parenting, three hours for financial). Available nationally, conducted via Google Meet.","about":{"@id":"https://onlinefdr.com.au/#organization"}}',
    extra_css=BOOK_CSS,
    breadcrumbs=[("Home", "/"), ("Book", "/book/")],
    page_html=BOOK_HTML,
    extra_js=BOOK_JS,
)
print("Book done.")

# ─────────────────────────────────────────────
# GET HELP — crisis and support services
# ─────────────────────────────────────────────
GET_HELP_CSS = """
.gethelp-header{background:var(--charcoal);padding:120px 0 72px;position:relative;overflow:hidden}
.gethelp-header::before{content:'';position:absolute;inset:0;background:radial-gradient(ellipse 60% 70% at 80% 30%,rgba(196,135,58,0.07) 0%,transparent 60%);pointer-events:none}
.gethelp-header-inner{position:relative;z-index:1;max-width:680px}
.gethelp-header h1{font-size:clamp(2.4rem,5vw,4.2rem);font-weight:800;line-height:1.0;letter-spacing:-0.03em;color:var(--white);margin-bottom:20px}
.gethelp-header-sub{font-size:1rem;font-weight:400;color:rgba(253,250,246,0.55);line-height:1.8;max-width:560px}

.gethelp-wrap{padding:72px 0 100px}
.gethelp-content{max-width:760px}

.gethelp-emergency{background:#FEF2F2;border:2px solid #DC2626;border-radius:12px;padding:28px 32px;margin-bottom:48px;display:flex;align-items:center;gap:24px;flex-wrap:wrap}
.gethelp-emergency-text{flex:1;min-width:280px}
.gethelp-emergency-text h2{font-size:1.1rem;font-weight:800;color:#991B1B;margin-bottom:6px;letter-spacing:-0.01em}
.gethelp-emergency-text p{font-size:0.9rem;font-weight:500;color:#7F1D1D;line-height:1.65;margin:0}
.gethelp-emergency-cta{display:inline-flex;align-items:center;justify-content:center;background:#DC2626;color:#FFFFFF;font-family:var(--f);font-size:1.4rem;font-weight:800;letter-spacing:0.04em;padding:18px 36px;border-radius:8px;text-decoration:none;transition:background 0.2s;white-space:nowrap}
.gethelp-emergency-cta:hover{background:#991B1B;color:#FFFFFF}

.gethelp-intro{font-size:1rem;font-weight:400;color:var(--charcoal);line-height:1.75;margin-bottom:48px}

.gethelp-category{margin-bottom:48px}
.gethelp-category-label{font-size:0.75rem;font-weight:700;letter-spacing:0.16em;text-transform:uppercase;color:var(--ochre);margin-bottom:8px;display:flex;align-items:center;gap:10px}
.gethelp-category-label::before{content:'';width:24px;height:2px;background:var(--ochre)}
.gethelp-category h2{font-size:1.4rem;font-weight:800;color:var(--charcoal);letter-spacing:-0.02em;margin-bottom:18px}

.gethelp-services{display:flex;flex-direction:column;gap:14px}
.gethelp-service{background:var(--white);border:1px solid var(--dust-3);border-radius:10px;padding:24px 28px;transition:border-color 0.2s}
.gethelp-service:hover{border-color:var(--dust-3)}
.gethelp-service-name{font-size:1.05rem;font-weight:800;color:var(--charcoal);letter-spacing:-0.01em;margin-bottom:6px}
.gethelp-service-desc{font-size:0.88rem;font-weight:400;color:var(--mid);line-height:1.65;margin-bottom:14px}
.gethelp-service-contact{display:flex;flex-wrap:wrap;gap:18px;align-items:center}
.gethelp-service-phone{display:inline-flex;align-items:center;gap:8px;font-family:var(--f);font-size:1.05rem;font-weight:800;color:var(--terra);text-decoration:none;letter-spacing:-0.01em;transition:color 0.2s}
.gethelp-service-phone:hover{color:var(--charcoal)}
.gethelp-service-phone svg{width:16px;height:16px}
.gethelp-service-meta{font-size:0.78rem;font-weight:500;color:var(--light-mid);line-height:1.5}
.gethelp-service-meta strong{font-weight:700;color:var(--mid)}
.gethelp-service-link{display:inline-flex;align-items:center;gap:6px;font-size:0.82rem;font-weight:600;color:var(--terra);text-decoration:none;transition:color 0.2s}
.gethelp-service-link:hover{color:var(--charcoal)}
.gethelp-service-link svg{width:12px;height:12px}

.gethelp-disclaimer{background:var(--dust);border:1px solid var(--dust-2);border-radius:10px;padding:24px 28px;margin-top:48px}
.gethelp-disclaimer p{font-size:0.86rem;font-weight:400;color:var(--mid);line-height:1.7;margin:0}
.gethelp-disclaimer p strong{font-weight:700;color:var(--charcoal)}

@media(max-width:760px){
  .gethelp-emergency{padding:22px 24px}
  .gethelp-emergency-cta{width:100%;font-size:1.2rem;padding:16px 24px}
  .gethelp-service{padding:20px 22px}
  .gethelp-service-contact{flex-direction:column;align-items:flex-start;gap:10px}
}
"""

GET_HELP_HTML = """
  <header class="gethelp-header">
    <div class="wrap gethelp-header-inner">
      <h1>Get help</h1>
      <p class="gethelp-header-sub">Crisis and support services for family violence, mental health, and immediate safety. Free, available across Australia, independent of this practice.</p>
    </div>
  </header>

  <section class="gethelp-wrap">
    <div class="wrap">
      <div class="gethelp-content">

        <div class="gethelp-emergency" role="alert">
          <div class="gethelp-emergency-text">
            <h2>In immediate danger</h2>
            <p>If you or someone you know is in immediate danger, call Triple Zero for police, fire, or ambulance.</p>
          </div>
          <a href="tel:000" class="gethelp-emergency-cta" aria-label="Call Triple Zero">Call 000</a>
        </div>

        <p class="gethelp-intro">The services below are independent of this practice. They are listed here because separation often intersects with family violence, mental health pressure, and safety concerns for children. Every service on this page is free, confidential, and operates independently of any legal process or court matter.</p>

        <div class="gethelp-category">
          <p class="gethelp-category-label">Family violence and abuse</p>
          <h2>If you or someone you know is experiencing family or sexual violence</h2>
          <div class="gethelp-services">

            <div class="gethelp-service">
              <div class="gethelp-service-name">1800RESPECT</div>
              <p class="gethelp-service-desc">National counselling, information, and support service for anyone in Australia impacted by domestic, family, or sexual violence. Available by phone, text, online chat, and video call.</p>
              <div class="gethelp-service-contact">
                <a href="tel:1800737732" class="gethelp-service-phone"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>1800 737 732</a>
                <span class="gethelp-service-meta"><strong>24 hours, 7 days.</strong> Text 0458 737 732.</span>
                <a href="https://www.1800respect.org.au/" class="gethelp-service-link" target="_blank" rel="noopener">1800respect.org.au<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7"/><path d="M7 7h10v10"/></svg></a>
              </div>
            </div>

            <div class="gethelp-service">
              <div class="gethelp-service-name">Men's Referral Service</div>
              <p class="gethelp-service-desc">National counselling, information, and referral service for men who use, or are at risk of using, family violence. Also for men experiencing family violence themselves. Operated by No to Violence.</p>
              <div class="gethelp-service-contact">
                <a href="tel:1300766491" class="gethelp-service-phone"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>1300 766 491</a>
                <span class="gethelp-service-meta"><strong>24 hours, 7 days</strong> in NSW and TAS. Other states 8am to 9pm Mon to Fri.</span>
                <a href="https://ntv.org.au/" class="gethelp-service-link" target="_blank" rel="noopener">ntv.org.au<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7"/><path d="M7 7h10v10"/></svg></a>
              </div>
            </div>

            <div class="gethelp-service">
              <div class="gethelp-service-name">The Orange Door (Victoria)</div>
              <p class="gethelp-service-desc">Single point of access for Victorians experiencing family violence, or needing support with the care and wellbeing of children. Free service, no referral required. Phone numbers vary by location across Victoria.</p>
              <div class="gethelp-service-contact">
                <span class="gethelp-service-meta"><strong>Business hours.</strong> Mon to Fri, 9am to 5pm. Victoria only. Statewide after-hours support also available.</span>
                <a href="https://www.orangedoor.vic.gov.au/" class="gethelp-service-link" target="_blank" rel="noopener">orangedoor.vic.gov.au<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7"/><path d="M7 7h10v10"/></svg></a>
              </div>
            </div>

          </div>
        </div>

        <div class="gethelp-category">
          <p class="gethelp-category-label">Mental health and crisis support</p>
          <h2>If you are in crisis or struggling with your mental health</h2>
          <div class="gethelp-services">

            <div class="gethelp-service">
              <div class="gethelp-service-name">Lifeline</div>
              <p class="gethelp-service-desc">National crisis support and suicide prevention service. Available by phone, text, and online chat. Trained crisis supporters available around the clock.</p>
              <div class="gethelp-service-contact">
                <a href="tel:131114" class="gethelp-service-phone"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>13 11 14</a>
                <span class="gethelp-service-meta"><strong>24 hours, 7 days.</strong> Text 0477 13 11 14.</span>
                <a href="https://www.lifeline.org.au/" class="gethelp-service-link" target="_blank" rel="noopener">lifeline.org.au<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7"/><path d="M7 7h10v10"/></svg></a>
              </div>
            </div>

            <div class="gethelp-service">
              <div class="gethelp-service-name">Beyond Blue</div>
              <p class="gethelp-service-desc">National service supporting people experiencing anxiety, depression, and those at increased risk of suicide. Counselling, information, and referrals.</p>
              <div class="gethelp-service-contact">
                <a href="tel:1300224636" class="gethelp-service-phone"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>1300 22 4636</a>
                <span class="gethelp-service-meta"><strong>24 hours, 7 days.</strong></span>
                <a href="https://www.beyondblue.org.au/" class="gethelp-service-link" target="_blank" rel="noopener">beyondblue.org.au<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7"/><path d="M7 7h10v10"/></svg></a>
              </div>
            </div>

          </div>
        </div>

        <div class="gethelp-category">
          <p class="gethelp-category-label">Children and young people</p>
          <h2>If a child or young person needs support</h2>
          <div class="gethelp-services">

            <div class="gethelp-service">
              <div class="gethelp-service-name">Kids Helpline</div>
              <p class="gethelp-service-desc">Free, private, and confidential counselling service for young people aged 5 to 25. Available by phone, webchat, and email.</p>
              <div class="gethelp-service-contact">
                <a href="tel:1800551800" class="gethelp-service-phone"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>1800 55 1800</a>
                <span class="gethelp-service-meta"><strong>24 hours, 7 days.</strong> Ages 5 to 25.</span>
                <a href="https://kidshelpline.com.au/" class="gethelp-service-link" target="_blank" rel="noopener">kidshelpline.com.au<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7"/><path d="M7 7h10v10"/></svg></a>
              </div>
            </div>

          </div>
        </div>

        <div class="gethelp-category">
          <p class="gethelp-category-label">Aboriginal and Torres Strait Islander support</p>
          <h2>If you would prefer to be supported by mob</h2>
          <div class="gethelp-services">

            <div class="gethelp-service">
              <div class="gethelp-service-name">13YARN</div>
              <p class="gethelp-service-desc">National crisis support service co-designed, developed, led, and delivered by Aboriginal and Torres Strait Islander people for Aboriginal and Torres Strait Islander people.</p>
              <div class="gethelp-service-contact">
                <a href="tel:139276" class="gethelp-service-phone"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>13 92 76</a>
                <span class="gethelp-service-meta"><strong>24 hours, 7 days.</strong></span>
                <a href="https://www.13yarn.org.au/" class="gethelp-service-link" target="_blank" rel="noopener">13yarn.org.au<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7"/><path d="M7 7h10v10"/></svg></a>
              </div>
            </div>

          </div>
        </div>

        <div class="gethelp-disclaimer">
          <p>This page provides general information about support services that operate independently of this practice. It is not legal advice, medical advice, or a referral. Contact details and operating hours were correct at time of publication and may change. In an emergency, always call <strong>Triple Zero (000)</strong>.</p>
        </div>

      </div>
    </div>
  </section>
"""

build_page(
    filename="get-help-v2.html",
    title="Get Help | Crisis and Support Services | onlinefdr.com.au",
    meta_desc="Crisis and support services for family violence, mental health, and immediate safety. Free, available across Australia, independent of this practice.",
    canonical="/get-help/",
    current_page="/get-help/",
    schema_json='{"@context":"https://schema.org","@type":"WebPage","@id":"https://onlinefdr.com.au/get-help/#webpage","url":"https://onlinefdr.com.au/get-help/","name":"Get Help","description":"Crisis and support services for family violence, mental health, and immediate safety. Lists national independent services including 1800RESPECT, Lifeline, Beyond Blue, Mens Referral Service, Kids Helpline, 13YARN, and The Orange Door.","about":{"@id":"https://onlinefdr.com.au/#organization"},"inLanguage":"en-AU"}',
    extra_css=GET_HELP_CSS,
    breadcrumbs=[("Home", "/"), ("Get Help", "/get-help/")],
    page_html=GET_HELP_HTML,
    show_marquee=False,
)
print("Get Help done.")

# ─────────────────────────────────────────────
# LOCATIONS — service availability by state and territory
# ─────────────────────────────────────────────
LOCATIONS_CSS = """
.loc-fold-grid{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:start;position:relative;z-index:1;width:100%;min-height:0}
.loc-fold-image-panel{position:relative;align-self:stretch;opacity:0;animation:fadeUp 0.9s var(--ease) 0.4s forwards}
.loc-fold-image-panel > .loc-fold-img-real{position:absolute;inset:0;width:100%;height:100%}
.loc-fold-image-panel img{width:100%;height:100%;object-fit:cover;object-position:center 50%;border-radius:8px}

.loc-wrap{padding:72px 0 100px}
.loc-content{max-width:760px}
.loc-intro{font-size:1rem;font-weight:400;color:var(--charcoal);line-height:1.75;margin-bottom:48px}
.loc-intro p{margin-bottom:14px}
.loc-intro p:last-child{margin-bottom:0}

.loc-state{margin-bottom:40px;padding-bottom:40px;border-bottom:1px solid var(--dust-2)}
.loc-state:last-of-type{border-bottom:none;margin-bottom:0;padding-bottom:0}
.loc-state-eyebrow{font-size:0.72rem;font-weight:700;letter-spacing:0.16em;text-transform:uppercase;color:var(--ochre);margin-bottom:8px;display:flex;align-items:center;gap:10px}
.loc-state-eyebrow::before{content:'';width:24px;height:2px;background:var(--ochre)}
.loc-state h2{font-size:1.6rem;font-weight:800;color:var(--charcoal);letter-spacing:-0.02em;margin-bottom:14px}
.loc-state p{font-size:0.95rem;font-weight:400;color:var(--mid);line-height:1.75;margin-bottom:10px}
.loc-state p:last-child{margin-bottom:0}
.loc-state-meta{display:flex;flex-wrap:wrap;gap:8px 24px;margin-top:14px;font-size:0.82rem}
.loc-state-meta-item{display:inline-flex;align-items:center;gap:6px;color:var(--light-mid);font-weight:500}
.loc-state-meta-item strong{color:var(--charcoal);font-weight:700}

.loc-wa-callout{background:var(--ochre-pale);border:1px solid rgba(196,135,58,0.3);border-radius:10px;padding:20px 24px;margin-top:18px}
.loc-wa-callout p{font-size:0.88rem;font-weight:500;color:var(--charcoal);line-height:1.7;margin:0}
.loc-wa-callout p strong{font-weight:700}

.loc-cta{background:var(--charcoal);border-radius:12px;padding:40px 44px;margin-top:64px;display:flex;align-items:center;justify-content:space-between;gap:32px;flex-wrap:wrap}
.loc-cta-text{flex:1;min-width:280px}
.loc-cta-text h2{font-size:1.4rem;font-weight:800;color:var(--white);letter-spacing:-0.02em;margin-bottom:8px}
.loc-cta-text p{font-size:0.9rem;font-weight:400;color:rgba(253,250,246,0.6);line-height:1.65;margin:0}
.loc-cta-btn{display:inline-flex;align-items:center;gap:10px;background:var(--ochre);color:var(--white);font-family:var(--f);font-size:0.95rem;font-weight:700;padding:16px 28px;border-radius:8px;text-decoration:none;transition:background 0.2s;white-space:nowrap}
.loc-cta-btn:hover{background:var(--terra)}

@media(max-width:960px){
  .loc-fold-grid{grid-template-columns:1fr;gap:0}
  .loc-fold-image-panel{position:static;align-self:auto;aspect-ratio:3/2;margin-top:32px;border-radius:8px;overflow:hidden}
  .loc-fold-image-panel > .loc-fold-img-real{position:static;width:100%;height:100%}
  .loc-fold-image-panel img{width:100%;height:100%;object-fit:cover;border-radius:8px}
}
@media(max-width:760px){
  .loc-wrap{padding:48px 0 72px}
  .loc-state h2{font-size:1.3rem}
  .loc-cta{padding:32px 28px}
}
"""

LOCATIONS_HTML = """
  <header class="article-page-header page-fold">
    <div class="wrap">
      <div class="loc-fold-grid">
        <div class="article-page-header-inner">
          <span class="page-label">Availability</span>
          <h1><span class="accent">Available</span> throughout Australia.</h1>
          <p class="page-intro">A nationally accessible online Family Dispute Resolution practice. Available to anyone in any state or territory, conducted online via Google Meet, from anywhere in the country.</p>
        </div>
        <div class="loc-fold-image-panel" aria-hidden="true">
          <div class="loc-fold-img-real"><img src="/images/locations-fold.jpg" alt="An open laptop on a warm timber desk beside a window with cool teal light, the screen displaying a simple ochre outline map of Australia on a dark charcoal background. A cream ceramic mug and a small plant sit alongside, suggesting calm online work from anywhere." fetchpriority="high"></div>
        </div>
      </div>
    </div>
  </header>

  <!-- ABOVE-FOLD MARQUEE -->
  <div class="marquee-bar" aria-label="Accreditation and credentials" role="marquee">
    <div class="marquee-track" aria-hidden="true">
      <span class="marquee-item">AGD-Accredited FDRP <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Australian Mediation Association Member <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Section 60I Certificates (s 66H in WA) <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Conducted Securely Online <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Available Anywhere in Australia <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Free Discovery Call <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">No Obligation <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Confidential under the Family Law Act <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Both Parenting and Financial Matters <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">AGD-Accredited FDRP <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Australian Mediation Association Member <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Section 60I Certificates (s 66H in WA) <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Conducted Securely Online <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Available Anywhere in Australia <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Free Discovery Call <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">No Obligation <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Confidential under the Family Law Act <span class="marquee-sep">&bull;</span></span>
      <span class="marquee-item">Both Parenting and Financial Matters <span class="marquee-sep">&bull;</span></span>
    </div>
  </div>

  <section class="loc-wrap">
    <div class="wrap">
      <div class="loc-content">

        <div class="loc-intro">
          <p>FDR is governed by the federal Family Law Act 1975. The same rules apply in every state and territory. A Section 60I certificate issued by an accredited FDR practitioner has the same legal effect whether the parties are in Melbourne, Mildura, Cairns, or Karratha.</p>
          <p>This page lists the Federal Circuit and Family Court of Australia registry locations for each state and territory, along with the key regional centres each registry serves. It is provided as a reference for people who may need to file applications, attend interim hearings, or otherwise interact with the court system after FDR concludes.</p>
        </div>

        <div class="loc-state">
          <p class="loc-state-eyebrow">Victoria</p>
          <h2>FDR for Victorians</h2>
          <p>The practice serves Victorians from anywhere in the state, including Melbourne and the regional centres of Geelong, Ballarat, Bendigo, Shepparton, Mildura, and Warrnambool. Sessions are conducted online and require nothing more than a stable internet connection.</p>
          <div class="loc-state-meta">
            <span class="loc-state-meta-item"><strong>Court registry:</strong> Melbourne (with circuit sittings in Albury, Ballarat, Bendigo, Dandenong, Geelong, Mildura, Morwell, Shepparton, and Warrnambool)</span>
          </div>
        </div>

        <div class="loc-state">
          <p class="loc-state-eyebrow">New South Wales</p>
          <h2>FDR for people in New South Wales</h2>
          <p>The practice serves clients in NSW from anywhere in the state, including Sydney, Newcastle, Wollongong, and regional centres such as Albury, Dubbo, Lismore, Tamworth, and Wagga Wagga.</p>
          <div class="loc-state-meta">
            <span class="loc-state-meta-item"><strong>Court registries:</strong> Sydney, Parramatta, Newcastle, Wollongong, Albury, Dubbo, and Lismore</span>
          </div>
        </div>

        <div class="loc-state">
          <p class="loc-state-eyebrow">Queensland</p>
          <h2>FDR for Queenslanders</h2>
          <p>The practice serves Queenslanders from anywhere in the state, including Brisbane, the Gold Coast, the Sunshine Coast, Townsville, Cairns, and Toowoomba. Time-zone differences are accommodated in session scheduling.</p>
          <div class="loc-state-meta">
            <span class="loc-state-meta-item"><strong>Court registries:</strong> Brisbane, Townsville, and Cairns</span>
          </div>
        </div>

        <div class="loc-state">
          <p class="loc-state-eyebrow">Western Australia</p>
          <h2>FDR for Western Australians</h2>
          <p>The practice serves Western Australians from anywhere in the state, including Perth and regional centres such as Geraldton, Bunbury, and the Pilbara. Time-zone differences from the eastern states are factored into scheduling.</p>
          <div class="loc-wa-callout">
            <p><strong>Note for Western Australia:</strong> Western Australia operates its own Family Court of Western Australia, separate from the federal Federal Circuit and Family Court of Australia. The Family Law Act 1975 still applies to most matters, and online FDR works identically. Section 60I certificates issued by an accredited FDRP are equally recognised. For a small number of WA-specific matters, the Family Court of WA in Perth has jurisdiction.</p>
          </div>
        </div>

        <div class="loc-state">
          <p class="loc-state-eyebrow">South Australia</p>
          <h2>FDR for South Australians</h2>
          <p>The practice serves South Australians from anywhere in the state, including Adelaide and regional centres.</p>
          <div class="loc-state-meta">
            <span class="loc-state-meta-item"><strong>Court registry:</strong> Adelaide</span>
          </div>
        </div>

        <div class="loc-state">
          <p class="loc-state-eyebrow">Tasmania</p>
          <h2>FDR for Tasmanians</h2>
          <p>The practice serves Tasmanians from anywhere in the state, including Hobart, Launceston, Devonport, and Burnie.</p>
          <div class="loc-state-meta">
            <span class="loc-state-meta-item"><strong>Court registries:</strong> Hobart and Launceston</span>
          </div>
        </div>

        <div class="loc-state">
          <p class="loc-state-eyebrow">Australian Capital Territory</p>
          <h2>FDR for the ACT</h2>
          <p>The practice serves people in the ACT and surrounding region, including Canberra and the nearby parts of NSW such as Queanbeyan.</p>
          <div class="loc-state-meta">
            <span class="loc-state-meta-item"><strong>Court registry:</strong> Canberra (Nigel Bowen Commonwealth Law Courts)</span>
          </div>
        </div>

        <div class="loc-state">
          <p class="loc-state-eyebrow">Northern Territory</p>
          <h2>FDR for the Northern Territory</h2>
          <p>The practice serves people in the NT from anywhere in the territory, including Darwin, Alice Springs, and remote communities. Time-zone scheduling is accommodated.</p>
          <div class="loc-state-meta">
            <span class="loc-state-meta-item"><strong>Court registries:</strong> Darwin and Alice Springs</span>
          </div>
        </div>

        <div class="loc-cta">
          <div class="loc-cta-text">
            <h2>Wherever you are in Australia</h2>
            <p>If you are separating, FDR is available to you. The first step is a free discovery call to confirm the process is appropriate for your circumstances.</p>
          </div>
          <a href="/book/" class="loc-cta-btn">
            Book a discovery call
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
          </a>
        </div>

      </div>
    </div>
  </section>
"""

build_page(
    filename="locations-v2.html",
    title="FDR Available Throughout Australia | onlinefdr.com.au",
    meta_desc="Online Family Dispute Resolution available in every Australian state and territory. Court registry locations and the Family Court of WA distinction explained.",
    canonical="/locations/",
    current_page="/locations/",
    schema_json='{"@context":"https://schema.org","@type":"WebPage","@id":"https://onlinefdr.com.au/locations/#webpage","url":"https://onlinefdr.com.au/locations/","name":"FDR Available Throughout Australia","description":"Online Family Dispute Resolution availability by state and territory, with Federal Circuit and Family Court of Australia registry locations for each jurisdiction. Includes the Family Court of Western Australia distinction.","about":{"@id":"https://onlinefdr.com.au/#organization"},"inLanguage":"en-AU"}',
    extra_css=ARTICLE_CSS + LOCATIONS_CSS,
    breadcrumbs=[("Home", "/"), ("Locations", "/locations/")],
    page_html=LOCATIONS_HTML,
    show_marquee=False,
)
print("Locations done.")
