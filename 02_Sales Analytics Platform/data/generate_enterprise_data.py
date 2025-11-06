"""
Enterprise Sales Analytics Platform
Professional-grade sales dashboard with advanced analytics and ML forecasting
Version: 1.0.0
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
from pathlib import Path

class EnterpriseSalesDataGenerator:
    """Enterprise-grade sales data generator with realistic business patterns"""
    
    def __init__(self, seed=42):
        np.random.seed(seed)
        self.industries = ['Technology', 'Healthcare', 'Retail', 'Finance', 'Manufacturing']
        self.company_sizes = ['Enterprise', 'Mid-Market', 'SMB', 'Startup']
        self.regions = ['North America', 'Europe', 'Asia Pacific', 'Latin America', 'Middle East']
        self.sales_stages = ['Prospecting', 'Qualification', 'Proposal', 'Negotiation', 'Closed Won', 'Closed Lost']
        self.product_categories = ['Software License', 'Professional Services', 'Support & Maintenance', 'Training', 'Hardware']
        
    def generate_companies(self, n_companies=500):
        """Generate company master data"""
        companies = []
        for i in range(n_companies):
            company = {
                'company_id': f'COMP{i+1:05d}',
                'company_name': f'Company {chr(65 + i % 26)}{i+1}',
                'industry': np.random.choice(self.industries),
                'company_size': np.random.choice(self.company_sizes, p=[0.1, 0.3, 0.4, 0.2]),
                'region': np.random.choice(self.regions),
                'country': self._get_country_for_region(np.random.choice(self.regions)),
                'annual_revenue': np.random.randint(1_000_000, 500_000_000),
                'employees': np.random.randint(10, 10000),
                'created_date': datetime(2020, 1, 1) + timedelta(days=np.random.randint(0, 1460)),
                'customer_since': None,
                'ltv_estimate': 0,
                'churn_risk': np.random.uniform(0, 1)
            }
            companies.append(company)
        
        return pd.DataFrame(companies)
    
    def generate_sales_team(self, n_reps=50):
        """Generate sales team data"""
        reps = []
        for i in range(n_reps):
            rep = {
                'rep_id': f'REP{i+1:04d}',
                'rep_name': f'{self._get_first_name()} {self._get_last_name()}',
                'role': np.random.choice(['AE', 'SDR', 'Manager', 'Director'], p=[0.5, 0.3, 0.15, 0.05]),
                'region': np.random.choice(self.regions),
                'hire_date': datetime(2018, 1, 1) + timedelta(days=np.random.randint(0, 2190)),
                'quota': np.random.randint(500_000, 5_000_000),
                'performance_rating': np.random.uniform(2.5, 5.0),
                'years_experience': np.random.randint(1, 15)
            }
            reps.append(rep)
        
        return pd.DataFrame(reps)
    
    def generate_products(self, n_products=100):
        """Generate product catalog"""
        products = []
        for i in range(n_products):
            category = np.random.choice(self.product_categories)
            base_price = self._get_base_price(category)
            
            product = {
                'product_id': f'PROD{i+1:04d}',
                'product_name': f'{category} - {self._get_product_tier()} Tier',
                'category': category,
                'tier': np.random.choice(['Basic', 'Professional', 'Enterprise'], p=[0.3, 0.5, 0.2]),
                'list_price': base_price * np.random.uniform(0.8, 1.5),
                'cost': base_price * np.random.uniform(0.2, 0.4),
                'margin_pct': np.random.uniform(40, 80),
                'recurring': category in ['Software License', 'Support & Maintenance'],
                'contract_term': np.random.choice([12, 24, 36]) if category == 'Software License' else 0,
                'active': True
            }
            products.append(product)
        
        return pd.DataFrame(products)
    
    def generate_opportunities(self, companies_df, reps_df, products_df, n_opportunities=2000):
        """Generate sales opportunities with realistic pipeline"""
        opportunities = []
        start_date = datetime(2023, 1, 1)
        
        for i in range(n_opportunities):
            company = companies_df.sample(1).iloc[0]
            rep = reps_df[reps_df['region'] == company['region']].sample(1).iloc[0] if len(reps_df[reps_df['region'] == company['region']]) > 0 else reps_df.sample(1).iloc[0]
            product = products_df.sample(1).iloc[0]
            
            created = start_date + timedelta(days=np.random.randint(0, 730))
            stage = np.random.choice(self.sales_stages, p=[0.15, 0.2, 0.2, 0.15, 0.2, 0.1])
            
            # Realistic deal sizing
            base_value = product['list_price'] * np.random.uniform(1, 20)
            discount_pct = self._get_discount_for_stage(stage)
            
            opp = {
                'opportunity_id': f'OPP{i+1:06d}',
                'company_id': company['company_id'],
                'rep_id': rep['rep_id'],
                'product_id': product['product_id'],
                'opportunity_name': f"{company['company_name']} - {product['product_name']}",
                'stage': stage,
                'amount': base_value * (1 - discount_pct),
                'probability': self._get_probability_for_stage(stage),
                'expected_value': base_value * (1 - discount_pct) * self._get_probability_for_stage(stage),
                'created_date': created,
                'close_date': created + timedelta(days=np.random.randint(30, 180)),
                'actual_close_date': created + timedelta(days=np.random.randint(30, 180)) if stage in ['Closed Won', 'Closed Lost'] else None,
                'days_in_stage': np.random.randint(1, 90),
                'forecast_category': self._get_forecast_category(stage),
                'lead_source': np.random.choice(['Inbound', 'Outbound', 'Partner', 'Event', 'Referral']),
                'competitor': np.random.choice(['Competitor A', 'Competitor B', 'Competitor C', 'None'], p=[0.2, 0.2, 0.15, 0.45])
            }
            opportunities.append(opp)
        
        return pd.DataFrame(opportunities)
    
    def generate_activities(self, opportunities_df, reps_df, n_activities=10000):
        """Generate sales activities (calls, emails, meetings)"""
        activities = []
        activity_types = ['Call', 'Email', 'Meeting', 'Demo', 'Proposal Sent']
        
        for i in range(n_activities):
            opp = opportunities_df.sample(1).iloc[0]
            activity_date = opp['created_date'] + timedelta(days=np.random.randint(0, 60))
            
            activity = {
                'activity_id': f'ACT{i+1:07d}',
                'opportunity_id': opp['opportunity_id'],
                'rep_id': opp['rep_id'],
                'activity_type': np.random.choice(activity_types),
                'activity_date': activity_date,
                'duration_minutes': np.random.randint(5, 120),
                'outcome': np.random.choice(['Positive', 'Neutral', 'Negative'], p=[0.5, 0.3, 0.2]),
                'notes': f"Activity notes for {opp['opportunity_name']}",
                'next_steps': np.random.choice(['Follow up', 'Send proposal', 'Schedule demo', 'None'])
            }
            activities.append(activity)
        
        return pd.DataFrame(activities)
    
    def generate_revenue_transactions(self, opportunities_df):
        """Generate actual revenue transactions from closed-won deals"""
        won_opps = opportunities_df[opportunities_df['stage'] == 'Closed Won'].copy()
        transactions = []
        
        for idx, opp in won_opps.iterrows():
            # Initial payment
            trans = {
                'transaction_id': f'TXN{len(transactions)+1:07d}',
                'opportunity_id': opp['opportunity_id'],
                'company_id': opp['company_id'],
                'transaction_date': opp['actual_close_date'],
                'amount': opp['amount'],
                'revenue_type': 'New Business',
                'payment_terms': np.random.choice(['Net 30', 'Net 60', 'Net 90']),
                'payment_status': np.random.choice(['Paid', 'Pending', 'Overdue'], p=[0.7, 0.2, 0.1]),
                'invoice_number': f'INV{len(transactions)+1:07d}',
                'fiscal_quarter': f"Q{((opp['actual_close_date'].month-1)//3)+1}",
                'fiscal_year': opp['actual_close_date'].year
            }
            transactions.append(trans)
            
            # Recurring revenue if applicable
            if np.random.random() > 0.5:  # 50% have recurring
                for month in range(1, 13):
                    recurring_date = opp['actual_close_date'] + timedelta(days=30*month)
                    trans_recurring = {
                        'transaction_id': f'TXN{len(transactions)+1:07d}',
                        'opportunity_id': opp['opportunity_id'],
                        'company_id': opp['company_id'],
                        'transaction_date': recurring_date,
                        'amount': opp['amount'] * 0.2,  # 20% of original as recurring
                        'revenue_type': 'Recurring',
                        'payment_terms': 'Net 30',
                        'payment_status': np.random.choice(['Paid', 'Pending'], p=[0.9, 0.1]),
                        'invoice_number': f'INV{len(transactions)+1:07d}',
                        'fiscal_quarter': f"Q{((recurring_date.month-1)//3)+1}",
                        'fiscal_year': recurring_date.year
                    }
                    transactions.append(trans_recurring)
        
        return pd.DataFrame(transactions)
    
    def generate_customer_interactions(self, companies_df, n_interactions=5000):
        """Generate customer support and success interactions"""
        interactions = []
        interaction_types = ['Support Ticket', 'Success Check-in', 'Escalation', 'Feature Request', 'Training']
        
        for i in range(n_interactions):
            company = companies_df.sample(1).iloc[0]
            
            interaction = {
                'interaction_id': f'INT{i+1:07d}',
                'company_id': company['company_id'],
                'interaction_type': np.random.choice(interaction_types),
                'interaction_date': datetime(2023, 1, 1) + timedelta(days=np.random.randint(0, 730)),
                'priority': np.random.choice(['Low', 'Medium', 'High', 'Critical'], p=[0.4, 0.3, 0.2, 0.1]),
                'status': np.random.choice(['Open', 'In Progress', 'Resolved', 'Closed'], p=[0.1, 0.2, 0.3, 0.4]),
                'resolution_time_hours': np.random.randint(1, 120),
                'satisfaction_score': np.random.randint(1, 6),
                'nps_score': np.random.randint(-100, 101)
            }
            interactions.append(interaction)
        
        return pd.DataFrame(interactions)
    
    def generate_complete_dataset(self):
        """Generate complete enterprise dataset"""
        print("Generating Enterprise Sales Data...")
        print("=" * 60)
        
        print("\n[1/7] Generating companies...")
        companies = self.generate_companies(500)
        print(f"  Created: {len(companies):,} companies")
        
        print("\n[2/7] Generating sales team...")
        reps = self.generate_sales_team(50)
        print(f"  Created: {len(reps):,} sales representatives")
        
        print("\n[3/7] Generating products...")
        products = self.generate_products(100)
        print(f"  Created: {len(products):,} products")
        
        print("\n[4/7] Generating opportunities...")
        opportunities = self.generate_opportunities(companies, reps, products, 2000)
        print(f"  Created: {len(opportunities):,} sales opportunities")
        
        print("\n[5/7] Generating activities...")
        activities = self.generate_activities(opportunities, reps, 10000)
        print(f"  Created: {len(activities):,} sales activities")
        
        print("\n[6/7] Generating revenue transactions...")
        transactions = self.generate_revenue_transactions(opportunities)
        print(f"  Created: {len(transactions):,} revenue transactions")
        
        print("\n[7/7] Generating customer interactions...")
        interactions = self.generate_customer_interactions(companies, 5000)
        print(f"  Created: {len(interactions):,} customer interactions")
        
        # Save all datasets
        print("\nSaving datasets...")
        companies.to_csv('data/raw/companies.csv', index=False)
        reps.to_csv('data/raw/sales_reps.csv', index=False)
        products.to_csv('data/raw/products.csv', index=False)
        opportunities.to_csv('data/raw/opportunities.csv', index=False)
        activities.to_csv('data/raw/activities.csv', index=False)
        transactions.to_csv('data/raw/transactions.csv', index=False)
        interactions.to_csv('data/raw/customer_interactions.csv', index=False)
        
        # Generate summary statistics
        summary = {
            'generated_date': datetime.now().isoformat(),
            'total_companies': len(companies),
            'total_reps': len(reps),
            'total_products': len(products),
            'total_opportunities': len(opportunities),
            'total_pipeline_value': float(opportunities['amount'].sum()),
            'total_revenue': float(transactions['amount'].sum()),
            'avg_deal_size': float(opportunities[opportunities['stage'] == 'Closed Won']['amount'].mean()),
            'win_rate': float(len(opportunities[opportunities['stage'] == 'Closed Won']) / len(opportunities[opportunities['stage'].isin(['Closed Won', 'Closed Lost'])]) * 100),
        }
        
        with open('data/raw/data_summary.json', 'w') as f:
            json.dump(summary, f, indent=2)
        
        print("\n" + "=" * 60)
        print("ENTERPRISE DATA GENERATION COMPLETE")
        print("=" * 60)
        print(f"\nTotal Pipeline Value: ${summary['total_pipeline_value']:,.2f}")
        print(f"Total Revenue: ${summary['total_revenue']:,.2f}")
        print(f"Average Deal Size: ${summary['avg_deal_size']:,.2f}")
        print(f"Win Rate: {summary['win_rate']:.1f}%")
        
        return {
            'companies': companies,
            'reps': reps,
            'products': products,
            'opportunities': opportunities,
            'activities': activities,
            'transactions': transactions,
            'interactions': interactions
        }
    
    # Helper methods
    def _get_country_for_region(self, region):
        countries = {
            'North America': ['USA', 'Canada', 'Mexico'],
            'Europe': ['UK', 'Germany', 'France', 'Spain', 'Italy'],
            'Asia Pacific': ['Japan', 'China', 'Australia', 'Singapore', 'India'],
            'Latin America': ['Brazil', 'Argentina', 'Chile', 'Colombia'],
            'Middle East': ['UAE', 'Saudi Arabia', 'Israel']
        }
        return np.random.choice(countries.get(region, ['Unknown']))
    
    def _get_first_name(self):
        names = ['John', 'Sarah', 'Michael', 'Emily', 'David', 'Jessica', 'Robert', 'Lisa', 'James', 'Mary']
        return np.random.choice(names)
    
    def _get_last_name(self):
        names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']
        return np.random.choice(names)
    
    def _get_base_price(self, category):
        prices = {
            'Software License': 50000,
            'Professional Services': 150,  # per hour
            'Support & Maintenance': 10000,
            'Training': 5000,
            'Hardware': 25000
        }
        return prices.get(category, 10000)
    
    def _get_product_tier(self):
        return np.random.choice(['Basic', 'Professional', 'Enterprise'])
    
    def _get_discount_for_stage(self, stage):
        discounts = {
            'Prospecting': 0,
            'Qualification': 0,
            'Proposal': 0.1,
            'Negotiation': 0.15,
            'Closed Won': 0.2,
            'Closed Lost': 0
        }
        return discounts.get(stage, 0)
    
    def _get_probability_for_stage(self, stage):
        probabilities = {
            'Prospecting': 0.1,
            'Qualification': 0.25,
            'Proposal': 0.5,
            'Negotiation': 0.75,
            'Closed Won': 1.0,
            'Closed Lost': 0.0
        }
        return probabilities.get(stage, 0.5)
    
    def _get_forecast_category(self, stage):
        if stage == 'Closed Won':
            return 'Closed'
        elif stage in ['Negotiation']:
            return 'Commit'
        elif stage in ['Proposal']:
            return 'Best Case'
        elif stage in ['Qualification']:
            return 'Pipeline'
        else:
            return 'Excluded'

if __name__ == "__main__":
    generator = EnterpriseSalesDataGenerator(seed=42)
    datasets = generator.generate_complete_dataset()
