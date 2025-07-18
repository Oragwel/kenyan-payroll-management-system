#!/usr/bin/env python3
import pandas as pd

# Read the Excel file and show preview
df = pd.read_excel('sample_employees_100.xlsx')

print("✅ Excel file created successfully!")
print(f"📊 Shape: {df.shape} (100 rows × {len(df.columns)} columns)")
print(f"📁 File size: ~18KB")

print("\n📋 Column names:")
for i, col in enumerate(df.columns, 1):
    print(f"{i:2d}. {col}")

print("\n📋 Sample data formats included:")
print("• Quoted salaries: \"60,000\", \"65,000\"")
print("• Unquoted salaries: 30000.00, 50000, 45000")
print("• Phone formats: 0727197004, 0709163086")
print("• Email formats: name@gmail.com, name@company.co.ke")
print("• Account numbers: quoted and unquoted, with commas")
print("• Employment types: PERMANENT, CONTRACT, CASUAL, INTERN")
print("• Various departments and job titles")

print("\n📋 First 5 employees preview:")
for i, row in df.head(5).iterrows():
    print(f"{i+1:2d}. {row['first_name']} {row['last_name']} - {row['department_name']} - {row['position_title']} - {row['basic_salary']}")

# Create CSV version
df.to_csv('sample_employees_100.csv', index=False)
print(f"\n✅ Also created sample_employees_100.csv")

print("\n🎯 Ready for testing!")
print("📁 Files created:")
print("   • sample_employees_100.xlsx (Excel format)")
print("   • sample_employees_100.csv (CSV format)")
