import os
import sys
import csv
import re

maxInt = sys.maxsize
decrement = True
while decrement:
    # decrease the maxInt value by factor 10
    # as long as the OverflowError occurs.
    decrement = False
    try:
        csv.field_size_limit(maxInt)
    except OverflowError:
        maxInt = int(maxInt / 10)
        decrement = True
count = 1
namefile = input("Enter file name: ")
file = open(namefile, 'r', encoding='utf-8')
reader = csv.reader(file)
reader = csv.reader(file, delimiter=',')
extracted_emails=[]
for line in reader:
    match = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', str(line))
    match1 = str(match)
    cor1 = match1.replace("[", "")
    cor2 = cor1.replace("'", "")
    cor3 = cor2.replace("]", "").strip()
    if cor3.startswith('-'):
        cor3 = cor3[1:]
    if cor3.endswith('-'):
        cor3 = cor3[:-1]

    print(count, cor3)
    count += 1
    if (cor3 != ""):
        extracted_emails.append(cor3)

# save emails
with open('Only_emails.csv', 'a', encoding='utf-8') as file1:
    # print("fileOpened")
    for save_mail in extracted_emails:
        if (save_mail!=""):
            file1.write(save_mail + '\n')



valid_email_pattern = r"[-a-zA-Z0-9_.+-]+@([a-zA-Z0-9-]([-a-z0-9]{0,61}[a-z0-9])?\.)*(aero|arpa|asia|biz|cat|com|coop|edu|gov|info|int|jobs|mil|mobi|museum|name|net|org|pro|xyz|tel|travel|[a-z][a-z])"
invalid_domains = []
with open('bad_domains.csv', 'r', encoding='utf-8', errors='ignore') as bad_domains_file:
    reader = csv.reader(bad_domains_file)
    for word in bad_domains_file:
        invalid_domains.append(word.strip())
common_domains = ['com', 'net', 'org', 'fm', 'io', 'mobi', 'gov', 'us', 'co']
personal_domains = []
with open('personal_domains.csv', 'r', encoding='utf-8', errors='ignore') as personal_domains_file:
    reader = csv.reader(personal_domains_file)
    for pword in personal_domains_file:
        personal_domains.append(pword.strip())
generic_list = []
with open('generic_email_names.csv', 'r', encoding='utf-8', errors='ignore') as generic_file:
    reader = csv.reader(generic_file)
    for word in generic_file:
        generic_list.append(word.strip())
        count = 1
with open('OnlyGood.csv', 'w', encoding='utf-8',
          errors='ignore', newline='') as OG:
    writer = csv.DictWriter(
        OG, fieldnames=['Email',
                        'Business or Personal', 'People or Generic',
                        'Common or Local', 'Valid or Invalid'])  # writing headers to the fieldnames

    for line in extracted_emails:

        email = line.strip('?').lower()
        email = email.strip()
        if email.split('@')[-1] in personal_domains:
            business_or_personal = 'personal'
        else:
            business_or_personal = 'business'
        if email.split('@')[0] in generic_list:
            people_or_generic = 'generic'
        else:
            people_or_generic = 'People'
        if email.split('.')[-1] in common_domains:
            common_or_local = 'common'
        else:
            common_or_local = 'local'
        try:
            true_email = re.search(valid_email_pattern, email).group()
        except AttributeError:
            continue
        if email != true_email or email.split('@')[-1] in invalid_domains:
            valid_or_invalid = 'Invalid'
        else:
            valid_or_invalid = 'Valid'

        data = {'Email': email, 'Business or Personal': business_or_personal,
                'People or Generic': people_or_generic, 'Common or Local': common_or_local,
                'Valid or Invalid': valid_or_invalid}

        if (business_or_personal == 'business' and  # logic of the program
                    people_or_generic == 'People' and
                    valid_or_invalid == 'Valid'):
            writer.writerow(data)
        print(count, email)
        data = {}
        count += 1
