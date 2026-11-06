"""One-off, READ-ONLY: print SKU | Supplier | supplier-URL host | price | stock | Status for every Sheet1 row,
so the suspended listings can be matched to their supplier offline. No cost cells, no writes."""
import json
import os
import re

import gspread
from oauth2client.service_account import ServiceAccountCredentials

SHEET_NAME = os.getenv("SHEET_NAME") or "Arden_Feed_Master"

creds = ServiceAccountCredentials.from_json_keyfile_dict(
    json.loads(os.environ["GOOGLE_CREDENTIALS"]),
    ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"])
ws = gspread.authorize(creds).open(SHEET_NAME).worksheet("Sheet1")
n = 0
for r in ws.get_all_records():
    sku = str(r.get("SKU") or "").replace(",", "").strip()
    if not sku:
        continue
    url = str(r.get("Supplier URL") or "").strip()
    host = (re.search(r"https?://([^/]+)", url) or [None, ""])[1]
    print(f"SUP|{sku}|{str(r.get('Supplier') or '').strip()}|{host}|{r.get('Selling Price (£)')}|{r.get('Stock')}|{str(r.get('Status') or '').strip()}")
    n += 1
print(f"DONE {n} rows")
