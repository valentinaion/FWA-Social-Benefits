"""
Deterministic generator for the FWA demo data estate.
All output is SYNTHETIC — fictitious names, IDs, IBANs, IPs, employers and figures.
Run:  python build_datasets.py   (writes CSVs into ../datasets/)
"""
import csv
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "datasets")
os.makedirs(OUT, exist_ok=True)

# Shared attributes for the coordinated ring (cluster #4471)
RING = dict(
    employer="Northwind Staffing Solutions LLC", cluster="4471",
    src_ip="203.0.113.45", asn="AS64500", asn_type="hosting/vpn",
    device="7f3a9b2e4d1180c1", fps=13.5, session_s=5,
    ua="HeadlessChrome/124.0 (automation)", channel="web",
    reported=0, tax_source="no-record",
)

# id, name, national_id, dob, address, declared, monthly, iban, phone, benefits, submitted
ring_rows = [
    ("A-90412","Andrei Volkov","UT-4471012","1989-03-12","12 Harbor St, Lakeside",18000,1420,"UT99BANK0000004471","+40 711 200 412","unemployment;housing","2026-06-23T14:02:01"),
    ("A-90413","Ivan Petrov","UT-4471013","1991-07-05","12 Harbor St, Lakeside",18500,1380,"UT99BANK0000004471","+40 711 200 413","unemployment","2026-06-23T14:02:03"),
    ("A-90414","Nadia Sokol","UT-4471014","1990-11-20","8 Market Rd, Lakeside",17800,1510,"UT99BANK0000004471","+40 711 999 000","unemployment;housing","2026-06-23T14:02:05"),
    ("A-90415","Radu Marin","UT-4471015","1987-02-28","8 Market Rd, Lakeside",19000,1295,"UT99BANK0000004471","+40 711 200 415","housing","2026-06-23T14:02:06"),
    ("A-90416","Dragan Ilic","UT-4471016","1992-09-09","55 Pine Ave, Lakeside",18200,1460,"UT99BANK0000004471","+40 711 200 416","unemployment","2026-06-23T14:02:08"),
    ("A-90417","Katarina Novak","UT-4471017","1993-05-14","55 Pine Ave, Lakeside",17500,1350,"UT99BANK0000004471","+40 711 999 000","unemployment;housing","2026-06-23T14:02:11"),
    ("A-90418","Sorin Toma","UT-4471018","1988-12-01","9 Dock St, Lakeside",19500,1540,"UT99BANK0000004471","+40 711 200 418","housing","2026-06-23T14:02:13"),
    ("A-90419","Luka Horvat","UT-4471019","1990-06-22","9 Dock St, Lakeside",18800,1400,"UT99BANK0000007788","+40 711 200 419","unemployment","2026-06-23T14:02:15"),
    ("A-90420","Maria Radu","UT-4471020","1991-01-30","9 Dock St, Lakeside",17900,1325,"UT99BANK0000007799","+40 711 200 420","unemployment","2026-06-23T14:02:18"),
]

# Legitimate / control applications (distinct IPs, devices, human cadence, registered employers)
# id, name, nid, dob, address, employer, declared, monthly, iban, phone, benefits, channel, submitted,
#   src_ip, asn, asn_type, device, fps, session_s, ua, reported, tax_source
legit_rows = [
    ("A-88150","Ana Dumitru","UT-8815001","1985-04-17","21 Elm St, Riverton","Tailspin Logistics",26000,980,"UT12BANK0000088150","+40 720 110 150","unemployment","web","2026-06-18T09:14:00","198.51.100.23","AS5618","residential","b21c77ad90e34f02",0.4,242,"Mozilla/5.0 (Windows NT 10.0) Chrome/124.0",26000,"matched"),
    ("A-88176","Mihai Stan","UT-8817601","1979-08-03","4 Oak Ln, Riverton","Contoso Ltd",31000,1050,"UT12BANK0000088176","+40 720 110 176","housing","mobile","2026-06-19T16:40:00","198.51.100.91","AS5618","residential","c0a1d2e3f4b5a6c7",0.5,198,"Mozilla/5.0 (iPhone) Safari/17",31000,"matched"),
    ("A-88204","Elena Marinescu","UT-8820401","1994-02-25","77 Birch Rd, Capital City","Contoso Ltd",24000,1100,"UT12BANK0000088204","+40 720 110 204","unemployment;housing","web","2026-06-22T11:05:00","203.0.113.200","AS8048","residential","aa11bb22cc33dd44",0.6,310,"Mozilla/5.0 (Macintosh) Safari/17",24000,"matched"),
    ("A-88210","Petru Olaru","UT-8821001","1983-10-11","33 Cedar Ave, Capital City","Fabrikam Services SRL",15000,1250,"UT12BANK0000088210","+40 720 110 210","unemployment","web","2026-06-22T15:32:00","198.51.100.140","AS8708","residential","dd44ee55ff660011",0.3,377,"Mozilla/5.0 (Windows NT 10.0) Firefox/126",24200,"mismatch"),
]


def ring_app(r):
    (aid, name, nid, dob, addr, declared, monthly, iban, phone, benefits, submitted) = r
    return dict(id=aid, name=name, nid=nid, dob=dob, addr=addr, employer=RING["employer"],
                declared=declared, monthly=monthly, iban=iban, phone=phone, benefits=benefits,
                channel=RING["channel"], submitted=submitted, cluster=RING["cluster"],
                src_ip=RING["src_ip"], asn=RING["asn"], asn_type=RING["asn_type"], device=RING["device"],
                fps=RING["fps"], session_s=RING["session_s"], ua=RING["ua"],
                reported=RING["reported"], tax_source=RING["tax_source"])


def legit_app(r):
    keys = ["id","name","nid","dob","addr","employer","declared","monthly","iban","phone","benefits",
            "channel","submitted","src_ip","asn","asn_type","device","fps","session_s","ua","reported","tax_source"]
    d = dict(zip(keys, r)); d["cluster"] = ""
    return d


apps = [ring_app(r) for r in ring_rows] + [legit_app(r) for r in legit_rows]


def write(name, header, rows):
    with open(os.path.join(OUT, name), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(header); w.writerows(rows)
    print("wrote", name, f"({len(rows)} rows)")


# applications.csv
write("applications.csv",
      ["application_id","applicant_name","national_id","dob","address","employer",
       "declared_annual_income_eur","monthly_benefit_eur","iban","phone","benefit_types",
       "channel","submitted_at","cluster_id"],
      [[a["id"],a["name"],a["nid"],a["dob"],a["addr"],a["employer"],a["declared"],a["monthly"],
        a["iban"],a["phone"],a["benefits"],a["channel"],a["submitted"],a["cluster"]] for a in apps])

# submission_telemetry.csv
write("submission_telemetry.csv",
      ["application_id","submitted_at","source_ip","asn","asn_type","device_fingerprint",
       "fields_per_second","session_duration_s","user_agent"],
      [[a["id"],a["submitted"],a["src_ip"],a["asn"],a["asn_type"],a["device"],
        a["fps"],a["session_s"],a["ua"]] for a in apps])

# tax_records.csv
def variance(rep, dec):
    if rep == 0:
        return "n/a"
    return f"{round((dec - rep) / rep * 100)}%"
write("tax_records.csv",
      ["national_id","applicant_name","reported_annual_income_eur","declared_annual_income_eur",
       "variance_pct","match","source"],
      [[a["nid"],a["name"],a["reported"],a["declared"],variance(a["reported"],a["declared"]),
        str(a["tax_source"] == "matched").lower(),a["tax_source"]] for a in apps])

# business_registry.csv
write("business_registry.csv",
      ["employer_name","registration_status","vat_id","vat_valid","registered_address","notes"],
      [["Northwind Staffing Solutions LLC","UNREGISTERED","VAT-INVALID","false","Virtual mailbox — 1 Office Park, box 220","No active registration; flagged fictitious"],
       ["Contoso Ltd","ACTIVE","UT-VAT-114829","true","100 Commerce Plaza, Capital City",""],
       ["Fabrikam Services SRL","ACTIVE","UT-VAT-220913","true","44 Industrial Rd, Riverton",""],
       ["Tailspin Logistics","ACTIVE","UT-VAT-336501","true","12 Transit Way, Riverton",""]])

# watchlist.csv
write("watchlist.csv",
      ["indicator_type","value","severity","reason","added"],
      [["ip","203.0.113.45","high","Hosting/VPN ASN linked to coordinated submissions","2026-06-23"],
       ["device_fingerprint","7f3a9b2e4d1180c1","high","Reused across 9 applications","2026-06-23"],
       ["iban","UT99BANK0000004471","high","Shared across 7 applications in cluster #4471","2026-06-23"],
       ["employer","Northwind Staffing Solutions LLC","high","Fictitious/unregistered employer","2026-06-23"],
       ["phone","+40 711 999 000","medium","Shared across 2 applications","2026-06-23"],
       ["asn","AS64500","medium","Hosting/VPN network","2026-06-23"]])

# graph_edges.csv (cluster subgraph — ring applications only)
edges = []
for a in apps:
    if a["cluster"] != "4471":
        continue
    edges.append([a["id"], f"ip:{a['src_ip']}", "ip", "USED_IP"])
    edges.append([a["id"], f"device:{a['device']}", "device", "USED_DEVICE"])
    edges.append([a["id"], "employer:northwind-staffing", "employer", "CLAIMS_EMPLOYER"])
    edges.append([a["id"], f"iban:{a['iban']}", "iban", "USES_IBAN"])
    edges.append([a["id"], f"phone:{a['phone'].replace(' ', '')}", "phone", "USES_PHONE"])
    edges.append([a["id"], f"address:{a['addr']}", "address", "RESIDES_AT"])
write("graph_edges.csv", ["source_id","target_id","target_type","edge_type"], edges)

print("done.")
