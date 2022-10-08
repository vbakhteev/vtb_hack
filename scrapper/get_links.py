from bs4 import BeautifulSoup

if __name__ == "__main__":
    for filename in ["social", "education", "industry", "innovation", "green", "futurology", "sharing"]:
        with open(f"rbc_data/{filename}.html", "r") as f:
            content = f.read()
        soup = BeautifulSoup(content)

        link_wrappers = soup.find_all("a", {"class": "item__image js-item-link"})
        links = [elem["href"] for elem in link_wrappers]

        category_wrappers = soup.find_all("div", {"class": "item__category"})
        categories = [wrapper.find("a").getText() for wrapper in category_wrappers]

        with open("rbc_data/rbc_links.txt", "a") as f:
            for link in links:
                f.write(link+"\n")
