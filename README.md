# CA Firm WhatsApp Support Bot

A comprehensive WhatsApp support bot for CA firm services built with Python Flask and Meta WhatsApp Business API.

## Features

✅ **No Authorization Required** - Open to all users
✅ **9-Option Main Menu** - Complete service navigation
✅ **Multiple Service Categories**:
   - Services Overview
   - GST Services
   - Income Tax Services
   - Audit Services
   - Company Registration
   - Consultation Booking
   - Client Support
   - Document Upload
   - Service Tracking

✅ **Smart Features**:
   - Quick commands (MENU, BACK, HELP, etc.)
   - Business hours detection
   - Reference ID generation
   - Interactive multi-step forms
   - Session management

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `.env` file and update with your credentials:

```env
# Meta WhatsApp Business API
WHATSAPP_TOKEN=your_access_token
WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id
VERIFY_TOKEN=your_verify_token
WHATSAPP_BUSINESS_ACCOUNT_ID=your_business_account_id
APP_ID=your_app_id
APP_SECRET=your_app_secret

# Business Configuration
CA_FIRM_NAME=Your CA Firm Name
BUSINESS_EMAIL=contact@yourfirm.com
EMERGENCY_NUMBER=+91-XXXXXXXXXX
BUSINESS_HOURS_START=9
BUSINESS_HOURS_END=21

# Server
PORT=3000
```

### 3. Run the Bot

```bash
python bot.py
```

### 4. Expose with ngrok (for development)

```bash
ngrok http 3000
```

### 5. Configure Webhook in Meta App Dashboard

1. Go to Meta for Developers Dashboard
2. Select your WhatsApp App
3. Navigate to WhatsApp > Configuration
4. Set Webhook URL: `https://your-ngrok-url.ngrok.io/webhook`
5. Set Verify Token: (same as in .env)
6. Subscribe to messages webhook

## Bot Menu Structure

### Main Menu (1-9 Options)
1. **Services We Offer** - Overview of all services (A-I submenus)
2. **GST Services** - GST registration, returns, compliance (8 options)
3. **Income Tax Services** - ITR filing, tax planning (9 options)
4. **Audit Services** - Various audit types (7 options)
5. **Company Registration** - Formation services (6 types)
6. **Book Consultation** - Schedule meetings (4 types)
7. **Existing Client Support** - Client assistance (7 options)
8. **Upload Documents** - Document submission
9. **Track Service Status** - Service tracking

### Quick Commands (Work Anywhere)
- `MENU` or `MAIN` - Return to main menu
- `BACK` - Go to previous menu
- `HELP` - Show help menu
- `HUMAN` or `AGENT` - Connect to human agent
- `STATUS` - Check service status
- `CALL` - Request callback

## API Endpoints

### GET /webhook
Webhook verification endpoint for Meta

### POST /webhook
Receives incoming WhatsApp messages

### POST /send-test
Test endpoint to send messages
```json
{
  "to": "919876543210",
  "message": "Test message"
}
```

### GET /
Health check endpoint

## Features in Detail

### Multi-Step Forms
The bot supports complex multi-step interactions for:
- GST Return Filing (Business type → Turnover → GSTIN → Period)
- ITR Filing (Year → Sources → Income → PAN)
- Company Registration (Names → Directors → Activity → Office)
- Consultation Booking (Name → Company → Contact → Requirement → Date → Time)

### Session Management
- Each user has their own session
- Sessions track current menu and step
- User data stored temporarily for form completion
- Sessions can be reset with MENU command

### Business Hours
- Automatically detects if within business hours
- Shows appropriate message outside hours
- Continues with automated service

### Reference ID Generation
- Auto-generates unique reference IDs
- Format: TYPE + TIMESTAMP (e.g., GST20240108143000)
- Helps track service requests

## Code Structure

```
support-bot/
├── bot.py              # Main bot application
├── requirements.txt    # Python dependencies
├── .env               # Environment configuration
└── README.md          # This file
```

### Main Components

1. **Config Class** - Environment variables and validation
2. **WhatsAppService** - API communication with Meta
3. **MenuSystem** - Menu navigation and user input handling
4. **Flask Routes** - Webhook and API endpoints

## Testing

### Local Testing
```bash
# Send test message
curl -X POST http://localhost:3000/send-test \
  -H "Content-Type: application/json" \
  -d '{"to": "919876543210", "message": "Hello from bot!"}'
```

### User Flow Testing
1. Send "HI" or "MENU" to start
2. Navigate through menus by sending numbers
3. Test quick commands: BACK, HELP, HUMAN
4. Complete multi-step forms
5. Test business hours message

## Deployment

### Production Deployment Options

1. **Heroku**
```bash
heroku create your-bot-name
git push heroku main
heroku config:set WHATSAPP_TOKEN=your_token
```

2. **AWS EC2 / DigitalOcean**
- Deploy Flask app with gunicorn
- Use nginx as reverse proxy
- Setup SSL certificate
- Configure webhook with public URL

3. **Docker**
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "bot.py"]
```

## Troubleshooting

### Common Issues

1. **Webhook verification fails**
   - Check VERIFY_TOKEN matches in .env and Meta dashboard
   - Ensure ngrok URL is correct

2. **Messages not sending**
   - Verify WHATSAPP_TOKEN is valid
   - Check phone number format (no + or -)
   - Review Meta API logs

3. **Bot not responding**
   - Check Flask logs for errors
   - Verify webhook is configured correctly
   - Test with /send-test endpoint

### Debug Mode
Enable detailed logging:
```python
app.run(host='0.0.0.0', port=PORT, debug=True)
```

## Security Best Practices

1. Never commit `.env` file to git
2. Use environment variables for all credentials
3. Implement rate limiting in production
4. Validate all user inputs
5. Use HTTPS in production
6. Regularly rotate access tokens

## Support & Maintenance

### Monitoring
- Monitor Flask logs for errors
- Track webhook delivery in Meta dashboard
- Monitor API rate limits

### Updates
- Keep dependencies updated
- Review Meta API changelog
- Test thoroughly before deploying

## License

MIT License - Feel free to modify and use for your CA firm.

## Contact

For issues or questions, contact your development team.
# whatsapp-support-bot
