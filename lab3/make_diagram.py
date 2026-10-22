import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Arc

fig, ax = plt.subplots(figsize=(16, 13.5))
ax.set_xlim(0, 16); ax.set_ylim(0, 13.5); ax.axis("off")
ax.text(8, 13.2, "Telemedicine Slot Booking & Prescription Portal - Microservices Architecture",
        ha="center", fontsize=14, fontweight="bold")
ax.text(8, 12.8, "UML Component Diagram - Set 1: Doctor Discovery & Slot Booking (with payment / notification hand-offs)",
        ha="center", fontsize=10, style="italic")

def lane(y0, y1, name):
    ax.add_patch(Rectangle((0.3, y0), 15.4, y1-y0, fill=False, ec="#888", lw=1.1, ls="--"))
    ax.text(0.45, y1-0.12, name, va="top", fontsize=9, fontweight="bold", color="#555")

H = 1.2
def comp(cx, cy, name, sub, color, W=2.8, stereo="<<component>>"):
    x, y = cx-W/2, cy-H/2
    ax.add_patch(Rectangle((x, y), W, H, fc=color, ec="#333", lw=1.5, zorder=3))
    ix, iy = x+W-0.4, y+H-0.38
    ax.add_patch(Rectangle((ix, iy), 0.26, 0.2, fc=color, ec="#333", lw=1, zorder=4))
    for dy in (0.04, 0.12):
        ax.add_patch(Rectangle((ix-0.07, iy+dy), 0.14, 0.05, fc=color, ec="#333", lw=1, zorder=5))
    ax.text(cx, cy+0.22, stereo, ha="center", fontsize=8, zorder=6)
    ax.text(cx, cy-0.03, name, ha="center", fontsize=10.5, fontweight="bold", zorder=6)
    ax.text(cx, cy-0.34, sub, ha="center", fontsize=7.5, style="italic", zorder=6)
    return dict(l=x, r=x+W, b=y, t=y+H, cx=cx, cy=cy)

R, S = 0.15, 0.27
RED = "#c0392b"
def arrow(x1, y1, x2, y2):
    return
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), zorder=7,
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.2, ls="--"))

def h_iface(prov_edge, cons_edge, y, name, label):
    d = 1 if cons_edge > prov_edge else -1
    bx = prov_edge + d*0.55
    ax.plot([prov_edge, bx-d*R], [y, y], "k", lw=1.5, zorder=2)
    ax.add_patch(Circle((bx, y), R, fc="white", ec="k", lw=1.5, zorder=4))
    th = (270, 90) if d == 1 else (90, 270)
    ax.add_patch(Arc((bx, y), 2*S, 2*S, theta1=th[0], theta2=th[1], lw=1.5, zorder=4))
    ax.plot([bx+d*S, cons_edge], [y, y], "k", lw=1.5, zorder=2)
    ax.text(bx, y-0.5, name, ha="center", fontsize=9, fontweight="bold")
    ax.text(bx, y-0.8, label, ha="center", va="top", fontsize=7.5)
    arrow(bx+d*(S+0.55), y+0.38, bx-d*(S+0.55), y+0.38)   # request flows consumer -> provider

def v_iface(prov_edge, cons_edge, x, name, label, lx=0.45):
    d = 1 if cons_edge > prov_edge else -1
    by = prov_edge + d*0.55
    ax.plot([x, x], [prov_edge, by-d*R], "k", lw=1.5, zorder=2)
    ax.add_patch(Circle((x, by), R, fc="white", ec="k", lw=1.5, zorder=4))
    th = (0, 180) if d == 1 else (180, 360)
    ax.add_patch(Arc((x, by), 2*S, 2*S, theta1=th[0], theta2=th[1], lw=1.5, zorder=4))
    ax.plot([x, x], [by+d*S, cons_edge], "k", lw=1.5, zorder=2)
    ha = "left" if lx > 0 else "right"
    ax.text(x+lx, by+0.1, name, fontsize=9, fontweight="bold", ha=ha)
    ax.text(x+lx, by-0.2, label, fontsize=7.5, va="top", ha=ha)
    my = (cons_edge + (by+d*S))/2
    arrow(x-0.3, by+d*(S+0.55), x-0.3, by+d*0.05) if False else arrow(x-0.3, cons_edge - d*0.0, x-0.3, by) 

# lanes
lane(10.6, 12.4, "Client Tier")
lane(7.4, 10.2, "Edge / API Tier")
lane(4.2, 7.0, "Business Microservices")
lane(0.45, 3.5, "Data & External Systems")

APP = comp(8, 11.4, "Patient Web / Mobile App", "Patient actor", "#cfe2f3", 3.6)
GW  = comp(8, 8.6, "API Gateway", "auth, TLS 1.3, routing", "#e6d5f0", 12.0)
SRCH= comp(3.0, 5.3, "Doctor Search Service", "UC-01 / FR-002", "#fff2cc")
BOOK= comp(8.0, 5.3, "Booking Service", "UC-02 / FR-003", "#fff2cc", 4.4)
PAY = comp(13.4, 5.3, "Payment Service", "UC-03 hand-off", "#fff2cc")
DDB = comp(3.0, 1.9, "Doctor Directory DB", "profiles & specialties", "#d9ead3")
BDB = comp(6.4, 1.9, "Booking & Slot DB", "slots, holds, bookings", "#d9ead3")
NOT = comp(10.5, 1.9, "Notification Service", "email / SMS confirmation", "#fff2cc")
EXT = comp(13.4, 1.9, "Payment Gateway", "external system", "#f4cccc", 2.8, "<<external>>")

# interfaces (provider edge, consumer edge)
v_iface(GW["t"], APP["b"], 8.0, "IPatientAPI", "REST / HTTPS (TLS 1.3)", 0.45)
v_iface(SRCH["t"], GW["b"], 3.0, "ISearchDoctors", "search requests [REST]", 0.45)
v_iface(BOOK["t"], GW["b"], 8.0, "IBooking", "book / confirm slot [REST]", 0.45)
h_iface(BOOK["l"], SRCH["r"], 5.3, "IAvailability", "open-slot queries [API]")
h_iface(PAY["l"], BOOK["r"], 5.3, "IPayment", "payment request [API]")
v_iface(DDB["t"], SRCH["b"], 3.0, "IDoctorData", "doctor queries [SQL]", 0.45)
v_iface(BDB["t"], BOOK["b"], 6.4, "ISlotStore", "slot hold / reserve [SQL]", 0.45)
v_iface(NOT["t"], BOOK["b"], 9.8, "INotify", "confirmation [queue]", 0.45)
v_iface(EXT["t"], PAY["b"], 13.4, "IGateway", "charge card [HTTPS]", 0.45)

# legend
ax.add_patch(Circle((0.9, 0.9), R, fc="white", ec="k", lw=1.3))
ax.text(1.2, 0.9, "provided interface (ball)", va="center", fontsize=8)
ax.add_patch(Arc((4.2, 0.9), 2*S*0.8, 2*S*0.8, theta1=90, theta2=270, lw=1.3))
ax.text(4.5, 0.9, "required interface (socket)", va="center", fontsize=8)

fig.savefig("Lab3_Telemedicine_Component_Diagram.png", dpi=170, bbox_inches="tight")
fig.savefig("Lab3_Telemedicine_Component_Diagram.pdf", bbox_inches="tight")
