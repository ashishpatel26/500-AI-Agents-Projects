"""
Verification tools for validating property listings and contact information
"""

import os
import logging
import re
from typing import Dict, Any, Optional
from crewai_tools import BaseTool
import requests
import phonenumbers
from email_validator import validate_email, EmailNotValidError

logger = logging.getLogger(__name__)


class DubaiLandDeptVerificationTool(BaseTool):
    name: str = "Dubai Land Department Verification"
    description: str = (
        "Verifies property listings against Dubai Land Department database. "
        "Validates property authenticity, ownership, and area information."
    )
    
    def _run(self, property_area: str, property_type: str = "apartment") -> Dict[str, Any]:
        """
        Verify property information with Dubai Land Department API
        
        Args:
            property_area: Area name to verify
            property_type: Type of property
            
        Returns:
            Verification result dictionary
        """
        api_url = os.getenv("DUBAI_LAND_DEPT_API_URL", "https://api.dubailand.gov.ae/v1")
        api_key = os.getenv("DUBAI_LAND_DEPT_API_KEY", "")
        
        logger.info(f"Verifying property area: {property_area}")
        
        try:
            # In production, make actual API call to Dubai Land Department
            # This is a mock implementation
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            # Mock verification logic
            verified_areas = [
                "Azizi Riviera", "Downtown Dubai", "Business Bay", "Dubai Marina",
                "JBR", "Palm Jumeirah", "Dubai Creek Harbour", "Dubai Hills Estate",
                "Arabian Ranches", "Jumeirah Village Circle"
            ]
            
            is_verified = any(area.lower() in property_area.lower() for area in verified_areas)
            
            result = {
                "verified": is_verified,
                "area": property_area,
                "property_type": property_type,
                "registration_status": "active" if is_verified else "unknown",
                "developer_verified": is_verified,
                "legal_status": "clear" if is_verified else "needs_verification",
                "timestamp": "2024-10-28T12:00:00Z"
            }
            
            if is_verified:
                logger.info(f"Property area {property_area} verified successfully")
            else:
                logger.warning(f"Property area {property_area} could not be verified")
                
            return result
            
        except Exception as e:
            logger.error(f"Error verifying property with Dubai Land Dept: {str(e)}")
            return {
                "verified": False,
                "error": str(e),
                "area": property_area
            }


class ContactVerificationTool(BaseTool):
    name: str = "Contact Information Verification"
    description: str = (
        "Verifies contact information including email addresses and phone numbers. "
        "Validates format and checks for common issues."
    )
    
    def _run(self, email: Optional[str] = None, phone: Optional[str] = None, 
             name: Optional[str] = None) -> Dict[str, Any]:
        """
        Verify contact information
        
        Args:
            email: Email address to verify
            phone: Phone number to verify
            name: Contact name to verify
            
        Returns:
            Verification result dictionary
        """
        result = {
            "email_valid": False,
            "phone_valid": False,
            "name_valid": False,
            "overall_valid": False
        }
        
        # Verify email
        if email:
            result["email_valid"] = self._verify_email(email)
            result["email"] = email
        
        # Verify phone
        if phone:
            result["phone_valid"] = self._verify_phone(phone)
            result["phone"] = phone
        
        # Verify name
        if name:
            result["name_valid"] = self._verify_name(name)
            result["name"] = name
        
        # Overall validation
        result["overall_valid"] = (
            (result["email_valid"] if email else True) and
            (result["phone_valid"] if phone else True) and
            (result["name_valid"] if name else True)
        )
        
        logger.info(f"Contact verification result: {result['overall_valid']}")
        return result
    
    def _verify_email(self, email: str) -> bool:
        """Verify email address format and validity"""
        try:
            # Validate email format
            valid = validate_email(email, check_deliverability=False)
            logger.info(f"Email {email} is valid")
            return True
        except EmailNotValidError as e:
            logger.warning(f"Email {email} is invalid: {str(e)}")
            return False
    
    def _verify_phone(self, phone: str) -> bool:
        """Verify phone number format and validity"""
        try:
            # Parse and validate phone number
            # Default to UAE region if no country code
            parsed = phonenumbers.parse(phone, "AE")
            is_valid = phonenumbers.is_valid_number(parsed)
            
            if is_valid:
                logger.info(f"Phone {phone} is valid")
            else:
                logger.warning(f"Phone {phone} is invalid")
                
            return is_valid
            
        except Exception as e:
            logger.warning(f"Phone {phone} validation error: {str(e)}")
            return False
    
    def _verify_name(self, name: str) -> bool:
        """Verify name format"""
        if not name or len(name.strip()) < 2:
            return False
        
        # Check if name contains at least some alphabetic characters
        if not re.search(r'[a-zA-Z]', name):
            return False
        
        # Check for suspicious patterns
        suspicious_patterns = [
            r'^\d+$',  # Only numbers
            r'^[^a-zA-Z]+$',  # No letters
            r'test|dummy|fake|example',  # Test data
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, name.lower()):
                logger.warning(f"Name {name} contains suspicious pattern")
                return False
        
        return True
