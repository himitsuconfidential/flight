from datetime import datetime
def run():
    with open('flight_data.csv','r') as f:
        rows = f.readlines()
    today = datetime.now().strftime("%Y-%m-%d")
    filtered_rows = [row for idx,row in enumerate(rows) if row[11:21] >= today or idx == 0]
    with open('flight_data_filtered.csv','w', newline='\r\n') as f:
        f.writelines(filtered_rows)

if __name__ == "__main__":
    run()