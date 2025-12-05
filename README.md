# Mortgage Calculator

A comprehensive Python-based mortgage calculator that helps you analyze the true cost of homeownership, including monthly payments, equity buildup, and opportunity cost analysis.

## Features

- **Complete Cost Breakdown**: Calculate monthly and annual costs including mortgage, property tax, home insurance, and HOA fees
- **Equity Tracking**: Year-by-year breakdown showing both new equity built and total equity owned
- **Opportunity Cost Analysis**: Compare home equity growth against alternative investment returns
- **Flexible Input Formats**: Support for human-readable numbers (1M, 500K, $1.5M, 1,000,000)
- **CSV Export**: Export detailed calculations to spreadsheet-compatible CSV files
- **Customizable Parameters**:
  - House price, down payment, closing costs, and realtor fees
  - Mortgage rate and loan term
  - Investment APR for alternative investment comparison
  - Monthly HOA fees

## Installation

No external dependencies required. Just Python 3.6+:

```bash
git clone <repository-url>
cd mortgage
python mortgage_calculator.py --help
```

## Usage

### Basic Usage

```bash
# Minimal required parameter
python mortgage_calculator.py --price=500000

# With custom mortgage rate and term
python mortgage_calculator.py --price=750K --rate=5.99 --term=30

# Complete example with all costs
python mortgage_calculator.py --price=1M --rate=6.0 --down=200K --closing=15K --realtor=3 --hoa=250 --apr=4.5
```

### Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--price` | House price (required) | - |
| `--rate` | Mortgage rate in percent | 6.0 |
| `--term` | Loan term in years | 15 |
| `--down` | Down payment amount | 0 |
| `--closing` | Closing costs | 0 |
| `--realtor` | Realtor cost as % of house price | 3.0 |
| `--hoa` | Monthly HOA fee | 0 |
| `--apr` | Investment APR for comparison | 3.75 |
| `--csv` | Export to CSV file | - |

### Input Format Examples

The calculator supports various human-readable number formats:

```bash
# Standard numbers
--price=1000000

# With commas
--price=1,000,000

# Thousands (K)
--price=750K

# Millions (M)
--price=1.5M

# With dollar signs (must be quoted)
--price='$1M'
```

## Sample Output

### Example Command

```bash
python mortgage_calculator.py --price=500K --rate=6.0 --down=100K --closing=8K --realtor=3 --term=15 --apr=4.0 --hoa=150
```

### Console Output

```
============================================================
MORTGAGE CALCULATOR
============================================================

============================================================
COST BREAKDOWN
============================================================

House Price:              $500,000
Down Payment:             $100,000
Closing Costs:            $8,000
Realtor Cost (3.0%):     $15,000
Loan Amount:              $400,000
Mortgage Rate:            6.0%
Loan Term:                15 years
Investment APR:           4.0%

------------------------------------------------------------
MONTHLY COSTS
------------------------------------------------------------
Mortgage (P&I):           $3,400
Property Tax (1.2%):      $500
Home Insurance (0.4%):    $150
HOA Fee:                  $150
------------------------------------------------------------
TOTAL MONTHLY:            $4,200

------------------------------------------------------------
ANNUAL COSTS
------------------------------------------------------------
Mortgage (P&I):           $40,500
Property Tax:             $6,000
Home Insurance:           $2,000
HOA Fee:                  $1,800
------------------------------------------------------------
TOTAL ANNUAL:             $50,300

============================================================
EQUITY BUILDUP BY YEAR
============================================================
Year   New Equity     Interest Paid  Total Equity   Investment Alt
------------------------------------------------------------
0      $          0  $          0  $    100,000  $    123,000
1      $     16,950  $     23,550  $    116,950  $    127,900
2      $     18,000  $     22,500  $    135,000  $    133,000
3      $     19,100  $     21,400  $    154,100  $    138,300
4      $     20,300  $     20,200  $    174,400  $    143,850
5      $     21,550  $     18,950  $    195,950  $    149,600
6      $     22,900  $     17,600  $    218,850  $    155,600
7      $     24,300  $     16,200  $    243,150  $    161,850
8      $     25,800  $     14,700  $    268,950  $    168,300
9      $     27,400  $     13,100  $    296,350  $    175,050
10     $     29,100  $     11,450  $    325,400  $    182,050
11     $     30,850  $      9,650  $    356,250  $    189,350
12     $     32,750  $      7,750  $    389,050  $    196,900
13     $     34,800  $      5,700  $    423,850  $    204,800
14     $     36,950  $      3,550  $    460,800  $    213,000
15     $     39,200  $      1,300  $    500,000  $    221,450
============================================================

Total Interest Paid Over 15 Years: $207,600
Total Amount Paid: $607,600
============================================================
```

## Understanding the Output

### Cost Breakdown
- **House Price**: Total purchase price
- **Down Payment**: Initial payment (reduces loan amount)
- **Closing Costs**: One-time costs at purchase
- **Realtor Cost**: Realtor/agent fees (default 3% of house price)
- **Loan Amount**: House price minus down payment

### Monthly/Annual Costs
- **Mortgage (P&I)**: Principal and Interest payments
- **Property Tax**: Calculated at 1.2% of house price annually
- **Home Insurance**: Calculated at 0.4% of house price annually
- **HOA Fee**: Monthly homeowners association fee

### Equity Buildup Table
- **Year**: Year number (0 = at purchase)
- **New Equity**: Equity built in that specific year (principal paid)
- **Interest Paid**: Interest paid that year
- **Total Equity**: Your total ownership = down payment + all principal paid to date
- **Investment Alt**: What your initial investment (down payment + closing costs + realtor fees) would be worth if invested at the APR rate instead

### Key Insights

At **Year 0**: You start with $100K equity (20% ownership) but could have had $123K if invested.

At **Year 15**: You own the house 100% ($500K equity) but the alternative investment would only be $221K.

This shows that building home equity outpaced the investment alternative in this scenario.

## CSV Export

Add `--csv=filename.csv` to export all calculations to a spreadsheet-compatible file:

```bash
python mortgage_calculator.py --price=1M --down=200K --csv=my_mortgage.csv
```

The CSV includes:
- Complete cost summary
- Monthly and annual cost breakdown
- Year-by-year amortization schedule with all equity and investment data
- Total interest and payment amounts

## Examples

### First-Time Homebuyer (Minimal Down Payment)
```bash
python mortgage_calculator.py --price=400K --down=20K --rate=6.5 --term=30
```

### Traditional 20% Down
```bash
python mortgage_calculator.py --price=750K --down=150K --rate=5.99 --term=30 --closing=10K
```

### Investment Property with HOA
```bash
python mortgage_calculator.py --price=600K --down=120K --rate=6.25 --term=15 --hoa=350 --apr=5.0
```

### No Realtor Cost (FSBO - For Sale By Owner)
```bash
python mortgage_calculator.py --price=500K --down=100K --realtor=0 --term=20
```

### High-Yield Investment Comparison
```bash
python mortgage_calculator.py --price=1M --down=200K --apr=7.0 --csv=high_yield_comparison.csv
```

## License

MIT License - feel free to use and modify as needed.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
