import matplotlib.pyplot as plt
import io
import base64
from decimal import Decimal

# Function to calculate export duties in India
def calculate_export_duty(value_in_inr):
    BCD_rate = Decimal('25')  # Basic Customs Duty rate in India
    IGST_rate = Decimal('18')  # Integrated GST rate in India
    SWS_rate = Decimal('10')  # Social Welfare Surcharge rate as a percentage of BCD

    # Calculate duties
    BCD = (value_in_inr * BCD_rate) / Decimal('100')
    SWS = (BCD * SWS_rate) / Decimal('100')
    IGST = (value_in_inr * IGST_rate) / Decimal('100')
    total_export_duty = BCD + SWS + IGST

    return total_export_duty

# Function to calculate import costs in Germany
def calculate_import_cost(value_in_eur, shipping_cost, vat_rate=19):
    vat_rate = Decimal(vat_rate)
    value_in_eur = Decimal(value_in_eur)
    shipping_cost = Decimal(shipping_cost)

    # Import duties and taxes in Germany
    if value_in_eur > Decimal('150'):
        import_duty = value_in_eur * Decimal('0.1')  # Assuming 10% duty (replace with actual data)
    else:
        import_duty = Decimal('0')

    import_vat = value_in_eur * (vat_rate / Decimal('100'))
    total_import_cost = value_in_eur + shipping_cost + import_duty + import_vat
    return total_import_cost

# Function to calculate total cost
def calculate_total_cost(value_in_inr, value_in_eur, shipping_cost, vat_rate=19):
    value_in_inr = Decimal(value_in_inr)
    value_in_eur = Decimal(value_in_eur)
    shipping_cost = Decimal(shipping_cost)

    export_duty = calculate_export_duty(value_in_inr)
    import_cost = calculate_import_cost(value_in_eur, shipping_cost, vat_rate)

    total_cost = export_duty + import_cost
    return total_cost, export_duty, shipping_cost, import_cost

# Function to create and save the donut chart
def create_donut_chart(export_duty, shipping_cost_inr, import_cost, output_file="cost_breakdown.png"):
    labels = ['Export Duty (India)', 'Shipping Costs', 'Import Duty (Germany)', 'Import VAT (Germany)', 'Excise Duty']
    sizes = [
        float(export_duty),
        float(shipping_cost_inr) * 85,
        float(import_cost) * 0.1,
        float(import_cost) * 0.19,
        0
    ]
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0']

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(
        sizes,
        labels=labels,
        colors=colors,
        autopct='%1.1f%%',
        startangle=90,
        wedgeprops=dict(width=0.4)
    )
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.savefig(output_file)
    print(f"Donut chart saved to {output_file}")

# Main function to handle user input and process data
def main():
    print("=== Import/Export Cost Calculator ===")
    value_in_inr = Decimal(input("Enter the value in INR for export: "))
    value_in_eur = Decimal(input("Enter the value in EUR for import: "))
    shipping_cost = Decimal(input("Enter the shipping cost in EUR: "))
    vat_rate = Decimal(input("Enter the VAT rate in Germany (default 19%): ") or "19")

    # Perform calculations
    total_cost, export_duty, shipping_cost_inr, import_cost = calculate_total_cost(
        value_in_inr, value_in_eur, shipping_cost, vat_rate
    )

    # Display results
    print("\n=== Cost Breakdown ===")
    print(f"Total Cost: {total_cost:.2f}")
    print(f"Export Duty (India): {export_duty:.2f}")
    print(f"Shipping Costs: {shipping_cost_inr:.2f}")
    print(f"Import Cost (Germany): {import_cost:.2f}")

    # Create and save donut chart
    create_donut_chart(export_duty, shipping_cost_inr, import_cost)

if __name__ == "__main__":
    main()
