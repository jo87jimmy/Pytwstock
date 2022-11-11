import assests_insert.balance_sheet_6Q as balnce
import assests_insert.income_statement_6Q as income
import assests_insert.cash_flow_10Q as cash
import assests_insert.financial_ratios_10Q as ratio

no = '3706'
balnce.insert_balance(no)
income.insert_income(no)
cash.insert_cash_flow(no)
ratio.insert_ratio(no)
