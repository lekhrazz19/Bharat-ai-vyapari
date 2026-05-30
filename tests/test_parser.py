from app.telegram.parser import parse_proposal_message


def test_parse_proposal_message():
    text = """/newproposal
Company Name: ABC Tools
Website: https://abc.com
Client Name: Rahul
Client Email: rahul@example.com
Services: AI SDR, WhatsApp Automate
Pricing Mode: Manual
Setup Cost: ₹100
Monthly Cost: ₹10
Sales Note: Expo lead
"""
    data = parse_proposal_message(text)
    assert data["company_name"] == "ABC Tools"
    assert data["selected_services"] == ["AI SDR", "WhatsApp Automate"]
