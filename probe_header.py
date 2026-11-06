"""One-off, READ-ONLY: print row 1 of Sheet1 EXACTLY as stored (repr per cell) -
get_all_records keys rows by the RAW header text, so an invisible character in
A1 silently blanks every row's SKU for dict-based readers."""
import json
import os

import gspread
from oauth2client.service_account import ServiceAccountCredentials

SHEET_NAME = os.getenv("SHEET_NAME") or "Arden_Feed_Master"

creds = ServiceAccountCredentials.from_json_keyfile_dict(
    json.loads(os.environ["GOOGLE_CREDENTIALS"]),
    ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"])
book = gspread.authorize(creds).open(SHEET_NAME)
ws = book.worksheet("Sheet1")
raw = ws.get_values("A1:AZ1")
row = raw[0] if raw else []
print(f"row 1 has {len(row)} cell(s)")
for i, c in enumerate(row, start=1):
    print(f"col {i}: {c!r}")
rec = ws.get_all_records(head=1)
if rec:
    keys = list(rec[0].keys())
    print("get_all_records keys:", [repr(k) for k in keys][:30])
    r0 = rec[0]
    print("first row SKU/EAN via dict:", repr(r0.get("SKU")), repr(r0.get("EAN")))
