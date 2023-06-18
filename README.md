# Discord Vanity URL Sniper

This is a Discord Vanity URL Sniper, a tool that automatically claims available Discord vanity URLs. This tool is built with Python, using asyncio and aiohttp for efficient, asynchronous network requests.

## Installation

1. Clone the repository:
    ```
    git clone https://github.com/idkconsole/VanityUrl-Sniper.git
    cd VanityUrl-Sniper
    ```

2. (Optional) Create a virtual environment and activate it:
    ```
    python -m venv venv
    source venv/bin/activate
    ```

3. Install the required Python packages:
    ```
    pip install -r requirements.txt
    ```

## Usage

1. Edit the `main.py` file and replace the `token`, `hook`, `guild` and `vanity_list` variables with your respective Discord information.

2. Run the script:
    ```
    python main.py
    ```

## Note

This tool is created for educational purposes and meant to demonstrate the efficiency of asynchronous programming. Misuse of this tool is strictly against Discord's Terms of Service and can lead to the termination of your account. Use it responsibly.

## License

This project is licensed under the MIT License.
