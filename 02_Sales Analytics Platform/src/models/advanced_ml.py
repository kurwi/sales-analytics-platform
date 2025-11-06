"""
Advanced Machine Learning Models for Sales Forecasting
Enterprise-grade predictive analytics
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score
import joblib
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class SalesForecastingEngine:
    """Enterprise sales forecasting with multiple ML models"""
    
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.feature_importance = {}
        
    def prepare_time_series_features(self, df, date_col='transaction_date', value_col='amount'):
        """Create time series features for forecasting"""
        df = df.copy()
        df[date_col] = pd.to_datetime(df[date_col])
        df = df.sort_values(date_col)
        
        # Aggregate by date
        daily_data = df.groupby(df[date_col].dt.date)[value_col].agg(['sum', 'count', 'mean']).reset_index()
        daily_data.columns = ['date', 'revenue', 'transactions', 'avg_value']
        daily_data['date'] = pd.to_datetime(daily_data['date'])
        
        # Time-based features
        daily_data['year'] = daily_data['date'].dt.year
        daily_data['month'] = daily_data['date'].dt.month
        daily_data['day'] = daily_data['date'].dt.day
        daily_data['dayofweek'] = daily_data['date'].dt.dayofweek
        daily_data['quarter'] = daily_data['date'].dt.quarter
        daily_data['weekofyear'] = daily_data['date'].dt.isocalendar().week
        daily_data['is_month_start'] = daily_data['date'].dt.is_month_start.astype(int)
        daily_data['is_month_end'] = daily_data['date'].dt.is_month_end.astype(int)
        daily_data['is_quarter_start'] = daily_data['date'].dt.is_quarter_start.astype(int)
        daily_data['is_quarter_end'] = daily_data['date'].dt.is_quarter_end.astype(int)
        
        # Lag features
        for lag in [1, 7, 14, 30]:
            daily_data[f'revenue_lag_{lag}'] = daily_data['revenue'].shift(lag)
            daily_data[f'transactions_lag_{lag}'] = daily_data['transactions'].shift(lag)
        
        # Rolling statistics
        for window in [7, 14, 30]:
            daily_data[f'revenue_rolling_mean_{window}'] = daily_data['revenue'].rolling(window).mean()
            daily_data[f'revenue_rolling_std_{window}'] = daily_data['revenue'].rolling(window).std()
            daily_data[f'transactions_rolling_mean_{window}'] = daily_data['transactions'].rolling(window).mean()
        
        # Growth rates
        daily_data['revenue_pct_change'] = daily_data['revenue'].pct_change()
        daily_data['revenue_diff'] = daily_data['revenue'].diff()
        
        return daily_data.dropna()
    
    def train_revenue_forecaster(self, transactions_df, test_size=0.2):
        """Train revenue forecasting model"""
        print("\nTraining Revenue Forecasting Model...")
        
        # Prepare features
        data = self.prepare_time_series_features(transactions_df)
        
        # Select features
        feature_cols = [col for col in data.columns if col not in ['date', 'revenue']]
        X = data[feature_cols]
        y = data['revenue']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, shuffle=False)
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train multiple models
        models = {
            'random_forest': RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42),
            'gradient_boosting': GradientBoostingRegressor(n_estimators=100, max_depth=5, random_state=42),
            'ridge': Ridge(alpha=1.0)
        }
        
        best_score = -np.inf
        best_model_name = None
        
        for name, model in models.items():
            model.fit(X_train_scaled, y_train)
            score = model.score(X_test_scaled, y_test)
            print(f"  {name}: R² = {score:.4f}")
            
            if score > best_score:
                best_score = score
                best_model_name = name
        
        # Save best model
        self.models['revenue_forecaster'] = models[best_model_name]
        self.scalers['revenue_forecaster'] = scaler
        
        # Feature importance (if available)
        if hasattr(models[best_model_name], 'feature_importances_'):
            importance = pd.DataFrame({
                'feature': feature_cols,
                'importance': models[best_model_name].feature_importances_
            }).sort_values('importance', ascending=False)
            self.feature_importance['revenue'] = importance
            print(f"\nTop 5 Important Features:")
            for idx, row in importance.head(5).iterrows():
                print(f"  {row['feature']}: {row['importance']:.4f}")
        
        print(f"\nBest Model: {best_model_name} (R² = {best_score:.4f})")
        
        return {
            'model': models[best_model_name],
            'scaler': scaler,
            'r2_score': best_score,
            'feature_cols': feature_cols
        }
    
    def forecast_revenue(self, transactions_df, days_ahead=30):
        """Generate revenue forecast for specified days"""
        if 'revenue_forecaster' not in self.models:
            raise ValueError("Revenue forecaster not trained. Call train_revenue_forecaster first.")
        
        data = self.prepare_time_series_features(transactions_df)
        last_date = data['date'].max()
        
        forecasts = []
        current_data = data.copy()
        
        for day in range(1, days_ahead + 1):
            forecast_date = last_date + timedelta(days=day)
            
            # Create features for forecast date
            forecast_row = pd.DataFrame({
                'date': [forecast_date],
                'year': [forecast_date.year],
                'month': [forecast_date.month],
                'day': [forecast_date.day],
                'dayofweek': [forecast_date.dayofweek],
                'quarter': [forecast_date.quarter],
                'weekofyear': [forecast_date.isocalendar()[1]],
                'is_month_start': [1 if forecast_date.day == 1 else 0],
                'is_month_end': [1 if forecast_date.day == pd.Timestamp(forecast_date).days_in_month else 0],
                'is_quarter_start': [1 if forecast_date.month in [1, 4, 7, 10] and forecast_date.day == 1 else 0],
                'is_quarter_end': [1 if forecast_date.month in [3, 6, 9, 12] and forecast_date.day == pd.Timestamp(forecast_date).days_in_month else 0],
            })
            
            # Add lag features from current data
            for lag in [1, 7, 14, 30]:
                if len(current_data) >= lag:
                    forecast_row[f'revenue_lag_{lag}'] = current_data.iloc[-lag]['revenue']
                    forecast_row[f'transactions_lag_{lag}'] = current_data.iloc[-lag]['transactions']
                else:
                    forecast_row[f'revenue_lag_{lag}'] = current_data['revenue'].mean()
                    forecast_row[f'transactions_lag_{lag}'] = current_data['transactions'].mean()
            
            # Add rolling statistics
            for window in [7, 14, 30]:
                if len(current_data) >= window:
                    forecast_row[f'revenue_rolling_mean_{window}'] = current_data['revenue'].tail(window).mean()
                    forecast_row[f'revenue_rolling_std_{window}'] = current_data['revenue'].tail(window).std()
                    forecast_row[f'transactions_rolling_mean_{window}'] = current_data['transactions'].tail(window).mean()
                else:
                    forecast_row[f'revenue_rolling_mean_{window}'] = current_data['revenue'].mean()
                    forecast_row[f'revenue_rolling_std_{window}'] = current_data['revenue'].std()
                    forecast_row[f'transactions_rolling_mean_{window}'] = current_data['transactions'].mean()
            
            # Growth rates
            if len(current_data) > 0:
                forecast_row['revenue_pct_change'] = 0
                forecast_row['revenue_diff'] = 0
            
            # Make prediction
            feature_cols = [col for col in forecast_row.columns if col != 'date']
            X_forecast = forecast_row[feature_cols]
            X_forecast_scaled = self.scalers['revenue_forecaster'].transform(X_forecast)
            
            predicted_revenue = self.models['revenue_forecaster'].predict(X_forecast_scaled)[0]
            predicted_revenue = max(0, predicted_revenue)  # Ensure non-negative
            
            forecast = {
                'date': forecast_date,
                'predicted_revenue': predicted_revenue,
                'day_of_forecast': day
            }
            forecasts.append(forecast)
            
            # Update current_data for next iteration
            new_row = forecast_row.copy()
            new_row['revenue'] = predicted_revenue
            new_row['transactions'] = current_data['transactions'].mean()
            new_row['avg_value'] = predicted_revenue / new_row['transactions']
            current_data = pd.concat([current_data, new_row], ignore_index=True)
        
        return pd.DataFrame(forecasts)
    
    def save_models(self, path='models/'):
        """Save trained models"""
        import os
        os.makedirs(path, exist_ok=True)
        
        for name, model in self.models.items():
            joblib.dump(model, f'{path}{name}.pkl')
        
        for name, scaler in self.scalers.items():
            joblib.dump(scaler, f'{path}{name}_scaler.pkl')
        
        print(f"\nModels saved to {path}")
    
    def load_models(self, path='models/'):
        """Load trained models"""
        import os
        
        for file in os.listdir(path):
            if file.endswith('.pkl'):
                name = file.replace('.pkl', '')
                if '_scaler' in name:
                    scaler_name = name.replace('_scaler', '')
                    self.scalers[scaler_name] = joblib.load(f'{path}{file}')
                else:
                    self.models[name] = joblib.load(f'{path}{file}')
        
        print(f"\nModels loaded from {path}")

class ChurnPredictionEngine:
    """Predict customer churn risk"""
    
    def __init__(self):
        self.model = None
        self.scaler = None
        
    def prepare_churn_features(self, companies_df, transactions_df, interactions_df):
        """Create features for churn prediction"""
        # Transaction-based features
        company_stats = transactions_df.groupby('company_id').agg({
            'amount': ['sum', 'mean', 'count'],
            'transaction_date': 'max'
        }).reset_index()
        company_stats.columns = ['company_id', 'total_revenue', 'avg_transaction', 'transaction_count', 'last_transaction']
        
        # Recency (days since last transaction)
        company_stats['days_since_last_transaction'] = (datetime.now() - pd.to_datetime(company_stats['last_transaction'])).dt.days
        
        # Interaction-based features
        interaction_stats = interactions_df.groupby('company_id').agg({
            'satisfaction_score': 'mean',
            'nps_score': 'mean',
            'interaction_id': 'count'
        }).reset_index()
        interaction_stats.columns = ['company_id', 'avg_satisfaction', 'avg_nps', 'interaction_count']
        
        # Merge features
        features = companies_df.merge(company_stats, on='company_id', how='left')
        features = features.merge(interaction_stats, on='company_id', how='left')
        
        # Fill missing values
        features = features.fillna(0)
        
        # Create churn label (based on recency and low satisfaction)
        features['is_churned'] = ((features['days_since_last_transaction'] > 90) & 
                                  (features['avg_satisfaction'] < 3)).astype(int)
        
        return features
    
    def train_churn_model(self, features_df):
        """Train churn prediction model"""
        print("\nTraining Churn Prediction Model...")
        
        # Select features
        feature_cols = ['annual_revenue', 'employees', 'total_revenue', 'avg_transaction', 
                       'transaction_count', 'days_since_last_transaction', 'avg_satisfaction', 
                       'avg_nps', 'interaction_count']
        
        X = features_df[feature_cols]
        y = features_df['is_churned']
        
        # Handle imbalanced data
        from sklearn.utils.class_weight import compute_class_weight
        class_weights = compute_class_weight('balanced', classes=np.unique(y), y=y)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train model
        from sklearn.ensemble import RandomForestClassifier
        model = RandomForestClassifier(n_estimators=100, max_depth=10, class_weight='balanced', random_state=42)
        model.fit(X_train_scaled, y_train)
        
        # Evaluate
        train_score = model.score(X_train_scaled, y_train)
        test_score = model.score(X_test_scaled, y_test)
        
        print(f"  Training Accuracy: {train_score:.4f}")
        print(f"  Test Accuracy: {test_score:.4f}")
        
        # Feature importance
        importance = pd.DataFrame({
            'feature': feature_cols,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print(f"\nTop 5 Churn Indicators:")
        for idx, row in importance.head(5).iterrows():
            print(f"  {row['feature']}: {row['importance']:.4f}")
        
        self.model = model
        self.scaler = scaler
        
        return {
            'model': model,
            'scaler': scaler,
            'accuracy': test_score,
            'feature_importance': importance
        }
    
    def predict_churn_risk(self, features_df):
        """Predict churn risk for companies"""
        if self.model is None:
            raise ValueError("Churn model not trained. Call train_churn_model first.")
        
        feature_cols = ['annual_revenue', 'employees', 'total_revenue', 'avg_transaction', 
                       'transaction_count', 'days_since_last_transaction', 'avg_satisfaction', 
                       'avg_nps', 'interaction_count']
        
        X = features_df[feature_cols].fillna(0)
        X_scaled = self.scaler.transform(X)
        
        churn_probabilities = self.model.predict_proba(X_scaled)[:, 1]
        churn_predictions = self.model.predict(X_scaled)
        
        results = features_df[['company_id', 'company_name']].copy()
        results['churn_probability'] = churn_probabilities
        results['churn_prediction'] = churn_predictions
        results['risk_level'] = pd.cut(churn_probabilities, bins=[0, 0.3, 0.7, 1.0], labels=['Low', 'Medium', 'High'])
        
        return results.sort_values('churn_probability', ascending=False)

if __name__ == "__main__":
    print("Advanced ML Models Module - Ready for Enterprise Deployment")
