cd util

python3 initiate.py
sqlite3 -cmd ".read initiate.sql" ".save main.db" ".quit"
mv ".save main.db" "main.db"
rm -rf initiate.sql

cd ..
mv ./util/main.db main.db
rm -rf