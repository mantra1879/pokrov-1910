from pathlib import Path
root = Path("_bundle/Pokrov-1910-Public-Site/site")
p = root / "heritage-models.js"
s = p.read_text()
start = s.index("  function roofPart(")
end = s.index("  function fittedRoof", start)
replacement = '''  function roofPart(id,lx,lz,w,d,rise=2.7){
    setBuilding(id);setPart('roof');const p=positions[id],q=local(p.x,p.z,p.a,lx,lz);
    if(id==='lenina80'){
      const points=outlines[id];let edge=null,longest=0;
      for(let i=0;i<points.length;i++){
        const a=points[i],b=points[(i+1)%points.length],dx=b[0]-a[0],dz=b[1]-a[1],len=Math.hypot(dx,dz);
        if(len>longest){longest=len;edge={dx,dz};}
      }
      const major=Math.max(w,d),minor=Math.min(w,d),angle=Math.atan2(-edge.dz,edge.dx);
      gableRoof(q[0],q[1],major+.2,minor+.2,p.sp.h+.5,3.2,roof,angle);
    }else if(id.startsWith('lenina')&&d>w)hippedRoof(q[0],q[1],d+.8,w+.8,p.sp.h+.95,rise,roof,p.a+Math.PI/2);
    else hippedRoof(q[0],q[1],w+.8,d+.8,p.sp.h+.95,rise,roof,p.a);
    setPart('details');
  }
'''
s = s[:start] + replacement + s[end:]
s = s.replace("    const attic=local(p.x,p.z,p.a,0,-p.d*.12);", "")
s = s.replace("    lbox(attic[0],attic[1],p.a,0,p.sp.h+.58,0,p.w*.54,.8,p.d*.34,p.sp.color);", "")
sig = "export function buildHeritage({"
if sig not in s: raise ValueError("buildHeritage signature not found")
if "gableRoof," not in s[s.index(sig):s.index("}",s.index(sig))]: s = s.replace(sig, sig+"gableRoof,", 1)
p.write_text(s)
city = root / "city.js"
c = city.read_text()
call = "buildHeritage({"
if call not in c: raise ValueError("buildHeritage call not found")
if "gableRoof," not in c[c.index(call):c.index("}",c.index(call))]: c = c.replace(call,call+"gableRoof,",1)
city.write_text(c)
app = root / "app.js"
lines = app.read_text().splitlines()
index = next(i for i, line in enumerate(lines) if "  }catch(error){console.error(error);" in line)
lines[index] = "  }catch(error){console.error(error);$('loading').hidden=true;$('error').hidden=false;const reason=error instanceof Error?(error.name+': '+error.message):String(error);$('error-message').textContent='Сбой 3D-сцены: '+reason+'. Проверьте доступность WebGL 2 и поддержку аппаратного ускорения.';}"
app.write_text(chr(10).join(lines)+chr(10))
