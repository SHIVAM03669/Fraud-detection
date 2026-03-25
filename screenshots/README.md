# Screenshots Directory

This directory contains screenshots of the fraud detection system interface.

## Required Screenshots

To complete the README documentation, please add the following screenshots:

### 1. dashboard-main.png
- Main dashboard interface showing the title and transaction input buttons
- Should show "Load Sample Data", "Generate Random Transaction", and "Load Fraud Example" buttons
- Include the transaction details form with Time and Amount fields

### 2. legitimate-transaction.png
- Screenshot showing a legitimate transaction result
- Should display green "Legit Transaction" message
- Show low fraud probability (< 5%)
- Include "Very Low Risk" indicator

### 3. fraud-detection.png
- Screenshot showing a fraudulent transaction result
- Should display red "Fraud Detected!" message
- Show high fraud probability (> 50%)
- Include "High Risk" indicator

### 4. risk-levels.png
- Screenshot showing different risk level indicators
- Can be a composite image showing various risk levels:
  - Very Low Risk (green)
  - Low Risk (yellow)
  - Medium Risk (orange)
  - High Risk (red)

### 5. batch-processing.png
- Screenshot of the CSV upload section
- Show file upload interface
- Display batch processing results table
- Include "Download Results" button

### 6. sample-downloads.png
- Screenshot of the sample files download section
- Show both "Download Legitimate Sample" and "Download Fraudulent Sample" buttons
- Include the tip message about expected probabilities

## How to Take Screenshots

1. **Start the application**:
   ```bash
   streamlit run dashboard/app.py
   ```

2. **Navigate to** http://localhost:8501

3. **Take screenshots** of each section mentioned above

4. **Save images** in this directory with the exact filenames listed

5. **Recommended image format**: PNG for best quality

6. **Recommended resolution**: 1920x1080 or higher

## Image Guidelines

- Use a consistent browser and theme
- Ensure text is clearly readable
- Crop images to show relevant content
- Keep file sizes reasonable (< 2MB each)
- Use descriptive filenames as specified above

## Alternative Screenshot Names

If you prefer different naming, update the image references in README.md accordingly:

```markdown
![Description](screenshots/your-filename.png)
```

The current README.md expects these exact filenames:
- dashboard-main.png
- legitimate-transaction.png
- fraud-detection.png
- risk-levels.png
- batch-processing.png
- sample-downloads.png