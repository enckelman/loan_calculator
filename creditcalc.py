import argparse
import sys
from math import ceil, log

parser = argparse.ArgumentParser(description="Loan calculator")

parser.add_argument("--type", type=str, help="Type of loan. Annuity or differentiated.")
parser.add_argument("--payment", type=float,
                    help="Annuity payment amount. Can be calculated using "
                         "the provided principal, interest, and number of months")
parser.add_argument("--principal", type=float,
                    help="Amount of money borrowed via loan. Can be calculated using "
                         "the provided interest, annuity payment, and number of months")
parser.add_argument("--periods", type=int,
                    help="Number of months needed to repay the loan. Can be calculated using "
                         "the provided interest, annuity payment, and principal")
parser.add_argument("--interest", type=float,
                    help="Interest rate, specified without percent sign. "
                         "The loan calculator can't calculate the interest, so it must always be provided")

args = parser.parse_args()

# Check for values: arguments no less than 4 and no negative numbers
args_dict = vars(args)
filtered_args = {key: value for key, value in args_dict.items() if value is not None}
if len(filtered_args) < 4:
    print("Incorrect parameters")
    sys.exit()
for value in filtered_args.values():
    if (isinstance(value, float) or isinstance(value, int)) and value < 0:
        print("Incorrect parameters")
        sys.exit()

# Calculating the interest rate
if args.interest is not None:
    interest_rate = args.interest / 100 / 12
else:
    print("Incorrect parameters")
    sys.exit()

if args.type == "diff":
    if args.principal or args.periods:
        total_payment = 0
        for m in range(1, args.periods + 1):
            # Calculate each month's payment using the formula from the image
            diff_payment = (args.principal / args.periods) + interest_rate * (args.principal - (args.principal * (m - 1)) / args.periods)
            total_payment += ceil(diff_payment)
            print(f"Month {m}: payment is {ceil(diff_payment)}")

        overpayment = round(total_payment - args.principal)
        print(f"\nOverpayment = {overpayment}")


elif args.type == "annuity":
    if args.payment is None:
        numerator = interest_rate * (1 + interest_rate) ** args.periods
        denominator = (1 + interest_rate) ** args.periods - 1
        annuity_payment = args.principal * (numerator / denominator)

        # Calculate and display the overpayment
        total_payment = ceil(annuity_payment) * args.periods
        overpayment = total_payment - args.principal
        print(f"Your monthly payment = {ceil(annuity_payment)}!")
        print(f"Overpayment = {int(overpayment)}")

    if args.periods is None:
        number_of_months = ceil(log(args.payment / (args.payment - interest_rate * args.principal), 1 + interest_rate))
        years, months = divmod(number_of_months, 12)
        if years == 0:
            print(f"It will take {months} month{'' if months == 1 else 's'} to repay this loan!")
        elif months == 0:
            print(f"It will take {years} year{'' if years == 1 else 's'} to repay this loan!")
        else:
            print(f"It will take {years} years and {months} months to repay this loan!")

        total_payment = args.payment * number_of_months
        overpayment = int(total_payment - args.principal)
        print(f"Overpayment = {overpayment}")

    if args.principal is None:
        numerator = interest_rate * (1 + interest_rate) ** args.periods
        denominator = (1 + interest_rate) ** args.periods - 1
        loan_principal = args.payment / (numerator / denominator)
        print(f"Your loan principal = {loan_principal:.0f}!")

else:
    print("Incorrect parameters")
