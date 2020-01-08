from Module1 import Module1
from Module2 import Module2
from jpype import shutdownJVM

def main():
    choice = 0
    print("Welcome User")
    while choice == 0 or choice == 1:
        print("Please enter 0 if you would like to run module 1, and 1 if you would like to run module 2")
        choice = int(input("Choice : "))
        if (choice == 0):
            m = Module1()
        elif (choice == 1):
            m = Module2()

    shutdownJVM()
    return 0


if __name__ == "__main__":
    main()
