from datetime import datetime

def generateOrderId(index):
    current_date = datetime.now()
    time = current_date.hour
    day = current_date.day
    month = current_date.month
    year = current_date.year

    return f"{year}{month}{day}{time}{index.zfill(5)}"

print(generateOrderId('3'))