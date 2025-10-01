# communication/response_handler.py
import json
from datetime import datetime


class ResponseHandler:
    def __init__(self, mistral_model, results_file="post_processed_data/results.json"):
        self.mistral = mistral_model
        self.results_file = results_file

    def handle_client_response(self, company_url, client_response):
        """Handle client response and generate simple summary"""
        
        print(f"Processing response for company: {company_url}")

        # Find our conversation using company_url as primary key
        our_conversation = self.find_our_conversation(company_url)
        if not our_conversation:
            return f"No previous conversation found for company URL: {company_url}"
        
        # Check if this is a potential client
        is_potential = self.is_potential_client(client_response)
        
        if is_potential:
            # Generate simple summary using existing data
            summary = self.generate_simple_summary(company_url, our_conversation, client_response)
            return summary
        else:
            return f"Client from {company_url} - Not interested"
    
    def find_our_conversation(self, company_url):
        """Find our conversation history"""
        try:
            with open(self.results_file, 'r') as f:
                all_results = json.load(f)
            
            for record in all_results:
                if record.get('company_url') == company_url:
                    return record
            
            return None
        except Exception as e:
            print("Error loading results:", e)
            return None
    
    def is_potential_client(self, client_response):
        """Check if client shows interest"""
        
        prompt = f"""
        Analyze this client response and determine if they show interest:

        "{client_response}"

        Return only: INTERESTED or NOT_INTERESTED

        Signs of interest: asking questions, wanting demo, curious about features, scheduling meetings
        Signs of no interest: "not interested", "unsubscribe", "wrong company", "no thanks"
        """
        
        try:
            response = self.mistral.generate_response(prompt).strip().upper()
            return "INTERESTED" in response
        except Exception as e:
            print("LLM error:", e)
            return True  # Default to interested for manual review
    def analyze_client_response_for_human(self,client_response):
    
        prompt = f"""
        Analyze this client response and provide specific guidance for a human sales representative on how to respond:

        CLIENT RESPONSE: "{client_response}"

        Please provide:
        1. RESPONSE TYPE: (Question/Meeting Request/Pricing Inquiry/Demo Request/Not Interested/Other)
        2. KEY POINTS: What the client is asking for or interested in
        3. SUGGESTED HUMAN RESPONSE: Specific guidance on how to respond
        4. NEXT ACTIONS: What the human should do (schedule meeting, send pricing, answer questions, etc.)
        5. URGENCY LEVEL: High/Medium/Low

        Format your response clearly for easy reading.
        """
        
        try:

            guidance = self.mistral.chat(prompt)
            return guidance
        except Exception as e:
            return f"Error analyzing response: {e}"

    
    def generate_simple_summary(self, company_url, our_conversation, client_response):
        """Generate simple summary for human"""
        
        summary = f"""
POTENTIAL CLIENT RESPONSE
========================
Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}

COMPANY URL: {company_url}

OUR SUMMARY TO THEM:
{our_conversation.get('summary')}

OUR EMAIL TO THEM:
{our_conversation.get('email')}

THEIR RESPONSE:
{client_response}

ACTION: Human follow-up required
        """
        
        return summary


