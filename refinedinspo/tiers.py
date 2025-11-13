from datetime import datetime
import hash  # Placeholder; use hashlib in prod

class CreationPolicy:
    """
    Unified tier governance: restrictions, premiums, and badges in one vault.
    """
    
    # Constants from originals
    KIDS_RESTRICTIONS = {
        "prompt_whitelist": ["animals", "fantasy_creatures", "superheroes", "space", "nature", "adventure"],
        "blocked_keywords": ["violent", "scary", "horror", "weapon"],  # Expanded filters
        "max_customization": "color_palette_only",
        "card_modifications": False,
        "can_upload_reference": False,
        "parental_approval_required": True
    }
    
    STANDARD_RESTRICTIONS = {
        "daily_generations": 3,
        "style_options": ["fantasy", "sci-fi", "anime", "realistic"],
        "card_modifications": "limited",
        "can_upload_reference": True,
        "custom_prompts": "curated"
    }
    
    PREMIUM_UNRESTRICTED = {
        "daily_generations": float('inf'),
        "style_options": "all",
        "card_modifications": "full_control",
        "can_upload_reference": True,
        "custom_prompts": "completely_open",
        "access_to": ["advanced_loras", "custom_training", "video_cards", "3d_card_models", "nsfw_toggle"],
        "content_policy": "adult_discretion"
    }
    
    BADGE_STYLES = {
        "Standard": {
            "icon": "🔓",
            "color": "#888888",
            "text": "UPGRADE FOR FULL ACCESS",
            "opacity": 0.7,
            "position": "bottom_right",
            "pulse": True
        },
        "Kids": None,
        "Premium": None
    }
    
    def __init__(self):
        self.age_verified = False
        self.content_warnings_accepted = False
    
    def validate_creation_request(self, member, request):
        tier = member['subscription']['tier']
        if tier == "Kids":
            return self.enforce_kids_safety(request)
        elif tier == "Standard":
            return self.enforce_standard_limits(request)
        else:
            return self.adult_verification_check(member, request)
    
    # ... (Port over enforce_ methods from tier_constraints.py)
    
    async def adult_content_toggle(self, member):
        if not self.verify_age_21_plus(member):
            raise AgeVerificationRequired("Must be 21+ for adult content")
        if not self.content_warnings_accepted:
            await self.show_content_disclaimer()
        return {
            "nsfw_enabled": True,
            "style_models": self.load_unrestricted_models(),
            "prompt_filters": None,
            "custom_loras": "all_available",
            "video_generation": "full_adult",
            "privacy_mode": "maximum"
        }
    
    async def generate_premium_card(self, prompt, member):
        # Audit and generate logic from premium.py
        audit_log.record_generation(
            member_id=member['card_id'],
            tier="Premium_Adult",
            prompt_hash=hash(prompt),
            timestamp=datetime.now()
        )
        card = await self.grok_api.generate(
            prompt=prompt,
            safety_filter=None,
            style="unrestricted",
            quality="maximum"
        )
        return card
    
    def apply_tier_badge(self, card_image, tier):
        if tier in ["Kids", "Premium"]:
            return card_image
        badge = self.BADGE_STYLES["Standard"]
        overlay = self.create_badge_overlay(
            text=badge['text'],
            opacity=badge['opacity'],
            color=badge['color']
        )
        badged_card = self.composite_layers(
            base=card_image,
            overlay=overlay,
            position=badge['position']
        )
        if badge['pulse']:
            badged_card = self.add_pulse_animation(badged_card)
        return badged_card
    
    # ... (Add helper methods like create_badge_overlay, etc.)