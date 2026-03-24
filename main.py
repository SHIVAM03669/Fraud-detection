from pipeline.cleaning import run_cleaning_pipeline
from pipeline.feature_engineering import add_features
from models.train import split_data, create_validation_split
from models.train import train_models, evaluate
from models.save_model import save_model

# Run pipeline
print("Running data pipeline...")
df = run_cleaning_pipeline("data/raw/fraud.csv")
df = add_features(df)

print(f"Dataset shape: {df.shape}")
print(f"Class distribution:\n{df['Class'].value_counts()}")
print(f"Fraud rate: {df['Class'].mean():.4f}")

# Split data with stratification
X_train, X_test, y_train, y_test = split_data(df)

# Create validation split for calibration (from training data)
X_train_fit, X_val, y_train_fit, y_val = create_validation_split(X_train, y_train)

print(f"\nData splits:")
print(f"Training: {X_train_fit.shape[0]} samples")
print(f"Validation: {X_val.shape[0]} samples") 
print(f"Test: {X_test.shape[0]} samples")

# Train models with calibration (no SMOTE needed)
print("\nStarting training with class balancing and calibration...")
models = train_models(X_train_fit, y_train_fit, X_val, y_val)
print("Training finished")

# Evaluate models
evaluate(models, X_test, y_test)

# Save the best model (logistic regression with calibration)
best_model = models["logistic"]
save_model(best_model)

print(f"\nModel saved! Feature order: {list(df.drop('Class', axis=1).columns)}")