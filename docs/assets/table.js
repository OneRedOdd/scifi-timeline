/* Sortable, filterable table built from a CSV file. MIT licence (see LICENSE-CODE). No dependencies.
   Usage: <div class="csvtable" data-src="data/films.csv" data-cols="title,release_year,..."
               data-filters="release_type,tone" data-num="release_year,gap_years" data-long="notes"></div> */
(function(){
  function parseCSV(text){
    var rows=[],row=[],f='',q=false,i=0,c;
    text=text.replace(/^\uFEFF/,'');
    for(;i<text.length;i++){c=text[i];
      if(q){ if(c==='"'){ if(text[i+1]==='"'){f+='"';i++;} else q=false; } else f+=c; }
      else if(c==='"') q=true;
      else if(c===','){row.push(f);f='';}
      else if(c==='\n'){row.push(f);rows.push(row);row=[];f='';}
      else if(c!=='\r') f+=c;
    }
    if(f!==''||row.length){row.push(f);rows.push(row);}
    var h=rows.shift();
    return rows.filter(function(r){return r.length>1||r[0]!=='';}).map(function(r){var o={};h.forEach(function(k,j){o[k]=r[j]===undefined?'':r[j];});return o;});
  }
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
  function label(k){return k.replace(/_/g,' ').replace(/^./,function(c){return c.toUpperCase();});}
  function cell(k,v,cfg){
    var cls=[];
    if(cfg.num.indexOf(k)>=0) cls.push('num');
    if(cfg.long.indexOf(k)>=0) cls.push('long');
    var html=esc(v);
    if(/^https?:\/\//.test(v)) html='<a href="'+esc(v)+'" rel="noopener">'+esc(v.replace(/^https?:\/\/(www\.)?/,'').slice(0,40))+(v.length>48?'…':'')+'</a>';
    else if(k==='title'&&/\*$/.test(v)) html='<span class="flag" title="Setting year ambiguous, derived or off-screen: see notes">'+esc(v)+'</span>';
    else if(k==='verdict') html='<span class="'+({'came true':'v-true','sort of':'v-sort'}[v]||'v-no')+'">'+esc(v)+'</span>';
    else if(/gap/.test(k)&&v!==''&&!isNaN(+v)) html=(+v).toLocaleString('en-GB');  // years stay unformatted (1910, not 1,910)
    return '<td'+(cls.length?' class="'+cls.join(' ')+'"':'')+'>'+html+'</td>';
  }
  function init(box){
    var cfg={src:box.dataset.src,cols:(box.dataset.cols||'').split(',').filter(Boolean),filters:(box.dataset.filters||'').split(',').filter(Boolean),
             num:(box.dataset.num||'').split(','),long:(box.dataset.long||'').split(','),sort:box.dataset.sort||''};
    box.innerHTML='<p class="count">Loading '+esc(cfg.src)+'…</p>';
    fetch(cfg.src).then(function(r){if(!r.ok) throw new Error(r.status);return r.text();}).then(function(t){
      var data=parseCSV(t); if(!cfg.cols.length) cfg.cols=Object.keys(data[0]||{});
      var state={q:'',f:{},k:cfg.sort,dir:1};
      var ctr='<div class="controls"><label>Search<input type="search" placeholder="Filter any text…"></label>';
      cfg.filters.forEach(function(k){
        var vals={};data.forEach(function(d){vals[d[k]]=1;});
        ctr+='<label>'+esc(label(k))+'<select data-k="'+esc(k)+'"><option value="">All</option>'+Object.keys(vals).sort().map(function(v){return '<option>'+esc(v)+'</option>';}).join('')+'</select></label>';
      });
      ctr+='<span class="count"></span></div>';
      box.innerHTML=ctr+'<div class="tablebox"><table><thead><tr>'+cfg.cols.map(function(k){return '<th class="sortable" data-k="'+esc(k)+'" tabindex="0" scope="col">'+esc(label(k))+'</th>';}).join('')+'</tr></thead><tbody></tbody></table></div>';
      var tb=box.querySelector('tbody'),cnt=box.querySelector('.count');
      function render(){
        var q=state.q.toLowerCase();
        var rows=data.filter(function(d){
          for(var k in state.f){ if(state.f[k]&&d[k]!==state.f[k]) return false; }
          if(!q) return true;
          for(var k2 in d){ if(String(d[k2]).toLowerCase().indexOf(q)>=0) return true; } return false;
        });
        if(state.k){ var k=state.k,isNum=cfg.num.indexOf(k)>=0;
          rows.sort(function(a,b){var x=a[k],y=b[k]; if(isNum){x=x===''?-Infinity:+x;y=y===''?-Infinity:+y;return (x-y)*state.dir;} return x.localeCompare(y,'en-GB')*state.dir;}); }
        tb.innerHTML=rows.map(function(d){return '<tr>'+cfg.cols.map(function(k){return cell(k,d[k],cfg);}).join('')+'</tr>';}).join('');
        cnt.textContent='Showing '+rows.length+' of '+data.length+' rows';
        box.querySelectorAll('th').forEach(function(th){ th.removeAttribute('aria-sort'); if(th.dataset.k===state.k) th.setAttribute('aria-sort',state.dir>0?'ascending':'descending'); });
      }
      box.querySelector('input[type=search]').addEventListener('input',function(e){state.q=e.target.value;render();});
      box.querySelectorAll('select').forEach(function(s){s.addEventListener('change',function(){state.f[s.dataset.k]=s.value;render();});});
      box.querySelectorAll('th').forEach(function(th){
        function go(){ if(state.k===th.dataset.k) state.dir=-state.dir; else {state.k=th.dataset.k;state.dir=1;} render(); }
        th.addEventListener('click',go); th.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();go();}});
      });
      render();
    }).catch(function(e){box.innerHTML='<p class="caveat">Could not load '+esc(cfg.src)+' ('+esc(e.message)+'). If you opened this file directly from disk, serve the folder instead, e.g. <code>python -m http.server</code>.</p>';});
  }
  document.querySelectorAll('.csvtable').forEach(init);
})();
