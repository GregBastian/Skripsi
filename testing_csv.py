import csv

with open('employee_file.csv', mode='w', newline = '') as employee_file:
    employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    employee_writer.writerow(['John Smith', 'Accounting', 'November'])
    employee_writer.writerow(['Erica Meyers', 'IT', 'March'])
    
    
#with open('employee_file.csv') as csv_file:
#    csv_reader = csv.reader(csv_file, delimiter=',')
#    line_count = 0
#    for row in csv_reader:
#            print(row)
#            line_count += 1
#    print(f'Processed {line_count} lines.')