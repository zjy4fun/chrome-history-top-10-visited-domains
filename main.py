import sqlite3
from urllib.parse import urlparse
import matplotlib.pyplot as plt
import tldextract

history_path = './History'
conn = sqlite3.connect(history_path)
cursor = conn.cursor()

cursor.execute('SELECT * FROM urls')
rows = cursor.fetchall()

domain_count = {}
for row in rows:
    url = row[1]
    parsed_url = urlparse(url)
    domain = f"{parsed_url.scheme}://{parsed_url.netloc}"
    extracted = tldextract.extract(domain)
    root_domain = f"{extracted.domain}.{extracted.suffix}"
    if domain.startswith("http://www."):
        root_domain = root_domain.replace("www.", "")
    elif domain.startswith("https://www."):
        root_domain = root_domain.replace("www.", "")
    if domain_count.get(root_domain):
        domain_count[root_domain] += 1
    else:
        domain_count[root_domain] = 1

sorted_domains = sorted(domain_count.items(),
                        key=lambda
                        item: item[1],
                        reverse=True)

sorted_domains = sorted_domains[:10]

domains = [domain for domain, count in sorted_domains]
counts = [count for domain, count in sorted_domains]

plt.bar(domains, counts)
plt.xlabel('domain')
plt.ylabel('visit count')
plt.title('Top 10 visited domains')
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()
cursor.close()
conn.close()
