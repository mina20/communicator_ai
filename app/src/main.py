import os, sys
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from models.model import MistralModel
from analysis.extractor import CompanyInfoExtractor
from analysis.summariser import CompanySummarizer
from communication.email_generator import LucidyaEmailGenerator

class LucidyaSalesSystem:
    def __init__(self, api_key, api_url, model="mistral-large-latest"):
        # Initialize core model
        self.mistral = MistralModel(api_key, api_url, model)
        
        # Initialize specialized components
        self.extractor = CompanyInfoExtractor()
        self.summarizer = CompanySummarizer(self.mistral)
        self.email_generator = LucidyaEmailGenerator(self.mistral)
    
    def process_company(self, url):
        """Complete pipeline: Extract → Summarize → Generate Email"""
        print(f"Processing: {url}")
        
        # Step 1: Extract company content
        company_info = self.extractor.extract_company_info(url)
        if not company_info:
            return {'error': 'Failed to extract company information'}
        
        # Step 2: Generate business summary
        summary_result = self.summarizer.generate_business_summary(company_info['about_text'])
        if summary_result['status'] != 'success':
            return {'error': summary_result['error']}
        
        # Step 3: Generate sales email
        email_result = self.email_generator.generate_sales_email(
            summary_result['summary'], 
            url
        )
        
        return {
            'url': url,
            'summary': summary_result['summary'],
            'email': email_result['email'] if email_result['status'] == 'success' else None,
            'status': email_result['status']
        }

# Usage
if __name__ == "__main__":
    system = LucidyaSalesSystem("your-api-key", "your-api-url")
    
    # Test companies
    companies = [
        "https://www.shopify.com/about",
        # "https://www.stripe.com/about"
    ]
    
    for url in companies:
        result = system.process_company(url)
        
        if result.get('status') == 'success':
            print(f"SUCCESS: {url}")
            print("SUMMARY:", result['summary'][:200] + "...")
            print("EMAIL:", result['email'])
        else:
            print(f"ERROR: {result.get('error')}")
        
        print("-" * 80)
