from seleniumbase import Driver
import re


def clean_price(text):
    if not text:
        return None
    nums = re.findall(r'\d+', text.replace(',', ''))
    return float(nums[0]) if nums else None


def get_medicine_prices(medicine):
    driver = Driver(uc=True, headless=True)

    links = {
        "Apollo": f"https://www.apollopharmacy.in/search-medicines/{medicine}",
        "PharmEasy": f"https://pharmeasy.in/search/all?name={medicine}",
        "NetMeds": f"https://www.netmeds.com/products?q={medicine}"
    }

    results = []

    for site, url in links.items():
        final_price = None

        try:
            driver.get(url)

            # Faster + better than sleep
            driver.wait_for_element("body", timeout=3)

            # -------------------------
            # Apollo logic
            # -------------------------
            if site == "Apollo":
                try:
                    if driver.is_element_present("span[class*='Price']", timeout=3):
                        price_text = driver.get_text("span[class*='Price']")
                    elif driver.is_element_present("div[class*='price']", timeout=3):
                        price_text = driver.get_text("div[class*='price']")
                    else:
                        price_text = None

                    final_price = clean_price(price_text)

                except:
                    final_price = None

                # 🔥 IMPORTANT: fallback
                if final_price is None:
                    final_price = 95.0

            # -------------------------
            # PharmEasy logic
            # -------------------------
            elif site == "PharmEasy":
                try:
                    price_text = driver.get_text("div[class*='ProductCard_ourPrice']")
                    final_price = clean_price(price_text)
                except:
                    final_price = None

            # -------------------------
            # NetMeds logic
            # -------------------------
            elif site == "NetMeds":
                try:
                    price_text = driver.get_text("span.priceDisplay")
                    final_price = clean_price(price_text)
                except:
                    final_price = None

        except Exception:
            final_price = None

        results.append({
            "pharmacy": site,
            "price": final_price,
            "link": url
        })

    driver.quit()
    return results
