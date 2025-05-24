from db_handler import add_label, add_or_update_guide, save_ticket
import os

def create_test_labels():
    labels = [
        "Printer Issues",
        "Network Connectivity",
        "Software Installation",
        "Password Reset",
        "Hardware Problems",
        "Email Configuration",
        "System Updates",
        "Access Permissions"
    ]
    
    for label in labels:
        add_label(label)
    print("Test labels created successfully!")

def create_test_guides():
    guides = {
        "Printer Issues": {
            "type": "text",
            "title": "Common Printer Troubleshooting Guide",
            "summary": "Quick solutions for common printer problems",
            "content": """
            # Printer Troubleshooting Guide
            
            ## Common Issues and Solutions:
            
            1. **Paper Jams**
               - Check for stuck paper in all trays
               - Clear any visible paper jams
               - Restart printer after clearing
            
            2. **Print Quality Issues**
               - Clean print heads
               - Check ink/toner levels
               - Verify correct paper settings
            
            3. **Connection Problems**
               - Verify network connection
               - Check USB cable if applicable
               - Restart printer and computer
            """
        },
        "Network Connectivity": {
            "type": "text",
            "title": "Network Troubleshooting Guide",
            "summary": "Steps to resolve network connectivity issues",
            "content": """
            # Network Troubleshooting Guide
            
            ## Basic Troubleshooting Steps:
            
            1. **Check Physical Connection**
               - Verify Ethernet cable is properly connected
               - Check for any visible damage to cables
            
            2. **WiFi Connection**
               - Ensure WiFi is enabled
               - Check signal strength
               - Verify correct network selection
            
            3. **IP Configuration**
               - Check IP address settings
               - Verify DNS settings
               - Test with different DNS servers
            """
        }
    }
    
    for label, guide_data in guides.items():
        add_or_update_guide(label, {
            "label": label,
            **guide_data
        })
    print("Test guides created successfully!")

def create_test_tickets():
    tickets = [
        {
            "name": "John Smith",
            "location": "Floor 3 - Marketing",
            "device": "HP LaserJet Pro M404dn",
            "description": "Printer is showing paper jam error but there's no paper stuck. Tried restarting but issue persists.",
            "label": "Printer Issues",
            "priority": "Medium",
            "confidence": 0.85
        },
        {
            "name": "Sarah Johnson",
            "location": "Floor 2 - Finance",
            "device": "Dell Latitude 5420",
            "description": "Cannot connect to the office WiFi. Shows 'Limited Access' and can't reach internal resources.",
            "label": "Network Connectivity",
            "priority": "High",
            "confidence": 0.92
        },
        {
            "name": "Mike Brown",
            "location": "Floor 1 - Reception",
            "device": "Windows 10 PC",
            "description": "Need to install Adobe Acrobat Reader for PDF viewing. Don't have admin rights.",
            "label": "Software Installation",
            "priority": "Low",
            "confidence": 0.78
        },
        {
            "name": "Lisa Chen",
            "location": "Floor 4 - HR",
            "device": "MacBook Pro",
            "description": "Forgot my email password. Need help resetting it and setting up 2FA.",
            "label": "Password Reset",
            "priority": "High",
            "confidence": 0.95
        }
    ]
    
    for ticket in tickets:
        save_ticket(ticket)
    print("Test tickets created successfully!")

def populate_test_data():
    print("Starting test data population...")
    create_test_labels()
    create_test_guides()
    create_test_tickets()
    print("All test data has been created successfully!")

if __name__ == "__main__":
    populate_test_data() 