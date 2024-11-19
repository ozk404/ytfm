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
        print("default.json not found, attempting to load config.json.")
        try:
            with open("config.json", "r") as file:
                data = load(file)
        except FileNotFoundError:
            print("Error: Both default.json and config.json are missing.")
            raise

    print("Configuration loaded successfully.")
    return data


def init_tabs(website, tab_amount):
    """Opens tabs according to tab amount set in config.json"""
    for i in range(tab_amount):
        try:
            website.new_tab()
            print(f"Tab {i + 1} opened successfully.")
        except Exception as e:
            print(f"Error while opening tab {i + 1}: {e}")


def open_single_link(website, tab):
    """Helper function to open a link in a single tab."""
    try:
        website.switch_tab(tab)
        website.get_vid()
        print(f"Link opened successfully in tab {tab + 1}.")
    except Exception as e:
        print(f"Error while opening link in tab {tab + 1}: {e}")


def play_single_video(website, tab):
    """Helper function to play a video in a single tab."""
    try:
        website.switch_tab(tab)
        website.play_video()
        print(f"Video started successfully in tab {tab + 1}.")
    except Exception as e:
        print(f"Error while playing video in tab {tab + 1}: {e}")


def refresh_single_tab(website, tab):
    """Helper function to refresh a single tab."""
    try:
        website.switch_tab(tab)
        website.refresh()
        print(f"Tab {tab + 1} refreshed successfully.")
    except Exception as e:
        print(f"Error while refreshing tab {tab + 1}: {e}")


def main():
    """Main Function"""
    print("Initialization")
    try:
        config = get_config()
    except Exception as e:
        print(f"Failed to load configuration: {e}")
        return

    # Initialize the bot
    try:
        website = driver.Bot(config["website"], config["browser"])
        print("Browser initialized successfully.")
    except Exception as e:
        print(f"Error while initializing the browser: {e}")
        return

    print("Opening new tabs")
    try:
        init_tabs(website, config["tab_amount"])
    except Exception as e:
        print(f"Error during tab initialization: {e}")
        website.close()
        return

    print("Open links")
    try:
        with ThreadPoolExecutor(max_workers=config["tab_amount"]) as executor:
            executor.map(lambda tab: open_single_link(website, tab), range(config["tab_amount"]))
    except Exception as e:
        print(f"Error while opening links in tabs: {e}")

    print("Cycle start")
    print("Playing videos")
    try:
        with ThreadPoolExecutor(max_workers=config["tab_amount"]) as executor:
            executor.map(lambda tab: play_single_video(website, tab), range(config["tab_amount"]))
    except Exception as e:
        print(f"Error while playing videos: {e}")

    for i in range(config["view_cycles"]):
        print(f"Starting view cycle {i + 1} of {config['view_cycles']}")
        try:
            sleep(config["watch_time"])  # Watch the video for n amount of time
        except Exception as e:
            print(f"Error while waiting during watch time: {e}")

        print("Refreshing all tabs")
        try:
            with ThreadPoolExecutor(max_workers=config["tab_amount"]) as executor:
                executor.map(lambda tab: refresh_single_tab(website, tab), range(config["tab_amount"]))
        except Exception as e:
            print(f"Error while refreshing tabs: {e}")

        print("Clearing cache")
        try:
            website.clear_cache()  # Clear cache and site cookies
            print(f"Cache cleared successfully after run {i + 1}.")
        except Exception as e:
            print(f"Error while clearing cache after run {i + 1}: {e}")

        print(f"Run {i + 1}/{config['view_cycles']} complete")

    print("Complete")
    try:
        website.close()
        print("Browser closed successfully.")
    except Exception as e:
        print(f"Error while closing the browser: {e}")


if __name__ == "__main__":
    main()
