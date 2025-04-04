<h1 align="center">
  <img src="https://i.ibb.co/fSNP7Rz/icons8-web-scraping-500.png" alt="Web Scraping Project Logo" width="150">
  <br>
  Zepto & BigBasket Price Comparison Chatbot
  <br>
</h1>

<p align="center">
  A Python-based web scraping and chatbot application to compare product prices between Zepto and BigBasket.
</p>

<p align="center">
  <a href="https://python.org">
    <img src="https://img.shields.io/badge/Python-3.10-blue.svg?style=flat-square" alt="Python Version">
  </a>
  <a href="https://www.selenium.dev/">
    <img src="https://img.shields.io/badge/Selenium-4.x-brightgreen.svg?style=flat-square" alt="Selenium Version">
  </a>
  <a href="https://pymongo.readthedocs.io/en/stable/">
    <img src="https://img.shields.io/badge/PyMongo-4.x-yellow.svg?style=flat-square" alt="PyMongo Version">
  </a>
  <a href="https://flask.palletsprojects.com/en/2.3.x/">
    <img src="https://img.shields.io/badge/Flask-2.x-red.svg?style=flat-square" alt="Flask Version">
  </a>
  <a href="https://github.com/Dhamodran16/webscraping/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/Dhamodran16/webscraping?style=flat-square" alt="License">
  </a>
</p>

---

##  Key Features

* **Web Scraping:** Automatically fetches product data (name, quantity, price, discount) from Zepto and BigBasket websites.
* **Data Storage:** Stores the scraped data in separate MongoDB databases for each platform.
* **Price Comparison:** Allows users to inquire about a specific product and get a price comparison between Zepto and BigBasket.
* **Product Information:** Provides detailed information (price, discount) for a requested product from either platform.
* **Bulk Product Comparison:** Enables users to compare the best available prices for multiple products at once.
* **Interactive Chatbot:** A user-friendly web interface built with Flask for interacting with the price comparison features.
* **Voice Input:** Integrated voice recognition for hands-free interaction with the chatbot.
* **Real-time Interaction:** Provides immediate responses and comparisons based on the scraped data.

## Tech Stack

* **Python:** The primary programming language used for scraping, data processing, and the Flask application.
* **Selenium:** A powerful tool for automating web browser interactions, used here to navigate and extract data from dynamic websites.
* **WebDriver Manager:** Simplifies the management of browser drivers (like ChromeDriver) required by Selenium.
* **PyMongo:** A Python driver for MongoDB, used to interact with the databases storing the scraped product information.
* **Flask:** A lightweight and flexible web framework for building the chatbot interface and handling user requests.
* **HTML, CSS, JavaScript:** Used for the structure, styling, and interactive elements of the chatbot web page.
* **Bootstrap:** A CSS framework to provide a responsive and visually appealing design for the chat interface.
* **Font Awesome:** An icon library for incorporating useful icons into the user interface.
* **MongoDB:** A NoSQL database used to store the scraped product data from Zepto and BigBasket.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Dhamodran16/webscraping.git](https://www.google.com/search?q=https://github.com/Dhamodran16/webscraping.git)
    cd webscraping
    ```

2.  **Install the required Python libraries:**
    ```bash
    pip install -r requirements.txt
    ```
    *(It is recommended to create and activate a virtual environment before installing the requirements.)*

3.  **Install MongoDB:**
    * Follow the official MongoDB installation guide for your operating system: [https://www.mongodb.com/docs/manual/installation/](https://www.mongodb.com/docs/manual/installation/)
    * Ensure that the MongoDB server is running on the default port (`mongodb://localhost:27017/`).

4.  **Download ChromeDriver:**
    * Selenium requires a browser driver to interact with Chrome. Download the ChromeDriver that matches your Chrome browser version from: [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads)
    * Place the downloaded `chromedriver` executable in a directory accessible by your system's PATH or in the project directory. *(WebDriver Manager in the code should handle this automatically, but manual setup can be a fallback.)*

5.  **Prepare URL files:**
    * Create text files (e.g., `zepto_urls.txt`, `bigbasket_urls.txt`) containing the category URLs you want to scrape from Zepto and BigBasket, with each URL on a new line.
    * Update the `url_file` paths in `zepto.py` and `bigbasket.py` to point to your respective URL files.
    ```python
    # In zepto.py
    url_file = r"C:\Users\dhanashri laptop\Downloads\httpswww.zepto.comcnfruits-vegetabl.txt" # Replace with your path

    # In bigbasket.py
    url_file = r"C:\Users\dhanashri laptop\Downloads\bigbasketlinks-copy.txt" # Replace with your path
    ```

## Usage

1.  **Run the web scraping scripts:**
    * Open separate terminal windows or tabs.
    * Navigate to the project directory in each terminal.
    * Execute the scraping scripts:
        ```bash
        python zepto.py
        python bigbasket.py
        ```
    * These scripts will scrape the product data from the specified URLs and store it in the `ZeptoDB` and `BigBasketDB` MongoDB databases.

2.  **Run the Flask chatbot application:**
    * Open another terminal window or tab.
    * Navigate to the project directory.
    * Execute the Flask application:
        ```bash
        python app.py
        ```
    * This will start the Flask development server. By default, it will be accessible at `http://127.0.0.1:5000/` in your web browser.

3.  **Interact with the Chatbot:**
    * Open your web browser and go to `http://127.0.0.1:5000/`.
    * You can now interact with the chatbot by typing messages in the chat window.
    * Available commands:
        * `hi` or `hello`: Get a list of available options.
        * `1`: Compare prices for a specific product. The chatbot will then ask for the product name and quantity.
        * `2`: Get information (price, discount) for a specific product. The chatbot will ask for the product name.
        * `3`: Compare the best prices for multiple products. Enter product names separated by commas, and then the quantities for each, also comma-separated.
        * `bye` or `goodbye`: End the chat.
    * You can also use the microphone icon to input your queries using voice.

##  Database Structure

The scraped data is stored in MongoDB with the following database and collection structure:

* **Database:**
    * `ZeptoDB`: Contains data scraped from Zepto.
        * **Collection:** `ZeptoProducts`
            * Documents in this collection will have the following fields:
                * `Name` (String): Name of the product.
                * `Quantity` (String): Quantity of the product (e.g., "1 kg", "500 gm").
                * `Price` (String): Current price of the product (e.g., "₹45").
                * `Discount` (String): Discounted price if available, otherwise "N/A".
                * `URL` (String): The URL from which the product information was scraped.
    * `BigBasketDB`: Contains data scraped from BigBasket.
        * **Collection:** `BigBasketProducts`
            * Documents in this collection will have the following fields:
                * `Name` (String): Name of the product.
                * `Quantity` (String): Quantity of the product.
                * `Price` (String): Current price of the product.
                * `Discount` (String): Discount information (e.g., "20% OFF", "No Discount").
                * `URL` (String): The URL from which the product information was scraped.

## Important Notes

* **Website Structure Changes:** The scraping scripts are dependent on the HTML structure of the Zepto and BigBasket websites. If these websites undergo significant changes, the scripts may need to be updated to correctly locate and extract the data.
* **Rate Limiting:** Be mindful of the scraping frequency to avoid overloading the target websites. The `time.sleep()` function is used to introduce delays between requests, but you may need to adjust these values.
* **Ethical Scraping:** Always review the `robots.txt` file of the websites you are scraping and adhere to their terms of service. Avoid scraping excessively or in a way that could harm the website's performance.
* **MongoDB Connection:** Ensure that your MongoDB server is running and accessible at the specified URI (`mongodb://localhost:27017/`).
* **File Paths:** Double-check the file paths for the URL lists in `zepto.py` and `bigbasket.py` to ensure they are correct for your system.
* **Error Handling:** The scripts include basic error handling, but you may want to enhance it for more robust performance in case of unexpected issues during scraping.

## Contributing

Contributions to this project are welcome! If you find any bugs, have suggestions for improvements, or want to add new features, feel free to:

1.  Fork the repository.
2.  Create a new branch for your changes.
3.  Make your modifications and commit them.
4.  Push your changes to your fork.
5.  Submit a pull request.

##  License

This project is licensed under the [MIT License](https://github.com/Dhamodran16/webscraping/blob/main/LICENSE).

## Acknowledgements

* This project utilizes the power of open-source libraries like Selenium, PyMongo, and Flask.
* The design of the chat interface is inspired by various online resources and Bootstrap templates.

---

<p align="center">
  <sub>Project by <a href="https://github.com/Dhamodran16" target="_blank">Dhamodran16</a></sub>
</p>
