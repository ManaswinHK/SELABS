from xml.sax.saxutils import escape
K = 60
X = lambda x: round(x*K); Y = lambda y: round((13.5-y)*K)
cells = []; nid = [1]
def new():
    nid[0] += 1; return f"c{nid[0]}"
def vtx(x, y, w, h, value, style):
    i = new()
    cells.append(f'<mxCell id="{i}" value="{escape(value, {chr(34): "&quot;"})}" style="{style}" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
    return i
def edge(src, tgt, style):
    i = new()
    cells.append(f'<mxCell id="{i}" style="{style}" edge="1" parent="1" source="{src}" target="{tgt}"><mxGeometry relative="1" as="geometry"/></mxCell>')
def cedge(comp, ball, style, fx, fy):
    edge(comp["id"], ball, style + f"exitX={fx:.4f};exitY={fy:.4f};exitDx=0;exitDy=0;entryX=0.5;entryY=0.5;entryPerimeter=0;")
def flow(x1, y1, x2, y2):
    return
    i = new()
    cells.append(f'<mxCell id="{i}" style="endArrow=block;dashed=1;html=1;strokeColor=#C0392B;strokeWidth=1.5;" edge="1" parent="1"><mxGeometry relative="1" as="geometry"><mxPoint x="{X(x1)}" y="{Y(y1)}" as="sourcePoint"/><mxPoint x="{X(x2)}" y="{Y(y2)}" as="targetPoint"/></mxGeometry></mxCell>')
def text(x, y, value, bold=False, align="left", w=3.2):
    st = f"text;html=1;align={align};verticalAlign=middle;whiteSpace=wrap;fontSize={11 if bold else 10};" + ("fontStyle=1;" if bold else "")
    vtx(X(x)- (X(w)//2 if align=="center" else (X(w) if align=="right" else 0)), Y(y)-12, X(w), 24, value, st)

# title and lanes
vtx(X(1), Y(13.4), X(14), 30, "Telemedicine Slot Booking & Prescription Portal - Microservices Architecture", "text;html=1;align=center;fontSize=18;fontStyle=1;")
vtx(X(1), Y(12.9), X(14), 24, "UML Component Diagram - Set 1: Doctor Discovery & Slot Booking (with payment / notification hand-offs)", "text;html=1;align=center;fontSize=12;fontStyle=2;")
for y0, y1, n in [(10.25,12.4,"Client Tier"),(7.4,10.2,"Edge / API Tier"),(4.2,7.0,"Business Microservices"),(0.45,3.5,"Data & External Systems")]:
    vtx(X(0.3), Y(y1), X(15.4), X(y1-y0), n, "rounded=0;dashed=1;fillColor=none;strokeColor=#888888;align=left;verticalAlign=top;spacingLeft=8;fontStyle=1;fontColor=#555555;html=1;")

H = 1.2
def comp(cx, cy, name, sub, color, W=2.8, stereo="&lt;&lt;component&gt;&gt;"):
    val = f"{stereo}<br><b>{escape(name)}</b><br><i><font style=\"font-size:9px\">{escape(sub)}</font></i>"
    i = vtx(X(cx-W/2), Y(cy+H/2), X(W), X(H), val,
        f"html=1;dropTarget=0;whiteSpace=wrap;shape=module;jettyWidth=16;jettyHeight=8;align=center;fillColor={color};strokeColor=#333333;strokeWidth=2;fontSize=11;")
    return dict(id=i, l=cx-W/2, r=cx+W/2, b=cy-H/2, t=cy+H/2)

APP = comp(8, 11.4, "Patient Web / Mobile App", "Patient actor", "#CFE2F3", 3.6)
GW  = comp(8, 8.6, "API Gateway", "auth, TLS 1.3, routing", "#E6D5F0", 12.0)
SRCH= comp(3.0, 5.3, "Doctor Search Service", "UC-01 / FR-002", "#FFF2CC")
BOOK= comp(8.0, 5.3, "Booking Service", "UC-02 / FR-003", "#FFF2CC", 4.4)
PAY = comp(13.4, 5.3, "Payment Service", "UC-03 hand-off", "#FFF2CC")
DDB = comp(3.0, 1.9, "Doctor Directory DB", "profiles & specialties", "#D9EAD3")
BDB = comp(6.4, 1.9, "Booking & Slot DB", "slots, holds, bookings", "#D9EAD3")
NOT = comp(10.5, 1.9, "Notification Service", "email / SMS confirmation", "#FFF2CC")
EXT = comp(13.4, 1.9, "Payment Gateway", "external system", "#F4CCCC", 2.8, "&lt;&lt;external&gt;&gt;")

BALL = 0.3
def seg(x1, y1, x2, y2, style):
    i = new()
    cells.append(f'<mxCell id="{i}" style="{style}" edge="1" parent="1"><mxGeometry relative="1" as="geometry"><mxPoint x="{X(x1)}" y="{Y(y1)}" as="sourcePoint"/><mxPoint x="{X(x2)}" y="{Y(y2)}" as="targetPoint"/></mxGeometry></mxCell>')
LINE = "endArrow=none;html=1;strokeColor=#000000;strokeWidth=2;"
SOCK = "html=1;endFill=0;strokeColor=#000000;strokeWidth=2;endArrow=halfCircle;endSize=14;"
BALLSTYLE = "ellipse;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;"
RB = BALL/2/ (K/60)
def iface(prov, cons, name, label, kind, pos, lx=0.45):
    """Provider keeps the ball; consumer gets the socket (half-circle) cupping the ball."""
    if kind == "v":
        d = 1 if cons["b"] > prov["t"] else -1
        pe = prov["t"] if d == 1 else prov["b"]
        ce = cons["b"] if d == 1 else cons["t"]
        by = pe + d*0.55
        seg(pos, pe, pos, by, LINE)                 # provider -> ball
        seg(pos, ce, pos, by + d*RB/60*K/K*0.0 + d*0.15, SOCK)   # consumer -> ball surface
        vtx(X(pos)-X(BALL)//2, Y(by)-X(BALL)//2, X(BALL), X(BALL), "", BALLSTYLE)
        text(pos+lx, by+0.1, name, True)
        text(pos+lx, by-0.2, label)
    else:
        d = 1 if cons["l"] > prov["r"] else -1
        pe = prov["r"] if d == 1 else prov["l"]
        ce = cons["l"] if d == 1 else cons["r"]
        by = pos; bx = pe + d*0.55
        seg(pe, by, bx, by, LINE)
        seg(ce, by, bx + d*0.15, by, SOCK)
        vtx(X(bx)-X(BALL)//2, Y(by)-X(BALL)//2, X(BALL), X(BALL), "", BALLSTYLE)
        text(bx, by-0.5, name, True, "center", 2.0)
        text(bx, by-0.8, label, False, "center", 2.4)

iface(GW, APP, "IPatientAPI", "REST / HTTPS (TLS 1.3)", "v", 8.0)
iface(SRCH, GW, "ISearchDoctors", "search requests [REST]", "v", 3.0)
iface(BOOK, GW, "IBooking", "book / confirm slot [REST]", "v", 8.0)
iface(BOOK, SRCH, "IAvailability", "open-slot queries [API]", "h", 5.3)
iface(PAY, BOOK, "IPayment", "payment request [API]", "h", 5.3)
iface(DDB, SRCH, "IDoctorData", "doctor queries [SQL]", "v", 3.0)
iface(BDB, BOOK, "ISlotStore", "slot hold / reserve [SQL]", "v", 6.4)
iface(NOT, BOOK, "INotify", "confirmation [queue]", "v", 9.8)
iface(EXT, PAY, "IGateway", "charge card [HTTPS]", "v", 13.4)

# legend
text(0.5, 0.9, "Ball = provided interface;  Socket (half-circle) = required interface", False, "left", 12)

xml = ('<mxfile host="app.diagrams.net"><diagram name="Component Diagram" id="lab3">'
       '<mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" page="1" pageScale="1" pageWidth="1000" pageHeight="700">'
       '<root><mxCell id="0"/><mxCell id="1" parent="0"/>' + "".join(cells) + '</root></mxGraphModel></diagram></mxfile>')
open("Lab3_Telemedicine_Component_Diagram.drawio", "w", encoding="utf-8").write(xml)
