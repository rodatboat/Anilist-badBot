from functions import *

cont = True
step = 0
while(cont):
    print("=============================================================================\n")
    choice = int(input("MENU:"
                   "\n(1) Follow Global Activity Users"
                   "\n(2) Un-Follow All Randoms"
                    "\n(3) Un-Follow Range of Randoms"
                       "\n(4) Un-Follow All Traitors"
                       "\n(5) Get Following Count"
                       "\n(6) Get Follower Count"
                       "\n(7) Follow all Followers"
                       "\n(8) Exit"))
    if choice == 1:
        followGlobal()
    elif choice == 2:
        unfollowRandoms(0)
    elif choice == 3:
        num = int(input("How many randoms would you like to un-follow?\n"))
        unfollowRandoms(num)
    elif choice == 4:
        unfollowTraitors()
    elif choice == 5:
        getFollowingCount()
    elif choice == 6:
        getFollowerCount()
    elif choice == 7:
        followAllFollowers()
    elif choice == 8:
        cont = False