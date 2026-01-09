"""
CA Firm Support WhatsApp Bot
=============================
A comprehensive support bot for CA firm services built with Python Flask.

Features:
- No authorization required (open to everyone)
- Interactive 9-option main menu
- Multiple service categories with submenus
- Smart follow-ups and quick commands
- Business hours management
- Document upload support
- Service tracking

Author: CA Firm Support Bot
License: MIT
"""

import os
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================
# Configuration
# ============================================
class Config:
    """Configuration class for storing all credentials and settings"""
    
    # Meta WhatsApp API Configuration
    WHATSAPP_TOKEN = os.getenv('WHATSAPP_TOKEN')
    WHATSAPP_PHONE_NUMBER_ID = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
    VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')
    WHATSAPP_BUSINESS_ACCOUNT_ID = os.getenv('WHATSAPP_BUSINESS_ACCOUNT_ID')
    APP_ID = os.getenv('APP_ID')
    APP_SECRET = os.getenv('APP_SECRET')
    
    # Business Configuration
    CA_FIRM_NAME = os.getenv('CA_FIRM_NAME', 'CA Firm')
    BUSINESS_EMAIL = os.getenv('BUSINESS_EMAIL', 'contact@cafirm.com')
    EMERGENCY_NUMBER = os.getenv('EMERGENCY_NUMBER', '+91-XXXXXXXXXX')
    BUSINESS_HOURS_START = int(os.getenv('BUSINESS_HOURS_START', 9))
    BUSINESS_HOURS_END = int(os.getenv('BUSINESS_HOURS_END', 18))  # 6 PM
    
    # Server Configuration
    PORT = int(os.getenv('PORT', 3000))
    
    @classmethod
    def validate(cls):
        """Validate required environment variables"""
        required_vars = ['WHATSAPP_TOKEN', 'WHATSAPP_PHONE_NUMBER_ID', 'VERIFY_TOKEN']
        missing_vars = [var for var in required_vars if not getattr(cls, var)]
        if missing_vars:
            logger.warning(f'⚠️  Warning: Missing environment variables: {", ".join(missing_vars)}')
        return len(missing_vars) == 0


# ============================================
# WhatsApp Service
# ============================================
class WhatsAppService:
    """Service for interacting with WhatsApp Business API"""
    
    def __init__(self):
        self.token = Config.WHATSAPP_TOKEN
        self.phone_number_id = Config.WHATSAPP_PHONE_NUMBER_ID
        self.api_url = f"https://graph.facebook.com/v18.0/{self.phone_number_id}/messages"
    
    def send_message(self, to: str, message: str) -> Optional[Dict]:
        """
        Send a text message to a WhatsApp user
        
        Args:
            to: Recipient phone number
            message: Message text to send
            
        Returns:
            API response data or None if error
        """
        try:
            headers = {
                'Authorization': f'Bearer {self.token}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'messaging_product': 'whatsapp',
                'to': to,
                'type': 'text',
                'text': {
                    'body': message
                }
            }
            
            response = requests.post(self.api_url, headers=headers, json=payload)
            response.raise_for_status()
            
            logger.info(f'✅ Message sent successfully to {to}')
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f'❌ Error sending message: {e}')
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f'Response: {e.response.text}')
            return None
    
    def mark_as_read(self, message_id: str) -> bool:
        """
        Mark a message as read
        
        Args:
            message_id: ID of the message to mark as read
            
        Returns:
            True if successful, False otherwise
        """
        try:
            headers = {
                'Authorization': f'Bearer {self.token}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'messaging_product': 'whatsapp',
                'status': 'read',
                'message_id': message_id
            }
            
            response = requests.post(self.api_url, headers=headers, json=payload)
            response.raise_for_status()
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f'❌ Error marking message as read: {e}')
            return False


# ============================================
# Menu System
# ============================================
class MenuSystem:
    """Menu and submenu management system for CA Firm Support Bot"""
    
    def __init__(self):
        self.user_sessions: Dict[str, Dict] = {}
        self.user_data: Dict[str, Dict] = {}
    
    def is_business_hours(self) -> bool:
        """Check if current time is within business hours (9 AM to 6 PM)"""
        current_hour = datetime.now().hour
        return Config.BUSINESS_HOURS_START <= current_hour < Config.BUSINESS_HOURS_END
    
    def get_main_menu(self) -> str:
        """Get the main menu"""
        return (
            f'🙏 *Welcome to {Config.CA_FIRM_NAME}!*\n\n'
            'I\'m your virtual assistant. How can I assist you?\n\n'
            '1️⃣ Services We Offer\n'
            '2️⃣ GST Services\n'
            '3️⃣ Income Tax Services\n'
            '4️⃣ Audit Services\n'
            '5️⃣ Company Registration\n'
            '6️⃣ Book Consultation\n'
            '7️⃣ Existing Client Support\n'
            '8️⃣ Upload Documents\n'
            '9️⃣ Track Service Status\n\n'
            'Reply with number (1-9)'
        )
    
    def get_services_menu(self) -> str:
        """Option 1: Services We Offer"""
        return (
            '📋 *Our Professional Services:*\n\n'
            'A. GST Services\n'
            'B. Income Tax (Individual & Business)\n'
            'C. Accounting & Book-keeping\n'
            'D. Audit Services\n'
            'E. Company Formation & Registration\n'
            'F. Financial Planning\n'
            'G. Business Consulting\n'
            'H. Tally Implementation\n'
            'I. Compliance Management\n\n'
            'Type letter (A-I) to know more\n'
            'Or reply "ALL" for complete service list'
        )
    
    def get_gst_services_menu(self) -> str:
        """Option 2: GST Services"""
        return (
            '📊 *GST Services:*\n\n'
            '1. GST Registration (New)\n'
            '2. GST Return Filing\n'
            '   • GSTR-1\n'
            '   • GSTR-3B\n'
            '   • Annual Return\n'
            '3. GST Compliance\n'
            '4. Input Tax Credit Reconciliation\n'
            '5. GST Refund\n'
            '6. GST Notices & Litigation\n'
            '7. E-way Bill Support\n'
            '8. GST Advisory\n\n'
            'What do you need help with? (Reply 1-8)'
        )
    
    def get_income_tax_menu(self) -> str:
        """Option 3: Income Tax Services"""
        return (
            '💰 *Income Tax Services:*\n\n'
            '*For Individuals:*\n'
            '1. ITR Filing (Salaried)\n'
            '2. ITR Filing (Business/Profession)\n'
            '3. Capital Gains Tax\n'
            '4. Tax Planning\n'
            '5. Notice Reply\n\n'
            '*For Businesses:*\n'
            '6. Corporate Tax Returns\n'
            '7. TDS Returns\n'
            '8. Transfer Pricing\n'
            '9. Tax Audit\n\n'
            'What applies to you? (Reply 1-9)'
        )
    
    def get_audit_services_menu(self) -> str:
        """Option 4: Audit Services"""
        return (
            '🔍 *Audit Services:*\n\n'
            '1. Statutory Audit\n'
            '2. Tax Audit (44AB)\n'
            '3. GST Audit\n'
            '4. Internal Audit\n'
            '5. Stock Audit\n'
            '6. Bank Audit\n'
            '7. Concurrent Audit\n\n'
            'Select service or type your requirement (Reply 1-7)'
        )
    
    def get_company_registration_menu(self) -> str:
        """Option 5: Company Registration"""
        return (
            '🏢 *Company Formation Services:*\n\n'
            '1. Private Limited Company\n'
            '2. LLP Registration\n'
            '3. Partnership Firm\n'
            '4. Sole Proprietorship\n'
            '5. One Person Company (OPC)\n'
            '6. Section 8 Company (NGO)\n\n'
            'Select type to know:\n'
            '• Registration Process\n'
            '• Required Documents\n'
            '• Timeline & Fees\n'
            '• Benefits\n\n'
            '(Reply 1-6)'
        )
    
    def get_business_hours_message(self) -> str:
        """Message for outside business hours"""
        return (
            '⏰ *Thank you for contacting us!*\n\n'
            f'Our office hours: {Config.BUSINESS_HOURS_START} AM - {Config.BUSINESS_HOURS_END} PM (Mon-Sat)\n\n'
            'Your message is important. You can:\n'
            '1. Leave a message (we\'ll respond in morning)\n'
            '2. Request callback tomorrow\n'
            f'3. Send email: {Config.BUSINESS_EMAIL}\n'
            f'4. Emergency? Call: {Config.EMERGENCY_NUMBER}\n\n'
            'Or continue with our automated service.'
        )
    
    def handle_quick_command(self, command: str, user_id: str) -> Optional[str]:
        """Handle quick commands that work from anywhere"""
        command = command.lower().strip()
        
        if command in ['menu', 'main', 'start', 'hi', 'hello']:
            self.reset_user_session(user_id)
            return self.get_main_menu()
        
        elif command == 'back':
            session = self.user_sessions.get(user_id, {})
            current_menu = session.get('menu', 'main')
            
            if current_menu == 'main':
                return 'You are already at the main menu.'
            else:
                self.user_sessions[user_id] = {'menu': 'main', 'step': None}
                return self.get_main_menu()
        
        elif command in ['human', 'agent', 'talk']:
            return (
                '👤 *Connect to Human Agent*\n\n'
                'I\'ll connect you with our team.\n\n'
                f'📧 Email: {Config.BUSINESS_EMAIL}\n'
                f'📞 Call: {Config.EMERGENCY_NUMBER}\n\n'
                'Or type your message and we\'ll have someone contact you shortly.\n\n'
                'Type *MENU* to return to main menu.'
            )
        
        elif command == 'status':
            return (
                '📊 *Track Service Status*\n\n'
                '📌 Enter your Reference ID:\n'
                '(Check your confirmation message)\n\n'
                'Or provide your PAN / GSTIN'
            )
        
        elif command == 'help':
            return (
                '💡 *Quick Commands:*\n\n'
                '• MENU - Main menu\n'
                '• BACK - Previous menu\n'
                '• HUMAN/AGENT - Talk to human\n'
                '• STATUS - Check service status\n'
                '• HELP - This help menu\n'
                '• CALL - Request callback\n\n'
                'Type any command to use it.'
            )
        
        elif command == 'call':
            return (
                '📞 *Callback Request*\n\n'
                '📌 Your Name:\n'
                '(Please type your name)'
            )
        
        return None
    
    def handle_user_input(self, user_id: str, message: str) -> str:
        """
        Handle user input and navigate through menus
        
        Args:
            user_id: User identifier (phone number)
            message: User's message text
            
        Returns:
            Response message text
        """
        input_text = message.strip()
        input_lower = input_text.lower()
        
        # Check for quick commands first
        quick_response = self.handle_quick_command(input_lower, user_id)
        if quick_response:
            return quick_response
        
        # Get or initialize user session
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = {'menu': 'main', 'step': None}
        
        if user_id not in self.user_data:
            self.user_data[user_id] = {}
        
        session = self.user_sessions[user_id]
        current_menu = session.get('menu', 'main')
        current_step = session.get('step')
        
        # Main Menu Handler
        if current_menu == 'main':
            if input_text == '1':
                session['menu'] = 'services'
                return self.get_services_menu()
            
            elif input_text == '2':
                session['menu'] = 'gst'
                return self.get_gst_services_menu()
            
            elif input_text == '3':
                session['menu'] = 'income_tax'
                return self.get_income_tax_menu()
            
            elif input_text == '4':
                session['menu'] = 'audit'
                return self.get_audit_services_menu()
            
            elif input_text == '5':
                session['menu'] = 'company_reg'
                return self.get_company_registration_menu()
            
            elif input_text == '6':
                session['menu'] = 'consultation'
                return (
                    '📞 *Book Your Consultation*\n\n'
                    'Consultation Type:\n'
                    '1. Tax Planning (₹500 / 30 min)\n'
                    '2. Business Advisory (₹1000 / hour)\n'
                    '3. Compliance Review (₹1500 / hour)\n'
                    '4. Free Initial Consultation (15 min)\n\n'
                    'Select option to proceed (Reply 1-4)'
                )
            
            elif input_text == '7':
                session['menu'] = 'client_support'
                session['step'] = 'ask_client_id'
                return (
                    '👥 *Client Support*\n\n'
                    'Please provide:\n'
                    '📌 Your Client ID / PAN / GSTIN:'
                )
            
            elif input_text == '8':
                session['menu'] = 'upload_docs'
                session['step'] = 'ask_client_id'
                return (
                    '📤 *Document Upload*\n\n'
                    'Please verify first:\n'
                    '📌 Your Client ID / PAN:'
                )
            
            elif input_text == '9':
                session['menu'] = 'track_status'
                session['step'] = 'ask_reference'
                return (
                    '📊 *Track Your Service*\n\n'
                    '📌 Enter your Reference ID:\n'
                    '(Check your confirmation message)\n\n'
                    'Or provide:\n'
                    '📌 PAN / GSTIN:'
                )
            
            else:
                return self.get_main_menu()
        
        # Services Menu Handler
        elif current_menu == 'services':
            input_upper = input_lower.upper()
            
            if input_upper == 'ALL':
                return (
                    '📋 *Complete Service List:*\n\n'
                    '✅ GST Services\n'
                    '✅ Income Tax Filing & Planning\n'
                    '✅ Accounting & Bookkeeping\n'
                    '✅ All Types of Audits\n'
                    '✅ Company/LLP Registration\n'
                    '✅ Financial Planning\n'
                    '✅ Business Consulting\n'
                    '✅ Tally Implementation\n'
                    '✅ Compliance Management\n'
                    '✅ TDS Returns\n'
                    '✅ ROC Filings\n'
                    '✅ FEMA Compliance\n'
                    '✅ Project Reports\n\n'
                    'Type *MENU* for main menu or *HUMAN* to talk to us'
                )
            
            elif input_upper in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']:
                service_details = {
                    'A': 'GST Services - Registration, Returns, Compliance, Notices',
                    'B': 'Income Tax - Individual & Business returns, Tax planning',
                    'C': 'Accounting & Bookkeeping - Complete accounting solutions',
                    'D': 'Audit Services - Statutory, Tax, GST, Internal audits',
                    'E': 'Company Formation - Pvt Ltd, LLP, Partnership registration',
                    'F': 'Financial Planning - Investment & wealth management',
                    'G': 'Business Consulting - Strategy & growth advisory',
                    'H': 'Tally Implementation - Setup, training & support',
                    'I': 'Compliance Management - All regulatory compliances'
                }
                
                return (
                    f'ℹ️ *{service_details.get(input_upper, "Service")}*\n\n'
                    'For detailed discussion:\n'
                    '• Type *6* for consultation booking\n'
                    '• Type *HUMAN* to talk to our team\n\n'
                    'Type *BACK* for services menu or *MENU* for main menu'
                )
            
            else:
                return self.get_services_menu()
        
        # GST Services Handler
        elif current_menu == 'gst':
            if input_text == '2':  # GST Return Filing
                session['menu'] = 'gst_return'
                session['step'] = 'business_type'
                return (
                    '📝 *GST Return Filing*\n\n'
                    'Your Business Type:\n'
                    '1. Regular Business\n'
                    '2. Composition Scheme\n'
                    '3. E-commerce Operator\n'
                    '4. Service Provider\n\n'
                    'Please select (Reply 1-4)'
                )
            
            elif input_text in ['1', '3', '4', '5', '6', '7', '8']:
                service_map = {
                    '1': 'GST Registration (New)',
                    '3': 'GST Compliance',
                    '4': 'Input Tax Credit Reconciliation',
                    '5': 'GST Refund',
                    '6': 'GST Notices & Litigation',
                    '7': 'E-way Bill Support',
                    '8': 'GST Advisory'
                }
                
                return (
                    f'✅ *{service_map.get(input_text)}*\n\n'
                    'Our team will assist you with this service.\n\n'
                    'Would you like to:\n'
                    '1. Book Consultation\n'
                    '2. Talk to Expert Now\n'
                    '3. Get Fee Details\n\n'
                    'Type *MENU* for main menu'
                )
            
            else:
                return self.get_gst_services_menu()
        
        # GST Return Filing Flow
        elif current_menu == 'gst_return':
            if current_step == 'business_type':
                if input_text in ['1', '2', '3', '4']:
                    self.user_data[user_id]['business_type'] = input_text
                    session['step'] = 'turnover'
                    return (
                        '💼 *Your Turnover:*\n\n'
                        '1. Below 40 Lakhs\n'
                        '2. 40 Lakhs - 1.5 Crores\n'
                        '3. 1.5 - 5 Crores\n'
                        '4. Above 5 Crores\n\n'
                        'Please select (Reply 1-4)'
                    )
                else:
                    return 'Please select a valid option (1-4)'
            
            elif current_step == 'turnover':
                if input_text in ['1', '2', '3', '4']:
                    self.user_data[user_id]['turnover'] = input_text
                    session['step'] = 'gstin'
                    return '📌 *Your GSTIN:*\n(Please enter your GSTIN)'
                else:
                    return 'Please select a valid option (1-4)'
            
            elif current_step == 'gstin':
                self.user_data[user_id]['gstin'] = input_text
                session['step'] = 'return_period'
                return '📌 *Return Period:* (MM/YYYY)\n(Example: 01/2024)'
            
            elif current_step == 'return_period':
                self.user_data[user_id]['return_period'] = input_text
                session['menu'] = 'main'
                session['step'] = None
                
                reference_id = f"GST{datetime.now().strftime('%Y%m%d%H%M%S')}"
                
                return (
                    '✅ *Received!*\n\n'
                    'Our team will:\n'
                    '• Verify your details\n'
                    '• Request necessary documents\n'
                    '• File return within 24-48 hours\n\n'
                    'Estimated Fee: ₹1500-3000\n\n'
                    'Want to proceed?\n'
                    '1. Yes, Proceed\n'
                    '2. Talk to CA First\n\n'
                    f'Reference ID: #{reference_id}'
                )
        
        # Income Tax Services Handler
        elif current_menu == 'income_tax':
            if input_text in ['1', '2']:  # ITR Filing
                session['menu'] = 'itr_filing'
                session['step'] = 'assessment_year'
                self.user_data[user_id]['itr_type'] = 'individual' if input_text == '1' else 'business'
                return (
                    '📄 *Income Tax Return Filing*\n\n'
                    'Assessment Year:\n'
                    '1. AY 2024-25\n'
                    '2. AY 2023-24 (Belated/Revised)\n'
                    '3. Other\n\n'
                    'Please select (Reply 1-3)'
                )
            
            elif input_text in ['3', '4', '5', '6', '7', '8', '9']:
                service_map = {
                    '3': 'Capital Gains Tax',
                    '4': 'Tax Planning',
                    '5': 'Notice Reply',
                    '6': 'Corporate Tax Returns',
                    '7': 'TDS Returns',
                    '8': 'Transfer Pricing',
                    '9': 'Tax Audit'
                }
                
                return (
                    f'✅ *{service_map.get(input_text)}*\n\n'
                    'Our tax experts will help you.\n\n'
                    'Next steps:\n'
                    '1. Book Consultation\n'
                    '2. Get Fee Quote\n'
                    '3. Talk to Tax Expert\n\n'
                    'Type *MENU* for main menu'
                )
            
            else:
                return self.get_income_tax_menu()
        
        # ITR Filing Flow
        elif current_menu == 'itr_filing':
            if current_step == 'assessment_year':
                if input_text in ['1', '2', '3']:
                    self.user_data[user_id]['assessment_year'] = input_text
                    session['step'] = 'income_sources'
                    return (
                        '💼 *Your Income Sources:*\n\n'
                        '1. Salary Only\n'
                        '2. Salary + House Property\n'
                        '3. Business/Profession\n'
                        '4. Capital Gains\n'
                        '5. Multiple Sources\n\n'
                        'Please select (Reply 1-5)'
                    )
                else:
                    return 'Please select a valid option (1-3)'
            
            elif current_step == 'income_sources':
                if input_text in ['1', '2', '3', '4', '5']:
                    self.user_data[user_id]['income_sources'] = input_text
                    session['step'] = 'income_range'
                    return (
                        '💰 *Annual Income Range:*\n\n'
                        '1. Below 5 Lakhs\n'
                        '2. 5-10 Lakhs\n'
                        '3. 10-25 Lakhs\n'
                        '4. Above 25 Lakhs\n\n'
                        'Please select (Reply 1-4)'
                    )
                else:
                    return 'Please select a valid option (1-5)'
            
            elif current_step == 'income_range':
                if input_text in ['1', '2', '3', '4']:
                    self.user_data[user_id]['income_range'] = input_text
                    session['step'] = 'pan'
                    return '📌 *Your PAN:*\n(Please enter your PAN number)'
                else:
                    return 'Please select a valid option (1-4)'
            
            elif current_step == 'pan':
                self.user_data[user_id]['pan'] = input_text
                session['menu'] = 'main'
                session['step'] = None
                
                return (
                    '✅ *Thank you!*\n\n'
                    'Required Documents:\n'
                    '• Form 16 / Salary Slips\n'
                    '• Bank Statement\n'
                    '• Investment Proofs\n'
                    '• Previous ITR (if available)\n\n'
                    'Reply "UPLOAD" to send documents now\n'
                    'Or reply "LATER" to send via email\n\n'
                    'Type *MENU* for main menu'
                )
        
        # Audit Services Handler
        elif current_menu == 'audit':
            if input_text in ['1', '2', '3', '4', '5', '6', '7']:
                audit_map = {
                    '1': 'Statutory Audit',
                    '2': 'Tax Audit (44AB)',
                    '3': 'GST Audit',
                    '4': 'Internal Audit',
                    '5': 'Stock Audit',
                    '6': 'Bank Audit',
                    '7': 'Concurrent Audit'
                }
                
                return (
                    f'✅ *{audit_map.get(input_text)}*\n\n'
                    'We provide comprehensive audit services.\n\n'
                    'To proceed:\n'
                    '1. Book Audit Consultation\n'
                    '2. Get Audit Quotation\n'
                    '3. Talk to Audit Partner\n\n'
                    'Type *MENU* for main menu'
                )
            else:
                return self.get_audit_services_menu()
        
        # Company Registration Handler
        elif current_menu == 'company_reg':
            if input_text == '1':  # Private Limited Company
                session['menu'] = 'pvt_ltd_reg'
                session['step'] = 'company_names'
                return (
                    '🏢 *Private Limited Company Registration*\n\n'
                    'Benefits:\n'
                    '✅ Limited Liability\n'
                    '✅ Easy Funding\n'
                    '✅ Professional Image\n'
                    '✅ Tax Benefits\n\n'
                    'Timeline: 10-15 days\n'
                    'Starting Fee: ₹10,000\n\n'
                    '📌 *Proposed Company Names* (3 options):\n'
                    '(Enter names separated by commas)'
                )
            
            elif input_text in ['2', '3', '4', '5', '6']:
                reg_map = {
                    '2': 'LLP Registration',
                    '3': 'Partnership Firm',
                    '4': 'Sole Proprietorship',
                    '5': 'One Person Company (OPC)',
                    '6': 'Section 8 Company (NGO)'
                }
                
                return (
                    f'✅ *{reg_map.get(input_text)}*\n\n'
                    'We provide complete registration services.\n\n'
                    'Next steps:\n'
                    '1. Get Detailed Process\n'
                    '2. Fee Quotation\n'
                    '3. Start Registration\n\n'
                    'Type *MENU* for main menu'
                )
            else:
                return self.get_company_registration_menu()
        
        # Pvt Ltd Registration Flow
        elif current_menu == 'pvt_ltd_reg':
            if current_step == 'company_names':
                self.user_data[user_id]['company_names'] = input_text
                session['step'] = 'num_directors'
                return '📌 *Number of Directors:*\n(Minimum 2 required)'
            
            elif current_step == 'num_directors':
                self.user_data[user_id]['num_directors'] = input_text
                session['step'] = 'business_activity'
                return '📌 *Business Activity:*\n(Brief description of your business)'
            
            elif current_step == 'business_activity':
                self.user_data[user_id]['business_activity'] = input_text
                session['step'] = 'registered_office'
                return (
                    '📌 *Registered Office:*\n\n'
                    '1. Own Premise\n'
                    '2. Need Virtual Office\n\n'
                    'Please select (Reply 1-2)'
                )
            
            elif current_step == 'registered_office':
                if input_text in ['1', '2']:
                    self.user_data[user_id]['office_type'] = input_text
                    session['menu'] = 'main'
                    session['step'] = None
                    
                    reference_id = f"REG{datetime.now().strftime('%Y%m%d%H%M%S')}"
                    
                    return (
                        '✅ *Registration Request Received!*\n\n'
                        'Would you like:\n'
                        '1. Start Registration Process\n'
                        '2. Schedule Consultation Call\n'
                        '3. Get Detailed Quotation\n\n'
                        f'Reference ID: #{reference_id}\n\n'
                        'Type *MENU* for main menu'
                    )
                else:
                    return 'Please select 1 or 2'
        
        # Consultation Booking Handler
        elif current_menu == 'consultation':
            if input_text in ['1', '2', '3', '4']:
                session['menu'] = 'book_appointment'
                session['step'] = 'ask_name'
                self.user_data[user_id]['consultation_type'] = input_text
                return '📌 *Your Name:*\n(Please enter your full name)'
            else:
                return 'Please select a valid option (1-4)'
        
        # Book Appointment Flow
        elif current_menu == 'book_appointment':
            if current_step == 'ask_name':
                self.user_data[user_id]['name'] = input_text
                session['step'] = 'ask_company'
                return '📌 *Company Name* (if applicable):\n(Type NA if not applicable)'
            
            elif current_step == 'ask_company':
                self.user_data[user_id]['company_name'] = input_text
                session['step'] = 'ask_contact'
                return '📌 *Contact Number:*\n(Please enter your contact number)'
            
            elif current_step == 'ask_contact':
                self.user_data[user_id]['contact'] = input_text
                session['step'] = 'ask_requirement'
                return '📌 *Brief Description of Requirement:*\n(What do you need help with?)'
            
            elif current_step == 'ask_requirement':
                self.user_data[user_id]['requirement'] = input_text
                session['step'] = 'ask_date'
                return (
                    '📌 *Preferred Date:*\n\n'
                    '1. Today\n'
                    '2. Tomorrow\n'
                    '3. This Week\n'
                    '4. Next Week\n\n'
                    'Please select (Reply 1-4)'
                )
            
            elif current_step == 'ask_date':
                if input_text in ['1', '2', '3', '4']:
                    self.user_data[user_id]['date_preference'] = input_text
                    session['step'] = 'ask_time'
                    return (
                        '📌 *Preferred Time:*\n\n'
                        '1. Morning (10 AM - 1 PM)\n'
                        '2. Afternoon (2 PM - 5 PM)\n'
                        '3. Evening (5 PM - 8 PM)\n\n'
                        'Please select (Reply 1-3)'
                    )
                else:
                    return 'Please select a valid option (1-4)'
            
            elif current_step == 'ask_time':
                if input_text in ['1', '2', '3']:
                    self.user_data[user_id]['time_preference'] = input_text
                    session['menu'] = 'main'
                    session['step'] = None
                    
                    reference_id = f"CONS{datetime.now().strftime('%Y%m%d%H%M%S')}"
                    
                    return (
                        '✅ *Appointment Requested!*\n\n'
                        'Confirmation will be sent within 30 minutes.\n\n'
                        f'Meeting Reference: #{reference_id}\n\n'
                        'Type *MENU* for main menu'
                    )
                else:
                    return 'Please select a valid option (1-3)'
        
        # Client Support Handler
        elif current_menu == 'client_support':
            if current_step == 'ask_client_id':
                self.user_data[user_id]['client_id'] = input_text
                session['step'] = 'support_options'
                return (
                    '✅ *Client Verified*\n\n'
                    'How can we help you?\n\n'
                    '1. Service Status Update\n'
                    '2. Request Documents/Reports\n'
                    '3. Upload Additional Documents\n'
                    '4. Schedule Follow-up\n'
                    '5. Billing/Payment Query\n'
                    '6. Speak with Assigned CA\n'
                    '7. Raise Issue/Complaint\n\n'
                    'Please select (Reply 1-7)'
                )
            
            elif current_step == 'support_options':
                if input_text in ['1', '2', '3', '4', '5', '6', '7']:
                    session['menu'] = 'main'
                    session['step'] = None
                    
                    support_map = {
                        '1': 'Service Status Update',
                        '2': 'Document Request',
                        '3': 'Document Upload',
                        '4': 'Follow-up Schedule',
                        '5': 'Billing Query',
                        '6': 'CA Connect',
                        '7': 'Issue/Complaint'
                    }
                    
                    return (
                        f'✅ *{support_map.get(input_text)} Request Received*\n\n'
                        'Our team will contact you within 2 hours.\n\n'
                        'Type *MENU* for main menu'
                    )
                else:
                    return 'Please select a valid option (1-7)'
        
        # Upload Documents Handler
        elif current_menu == 'upload_docs':
            if current_step == 'ask_client_id':
                self.user_data[user_id]['client_id'] = input_text
                session['step'] = 'service_type'
                return (
                    '📌 *Service Type:*\n\n'
                    '1. GST Returns\n'
                    '2. ITR Filing\n'
                    '3. Audit\n'
                    '4. Other\n\n'
                    'Please select (Reply 1-4)'
                )
            
            elif current_step == 'service_type':
                if input_text in ['1', '2', '3', '4']:
                    self.user_data[user_id]['service_type'] = input_text
                    session['menu'] = 'main'
                    session['step'] = None
                    
                    return (
                        '📎 *Please send your documents:*\n\n'
                        '✅ Supported formats:\n'
                        '• PDF, Excel, Images\n'
                        '• Zip files for multiple docs\n'
                        '• Max 25 MB per file\n\n'
                        'After uploading, you\'ll receive:\n'
                        '• Upload confirmation\n'
                        '• Document checklist\n'
                        '• Processing timeline\n\n'
                        'Type *MENU* when done'
                    )
                else:
                    return 'Please select a valid option (1-4)'
        
        # Track Status Handler
        elif current_menu == 'track_status':
            if current_step == 'ask_reference':
                self.user_data[user_id]['reference_id'] = input_text
                session['menu'] = 'main'
                session['step'] = None
                
                return (
                    '📋 *Service Status:*\n\n'
                    f'Service: GST Return Filing\n'
                    'Status: In Progress\n'
                    'Assigned To: CA Rajesh Kumar\n'
                    'Expected Completion: 2 days\n\n'
                    'Latest Update:\n'
                    'Documents received. Processing return filing.\n\n'
                    'Need assistance?\n'
                    '1. Talk to Assigned CA\n'
                    '2. Upload Pending Documents\n'
                    '3. Mark as Urgent\n\n'
                    'Type *MENU* for main menu'
                )
        
        # Default fallback
        return (
            '❓ I didn\'t understand that.\n\n'
            'Type *MENU* for main menu or *HELP* for quick commands.'
        )
    
    def reset_user_session(self, user_id: str):
        """Reset a user's session"""
        if user_id in self.user_sessions:
            self.user_sessions[user_id] = {'menu': 'main', 'step': None}


# ============================================
# Flask Application
# ============================================
app = Flask(__name__)

# Initialize services
whatsapp_service = WhatsAppService()
menu_system = MenuSystem()

logger.info('🤖 CA Firm Support Bot Starting...')


@app.route('/webhook', methods=['GET'])
def webhook_verify():
    """Webhook verification endpoint for Meta"""
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    logger.info('Webhook verification request received')
    
    if mode == 'subscribe' and token == Config.VERIFY_TOKEN:
        logger.info('✅ Webhook verified successfully!')
        return challenge, 200
    else:
        logger.warning('❌ Webhook verification failed')
        return 'Forbidden', 403


@app.route('/webhook', methods=['POST'])
def webhook_receive():
    """Webhook endpoint to receive messages from WhatsApp"""
    try:
        data = request.get_json()
        logger.info(f'Incoming webhook: {json.dumps(data, indent=2)}')
        
        # Extract message data
        entry = data.get('entry', [{}])[0]
        changes = entry.get('changes', [{}])[0]
        value = changes.get('value', {})
        messages = value.get('messages', [])
        
        if not messages:
            return 'OK', 200
        
        message = messages[0]
        from_number = message.get('from')
        message_id = message.get('id')
        message_text = message.get('text', {}).get('body', '')
        
        logger.info(f'📩 Message received from {from_number}: {message_text}')
        
        # Mark message as read
        whatsapp_service.mark_as_read(message_id)
        
        # No authorization required - open to everyone
        logger.info(f'👤 Processing message for user: {from_number}')
        
        # Check business hours for first-time users
        if from_number not in menu_system.user_sessions and not menu_system.is_business_hours():
            whatsapp_service.send_message(from_number, menu_system.get_business_hours_message())
        
        # Process menu navigation
        response = menu_system.handle_user_input(from_number, message_text)
        
        # Send response
        whatsapp_service.send_message(from_number, response)
        
        return 'OK', 200
        
    except Exception as e:
        logger.error(f'Error processing webhook: {e}', exc_info=True)
        return 'Internal Server Error', 500


@app.route('/send-test', methods=['POST'])
def send_test_message():
    """Test endpoint to send messages manually"""
    try:
        data = request.get_json()
        to = data.get('to')
        message = data.get('message')
        
        if not to or not message:
            return jsonify({'error': 'Missing "to" or "message" in request body'}), 400
        
        result = whatsapp_service.send_message(to, message)
        
        if result:
            return jsonify({'success': True, 'message': 'Message sent successfully'}), 200
        else:
            return jsonify({'success': False, 'message': 'Failed to send message'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'running',
        'message': f'{Config.CA_FIRM_NAME} Support Bot is active',
        'endpoints': {
            'webhook_verification': 'GET /webhook',
            'webhook_receiver': 'POST /webhook',
            'test_send': 'POST /send-test'
        }
    }), 200


if __name__ == '__main__':
    # Validate configuration
    Config.validate()
    
    PORT = Config.PORT
    logger.info(f'\n✅ Server running on port {PORT}')
    logger.info(f'📍 Webhook URL: http://localhost:{PORT}/webhook')
    logger.info(f'\n🏢 {Config.CA_FIRM_NAME} Support Bot')
    logger.info('📝 Setup Instructions:')
    logger.info('1. Update .env file with your Meta WhatsApp API credentials')
    logger.info('2. Use ngrok or similar tool to expose your local server')
    logger.info('3. Configure webhook URL in Meta App Dashboard')
    logger.info('4. Update business configuration in .env')
    logger.info('\n🚀 Bot is ready to receive messages!')
    logger.info('✅ No authorization required - open to all users\n')
    
    app.run(host='0.0.0.0', port=PORT, debug=False)
