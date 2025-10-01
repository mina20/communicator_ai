# systems/lucidya_sales_system.py
import os, sys
import inspect
import json
import uuid
from datetime import datetime

from models.model import MistralModel
from analysis.extractor import CompanyInfoExtractor
from analysis.summariser import CompanySummarizer
from communication.email_generator import LucidyaEmailGenerator
from communication.response_handler import ResponseHandler

class LucidyaSalesSystem:
    def __init__(self, results_file="post_processed_data/results.json"):
        self.mistral = MistralModel()
        self.results_file = results_file
        
        self.extractor = CompanyInfoExtractor()
        self.summarizer = CompanySummarizer(self.mistral)
        self.email_generator = LucidyaEmailGenerator(self.mistral)
        self.response_handler = ResponseHandler(self.mistral, self.results_file)
        self.ensure_results_file()
    
    def ensure_results_file(self):
        os.makedirs(os.path.dirname(self.results_file), exist_ok=True)
        if not os.path.exists(self.results_file):
            with open(self.results_file, 'w') as f:
                json.dump([], f)
    
    def process_company_from_data(self, company_data):
        """Process company using your input format"""
        company_info = company_data.get('company', {})
        website_url = company_info.get('website')
        
        if not website_url:
            return {'error': 'No website URL provided'}
        
        print(f"Processing: {company_info.get('name', 'Unknown')} ({website_url})")
        
        # Process the company
        result = self.process_company(website_url)
        
        if result.get('status') == 'success':
            # Just add the URL for reference
            result['company_url'] = website_url
        
        return result
    
    def process_company(self, url):
        """Core processing pipeline"""
        print(f"Processing: {url}")
        
        # Extract company content
        company_info = self.extractor.extract_company_info(url)
        if not company_info:
            return {'error': 'Failed to extract company information'}
        
        # Generate business summary
        summary_result = self.summarizer.generate_business_summary(company_info['about_text'])
        if summary_result['status'] != 'success':
            return {'error': summary_result['error']}
        
        # Generate sales email
        email_result = self.email_generator.generate_sales_email(
            summary_result['summary']
        )
        
        return {
            'url': url,
            'summary': summary_result['summary'],
            'email': email_result['email'] if email_result['status'] == 'success' else None,
            'status': email_result['status']
        }
    
    def save_processed_company(self, processed_result):
        """Save only essential processing results"""
        if processed_result.get('status') != 'success':
            return False
        
        with open(self.results_file, 'r') as f:
            all_results = json.load(f)
        
        unique_id = str(uuid.uuid4())
        
        # Save only what we generated, not input data
        record = {
            "id": unique_id,
            "company_url": processed_result['url'],  # URL as key
            "summary": processed_result['summary'],
            "email": processed_result['email'],
            "timestamp": datetime.utcnow().isoformat(),
            "status": "email_sent"
        }
        
        all_results.append(record)
        
        with open(self.results_file, 'w') as f:
            json.dump(all_results, f, indent=4)
        
        print(f"Saved processing result for: {processed_result['url']}")
        return True
    
    def find_company_by_url(self, company_url):
        """Find company record by URL"""
        with open(self.results_file, 'r') as f:
            all_results = json.load(f)
        
        for record in all_results:
            if record.get('company_url') == company_url:
                return record
        
        return None
    
    def process_client_response(self, client_email, client_response, company_data_file="company_data.json"):
        """Process client response and identify potential clients"""
        
        summary = self.response_handler.handle_client_response(
            client_email, client_response, company_data_file
        )
        
        print("\n" + "="*50)
        print("CLIENT RESPONSE SUMMARY")
        print("="*50)
        print(summary)
        print("="*50)
        
        return summary

    

