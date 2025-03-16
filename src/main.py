from file import dump_json_to_file, open_file_in_editor
from scraper import scrape

WEBLET_URL = "https://britishwrestling.justgo.com/weblets/CoachAndClubFinder/74728f3b-1e94-44fc-8217-e70f15953222/"
TARGET_ELEMENT = "webletsCoachAndClubFinder74728f3b-1e94-44fc-8217-e70f15953222"
PARENT_CONTAINER_DIV_CLASS = ".flex.flex-col.md\\:flex-row.relative.space-y-4.md\\:space-y-0.md\\:space-x-4"
CLUB_NAME_DIV_CLASS = ".text-globalTextSizeLg.font-medium.text-jg-metal-900"
DETAILS_DIV_CLASS = ".text-jg-metal-800.text-globalTextSizeSm"

def main():
    clubs = scrape(WEBLET_URL, TARGET_ELEMENT, PARENT_CONTAINER_DIV_CLASS, CLUB_NAME_DIV_CLASS, DETAILS_DIV_CLASS);

    file_name = input("Enter a file name (default=\"clubs.json\"): ") or "clubs.json"
    dump_json_to_file(file_name, clubs)
    open_file_in_editor(file_name)

if __name__ == "__main__":
    main()