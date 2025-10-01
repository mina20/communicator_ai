# # using apollo ai, fetch the company, title, email etc..
# import requests

# class ApolloRetailContacts:
#     """
#     Fetch Retail companies and marketing decision makers from Apollo API.
#     """
#     def __init__(self, api_key):
#         self.api_key = api_key
#         self.base_url = "https://api.apollo.io/v1/companies/search"

#     def fetch_retail_companies_with_marketing(self, page=1, per_page=50):
#         headers = {"Authorization": f"Bearer {self.api_key}"}
#         params = {
#             "industry": "Retail",
#             "page": page,
#             "per_page": per_page
#         }

#         response = requests.get(self.base_url, headers=headers, params=params)
#         if response.status_code != 200:
#             raise Exception(f"Failed to fetch data: {response.status_code} - {response.text}")

#         data = response.json()
#         result = []

#         for company in data.get("companies", []):
#             contacts = company.get("contacts", [])
#             marketing_contacts = [
#                 c for c in contacts if "marketing" in (c.get("title") or "").lower()
#             ]
#             if marketing_contacts:
#                 result.append({
#                     "company_name": company.get("name"),
#                     "company_domain": company.get("domain"),
#                     "contacts": marketing_contacts
#                 })

#         return result


# # Example usage
# if __name__ == "__main__":
#     API_KEY = "YOUR_APOLLO_API_KEY"
#     fetcher = ApolloRetailContacts(API_KEY)

#     retail_marketing_contacts = fetcher.fetch_retail_companies_with_marketing()
#     for company in retail_marketing_contacts:
#         print(f"\nCompany: {company['company_name']} ({company['company_domain']})")
#         for c in company["contacts"]:
#             print(f"  Name: {c['first_name']} {c['last_name']}, Title: {c['title']}, Email: {c['email']}")