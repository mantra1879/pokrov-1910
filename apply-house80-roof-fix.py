from pathlib import Path
root=Path("_bundle/Pokrov-1910-Public-Site/site")
p=root/"heritage-models.js"
s=p.read_text()
start=s.index("  function roofPart(")
end=s.index("  function fittedRoof",start)
replacement='''  function roofPart(id,lx,lz,w,d,rise=2.7){
    setBuilding(id);setPart('roof');const p=positions[id];let q=local(p.x,p.z,p.a,lx,lz);
    if(id.startsWith('lenina')){
      const points=outlines[id];let edge=null,longest=0;
      q=points.reduce((c,v)=>[c[0]+v[0]/points.length,c[1]+v[1]/points.length],[0,0]);
      for(let i=0;i<points.length;i++){
        const a=points[i],b=points[(i+1)%points.length],dx=b[0]-a[0],dz=b[1]-a[1],len=Math.hypot(dx,dz);
        if(len>longest){longest=len;edge={dx,dz};}
      }
      const major=Math.max(w,d),minor=Math.min(w,d),ridgeAngle=Math.atan2(-edge.dz,edge.dx);
      const pitch={lenina47:2.2,lenina80:2.7,lenina86:2.15,lenina106:2.35}[id]||rise;
      if(id==='lenina80')gableRoof(q[0],q[1],minor+.2,major+.2,p.sp.h+.5,pitch,roof,Math.atan2(edge.dx,edge.dz));
      else hippedRoof(q[0],q[1],major+.2,minor+.2,p.sp.h+.5,pitch,roof,ridgeAngle);
    }else hippedRoof(q[0],q[1],w+.8,d+.8,p.sp.h+.5,rise,id==='cheburov'?palette.roof3:roof,p.a);
    setPart('details');
  }
'''
s=s[:start]+replacement+s[end:]
s=s.replace("    const attic=local(p.x,p.z,p.a,0,-p.d*.12);","")
s=s.replace("    lbox(attic[0],attic[1],p.a,0,p.sp.h+.58,0,p.w*.54,.8,p.d*.34,p.sp.color);","")
sig="export function buildHeritage({"
if sig not in s:raise ValueError("buildHeritage missing")
if "gableRoof," not in s[s.index(sig):s.index("}",s.index(sig))]:s=s.replace(sig,sig+"gableRoof,",1)
p.write_text(s)
city=root/"city.js"
c=city.read_text()
helper='''  function gableRoof(x,z,w,d,base,h,material,a=0,cat='known'){
    const ww=w/2,dd=d/2;
    const pos=[-ww,0,-dd,ww,0,-dd,ww,h,0,-ww,0,-dd,ww,h,0,-ww,h,0,ww,0,dd,-ww,0,dd,-ww,h,0,ww,0,dd,-ww,h,0,ww,h,0,-ww,0,dd,-ww,0,-dd,-ww,h,0,ww,0,-dd,ww,0,dd,ww,h,0];
    for(let i=0;i<pos.length;i+=9)for(let k=0;k<3;k++){const t=pos[i+3+k];pos[i+3+k]=pos[i+6+k];pos[i+6+k]=t;}
    const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));g.computeVertexNormals();push(g,material,x,base,z,1,1,1,a,cat);g.dispose();
  }
'''
if "function gableRoof(" not in c:
 marker="  function lathe("
 if marker not in c:raise ValueError("city insertion point missing")
 c=c.replace(marker,helper+marker,1)
call="buildHeritage({"
if call not in c:raise ValueError("buildHeritage call missing")
if "gableRoof," not in c[c.index(call):c.index("}",c.index(call))]:c=c.replace(call,call+"gableRoof,",1)
city.write_text(c)
app=root/"app.js"
lines=app.read_text().splitlines()
i=next(i for i,line in enumerate(lines) if "  }catch(error){console.error(error);" in line)
lines[i]="  }catch(error){console.error(error);$('loading').hidden=true;$('error').hidden=false;const reason=error instanceof Error?(error.name+': '+error.message):String(error);$('error-message').textContent='Сбой 3D-сцены: '+reason+'. Проверьте доступность WebGL 2 и поддержку аппаратного ускорения.';}"
app.write_text(chr(10).join(lines)+chr(10))
