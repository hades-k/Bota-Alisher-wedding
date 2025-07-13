# Bota & Alisher Wedding Invitation App

This is a custom Streamlit web app for managing wedding invitations and RSVPs for Ботагоз & Алишер. Guests log in with a unique code, view event details, and submit their RSVP, which is recorded in a connected Google Sheet.

## Features

- **Personalized RSVP:** Guests enter a unique 4-digit code to access their invitation.
- **Bilingual Support:** Russian and Kazakh language options.
- **Custom Theming:** Star Wars-inspired design with custom backgrounds and fonts.
- **Google Sheets Integration:** RSVP responses are saved directly to a Google Sheet.
- **Countdown Timer:** Shows time remaining until the event.

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/hades-k/Bota-Alisher-wedding
cd Bota-Alisher-wedding
```

### 2. Install Dependencies

It's recommended to use a virtual environment.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Google Sheets API Setup

1. **Create a Google Cloud Project** and enable the Google Sheets API.
2. **Create a Service Account** and download the JSON credentials.
3. **Share your Google Sheet** (with a worksheet named `guests`) with the service account email.
4. **Add your credentials and sheet URL to Streamlit secrets:**

Create a `.streamlit/secrets.toml` file:

```toml
type = "service_account"
project_id = "<your-project-id>"
private_key_id = "<your-private-key-id>"
private_key = "<your-private-key>"
client_email = "<your-service-account-email>"
client_id = "<your-client-id>"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "<your-cert-url>"
gcp_spreadsheet_url = "<your-google-sheet-url>"
```

**Note:** Never commit your secrets file to version control.

### 4. Prepare the Google Sheet

- The sheet should have a worksheet named `guests`.
- Columns should be: `code`, `name`, `status`, `guest_count`
- Each guest should have a unique 4-digit code.

### 5. Run the App

```bash
streamlit run app.py
```

## File Structure

```
Bota-Alisher-wedding/
  app.py
  requirements.txt
  background-1.png
  background.png
  envelope.png
  envelope-untrimmed.png
  guests _tentative.csv
```

## Customization

- **Backgrounds and Images:** Replace `background-1.png` and other images for a different look.
- **Languages:** Edit the `content` dictionary in `app.py` to change or add languages.
- **Event Details:** Update the event date, time, address, and other details in `app.py`.

## Troubleshooting

- **Google Sheets errors:** Ensure your service account has access to the sheet and the credentials are correct.
- **Streamlit secrets:** Make sure `.streamlit/secrets.toml` exists and is properly formatted.
- **App not loading:** Check the terminal for error messages and verify all dependencies are installed.

## License

This project is for personal use. Please contact the authors for reuse or adaptation. 