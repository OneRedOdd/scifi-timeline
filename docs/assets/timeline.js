/* Interactive timeline of the films (SVG, no dependencies). MIT licence (see LICENSE-CODE).
   Reads data/films.csv and draws one row per film: release year -> setting year, with a linear
   near-future panel (to 2125) and a compressed far-future panel (2125-5400), plus off-scale arrows. */
(function(){
  var root=document.getElementById('itl'); if(!root) return;
  var SRC=root.dataset.src||'data/films.csv';
  var C={bg:'#0d1424',fg:'#e8ecf4',muted:'#8b97b0',grid:'#1f2a40',band:'#121b30',near:'#4fc3f7',far:'#ff8a65',rel:'#ffd54f',amb:'#ce93d8',dec:'#5c6b8a',badge:'#26c6a6',stream:'#ff6fae'};
  var SPLIT=2125,NEARMIN=1900,FARMAX=5400,OFF=4850;
  var LW=330, NX0=LW+50, NX1=NX0+720, FX0=NX1+26, FX1=FX0+250, W=FX1+20, RH=24, HEAD=46;
  var ISO={'Germany':'DE','West Germany (West Berlin)':'DE','West Germany':'DE','Austria':'AT','Czechoslovakia':'CS','Czech Republic':'CZ','Denmark':'DK','Italy':'IT','France':'FR','Finland':'FI','Canada':'CA','Japan':'JP','Hong Kong':'HK','South Korea':'KR','China':'CN','Australia':'AU','Ireland':'IE','Hungary':'HU','Jordan':'JO','Romania':'RO','Soviet Union':'SU','Poland':'PL','India':'IN','Belgium':'BE','Luxembourg':'LU','South Africa':'ZA','Russia':'RU','Slovakia':'SK','Serbia':'RS','East Germany':'DD','Spain':'ES','Bulgaria':'BG','Switzerland':'CH','Argentina':'AR','New Zealand':'NZ','Indonesia':'ID','Dominican Republic':'DO','Kenya':'KE'};
  var NOBADGE={'Terminator: Dark Fate':1};
  var NS='http://www.w3.org/2000/svg';
  function parseCSV(text){var rows=[],row=[],f='',q=false,c;text=text.replace(/^\uFEFF/,'');
    for(var i=0;i<text.length;i++){c=text[i];
      if(q){if(c==='"'){if(text[i+1]==='"'){f+='"';i++;}else q=false;}else f+=c;}
      else if(c==='"')q=true;else if(c===','){row.push(f);f='';}else if(c==='\n'){row.push(f);rows.push(row);row=[];f='';}else if(c!=='\r')f+=c;}
    if(f!==''||row.length){row.push(f);rows.push(row);}
    var h=rows.shift();return rows.filter(function(r){return r.length>1;}).map(function(r){var o={};h.forEach(function(k,j){o[k]=r[j]||'';});return o;});}
  function el(tag,attrs,parent,text){var e=document.createElementNS(NS,tag);for(var k in attrs)e.setAttribute(k,attrs[k]);if(text!=null)e.textContent=text;if(parent)parent.appendChild(e);return e;}
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
  function fmt(n){return n.toLocaleString('en-GB');}
  function yr(y){return y>=10000?fmt(y):String(y);}
  function yrs(g){return '+'+fmt(g)+(g===1?' yr':' yrs');}
  function lab(g,x,y,text,anchor,bandFill){var t=el('text',{x:x,y:y,fill:C.fg,'font-size':11,'text-anchor':anchor||'start'},g,text);
    if(bandFill){try{var b=t.getBBox();var r=el('rect',{x:b.x-2,y:b.y-1,width:b.width+4,height:b.height+2,rx:2,fill:bandFill,opacity:.92});g.insertBefore(r,t);}catch(e){}}return t;}
  function xn(y){return NX0+(y-NEARMIN)/(SPLIT+12-NEARMIN)*(NX1-NX0);}
  function xf(y){return FX0+(y-SPLIT)/(FARMAX-SPLIT)*(FX1-FX0);}
  function badge(country){var cs=country.split(';').map(function(s){return s.trim();});
    var us=function(c){return /^(United States|United Kingdom)/.test(c);};
    var base=cs.filter(function(c){return !us(c);}); if(!base.length) return null;
    if(base.length===cs.length){var seen={},codes=[];cs.forEach(function(c){var k=ISO[c]||'??';if(!seen[k]){seen[k]=1;codes.push(k);}});return{solid:true,code:codes.join('/')};}
    if(!us(cs[0])) return{solid:false,code:ISO[cs[0]]||'??'}; return null;}
  function flagReason(notes){var m=notes.match(/(?:FLAG|AMBIGUOUS)[^:]*:\s*([\s\S]*)$/);return m?m[1].trim():'See the source note below.';}

  root.innerHTML='<div class="itl-controls" role="group" aria-label="Chart controls">'+
    '<div class="itl-chips" role="group" aria-label="Filter by release decade"></div>'+
    '<label class="itl-sort">Sort<select aria-label="Sort films"><option value="release">By release year</option><option value="gap-asc">By gap, smallest first</option><option value="gap-desc">By gap, largest first</option></select></label>'+
    '<span class="count" aria-live="polite"></span></div>'+
    '<div class="itl-frame"><div class="itl-head"></div><div class="itl-body" tabindex="-1"></div></div>'+
    '<div class="itl-tip" role="tooltip" hidden></div>'+
    '<div class="itl-modal" hidden><div class="itl-dialog" role="dialog" aria-modal="true" aria-labelledby="itl-mtitle"><button class="itl-close" aria-label="Close">×</button><div class="itl-mbody"></div></div></div>';
  var chipsBox=root.querySelector('.itl-chips'),sel=root.querySelector('select'),cnt=root.querySelector('.count'),
      head=root.querySelector('.itl-head'),body=root.querySelector('.itl-body'),tip=root.querySelector('.itl-tip'),
      modal=root.querySelector('.itl-modal'),mbody=root.querySelector('.itl-mbody'),lastFocus=null;
  body.addEventListener('scroll',function(){head.scrollLeft=body.scrollLeft;});

  fetch(SRC).then(function(r){if(!r.ok)throw new Error(r.status);return r.text();}).then(function(t){
    var films=parseCSV(t).map(function(r,i){var o=Object.assign({},r);o.ry=+r.release_year;o.sy=+r.setting_year;o.g=+r.gap_years;o.amb=/\*$/.test(r.title);o.idx=i;o.dec=Math.floor(o.ry/10)*10;return o;});
    var decs=[];films.forEach(function(f){if(decs.indexOf(f.dec)<0)decs.push(f.dec);});decs.sort();
    var active={};
    chipsBox.innerHTML='<button type="button" class="chip" data-d="all" aria-pressed="true">All</button>'+decs.map(function(d){return '<button type="button" class="chip" data-d="'+d+'" aria-pressed="false">'+d+'s</button>';}).join('');
    chipsBox.addEventListener('click',function(e){var b=e.target.closest('.chip');if(!b)return;var d=b.dataset.d;
      if(d==='all')active={};else{if(active[d])delete active[d];else active[d]=1;}
      chipsBox.querySelectorAll('.chip').forEach(function(c){c.setAttribute('aria-pressed',c.dataset.d==='all'?String(!Object.keys(active).length):String(!!active[c.dataset.d]));});
      draw();});
    sel.addEventListener('change',draw);
    drawHead(); draw();

    function drawHead(){
      head.innerHTML='';var s=el('svg',{width:W,height:HEAD,viewBox:'0 0 '+W+' '+HEAD,'aria-hidden':'true'},head);
      el('rect',{x:0,y:0,width:W,height:HEAD,fill:C.bg},s);
      el('text',{x:NX0,y:16,fill:C.near,'font-size':14},s,'Near future (to 2125)');
      el('text',{x:FX0,y:16,fill:C.far,'font-size':14},s,'Far future (compressed scale)');
      for(var y=1900;y<=2120;y+=20) el('text',{x:xn(y),y:38,fill:C.muted,'font-size':11,'text-anchor':'middle'},s,y);
      [2500,3000,3500,4000,4500,5000].forEach(function(y){el('text',{x:xf(y),y:38,fill:C.muted,'font-size':11,'text-anchor':'middle'},s,y);});
      el('text',{x:xn(2026)+4,y:16,fill:C.fg,'font-size':11,opacity:.85},s,'Today (2026)');
    }
    function draw(){
      var mode=sel.value, keys=Object.keys(active);
      var rows=films.filter(function(f){return !keys.length||active[f.dec];});
      rows.sort(mode==='release'?function(a,b){return a.ry-b.ry||a.sy-b.sy||a.idx-b.idx;}:mode==='gap-asc'?function(a,b){return a.g-b.g||a.ry-b.ry;}:function(a,b){return b.g-a.g||a.ry-b.ry;});
      cnt.textContent='Showing '+rows.length+' of '+films.length+' films';
      body.innerHTML='';var H=rows.length*RH+12;
      var s=el('svg',{width:W,height:H,viewBox:'0 0 '+W+' '+H,role:'list','aria-label':'Timeline of '+rows.length+' films','class':'itl-svg'},body);
      el('rect',{x:0,y:0,width:W,height:H,fill:C.bg},s);
      var grid=el('g',{},s);
      for(var y=1900;y<=2120;y+=20) el('line',{x1:xn(y),x2:xn(y),y1:0,y2:H,stroke:C.grid},grid);
      [2500,3000,3500,4000,4500,5000].forEach(function(y){el('line',{x1:xf(y),x2:xf(y),y1:0,y2:H,stroke:C.grid},grid);});
      var prev=null;
      rows.forEach(function(f,i){
        var cy=6+i*RH+RH/2, g=el('g',{'class':'itl-row',tabindex:0,role:'listitem','data-i':f.idx,
          'aria-label':f.title.replace(/\*$/,' (year flagged)')+', released '+f.ry+', set in '+f.sy+', gap '+yrs(f.g)+'. Press Enter for the source note.'},s);
        if(i%2===0) el('rect',{x:0,y:cy-RH/2,width:W,height:RH,fill:C.band},g);
        el('rect',{'class':'itl-hit',x:0,y:cy-RH/2,width:W,height:RH,fill:'transparent'},g);
        if(mode==='release'&&f.dec!==prev){ if(prev!==null) el('line',{x1:0,x2:W,y1:cy-RH/2,y2:cy-RH/2,stroke:C.dec,'stroke-width':1.2},s);
          el('text',{x:6,y:cy+5,fill:C.dec,'font-size':14,'font-weight':700},g,f.dec+'s'); prev=f.dec; }
        var far=f.sy>SPLIT, col=far?C.far:C.near;
        if(far){
          el('line',{x1:xn(f.ry),x2:NX1,y1:cy,y2:cy,stroke:col,'stroke-width':5},g);
          if(f.sy>FARMAX){
            el('line',{x1:FX0,x2:xf(OFF),y1:cy,y2:cy,stroke:col,'stroke-width':5},g);
            el('path',{d:'M'+xf(OFF)+' '+(cy-7)+' L'+(xf(OFF)+14)+' '+cy+' L'+xf(OFF)+' '+(cy+7)+' Z',fill:col},g);
            lab(g,FX0+4,cy+4,fmt(f.sy)+' AD (off scale)  '+yrs(f.g),'start',C.bg);
          } else {
            el('line',{x1:FX0,x2:xf(f.sy),y1:cy,y2:cy,stroke:col,'stroke-width':5},g);
            el('circle',{cx:xf(f.sy),cy:cy,r:5,fill:col,stroke:C.bg,'stroke-width':2},g);
            var right=f.sy>4600; lab(g,xf(f.sy)+(right?-8:6),cy+4,f.sy+'  '+yrs(f.g),right?'end':'start',right?(i%2===0?C.band:C.bg):null);
          }
        } else {
          el('line',{x1:xn(f.ry),x2:xn(f.sy),y1:cy,y2:cy,stroke:col,'stroke-width':5},g);
          el('circle',{cx:xn(f.sy),cy:cy,r:5,fill:col,stroke:C.bg,'stroke-width':2},g);
          var lft=f.sy>2100; lab(g,xn(f.sy)+(lft?-8:7),cy+4,f.sy+'  '+yrs(f.g),lft?'end':'start',lft?(i%2===0?C.band:C.bg):null);
        }
        var stream=f.release_type==='streaming';
        if(stream){ var x=xn(f.ry); el('path',{d:'M'+x+' '+(cy-6)+' L'+(x+6)+' '+cy+' L'+x+' '+(cy+6)+' L'+(x-6)+' '+cy+' Z',fill:C.bg,stroke:C.stream,'stroke-width':2},g);
          el('rect',{x:x-92,y:cy-8,width:48,height:16,rx:4,fill:C.stream},g); el('text',{x:x-68,y:cy+4,fill:C.bg,'font-size':9.5,'font-weight':700,'text-anchor':'middle'},g,'STREAM'); }
        else el('circle',{cx:xn(f.ry),cy:cy,r:4.5,fill:C.rel,stroke:C.bg,'stroke-width':2},g);
        el('text',{x:xn(f.ry)-(stream?10:8),y:cy+4,fill:stream?C.stream:C.rel,'font-size':10.5,'text-anchor':'end'},g,f.ry).setAttribute('class','itl-ry');
        var title=f.title==='Electronic Labyrinth: THX 1138 4EB*'?'THX 1138 4EB*':f.title;
        if(f.format==='short'||f.format==='serial') title+=' ('+f.format+')';
        var tt=el('text',{x:LW,y:cy+4,fill:f.amb?C.amb:C.fg,'font-size':12.5,'font-weight':700,'text-anchor':'end','class':'itl-title'},g,title);
        var b=NOBADGE[f.title.replace(/\*$/,'')]?null:badge(f.country);
        if(b){ var tw=tt.getComputedTextLength?tt.getComputedTextLength():title.length*7; var bw=b.code.length*7+10, bx=LW-tw-8-bw;
          el('rect',{x:bx,y:cy-8,width:bw,height:16,rx:4,fill:b.solid?C.badge:C.bg,stroke:C.badge,'stroke-width':1.4},g);
          el('text',{x:bx+bw/2,y:cy+4,fill:b.solid?C.bg:C.badge,'font-size':10,'font-weight':700,'text-anchor':'middle'},g,b.code); }
        // shift the release-year label left of the STREAM tag
        if(stream){ var ryl=g.querySelector('.itl-ry'); ryl.setAttribute('x',xn(f.ry)-96); }
      });
      el('line',{x1:xn(2026),x2:xn(2026),y1:0,y2:H,stroke:'#ffffff','stroke-width':1.5,'stroke-dasharray':'4 4',opacity:.55,'pointer-events':'none'},s);
      el('text',{x:NX1+13,y:16,fill:C.muted,'font-size':16,'font-weight':700,'text-anchor':'middle'},s,'//');
      root.dataset.rendered=rows.length;
    }

    function film(g){return films[+g.dataset.i];}
    function showTip(f,x,y){tip.innerHTML='<strong>'+esc(f.title)+'</strong><br>Released '+f.ry+' · set in '+yr(f.sy)+'<br>Gap: '+yrs(f.g);tip.hidden=false;
      var r=root.getBoundingClientRect(),tw=tip.offsetWidth,th=tip.offsetHeight,lx=x-r.left+14,ly=y-r.top+14;
      if(lx+tw>r.width) lx=Math.max(4,x-r.left-tw-10); tip.style.left=lx+'px';tip.style.top=ly+'px';}
    function hideTip(){tip.hidden=true;}
    function openNote(f){lastFocus=document.activeElement;hideTip();
      var h='<h3 id="itl-mtitle">'+esc(f.title)+'</h3><p class="itl-meta">Released '+f.ry+' · set in '+yr(f.sy)+' · gap '+yrs(f.g)+'<br>'+esc(f.country)+(f.director?' · directed by '+esc(f.director):'')+(f.release_type==='streaming'?' · streaming release':'')+'</p>';
      var k=f.notes.search(/FLAG|AMBIGUOUS/), note=f.notes;
      if(f.amb){ h+='<p class="itl-flag"><strong>Why the year is flagged:</strong> '+esc(flagReason(f.notes))+'</p>'; if(k>=0) note=f.notes.slice(0,k).trim(); }
      if(note) h+='<p><strong>Source note:</strong> '+esc(note)+'</p>';
      h+='<p><p><a href="'+esc(f.source_url)+'" rel="noopener" target="_blank">'+esc(f.source_url)+'</a></p>';
      mbody.innerHTML=h;modal.hidden=false;document.body.classList.add('itl-open');modal.querySelector('.itl-close').focus();}
    function closeNote(){modal.hidden=true;document.body.classList.remove('itl-open');if(lastFocus&&lastFocus.focus)lastFocus.focus();}
    body.addEventListener('mousemove',function(e){var g=e.target.closest('.itl-row');if(g)showTip(film(g),e.clientX,e.clientY);else hideTip();});
    body.addEventListener('mouseleave',hideTip);
    body.addEventListener('click',function(e){var g=e.target.closest('.itl-row');if(g)openNote(film(g));});
    body.addEventListener('focusin',function(e){var g=e.target.closest('.itl-row');if(!g)return;var r=g.getBoundingClientRect();showTip(film(g),Math.min(r.left+LW+40,window.innerWidth-20),r.top);});
    body.addEventListener('focusout',hideTip);
    body.addEventListener('keydown',function(e){var g=e.target.closest('.itl-row');if(!g)return;
      if(e.key==='Enter'||e.key===' '){e.preventDefault();openNote(film(g));}
      else if(e.key==='ArrowDown'||e.key==='ArrowUp'){e.preventDefault();var n=e.key==='ArrowDown'?g.nextElementSibling:g.previousElementSibling;while(n&&!n.classList.contains('itl-row'))n=e.key==='ArrowDown'?n.nextElementSibling:n.previousElementSibling;if(n)n.focus();}});
    modal.addEventListener('click',function(e){if(e.target===modal||e.target.closest('.itl-close'))closeNote();});
    document.addEventListener('keydown',function(e){if(e.key==='Escape'){if(!modal.hidden)closeNote();else hideTip();}
      if(e.key==='Tab'&&!modal.hidden){var fs=modal.querySelectorAll('button,a[href]');if(!fs.length)return;var a=fs[0],z=fs[fs.length-1];
        if(e.shiftKey&&document.activeElement===a){e.preventDefault();z.focus();}else if(!e.shiftKey&&document.activeElement===z){e.preventDefault();a.focus();}}});
  }).catch(function(e){root.innerHTML='<p class="caveat">Could not load the chart data ('+esc(e.message)+'). The static chart is linked above.</p>';});
})();
