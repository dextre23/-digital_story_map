import json
with open('data/cached_books.json', encoding='utf-8') as f:
    data = json.load(f)
print(f"Total: {len(data)} entries")
print("---")
for b in data[:3]:
    print(f'{b["id"]}: {b["title"]} - {b["author"]} ({b["publication_year"]}) [{b["city"]}]')
print("...")
for b in data[-3:]:
    print(f'{b["id"]}: {b["title"]} - {b["author"]} ({b["publication_year"]}) [{b["city"]}]')
fictional = [b for b in data if "kurgu" in b.get("genre", "")]
print(f"---")
print(f"Fictional entries: {len(fictional)}")
years = [b["publication_year"] for b in data]
print(f"Min year: {min(years)}, Max year: {max(years)}")
print(f"All post-1922: {all(y >= 1922 for y in years)}")
