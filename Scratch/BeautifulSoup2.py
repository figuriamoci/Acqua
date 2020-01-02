from bs4 import BeautifulSoup
data = """
<div>
<label>Name:</label>
John Smith
</div>
"""
soup = BeautifulSoup(data, "html.parser")
label = soup.find("label", text="Name:")
print(label.next_sibling.strip())