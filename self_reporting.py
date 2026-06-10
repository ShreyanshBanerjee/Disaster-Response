from supabase import create_client
from datetime import datetime

now = datetime.now()

url = "{data base url}"
key = "{api token here}"

supabase = create_client(url, key)

#status 1-4/4 indicates occupancy level
def report_occupancy(loc, status):
    data = supabase.table("events").insert({
        "event_date": str(datetime.now()),
        "label": loc,
        "count": status
    }).execute()


def get_occupancy(loc):
    response = supabase.table("events") \
        .select("*") \
        .eq("label", loc) \
        .execute()

    return response.data
