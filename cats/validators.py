import requests
from rest_framework.exceptions import ValidationError

def validate_cat_breed(breed):
    """Validate cat breed using TheCatAPI"""
    try:
        response = requests.get(
            'https://api.thecatapi.com/v1/breeds',
            timeout=5
        )
        response.raise_for_status()
        breeds = response.json()
        
        valid_breeds = [b['name'].lower() for b in breeds]
        
        if breed.lower() not in valid_breeds:
            raise ValidationError(
                f"Invalid breed. Breed must be one of the valid cat breeds from TheCatAPI."
            )
    except requests.RequestException as e:
        raise ValidationError(f"Unable to validate breed: {str(e)}")