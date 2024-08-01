import csv

def export_to_csv(results, filename):
    if not results:
        print("No results to export.")
        return
    
    keys = results[0].keys()
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)
    
    print(f"Results exported to {filename}")
