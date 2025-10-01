import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.model import MistralModel

# communication/email_generator.py

from models.model import MistralModel

class LucidyaEmailGenerator:
    def __init__(self, mistral_model: MistralModel):
        self.mistral = mistral_model
    
    # REPLACE this method with the enhanced version
    def generate_sales_email(self, company_summary, receptant_name=None):
        """Generate personalized email with Lucidya use cases and Sabahat signature"""
        
        name = receptant_name if receptant_name else 'there'
        
        email_prompt = f"""
Write a professional sales email from Sabahat Ahmed at Lucidya to {name}.

COMPANY ANALYSIS: {company_summary[:1500]}

Include these elements naturally in conversation:

1. SPECIFIC LUCIDYA CAPABILITIES for their business:
- Real-time social media monitoring across 30+ platforms
- Advanced Arabic sentiment analysis (Lucidya's specialty)
- Crisis detection and early warning alerts
- Competitor intelligence and benchmarking
- Customer feedback analysis and insights
- Influencer identification and engagement tracking

2. CONCRETE USE CASES based on their industry:
- Show exactly how they would use Lucidya daily
- Specific scenarios relevant to their business model
- Real examples of insights they'd gain

3. QUANTIFIED BENEFITS:
- Crisis response time reduction (60% faster)
- Customer satisfaction improvement (15-20% increase)
- Brand reputation protection (prevent revenue loss)
- Competitive advantage gains (10-15% market share)

Structure the email naturally:
- Personal greeting referencing their specific business
- Mention a challenge they likely face
- Explain how Lucidya solves it with specific use cases
- Give concrete examples of what they'd see/do
- Quantify the business impact
- Suggest next step

Example use case integration:
"For example, when [specific scenario for their industry], Lucidya would automatically alert you within 15 minutes and provide sentiment analysis in both English and Arabic. You'd see exactly which customers are talking about [relevant topic], their sentiment scores, and suggested response strategies."

Keep it conversational, 250-300 words.

End with Sabahat's signature:
Best regards,
Sabahat Ahmed
Business Development Manager  
Lucidya - Social Listening & Customer Experience
📞 +966 11 454 9797
✉️ sabahat@lucidya.com
🌐 www.lucidya.com
"""
        
        try:
            email = self.mistral.chat(email_prompt)
            return {
                'status': 'success',
                'email': email
            }
        except Exception as e:
            return {
                'status': 'failed',
                'error': f"Email generation failed: {str(e)}",
                'email': None
            }




