"""One-off, READ-ONLY: print every worksheet's SKU column of this store's
sheet, between per-tab BEGIN/END markers - the sheet-side pardon list for
cleanup joins against the shared OnBuy account's live listings (the
Supabase rows_dump can miss rows added to the sheet but never synced).
Reads the sheet only; writes nothing anywhere."""
import json
import os

import gspread
from oauth2client.service_account import ServiceAccountCredentials

SHEET_NAME = os.getenv("SHEET_NAME") or "Arden_Feed_Master"


def main():
    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        json.loads(os.environ["GOOGLE_CREDENTIALS"]),
        ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"])
    book = gspread.authorize(creds).open(SHEET_NAME)
    for tab in book.worksheets():
        headers = [str(x).strip() for x in tab.row_values(1)]
        if "SKU" not in headers:
            print(f"TAB {tab.title}: no SKU column")
            continue
        vals = [str(v).replace(",", "").strip() for v in tab.col_values(headers.index("SKU") + 1)[1:]]
        vals = [v for v in vals if v]
        print(f"TAB {tab.title}: {len(vals)} SKU(s)")
        print(f"BEGIN-SKUS {tab.title}")
        for v in vals:
            print(v)
        print(f"END-SKUS {tab.title}")


if __name__ == "__main__":
    main()
