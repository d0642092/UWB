numbers = []
loop = True

try: 
    # ===========SUBROUTINES==================

    def help():
        print("To view the list type 'view'"
              "\n To add an item type 'add'"
              "\n To remove an item type 'remove'"
              "\n To exit type exit or Ctrl + c can be used at any time")

    # =========SUBROUTENES END===============


    while loop:
        # task = input("What do you want to do? Type \"help\" for help:- ")
        # if task == 'help':
        #     help()
        # else:
        #     print("Invalid return please try again.")
        print("running")

except KeyboardInterrupt:
    print("InterRupt")
    exit()
