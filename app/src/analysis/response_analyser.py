import json
from datetime import datetime

class ClientResponseAnalyzer:
    def __init__(self, mistral_model):
        self.mistral = mistral_model
    
    def analyze_response(self, client_email, response_text, company_data):
        """Analyze client response and create summary for human"""
        
        print(f"Analyzing response from: {client_email}")
        
        # Use LLM to classify interest
        interest_analysis = self.classify_interest(response_text)
        
        if interest_analysis['is_interested']:
            # Create human summary
            handoff_summary = self.create_handoff_summary(
                client_email, response_text, company_data, interest_analysis
            )
            
            print("INTERESTED CLIENT - ROUTING TO HUMAN")
            print("-" * 60)
            print(handoff_summary)
            
            return {
                'route_to_human': True,
                'interest_level': interest_analysis['interest_level'],
                'demo_requested': interest_analysis.get('demo_requested', False),
                'handoff_summary': handoff_summary,
                'analysis_timestamp': datetime.utcnow().isoformat()
            }
        else:
            print(f"Client not interested - {interest_analysis['reason']}")
            return {
                'route_to_human': False,
                'interest_level': interest_analysis['interest_level'],
                'reason': interest_analysis['reason'],
                'analysis_timestamp': datetime.utcnow().isoformat()
            }
    
    def classify_interest(self, response_text):
        """Classify client interest using LLM"""
        classification_prompt = f"""
        Analyze this email response and classify interest level:
        
        "{response_text}"
        
        Pay special attention to:
        - Demo requests ("demo", "show me", "presentation", "see it")
        - Meeting requests ("call", "meeting", "schedule", "talk")
        - Urgent language ("ASAP", "this week", "soon", "urgent")
        
        Return JSON:
        {{
            "interest_level": "DEMO_REQUEST/HIGH/MEDIUM/LOW/NOT_INTERESTED",
            "is_interested": true/false,
            "demo_requested": true/false,
            "meeting_intent": true/false,
            "urgency": "HIGH/MEDIUM/LOW",
            "key_signals": ["signal1", "signal2"],
            "reason": "brief explanation"
        }}
        """
        
        try:
            response = self.mistral.generate_response(classification_prompt)
            clean_response = response.strip().replace('``````', '')
            analysis = json.loads(clean_response)
            
            # Special handling for demo requests
            if analysis['interest_level'] == 'DEMO_REQUEST':
                analysis['demo_requested'] = True
                analysis['is_interested'] = True
            
            return analysis
        except Exception as e:
            print(f"Classification error: {e}")
            # Fallback
            return {
                "interest_level": "MEDIUM",
                "is_interested": True,
                "demo_requested": False,
                "meeting_intent": False,
                "urgency": "MEDIUM",
                "key_signals": ["requires_review"],
                "reason": "Could not parse - defaulting to interested for human review"
            }
    
    def create_handoff_summary(self, client_email, response_text, company_data, analysis):
        """Create comprehensive summary for human sales rep"""
        
        company_info = company_data.get('company', {}) if isinstance(company_data, dict) else {}
        
        # Handle case where company_data is from results.json
        if not company_info and company_data.get('company_name'):
            company_info = {
                'name': company_data.get('company_name'),
                'domain': company_data.get('company_domain'),
                'industry': company_data.get('company_industry'),
                'website': company_data.get('url')
            }
        
        urgency_indicator = "🚨🚨 URGENT" if analysis.get('demo_requested') else "⚡ HIGH PRIORITY" if analysis['interest_level'] == 'HIGH' else "📋 STANDARD"
        
        summary = f"""
{urgency_indicator} - INTERESTED PROSPECT
=======================================

CLIENT DETAILS:
Email: {client_email}
Company: {company_info.get('name', 'N/A')} ({company_info.get('domain', 'N/A')})
Website: {company_info.get('website', 'N/A')}
Industry: {company_info.get('industry', 'N/A')}
Size: {company_info.get('employees', 'N/A')} employees
Location: {company_info.get('location', 'N/A')}
Interest Level: {analysis['interest_level']}

COMPANY CONTEXT:
===============
Revenue: {company_info.get('revenue_rank', 'N/A')}
Business Type: {company_info.get('size', 'N/A')}
Products: {', '.join(company_info.get('product_categories', [])) if company_info.get('product_categories') else 'N/A'}

OUR INITIAL OUTREACH:
====================
Summary: {company_data.get('summary', 'No summary available')[:300]}...
Email: {company_data.get('email', 'No email available')[:200]}...
Date: {company_data.get('timestamp', 'N/A')}

CLIENT'S RESPONSE (JUST RECEIVED):
=================================
{response_text}

AI ANALYSIS:
============
Interest Signals: {', '.join(analysis.get('key_signals', []))}
Demo Requested: {'YES - SCHEDULE IMMEDIATELY' if analysis.get('demo_requested') else 'No'}
Meeting Intent: {'Yes' if analysis.get('meeting_intent') else 'No'}
Urgency Level: {analysis.get('urgency', 'Medium')}

RECOMMENDED ACTIONS:
==================
• {"SCHEDULE DEMO WITHIN 24 HOURS" if analysis.get('demo_requested') else "Send detailed product information"}
• {"Respond within 2 hours" if analysis['interest_level'] in ['DEMO_REQUEST', 'HIGH'] else "Respond within 24 hours"}
• Reference their industry: {company_info.get('industry', 'N/A')}
• Mention scale relevance: {company_info.get('employees', 'N/A')} employees
• {"Prepare customized demo" if analysis.get('demo_requested') else "Include relevant case studies"}

REPLY TO: {client_email}
        """
        
        return summary
