from pathlib import Path
p = Path("_bundle/Pokrov-1910-Public-Site/site/heritage-models.js")
s = p.read_text()
start = s.index("  function roofPart(")
end = s.index("  function fittedRoof", start)
replacement = '''  function roofPart(id,lx,lz,w,d,rise=2.7){
    setBuilding(id);setPart('roof');const p=positions[id],q=local(p.x,p.z,p.a,lx,lz);
    if(id.startsWith('lenina')){
      const points=outlines[id];let edge=null,longest=0;
      for(let i=0;i<points.length;i++){
        const a=points[i],b=points[(i+1)%points.length],dx=b[0]-a[0],dz=b[1]-a[1],len=Math.hypot(dx,dz);
        if(len>longest){longest=len;edge={dx,dz};}
      }
      const major=Math.max(w,d),minor=Math.min(w,d),angle=Math.atan2(-edge.dz,edge.dx);
      hippedRoof(q[0],q[1],major+.35,minor+.35,p.sp.h+.5,id==='lenina80'?1.8:rise,id==='cheburov'?palette.roof3:roof,angle);
    }else hippedRoof(q[0],q[1],w+.8,d+.8,p.sp.h+.5,rise,id==='cheburov'?palette.roof3:roof,p.a);
    setPart('details');
  }
'''
s = s[:start] + replacement + s[end:]
p.write_text(s.replace("roofPart('lenina80',0,0,p.w,p.d,3.0);", "roofPart('lenina80',0,0,p.w,p.d,1.8);"))
