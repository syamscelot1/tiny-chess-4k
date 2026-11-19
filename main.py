import json,os,urllib.request as u
V=(0,100,320,330,500,900,0)
A="0123456789abcdefghijk"
PS=["aaaabcc6b98aaaaebbcfccegkkkkaaaa","024426ab4bcd4ade4bde4acd26aa0244","68888baa8ccc8acc8bbc8abc8aaa6888","egcaeeaa866664424220422042204220"]
def ex(s):return[(A.index(s[(x>>4)*4+min(x&7,7-(x&7))])-10)*5 for x in range(128)]
PT=[0]+list(map(ex,PS[:3]))+[[0]*128]*2+[ex(PS[3])]
ZK=[i*2654435761+1 for i in range(1537)]
B=[0]*128;S=1;C=15;E=0;Z=0;K=[4,116];st=[];T={};N=0;NL=50000
X=Exception
KN=(18,33,31,14,-14,-31,-33,-18);BD=(17,15,-17,-15);RD=(1,-1,16,-16);QR=BD+RD
DT=(0,0,KN,BD,RD,QR,QR)
R={0:2,7:1,112:8,119:4,4:3,116:12}
def ad(p,s,n):
 global E,Z
 Z^=ZK[(p-1 if p>0 else 5-p)*128+s]
 q=abs(p)
 if q==6:return
 v=V[q]+(PT[q][s]if p>0 else PT[q][s^112]);E+=n*v if p>0 else -n*v
def ps(s):return ord(s[0])-97+(int(s[1])-1)*16
def post(p,b):
 return json.load(u.urlopen(os.environ["MAKEFUN_ENV_URL"]+p,json.dumps(b).encode()))
def setup():
 global B,S,C,E,Z
 B=[0]*128;E=0;Z=0;st.clear();S=1;C=15;K[0]=4;K[1]=116
 O=(4,2,3,5,6,3,2,4)
 for f in range(8):
  for o,p in((0,O[f]),(112,-O[f]),(16,1),(96,-1)):B[o+f]=p;ad(p,o+f,1)
def att(q,by):
 for o in(-15,-17)if by>0 else(15,17):
  t=q+o
  if not t&0x88 and B[t]==by:return 1
 if any(not(t:=q+o)&136 and B[t]==by*v for D,v in((KN,2),(QR,6))for o in D):return 1
 for j,o in enumerate(QR):
  t=q+o
  while not t&0x88:
   p=B[t]
   if p:
    if p==by*5 or p==by*(3 if j<4 else 4):return 1
    break
   t+=o
 return 0
def pm(m,s,t):
 for pr in(5,4,3,2)if(t>>4)==(7+7*S)//2 else(0,):m.append(s|t<<7|pr<<14)
def gen(c):
 m=[]
 for s in range(128):
  if s&0x88:continue
  p=B[s]
  if p*S<=0:continue
  q=abs(p)
  if q==1:
   d=16*S;t=s+d
   if not t&0x88 and not B[t]:
    if(t>>4)==(7+7*S)//2 or c==0:pm(m,s,t)
    u=s+2*d
    if c==0 and(s>>4)==(7-5*S)//2 and not B[u]:m.append(s|u<<7)
   for t in(s+d+1,s+d-1):
    if not t&0x88 and B[t]*S<0 and abs(B[t])!=6:pm(m,s,t)
  elif q>1:
   for o in DT[q]:
    t=s+o
    while not t&0x88:
     v=B[t]
     if v:
      if v*S<0 and abs(v)!=6:m.append(s|t<<7)
      break
     if c==0:m.append(s|t<<7)
     if q%4==2:break
     t+=o
 if c==0:
  h=4 if S>0 else 116
  for g in(1,-1):
   k=h+2*g
   if C&1<<(g<0)+(S<0)*2 and not(B[h+g] or B[k])and(g>0 or not B[k-1])and not any(att(x,-S)for x in(h,h+g,k)):m.append(h|k<<7)
 return m
def mk(m):
 global S,C,E,Z
 f=m&127;t=m>>7&127;pr=m>>14
 pc=B[f];cap=B[t]
 st.append((B[:],S,C,E,Z,K[0],K[1]))
 B[f]=0;ad(pc,f,-1)
 if cap:ad(cap,t,-1)
 np=pr*S if pr else pc
 B[t]=np;ad(np,t,1)
 if abs(pc)==6:
  K[pc<0]=t
  if abs(t-f)==2:
   rf,rt=(f+3,f+1)if t>f else(f-4,f-1)
   rk=B[rf];B[rf]=0;B[rt]=rk;ad(rk,rf,-1);ad(rk,rt,1)
 C&=~R.get(f,0)&~R.get(t,0)
 Z^=ZK[1536];S=-S
def un():
 global S,C,E,Z
 B[:],S,C,E,Z,K[0],K[1]=st.pop()
def ev():return(E+PT[6][K[0]]-PT[6][K[1]^112])*S
def ok(m):return V[abs(B[(m>>7)&127])]*16-V[abs(B[m&127])]//16+900*(m>>14>0)
def Sr(d,a,b,pl):
 global N
 N+=1
 if N>NL:raise X
 if d<=0:
  s=ev()
  if s>=b:return s
  if s>a:a=s
  ms=gen(1)
  for m in ms:
   mk(m)
   if att(K[S>0],S):un();continue
   s=-Sr(0,-b,-a,pl+1);un()
   if s>=b:return s
   if s>a:a=s
  return a
 if(e:=T.get(Z))and e[0]>=d:return e[1]
 ms=gen(0)
 ms.sort(key=ok,reverse=True)
 bs=-10**9;l=0
 for m in ms:
  mk(m)
  if att(K[S>0],S):un();continue
  l+=1
  s=-Sr(d-1,-b,-a,pl+1);un()
  if s>bs:bs=s
  if s>a:a=s
  if a>=b:break
 if not l:return-1000000+pl if att(K[S<0],-S)else 0
 T[Z]=(d,bs)
 if len(T)>200000:T.clear()
 return bs
def choose(g):
 global N
 setup()
 for mv in g['moves']:mk(ps(mv[:2])|ps(mv[2:4])<<7|("  nbrq".index(mv[4])if len(mv)>4 else 0)<<14)
 ms=gen(0)
 if len(ms)==1:return ms[0]
 bm=ms[0];N=0
 for d in range(64):
  a=-10**9;cm=bm
  try:
   for m in ms:
    mk(m)
    if att(K[S>0],S):un();continue
    s=-Sr(d-1,-10**9,-a,1);un()
    if s>a:a=s;cm=m
  except X:break
  bm=cm
 return bm
def uci(m):
 return sq(m&127)+sq(m>>7&127)+("  nbrq"[m>>14]if m>>14 else'')
def sq(x):return chr(97+x%8)+str(x//16+1)
while(g:=post("/game",{}))["status"]!="done":
 while g["status"]=="your_move":g=post("/move",{"game":g["game"],"move":uci(choose(g))})
