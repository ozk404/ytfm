from json import load
from time import sleep
import driver
from concurrent.futures import ThreadPoolExecutor


def get_config():
    """Read configuration file"""
    try:
        with open("default.json", "r") as file:
            data = load(file)
    except FileNotFoundError:
        with open("config.json", "r") as file:
            data = load(file)

    return data


def init_tabs(website, tab_amount):
    """Opens tabs according to tab amount set in config.json"""
    for _ in range(tab_amount):
        website.new_tab()


def open_single_link(website, tab):
    """Helper function to open a link in a single tab."""
    website.switch_tab(tab)
    website.get_vid()


def play_single_video(website, tab):
    """Helper function to play a video in a single tab."""
    website.switch_tab(tab)
    website.play_video()


def refresh_single_tab(website, tab):
    """Helper function to refresh a single tab."""
    website.switch_tab(tab)
    website.refresh()


def main():
    """Main Function"""
    print("Initialization")
    config = get_config()

    # Initialize the bot
    website = driver.Bot(config["website"], config["browser"])

    print("Opening new tabs")
    init_tabs(website, config["tab_amount"])

    print("Open links")
    with ThreadPoolExecutor(max_workers=config["tab_amount"]) as executor:
        executor.map(lambda tab: open_single_link(website, tab), range(config["tab_amount"]))

    print("Cycle start")
    print("Playing videos")
    with ThreadPoolExecutor(max_workers=config["tab_amount"]) as executor:
        executor.map(lambda tab: play_single_video(website, tab), range(config["tab_amount"]))

    for i in range(config["view_cycles"]):
        sleep(config["watch_time"])  # Watch the video for n amount of time

        print("Refreshing all tabs")
        with ThreadPoolExecutor(max_workers=config["tab_amount"]) as executor:
            executor.map(lambda tab: refresh_single_tab(website, tab), range(config["tab_amount"]))

        print("Clearing cache")
        website.clear_cache()  # Clear cache and site cookies
        print(f"Run {i+1}/{config['view_cycles']} complete")

    print("Complete")
    website.close()


if __name__ == "__main__":
    main()
