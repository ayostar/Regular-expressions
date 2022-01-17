from pprint import pprint
# читаем адресную книгу в формате CSV в список contacts_list
import csv
import re

with open("phonebook_raw.csv") as f:
    rows = csv.reader(f, delimiter = ",")
    contacts_list = list(rows)

for lists in contacts_list:
    phone_pattern_1 = r'(\+7|7|8)?\s*\((\d+)\)[\s-]*(\d+)[\s-]*(\d+)[\s-]*(\d+)'
    phone_pattern_2 = r'(\+7)(\d{3})(\d{3})(\d{2})(\d{2})'
    phone_pattern_3 = r'(8)\s*(\d{3})-(\d{3})-(\d{2})(\d{2})'
    local_phone_number_pattern = r'\s*\(*(\(*доб.)\s*(\d+)(\)*)'
    phone_string = lists[5]
    sub_phone_pattern = r'+7(\2)\3-\4-\5'
    sub_local_phone_pattern = r' \1\2'
    result_phones_1 = re.sub(phone_pattern_1, sub_phone_pattern, phone_string)
    result_phones_2 = re.sub(phone_pattern_2, sub_phone_pattern, result_phones_1)
    result_phones_3 = re.sub(phone_pattern_3, sub_phone_pattern, result_phones_2)
    result_final_phones = re.sub(local_phone_number_pattern, sub_local_phone_pattern, result_phones_3)
    lists[5] = result_final_phones

raw_contacts_list = contacts_list.copy()
for lists in raw_contacts_list:
    lastname_list = lists[0].split()
    firstname_list = lists[1].split()
    surname_list = lists[2].split()
    if len(lastname_list) == 3:
        lists[0] = lastname_list[0]
        lists[1] = lastname_list[1]
        lists[2] = lastname_list[2]
    if len(lastname_list) == 2 and len(firstname_list) == 0 and len(surname_list) == 0:
        lists[0] = lastname_list[0]
        lists[1] = lastname_list[1]
    if len(lastname_list) == 1 and len(firstname_list) == 2:
        lists[0] = lastname_list[0]
        lists[2] = firstname_list[1]
        lists[1] = firstname_list[0]

ready_contact_list = raw_contacts_list.copy()

for ready_lists in ready_contact_list:
    for raw_lists in raw_contacts_list:
        if ready_lists[0] == raw_lists[0] and ready_lists[1] == raw_lists[1]:
            if ready_lists[3] == '':
                ready_lists[3] = raw_lists[3]
            if ready_lists[4] == '':
                ready_lists[4] = raw_lists[4]
            if ready_lists[5] == '':
                ready_lists[5] = raw_lists[5]
            if ready_lists[6] == '':
                ready_lists[6] = raw_lists[6]

temp_phone_list = []
for copy_lists in ready_contact_list:
    if copy_lists[0] != '' and copy_lists[1] != '' and copy_lists[1] != '' and copy_lists[5]:
        if copy_lists[5] in temp_phone_list:
            ready_contact_list.remove(copy_lists)
        else:
            temp_phone_list.append(copy_lists[5])

with open("phonebook.csv", "w") as f:
    datawriter = csv.writer(f, delimiter = ',')
    datawriter.writerows(ready_contact_list)
