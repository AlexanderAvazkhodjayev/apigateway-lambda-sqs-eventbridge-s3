from dotenv import dotenv_values
props = dotenv_values("../.env")

print(props["ACCOUNT_ID"])