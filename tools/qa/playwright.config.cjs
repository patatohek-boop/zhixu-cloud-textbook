const {defineConfig}=require('@playwright/test');
module.exports=defineConfig({
 testDir:__dirname,testMatch:'learning-ui.spec.cjs',timeout:180000,expect:{timeout:10000},fullyParallel:false,workers:2,
 reporter:[['list'],['html',{outputFolder:'../../work/learning-ui-report',open:'never'}]],outputDir:'../../work/learning-ui-results',
 use:{baseURL:'http://127.0.0.1:8767',browserName:'chromium',reducedMotion:'reduce',trace:'retain-on-failure',screenshot:'only-on-failure'},
 projects:[320,360,390,768,1165,1440].map(width=>({name:'width-'+width,use:{viewport:{width,height:900},deviceScaleFactor:1}})),
 webServer:{command:'python -m http.server 8767 --bind 127.0.0.1 --directory ../../site',url:'http://127.0.0.1:8767',reuseExistingServer:!process.env.CI,timeout:30000}
});
