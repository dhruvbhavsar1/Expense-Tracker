from DB_Manage import *

def print_expense_formet(r):
        #r 0,1,2,3,4
        #id, date, category, amount, note
        print(f"{r[0]:>4}| {r[1]:19}| {r[2]:12}| {r[3]:8.2f}| {r[4]:5}")
#to create tables/views/triggers if missing
init_db()
while True :
        print("\n===== Expense Tracker =====")
        print("1) Add expense")
        print("2) List expenses")
        print("3) Search expenses")
        print("4) Totals by category")
        print("5) Update expense")
        print("6) Delete expense")
        print("7) Exit")
        ch=int(input("Enter Choice "))
        if ch==1:
                category=input("category: ").strip()
                amount=float(input("Enter amount amount shold be Grater than 0: ").strip())
                note=input("Note (optional):").strip()
                eid=add_expense(category, amount, note)
                print("Expense is added",eid)
        elif ch==2:
                limit=int(input("How many rows to show (max is 10) ").strip())
                if limit>10:
                     print("limit is just 10")
                else:
                     rows=list_expenses(limit=limit)
                     if rows:
                         print("\n ID | Date                | Category     |   Amount | Note")
                         for r in rows:
                            print_expense_formet(r)
                     else:
                        print("no expenses")
        elif ch ==3:
              kw=input("Search keyword (category/note/date)").strip()
              rows=search_expenses(kw)
              if rows :
                 print("\n ID | Date                | Category   | Amount |7 Note")
                 for r in rows:
                       print_expense_formet(r)
              else:
                print("No matches.")
        elif ch ==4:
             rows=total_by_cat()
             if rows :
                  print("Category         | Total Amount  | Count")
                  for catg,tot_am,cnt in rows:
                       print(f"{catg:16}| {tot_am:6.2f}|   {cnt}")
             else:
                print("No data for totals.")
        elif ch==5:
             eid=int(input("Enter Expense ID to update "))
             if not eid_exist(eid):
                  print("Id not Exist ")
             else:
                category=input("category: ").strip()
                amount=float(input("Enter amount amount shold be Grater than 0: ").strip())
                note=input("Note (optional):").strip()
                update_expense(eid,category, amount, note)
        elif ch==6:
             eid=int(input("Enter Expense id for delete "))
             if not eid_exist(eid):
                  print("Id not exist")
             else :
                  delete_expense(eid)
                  print("Expense deleted")
        
        elif ch ==7:
             break
        else:
             print("invalid choise")
                    


                
                