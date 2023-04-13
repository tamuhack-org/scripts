import csv

inputFile = "contacts.csv"
outputFile = "tamuhackcontacts.vcf"
rowNumberForName = 0
rowNumberForPhone = 1

with open('contacts.csv', 'r') as csvfile:
  reader = csv.reader(csvfile)
  with open(outputFile, 'w') as f:
    for i, row in enumerate(reader):
      name_parts = row[rowNumberForName].split()
      last_name = name_parts[-1]
      first_name = ' '.join(name_parts[:-1])
      phone = row[rowNumberForPhone]
      print(first_name, last_name, phone)
      f.write('BEGIN:VCARD\n')
      f.write('VERSION:3.0\n')
      f.write(f'PRODID:-//Apple Inc.//macOS 12.6//EN\n')
      f.write(f'N:{last_name};{first_name};;;\n')
      f.write(f'FN:{first_name} {last_name}\n')
      f.write(f'TEL;type=HOME;type=VOICE;type=pref:{phone}\n')
      f.write('END:VCARD\n')


