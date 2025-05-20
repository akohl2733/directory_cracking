# from test import runner
# from db import insert_rec, test_connection



# # url for Jacksonville State's capital planning and facilities department
# link = "https://www.jsu.edu/physicalplant/staff.html"
# # link = "https://space.virginia.edu/"
# # link = "https://lsu.edu/pdc/about/staff.php"
# # link = "https://facilities.lehigh.edu/capital-projects-and-planning/planning-design-construction"

# def modify_val(person):
#     modified_person = person.copy()
#     fields = ['name', 'title', 'email', 'phone']

#     for field in fields:
#         if input(f"Update {field.upper()}? [y/n]: ").strip().lower() == 'y':
#             modified_person[field] = input(f"New {field}: ").strip()

#     return modified_person

# if __name__ == "__main__":
#     data = runner(link)

#     for person in data:
#         # allow user to see values
#         print("\n" + person['name'] + '\n' + person['title'] + '\n' + person['email'] + '\n' + person['phone'] + '\n' + ("-" * 40))

#         # logic for determining whether values should be added to the database
#         checker = input("Do you want to add this person to the database?\nPlease type [y] if yes, or [n] if not. If you would like to modify the values, please type [m]\n")
#         if checker.lower() == "y":
#             insert_rec(person)
#             print(f"Inserted: {person['name']}" + '\n')
#         elif checker.lower() == 'm':
#             while True:
#                 new_person = modify_val(person)
#                 lets_see = input("Does this look correct:\n"  + new_person['name'] + '\n' + new_person['title'] + '\n' + new_person['email'] + '\n' + new_person['phone'] + '\n' + ("-" * 40) + '\n' + "Type [y/n] for [yes/no]")
#                 if lets_see.lower() == "y":
#                     insert_rec(new_person)
#                     break
#         else:
#             print("We did not add: " + person["name"])