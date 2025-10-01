import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.model import MistralModel

class CompanySummarizer:
    def __init__(self, mistral_model: MistralModel):
        self.mistral = mistral_model
    
    def generate_business_summary(self, company_content):
        """Generate focused business summary for Lucidya value analysis"""
        summary_prompt = f"""
Analyze this company information and create a structured business summary focused on social listening opportunities:

**BUSINESS OVERVIEW:**
- What does the company do? (main products/services)
- What industry are they in?
- Who are their target customers? (B2B, B2C, specific markets)

**BUSINESS MODEL & SCALE:**
- How do they make money?
- What's their value proposition?
- What size/stage company is this? (startup, growth, enterprise)
- What geographic markets do they serve?

**DIGITAL PRESENCE & REPUTATION FACTORS:**
- Do they have customer-facing products that generate online discussions?
- Are they in a competitive/reputation-sensitive industry?
- Do they mention social media, customer feedback, or brand reputation?

**POTENTIAL SOCIAL LISTENING NEEDS:**
- What business challenges would social listening solve?
- Where might they need market intelligence or customer insights?
- What competitive pressures do they face?
- How important is brand reputation management for them?

**LUCIDYA OPPORTUNITY ASSESSMENT:**
- Crisis prevention potential (reputation risks)
- Customer sentiment analysis value
- Competitive intelligence needs
- Market trend monitoring relevance
- ROI potential from social insights

Company Content:
{company_content[:3000]}

Provide a comprehensive business analysis in 400-500 words that identifies specific Lucidya value opportunities.
"""
        
        try:
            summary = self.mistral.chat(summary_prompt)
            return {
                'status': 'success',
                'summary': summary,
                'original_word_count': len(company_content.split()),
                'summary_word_count': len(summary.split())
            }
        except Exception as e:
            return {
                'status': 'failed',
                'error': f"Summary generation failed: {str(e)}",
                'summary': None
            }
