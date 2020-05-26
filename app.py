#imported from standard library

#imported from third party repos

#imported from local directories
import post2db
import scrape

if __name__ == '__main__':
    print()
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("               AC - TIMESHEET SCRAPPER APP")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print()
    scrape.main()
    print()
    post2db.main()
    print()
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("                        VICTORY!")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print()