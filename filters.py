# filters.py
DEFAULT_FILTERS = {
    "keywords": "",
    "location": "",
    "date_posted": "any",         # "any", "1", "3", "7", "14"
    "job_type": [],
    "company": "",
    "remote": False,
}

def merge_filters(user_filters):
    filters = DEFAULT_FILTERS.copy()
    filters.update({k:v for k,v in user_filters.items() if v is not None})
    return filters