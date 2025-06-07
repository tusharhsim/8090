#!/bin/bash

# Black Box Challenge - Your Implementation
# This script takes three parameters and outputs the reimbursement amount
# Usage: ./run.sh <trip_duration_days> <miles_traveled> <total_receipts_amount>

# Call the Python implementation
py calculate_reimbursement.py "$1" "$2" "$3"
