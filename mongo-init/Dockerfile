FROM mongo

COPY init.json /init.json
CMD mongoimport --host mongo --db streamers --collection col1 --type json --file /init.json --jsonArray
