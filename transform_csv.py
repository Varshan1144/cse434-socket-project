import csv
import sys

def transform(year):
    input_file = f"details-{year}.csv"
    output_file = f"details-{year}_transformed.csv"
    
    # PDF Field Mapping (Indices in real NCEI file)
    # 0: EVENT_ID (7)
    # 1: STATE (8)
    # 2: YEAR (10)
    # 3: MONTH_NAME (11)
    # 4: EVENT_TYPE (12)
    # 5: CZ_TYPE (13)
    # 6: CZ_NAME (15)
    # 7: INJURIES_DIRECT (20)
    # 8: INJURIES_INDIRECT (21)
    # 9: DEATHS_DIRECT (22)
    # 10: DEATHS_INDIRECT (23)
    # 11: DAMAGE_PROPERTY (24)
    # 12: DAMAGE_CROPS (25)
    # 13: TOR_F_SCALE (31)
    
    indices = [7, 8, 10, 11, 12, 13, 15, 20, 21, 22, 23, 24, 25, 31]
    header = ["event_id", "state", "year", "month_name", "event_type", "cz_type", "cz_name", 
              "injuries_direct", "injuries_indirect", "deaths_direct", "deaths_indirect", 
              "damage_property", "damage_crops", "tor_f_scale"]

    try:
        with open(input_file, 'r', newline='') as csvfile_in:
            reader = csv.reader(csvfile_in)
            rows = list(reader)
            
            if not rows:
                print("Empty file")
                return

            with open(output_file, 'w', newline='') as csvfile_out:
                writer = csv.writer(csvfile_out)
                writer.writerow(header)
                
                # Skip the original header
                for row in rows[1:]:
                    if len(row) > max(indices):
                        new_row = [row[i] for i in indices]
                        writer.writerow(new_row)
        
        import os
        os.replace(output_file, input_file)
        print(f"Successfully transformed {input_file} to 14-field format.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python transform_csv.py <year>")
    else:
        transform(sys.argv[1])
