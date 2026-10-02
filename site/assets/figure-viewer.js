/* Local-only figure enlargement, including Android's offline WebView. */
(function(root){
'use strict';
let dialog,opener,zoom=2;
function init(doc){
 if(dialog)return;
 dialog=doc.createElement('dialog');dialog.id='figure-dialog';dialog.setAttribute('aria-labelledby','figure-title');
 dialog.innerHTML='<div class="figure-viewer-head"><h2 id="figure-title">放大看图</h2><button type="button" class="secondary" data-figure-close aria-label="关闭大图">关闭 ×</button></div><div class="figure-viewer-tools"><button type="button" class="secondary" data-figure-zoom="out" aria-label="缩小图片">−</button><output id="figure-zoom" aria-live="polite">200%</output><button type="button" class="secondary" data-figure-zoom="in" aria-label="放大图片">＋</button><button type="button" class="secondary" data-figure-zoom="fit">看整张图</button></div><p class="figure-viewer-help">字太小就点＋。放大后可左右、上下滑动看图；键盘也可在图框中滚动。</p><div class="figure-viewport" tabindex="0" role="region" aria-label="大图，可左右上下滚动"><img class="figure-enlarged" alt="" draggable="false"></div><p class="figure-viewer-caption"></p>';
 doc.body.append(dialog);
 dialog.querySelector('[data-figure-close]').onclick=()=>dialog.close();
 dialog.addEventListener('click',e=>{if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dialog.close();}});
 dialog.addEventListener('close',()=>{if(opener?.isConnected)opener.focus();});
 dialog.querySelectorAll('[data-figure-zoom]').forEach(button=>button.onclick=()=>{zoom=button.dataset.figureZoom==='fit'?1:Math.max(1,Math.min(4,zoom+(button.dataset.figureZoom==='in'?.5:-.5)));paint();});
}
function paint(){dialog.querySelector('.figure-enlarged').style.width=(zoom*100)+'%';dialog.querySelector('#figure-zoom').textContent=Math.round(zoom*100)+'%';dialog.querySelector('[data-figure-zoom=out]').disabled=zoom<=1;dialog.querySelector('[data-figure-zoom=in]').disabled=zoom>=4;}
function bind(container){
 init(container.ownerDocument);
 container.querySelectorAll('figure a[href]').forEach(a=>{
  const img=a.querySelector('img');if(!img||!/^assets\/diagrams\/[a-z0-9-]+\.svg$/.test(img.getAttribute('src')||''))return;
  a.setAttribute('aria-haspopup','dialog');a.setAttribute('aria-label','放大看图：'+img.alt);
  a.addEventListener('click',e=>{if(e.ctrlKey||e.metaKey||e.shiftKey||e.button>0)return;e.preventDefault();opener=a;zoom=root.innerWidth<600?2:1;const full=dialog.querySelector('.figure-enlarged');full.src=img.getAttribute('src');full.alt=img.alt;dialog.querySelector('.figure-viewer-caption').textContent=a.closest('figure').querySelector('figcaption')?.textContent||img.alt;paint();dialog.showModal();const viewport=dialog.querySelector('.figure-viewport');viewport.scrollTop=0;viewport.scrollLeft=0;dialog.querySelector('[data-figure-close]').focus();});
 });
}
root.FigureViewer={bind,isOpen:()=>!!dialog?.open,close:()=>{if(dialog?.open)dialog.close();}};
})(typeof window==='undefined'?globalThis:window);
