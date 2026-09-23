/* Loaded only in the Android package, before app.js; no JavaScript-native object bridge. */
(() => {
 'use strict';
 if(location.origin!=='https://appassets.androidplatform.net'||location.pathname!=='/assets/www/index.html')return;
 let notificationTimer;
 window.ZhixuAndroid=Object.freeze({
  isApp:true,
  notify(message){
   const toast=document.getElementById('toast');if(!toast)return;
   toast.textContent=String(message);toast.classList.add('show');
   clearTimeout(notificationTimer);notificationTimer=setTimeout(()=>toast.classList.remove('show'),4000);
  }
 });
 // Capture before the normal webpage button handlers create a download or file input.
 document.addEventListener('click',event=>{
  const button=event.target instanceof Element?event.target.closest('button'):null;
  if(!button||!['export','import','print'].includes(button.id))return;
  event.preventDefault();event.stopImmediatePropagation();
  location.href='zhixu://'+button.id;
 },true);
 document.addEventListener('visibilitychange',()=>{if(document.visibilityState==='hidden')window.ZHIXU?.flush();});
})();
