Dependency Modules =>
             1] account_reconciliation_widget need to install
=============================================
Configuration:
=============================================
1] Goto Accounting =>Configuration  => select Chart of Accounts Create New Account like """Bank Charges""" type as "Bank and Cash".
                                    => and create "Reverse Charge Tax Receivable" account with type "Current Assets".

2] Goto Accounting => Configuration => select Reconciliation Models Menu
                                    => Create "Bank Fees" and
                                    => select Manually create a write-off on clicked button
                                    => select Counterpart Values lines under
                                          bank as ""Bank Charges"", and based on requirement select Tax also.
*************** ""einv_sa"" need to uninstall.