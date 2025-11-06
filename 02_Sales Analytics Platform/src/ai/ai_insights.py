"""
AI-powered sales insights and opportunity scoring engine.

This module provides intelligent analysis of sales data using large language models
(OpenAI GPT) or rule-based fallback algorithms. It generates contextual insights,
scores opportunities, and provides actionable recommendations for sales teams.

Features:
- LLM-powered sales trend analysis
- Opportunity scoring with explanations
- Automated insight generation
- Graceful fallback to rule-based scoring when API is unavailable
"""
import os
import logging
import pandas as pd
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("OpenAI package not installed. Using fallback mode.")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

class AIInsightsEngine:
    """
    AI insights engine for sales analytics.
    
    Provides intelligent analysis using LLM or fallback rule-based algorithms.
    Configured via environment variable OPENAI_API_KEY.
    """
    
    def __init__(self, model: str = "gpt-4", temperature: float = 0.2):
        """
        Initialize the AI insights engine.
        
        Args:
            model (str): OpenAI model identifier (default: gpt-4)
            temperature (float): Sampling temperature for response generation (0.0-1.0)
        """
        self.model = model
        self.temperature = temperature
        self.use_llm = OPENAI_AVAILABLE and bool(OPENAI_API_KEY)
        
        if self.use_llm:
            openai.api_key = OPENAI_API_KEY
            logger.info(f"AI Insights Engine initialized with model: {model}")
        else:
            logger.info("AI Insights Engine initialized in fallback mode")

    def generate_sales_insights(self, sales_df: pd.DataFrame) -> str:
        """
        Generate contextual sales insights from transaction data.
        
        Args:
            sales_df (pd.DataFrame): Sales transaction dataset
        
        Returns:
            str: Formatted insights with actionable recommendations
        """
        if self.use_llm:
            try:
                prompt = self._build_sales_prompt(sales_df)
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are an experienced sales analyst providing data-driven insights."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=self.temperature,
                    max_tokens=400
                )
                return response.choices[0].message['content'].strip()
            except Exception as e:
                logger.error(f"LLM insight generation failed: {e}. Using fallback.")
                return self._fallback_sales_insights(sales_df)
        else:
            return self._fallback_sales_insights(sales_df)

    def score_opportunities(self, opp_df: pd.DataFrame) -> List[Dict]:
        """
        Score and rank sales opportunities.
        
        Args:
            opp_df (pd.DataFrame): Opportunity dataset with company, value, stage, activity data
        
        Returns:
            List[Dict]: List of scored opportunities with explanations
        """
        if self.use_llm:
            try:
                prompt = self._build_opportunity_prompt(opp_df)
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a B2B sales strategist specializing in deal qualification."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=self.temperature,
                    max_tokens=400
                )
                return self._parse_llm_opportunity_scores(response.choices[0].message['content'])
            except Exception as e:
                logger.error(f"LLM opportunity scoring failed: {e}. Using fallback.")
                return self._fallback_opportunity_scores(opp_df)
        else:
            return self._fallback_opportunity_scores(opp_df)

    def _build_sales_prompt(self, sales_df: pd.DataFrame) -> str:
        """Build LLM prompt from sales data summary."""
        total_revenue = sales_df['revenue'].sum()
        top_region = sales_df['region'].value_counts().idxmax() if 'region' in sales_df.columns and len(sales_df) > 0 else 'Unknown'
        top_product = sales_df['product_id'].value_counts().idxmax() if 'product_id' in sales_df.columns and len(sales_df) > 0 else 'Unknown'
        
        prompt = f"""Analyze the following sales performance data and provide 3 specific, actionable insights:

Dataset Summary:
- Total Revenue: ${total_revenue:,.0f}
- Top Performing Region: {top_region}
- Best-Selling Product ID: {top_product}
- Transaction Count: {len(sales_df):,}

Provide insights focused on revenue optimization, market opportunities, and operational improvements."""
        return prompt

    def _build_opportunity_prompt(self, opp_df: pd.DataFrame) -> str:
        """Build LLM prompt for opportunity scoring."""
        prompt = "Analyze and score these sales opportunities (scale 1-100) with specific reasoning:\n\n"
        
        for idx, row in opp_df.head(5).iterrows():
            company = row.get('company', 'Unknown Company')
            value = row.get('value', 0)
            stage = row.get('stage', 'Unknown')
            last_activity = row.get('last_activity', 'Unknown')
            
            prompt += f"Opportunity {idx + 1}:\n"
            prompt += f"  Company: {company}\n"
            prompt += f"  Deal Value: ${value:,.0f}\n"
            prompt += f"  Current Stage: {stage}\n"
            prompt += f"  Last Activity: {last_activity}\n\n"
        
        return prompt

    def _parse_llm_opportunity_scores(self, llm_output: str) -> List[Dict]:
        """
        Parse LLM response into structured opportunity scores.
        
        Note: Current implementation returns sample data. In production,
        implement proper parsing of LLM JSON/structured output.
        """
        logger.warning("Using placeholder opportunity scores. Implement structured LLM output parsing.")
        return [
            {"company": "Sample Company", "score": 85, "reason": "High engagement with strong fit profile"}
        ]

    def _fallback_sales_insights(self, sales_df: pd.DataFrame) -> str:
        """Generate rule-based sales insights when LLM is unavailable."""
        if len(sales_df) == 0:
            return "Insufficient data for analysis. Please ensure sales data is loaded."
        
        total_revenue = sales_df['revenue'].sum()
        avg_order = sales_df['revenue'].mean()
        transaction_count = len(sales_df)
        
        insights = []
        insights.append(
            f"1. Total revenue of ${total_revenue:,.0f} from {transaction_count:,} transactions. "
            f"Focus on expanding reach in top-performing regions."
        )
        insights.append(
            f"2. Average order value is ${avg_order:,.0f}. "
            f"Consider product bundling strategies to increase transaction value."
        )
        insights.append(
            "3. Monitor sales pipeline for stalled opportunities in proposal and negotiation stages. "
            "Implement proactive follow-up cadence."
        )
        
        return "\n".join(insights)

    def _fallback_opportunity_scores(self, opp_df: pd.DataFrame) -> List[Dict]:
        """Generate rule-based opportunity scores when LLM is unavailable."""
        results = []
        
        for _, row in opp_df.iterrows():
            value = row.get('value', 0)
            stage = row.get('stage', '')
            last_activity = row.get('last_activity', '')
            company = row.get('company', 'Unknown')
            
            # Simple scoring algorithm
            base_score = min(int(value / 1000), 70)
            
            # Stage-based bonus
            stage_bonus = {
                'Negotiation': 15,
                'Proposal': 10,
                'Qualification': 5,
                'Discovery': 3
            }.get(stage, 0)
            
            # Activity recency bonus
            activity_bonus = 10 if 'today' in last_activity.lower() else 0
            
            final_score = min(base_score + stage_bonus + activity_bonus, 100)
            
            results.append({
                "company": company,
                "score": final_score,
                "reason": f"Scored based on deal value, stage ({stage}), and recent activity"
            })
        
        return results
