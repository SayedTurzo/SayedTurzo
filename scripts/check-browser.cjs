const {chromium}=require('playwright');
const fs=require('node:fs');fs.mkdirSync('tmp/qa',{recursive:true});
const assert=require('node:assert/strict');
const profile=JSON.parse(fs.readFileSync('profile.json','utf8'));
(async()=>{
const browser=await chromium.launch({headless:true,channel:process.env.BROWSER_CHANNEL||(process.platform==='win32'?'msedge':undefined)});const page=await browser.newPage({viewport:{width:1440,height:1000}});const errors=[];page.on('pageerror',e=>errors.push(e.message));
await page.goto('http://127.0.0.1:8000');await page.waitForSelector('.game-card');assert.equal(await page.locator('.game-card').count(),profile.games.length);
if(new Set(profile.games.map(g=>g.platform)).size>1){await page.getByRole('button',{name:'Roblox',exact:true}).click();assert.equal(await page.locator('.game-card').count(),profile.games.filter(g=>g.platform==='Roblox').length);await page.getByRole('button',{name:'All',exact:true}).click();}
if(profile.worlds.length===0)assert.equal(await page.locator('#worlds').isVisible(),false);
await page.screenshot({path:'tmp/qa/portfolio-desktop.png',fullPage:true});
await page.locator('#arcade').scrollIntoViewIfNeeded();await page.locator('#start').click();await page.waitForTimeout(300);assert.equal(await page.locator('#game-state').textContent(),'PLAYING');await page.locator('#snake').press('Space');assert.equal(await page.locator('#game-state').textContent(),'PAUSED');await page.locator('#pause').click();assert.equal(await page.locator('#game-state').textContent(),'PLAYING');await page.waitForTimeout(1800);assert.equal(await page.locator('#game-state').textContent(),'GAME OVER');await page.locator('#start').click();assert.equal(await page.locator('#game-state').textContent(),'PLAYING');await page.locator('#pause').click();
await page.screenshot({path:'tmp/qa/portfolio-game.png'});
await page.setViewportSize({width:390,height:844});await page.goto('http://127.0.0.1:8000');await page.waitForSelector('.game-card');assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'Mobile should not overflow horizontally');await page.screenshot({path:'tmp/qa/portfolio-mobile.png',fullPage:true});
await page.locator('#start').click();await page.getByRole('button',{name:'Move up',exact:true}).click();assert.equal(await page.locator('#game-state').textContent(),'PLAYING');
assert.deepEqual(errors,[]);console.log('Browser: desktop/mobile, configured games, applicable filters, start/pause/resume/game-over/restart, touch buttons and no JS errors passed.');await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
