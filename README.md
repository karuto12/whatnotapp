# WhatsApp Automation via Web Scraping

This project automates sending WhatsApp messages using **web scraping**, with **headless option**, instead of costly API calls. Unlike APIs that require payment, this method is entirely **free** and leverages WhatsApp Web to send messages programmatically.

## Features
- **Send Messages**: Automate sending text messages to any phone number with WhatsApp.
- **Free Solution**: Avoid API costs by using web scraping to interact with WhatsApp Web.
- **Future Plans**: Work is in progress to support sending **images** and **files**.

## How to Use
1. **Install Dependencies**: Ensure all required libraries are installed (see `requirements.txt`).
2. **Create an Instance**:
   ```python
   from send_text import WhatsApp
   wa = WhatsApp("phone_number_with_country_code")
   ```
3. **login**: Call the login() method to authenticate with WhatsApp Web.
    ```python
    wa.login()
    ```
4. **Send Messages**: Use the send_text() method to send a message.
    ```python
    wa.send_text(["recipient_number"], "Your message here")
    ```

## Example
```python
from send_text import WhatsApp

no = "917975201973"  # Replace with your phone number
wa = WhatsApp(no)
wa.login()
wa.send_text(["918123456789"], "Hello from Python!") # Replace with whom you want to send
```

## Notes
- Ensure the phone number includes the country code.
- The project uses web scraping to interact with WhatsApp Web, so it requires a browser session.
- Currently, only text messages are supported. Image and file support is under development.