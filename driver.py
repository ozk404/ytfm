import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options


def get_driver(browser):
    driver_path = "/usr/local/bin/geckodriver"  # Ruta específica para geckodriver
    if browser.lower() in ("firefox", "ff", "mozilla", "firefox-esr"):
        options = Options()
        # Specify the binary location of Firefox
        options.binary_location = "/usr/bin/firefox"
        # Add necessary arguments for Linux environments
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        # Uncomment the next line to run Firefox in headless mode
        options.add_argument("--headless")
        
        # Usando executable_path en lugar de service para versiones más antiguas de Selenium
        return webdriver.Firefox(executable_path=driver_path, options=options)

    raise RuntimeError(f"Unsupported browser: {browser}")


class Bot:
    """A bot to handle interactions with the web driver."""

    def __init__(self, website, browser):
        """Initialize the bot with a browser and website URL."""
        self.driver = get_driver(browser)
        self.website = website
        self.wait = WebDriverWait(self.driver, 20)  # Explicit wait for elements

    def get_vid(self):
        """Navigate to the specified website."""
        self.driver.get(self.website)

    def play_video(self):
        """Click the play button on a YouTube video and confirm playback."""
        try:
            # Esperar a que la página cargue completamente
            self.wait.until(EC.presence_of_element_located((By.ID, "movie_player")))
            
            # Encontrar el botón de reproducir
            play_button = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(@class, 'ytp-large-play-button')]")
                )
            )
            play_button.click()
            
            # Esperar un poco para que el video comience a reproducirse
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "playing-mode")))
            
            # Comprobar si el botón de reproducción ahora tiene "Pausa" en el aria-label
            pause_button = self.driver.find_element(By.XPATH, "//button[@title='Pause (k)']")
            if pause_button:
                print("El video se está reproduciendo correctamente.")
            else:
                print("El video no se está reproduciendo.")
                
        except Exception as e:
            print(f"Error while trying to play video: {e}")

    def clear_cache(self):
        """Clear browser cookies."""
        self.driver.delete_all_cookies()

    def refresh(self):
        """Refresh the current page."""
        self.driver.refresh()
  
    def switch_tab(self, tab_index):
        """Switch to the specified browser tab by index."""
        if tab_index < len(self.driver.window_handles):
            self.driver.switch_to.window(self.driver.window_handles[tab_index])
        else:
            print(f"Invalid tab index: {tab_index}. Total tabs: {len(self.driver.window_handles)}")

    def new_tab(self):
        """Open a new blank tab."""
        self.driver.execute_script("window.open('about:blank');")

    def close(self):
        """Close the browser session."""
        self.driver.quit()


if __name__ == "__main__":
    # Example usage for testing purposes
    website = "https://www.youtube.com/watch?v=sOWzqrVNfzI"
    browser = "firefox"

    bot = Bot(website, browser)
    try:
        bot.get_vid()
        bot.play_video()
    finally:
        bot.close()
