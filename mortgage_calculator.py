#!/usr/bin/env python3
"""
Mortgage Calculator
Calculates monthly/annual costs and equity buildup for home purchase
"""
import csv
import argparse
from datetime import datetime

def parse_human_readable_number(value):
    """
    Parse human-readable number formats like:
    - 1,000,000 (with commas)
    - 1M or 1m (millions)
    - $1M (with dollar sign)
    - 1000K or 1000k (thousands)
    - 1.5M (decimal values)
    """
    if isinstance(value, (int, float)):
        return float(value)

    # Remove whitespace and dollar signs
    value = str(value).strip().replace('$', '').replace(',', '')

    # Handle K/M suffixes (case-insensitive)
    multiplier = 1
    if value.upper().endswith('M'):
        multiplier = 1_000_000
        value = value[:-1]
    elif value.upper().endswith('K'):
        multiplier = 1_000
        value = value[:-1]

    try:
        return float(value) * multiplier
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid number format: {value}")


def round_to_nearest_50(value):
    """Round value to nearest $50 for display purposes"""
    return round(value / 50) * 50


def calculate_monthly_mortgage_payment(principal, annual_rate, years):
    """Calculate monthly mortgage payment using standard formula"""
    monthly_rate = annual_rate / 12 / 100
    num_payments = years * 12

    if monthly_rate == 0:
        return principal / num_payments

    monthly_payment = principal * (monthly_rate * (1 + monthly_rate)**num_payments) / \
                     ((1 + monthly_rate)**num_payments - 1)
    return monthly_payment


def generate_amortization_schedule(principal, annual_rate, years):
    """Generate year-by-year amortization schedule"""
    monthly_rate = annual_rate / 12 / 100
    monthly_payment = calculate_monthly_mortgage_payment(principal, annual_rate, years)

    schedule = []
    remaining_balance = principal

    for year in range(1, years + 1):
        year_principal = 0
        year_interest = 0

        for month in range(12):
            if remaining_balance <= 0:
                break

            interest_payment = remaining_balance * monthly_rate
            principal_payment = monthly_payment - interest_payment

            year_principal += principal_payment
            year_interest += interest_payment
            remaining_balance -= principal_payment

        schedule.append({
            'year': year,
            'principal_paid': year_principal,  # This is "New Equity" - equity built this year
            'interest_paid': year_interest,
            'remaining_balance': max(0, remaining_balance),
            'cumulative_principal': principal - remaining_balance  # Cumulative principal paid (for total equity calc)
        })

    return schedule


def calculate_investment_growth(initial_investment, apr, years):
    """Calculate what initial investment would grow to if invested at APR"""
    growth_schedule = []

    # Year 0 - initial investment
    growth_schedule.append({
        'year': 0,
        'investment_value': initial_investment
    })

    # Years 1 through loan term
    for year in range(1, years + 1):
        future_value = initial_investment * ((1 + apr / 100) ** year)
        growth_schedule.append({
            'year': year,
            'investment_value': future_value
        })
    return growth_schedule


def export_to_csv(filename, house_price, down_payment, loan_amount, mortgage_rate,
                  loan_term, monthly_mortgage, monthly_property_tax, monthly_insurance,
                  monthly_hoa, monthly_total, annual_total, amortization, investment_apr,
                  investment_growth, closing_costs, realtor_cost):
    """Export mortgage calculations to CSV file"""
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Write summary section
        writer.writerow(['MORTGAGE SUMMARY'])
        writer.writerow(['House Price', f'${house_price:,.2f}'])
        writer.writerow(['Down Payment', f'${down_payment:,.2f}'])
        writer.writerow(['Closing Costs', f'${closing_costs:,.2f}'])
        writer.writerow(['Realtor Cost', f'${realtor_cost:,.2f}'])
        writer.writerow(['Loan Amount', f'${loan_amount:,.2f}'])
        writer.writerow(['Mortgage Rate', f'{mortgage_rate}%'])
        writer.writerow(['Loan Term', f'{loan_term} years'])
        writer.writerow(['Investment APR', f'{investment_apr}%'])
        writer.writerow([])

        # Write monthly costs
        writer.writerow(['MONTHLY COSTS'])
        writer.writerow(['Mortgage (P&I)', f'${monthly_mortgage:,.2f}'])
        writer.writerow(['Property Tax (1.2%)', f'${monthly_property_tax:,.2f}'])
        writer.writerow(['Home Insurance (0.4%)', f'${monthly_insurance:,.2f}'])
        writer.writerow(['HOA Fee', f'${monthly_hoa:,.2f}'])
        writer.writerow(['TOTAL MONTHLY', f'${monthly_total:,.2f}'])
        writer.writerow([])

        # Write annual costs
        writer.writerow(['ANNUAL COSTS'])
        writer.writerow(['Mortgage (P&I)', f'${monthly_mortgage * 12:,.2f}'])
        writer.writerow(['Property Tax', f'${monthly_property_tax * 12:,.2f}'])
        writer.writerow(['Home Insurance', f'${monthly_insurance * 12:,.2f}'])
        writer.writerow(['HOA Fee', f'${monthly_hoa * 12:,.2f}'])
        writer.writerow(['TOTAL ANNUAL', f'${annual_total:,.2f}'])
        writer.writerow([])

        # Write amortization schedule
        writer.writerow(['EQUITY BUILDUP BY YEAR'])
        writer.writerow(['Year', 'Principal Paid', 'Interest Paid', 'New Equity', 'Total Equity', 'Remaining Balance', 'Investment Value (Alternative)'])

        # Year 0 - Initial state
        year_0_inv = investment_growth[0]['investment_value'] if len(investment_growth) > 0 else 0
        writer.writerow([
            0,
            '$0.00',
            '$0.00',
            '$0.00',
            f'${down_payment:,.2f}',  # Total equity starts with down payment
            f'${loan_amount:,.2f}',
            f'${year_0_inv:,.2f}'
        ])

        # Years 1 through loan term
        for i, entry in enumerate(amortization):
            # investment_growth has Year 0 at index 0, so Year 1 is at index 1
            inv_value = investment_growth[i + 1]['investment_value'] if (i + 1) < len(investment_growth) else 0
            total_equity = down_payment + entry['cumulative_principal']
            writer.writerow([
                entry['year'],
                f'${entry["principal_paid"]:,.2f}',
                f'${entry["interest_paid"]:,.2f}',
                f'${entry["principal_paid"]:,.2f}',  # New equity is the principal paid this year
                f'${total_equity:,.2f}',  # Total equity includes down payment
                f'${entry["remaining_balance"]:,.2f}',
                f'${inv_value:,.2f}'
            ])

        writer.writerow([])
        writer.writerow(['TOTALS'])
        total_interest = sum(e['interest_paid'] for e in amortization)
        total_paid = sum(e['principal_paid'] + e['interest_paid'] for e in amortization)
        writer.writerow(['Total Interest Paid', f'${total_interest:,.2f}'])
        writer.writerow(['Total Amount Paid', f'${total_paid:,.2f}'])


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description='Calculate mortgage costs and equity buildup',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --price=500000
  %(prog)s --price=500K --rate=5.99 --term=30
  %(prog)s --price=1M --rate=6.5 --down=200K --closing=15K --realtor=3 --hoa=250 --apr=4.0
  %(prog)s --price=$1.5M --rate=5.99 --down=$300K --closing=$20K --realtor=2.5 --apr=3.5 --csv=results.csv
  %(prog)s --price=1,000,000 --rate=6.0 --down=200K --closing=10000 --realtor=0
        """
    )

    # Required arguments
    parser.add_argument('--price', type=parse_human_readable_number, required=True,
                        help='House price (supports: 1M, 500K, $1.5M, 1,000,000)')

    # Optional arguments with defaults
    parser.add_argument('--rate', type=float, default=6.0,
                        help='Mortgage rate in percent (default: 6.0)')

    parser.add_argument('--term', type=int, default=15,
                        help='Loan term in years (default: 15)')

    parser.add_argument('--down', type=parse_human_readable_number, default=0,
                        help='Down payment amount (supports: 100K, $200K, etc.) (default: 0)')

    parser.add_argument('--closing', type=parse_human_readable_number, default=0,
                        help='Closing costs (supports: 10K, $15K, etc.) (default: 0)')

    parser.add_argument('--realtor', type=float, default=3.0,
                        help='Realtor cost as percentage of house price (default: 3.0)')

    parser.add_argument('--hoa', type=parse_human_readable_number, default=0,
                        help='Monthly HOA fee (supports: 250, $250, etc.) (default: 0)')

    parser.add_argument('--apr', type=float, default=3.75,
                        help='Investment APR for down payment alternative (default: 3.75)')

    parser.add_argument('--csv', type=str, default=None,
                        help='Export to CSV file (specify filename)')

    args = parser.parse_args()

    # Extract values from arguments
    house_price = args.price
    mortgage_rate = args.rate
    loan_term = args.term
    down_payment = args.down
    closing_costs = args.closing
    realtor_percentage = args.realtor
    monthly_hoa = args.hoa
    investment_apr = args.apr

    # Calculate realtor cost as percentage of house price
    realtor_cost = house_price * (realtor_percentage / 100)

    print("=" * 60)
    print("MORTGAGE CALCULATOR")
    print("=" * 60)

    # Calculate loan amount
    loan_amount = house_price - down_payment

    # Calculate monthly mortgage payment (Principal + Interest)
    monthly_mortgage = calculate_monthly_mortgage_payment(loan_amount, mortgage_rate, loan_term)

    # Calculate property tax (1.2% annually)
    annual_property_tax = house_price * 0.012
    monthly_property_tax = annual_property_tax / 12

    # Calculate home insurance (0.4% annually)
    annual_insurance = house_price * 0.004
    monthly_insurance = annual_insurance / 12

    # Calculate totals
    monthly_total = monthly_mortgage + monthly_property_tax + monthly_insurance + monthly_hoa
    annual_total = monthly_total * 12

    # Generate amortization schedule
    amortization = generate_amortization_schedule(loan_amount, mortgage_rate, loan_term)

    # Calculate investment growth for comparison (down payment + closing costs + realtor cost)
    total_initial_investment = down_payment + closing_costs + realtor_cost
    investment_growth = calculate_investment_growth(total_initial_investment, investment_apr, loan_term)

    # Display results
    print("\n" + "=" * 60)
    print("COST BREAKDOWN")
    print("=" * 60)
    print(f"\nHouse Price:              ${round_to_nearest_50(house_price):,.0f}")
    print(f"Down Payment:             ${round_to_nearest_50(down_payment):,.0f}")
    print(f"Closing Costs:            ${round_to_nearest_50(closing_costs):,.0f}")
    print(f"Realtor Cost ({realtor_percentage}%):     ${round_to_nearest_50(realtor_cost):,.0f}")
    print(f"Loan Amount:              ${round_to_nearest_50(loan_amount):,.0f}")
    print(f"Mortgage Rate:            {mortgage_rate}%")
    print(f"Loan Term:                {loan_term} years")
    print(f"Investment APR:           {investment_apr}%")

    print("\n" + "-" * 60)
    print("MONTHLY COSTS")
    print("-" * 60)
    print(f"Mortgage (P&I):           ${round_to_nearest_50(monthly_mortgage):,.0f}")
    print(f"Property Tax (1.2%):      ${round_to_nearest_50(monthly_property_tax):,.0f}")
    print(f"Home Insurance (0.4%):    ${round_to_nearest_50(monthly_insurance):,.0f}")
    print(f"HOA Fee:                  ${round_to_nearest_50(monthly_hoa):,.0f}")
    print("-" * 60)
    print(f"TOTAL MONTHLY:            ${round_to_nearest_50(monthly_total):,.0f}")

    print("\n" + "-" * 60)
    print("ANNUAL COSTS")
    print("-" * 60)
    print(f"Mortgage (P&I):           ${round_to_nearest_50(monthly_mortgage * 12):,.0f}")
    print(f"Property Tax:             ${round_to_nearest_50(annual_property_tax):,.0f}")
    print(f"Home Insurance:           ${round_to_nearest_50(annual_insurance):,.0f}")
    print(f"HOA Fee:                  ${round_to_nearest_50(monthly_hoa * 12):,.0f}")
    print("-" * 60)
    print(f"TOTAL ANNUAL:             ${round_to_nearest_50(annual_total):,.0f}")

    # Display equity buildup
    print("\n" + "=" * 60)
    print("EQUITY BUILDUP BY YEAR")
    print("=" * 60)
    print(f"{'Year':<6} {'New Equity':<14} {'Interest Paid':<14} {'Total Equity':<14} {'Investment Alt':<14}")
    print("-" * 60)

    # Year 0 - Initial state
    year_0_inv = investment_growth[0]['investment_value'] if len(investment_growth) > 0 else 0
    print(f"{0:<6} "
          f"${0:>11,.0f}  "
          f"${0:>11,.0f}  "
          f"${round_to_nearest_50(down_payment):>11,.0f}  "
          f"${round_to_nearest_50(year_0_inv):>11,.0f}")

    # Years 1 through loan term
    for i, entry in enumerate(amortization):
        # investment_growth has Year 0 at index 0, so Year 1 is at index 1
        inv_value = investment_growth[i + 1]['investment_value'] if (i + 1) < len(investment_growth) else 0
        new_equity = entry['principal_paid']  # Equity built this year
        total_equity = down_payment + entry['cumulative_principal']  # Down payment + all principal paid
        print(f"{entry['year']:<6} "
              f"${round_to_nearest_50(new_equity):>11,.0f}  "
              f"${round_to_nearest_50(entry['interest_paid']):>11,.0f}  "
              f"${round_to_nearest_50(total_equity):>11,.0f}  "
              f"${round_to_nearest_50(inv_value):>11,.0f}")

    print("=" * 60)
    total_interest = sum(e['interest_paid'] for e in amortization)
    total_paid = sum(e['principal_paid'] + e['interest_paid'] for e in amortization)
    print(f"\nTotal Interest Paid Over {loan_term} Years: ${round_to_nearest_50(total_interest):,.0f}")
    print(f"Total Amount Paid: ${round_to_nearest_50(total_paid):,.0f}")
    print("=" * 60)

    # Export to CSV if requested
    if args.csv:
        filename = args.csv

        # Ensure .csv extension
        if not filename.endswith('.csv'):
            filename += '.csv'

        export_to_csv(
            filename, house_price, down_payment, loan_amount, mortgage_rate,
            loan_term, monthly_mortgage, monthly_property_tax, monthly_insurance,
            monthly_hoa, monthly_total, annual_total, amortization, investment_apr,
            investment_growth, closing_costs, realtor_cost
        )

        print(f"\nData successfully exported to: {filename}")
        print("=" * 60)


if __name__ == "__main__":
    main()
