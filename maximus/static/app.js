document.querySelector('[data-menu]')?.addEventListener('click',()=>document.querySelector('#sidebar').classList.toggle('open'));
const moduleSelect=document.querySelector('select[name="module_id"]');
if(moduleSelect){const sync=()=>{const hidden=document.querySelector('input[name="module_slug"]');if(hidden)hidden.value=moduleSelect.selectedOptions[0]?.dataset.slug||''};moduleSelect.addEventListener('change',sync);sync()}
document.querySelectorAll('[data-view]').forEach(button=>button.addEventListener('click',()=>{
  document.querySelectorAll('[data-view]').forEach(item=>item.classList.toggle('active',item===button));
  document.querySelectorAll('[data-panel]').forEach(panel=>panel.classList.toggle('active',panel.dataset.panel===button.dataset.view));
}));
const sideScrollbar=document.querySelector('[data-side-scrollbar]');
const sideContent=document.querySelector('[data-side-content]');
if(sideScrollbar&&sideContent){
  let syncing=false;
  const sync=(source,target)=>{if(syncing)return;syncing=true;target.scrollLeft=source.scrollLeft;requestAnimationFrame(()=>syncing=false)};
  sideScrollbar.addEventListener('scroll',()=>sync(sideScrollbar,sideContent));
  sideContent.addEventListener('scroll',()=>sync(sideContent,sideScrollbar));
}
const pmoSections=[...document.querySelectorAll('.pmo-journey [id^="modulo-"]')];
const pmoNavLinks=[...document.querySelectorAll('[data-pmo-nav]')];
if(pmoSections.length&&pmoNavLinks.length){
  const highlightPmoModule=id=>pmoNavLinks.forEach(link=>link.classList.toggle('active',link.dataset.pmoNav===id));
  const pmoObserver=new IntersectionObserver(entries=>{
    const visible=entries.filter(entry=>entry.isIntersecting).sort((a,b)=>a.boundingClientRect.top-b.boundingClientRect.top)[0];
    if(visible)highlightPmoModule(visible.target.id.replace('modulo-',''));
  },{rootMargin:'-20% 0px -65% 0px'});
  pmoSections.forEach(section=>pmoObserver.observe(section));
}
