from stats_update import update_romanian_stats
from os import environ,sep, curdir
from upload import save_file_from_environ, upload_blob

CREDS_ENV_KEY="GOOGLE_CREDS"
CREDS_FILE=curdir+sep+"google-creds.json"
BUCKET_NAME="romania-covid19-stats"
STATS_PNG_NAME="static/romania_stats.png"
DEST_STATS_PNG_NAME="romania_stats.png"


update_romanian_stats(STATS_PNG_NAME)

save_file_from_environ(CREDS_ENV_KEY, CREDS_FILE)

upload_blob(BUCKET_NAME,STATS_PNG_NAME, DEST_STATS_PNG_NAME, CREDS_FILE)