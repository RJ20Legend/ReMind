from datetime import datetime

def today_iso():
    return datetime.utcnow().date().isoformat()
