# Sentiment Analysis Mapping
# This module maps emojis to specific 3D Avatar animation states.
# It covers a wide range of emotions, gestures, and reactions.

ANIMATION_MAP = {
    # --- HAPPINESS & JOY ---
    "😊": "idle_happy",          # Standard happy
    "😃": "smile_open",          # Open mouth smile
    "😄": "laughing_soft",       # Soft laugh
    "😁": "grin_teeth",          # Grin showing teeth
    "😆": "laughing_eyes_closed",# Laughing with closed eyes
    "😂": "laughing_tears",      # ROFL
    "🤣": "rofl_floor",          # Rolling on floor laughing
    "🙂": "smile_polite",        # Polite/Subtle smile
    "🙃": "silly_tilt",          # Head tilt (silly)
    "😇": "innocent_halo",       # Innocent look
    "🥰": "in_love_fawn",        # Hands on cheeks
    "😍": "eyes_heart",          # Heart eyes stun
    "🤩": "star_struck",         # Amazed
    "😋": "tasty_lick",          # Licking lips
    "🥳": "celebrate_jump",      # Jumping/Party
    "🫂": "hug_open",            # Open arms for hug
    "🤗": "hug_warm",            # Warm hug gesture
    "😽": "cat_kiss",

    # --- SADNESS & GRIEF ---
    "😢": "cry_soft",            # Single tear
    "😭": "cry_loud",            # Bawling
    "😞": "head_down_sad",       # Disappointed
    "😔": "pensive_look",        # Reflective sad
    "😟": "worried_face",        # Worried
    "🥺": "puppy_eyes",          # Begging/Puppy eyes
    "💔": "heartbreak_clutch",   # Hand on chest
    "😩": "weary_sigh",          # Sighing
    "😫": "tired_rub_eyes",      # Rubbing eyes
    "😓": "sweat_sad",           # Downcast sweat

    # --- ANGER & FRUSTRATION ---
    "😡": "angry_stomp",         # Stomping foot
    "😠": "annoyed_glare",       # Crossed arms glare
    "🤬": "cursing_rage",        # Aggressive shouting
    "😤": "steam_nose",          # Huffing
    "🙄": "eye_roll",            # Eye roll
    "😒": "unimpressed_look",    # Side eye
    "😑": "blank_stare",         # Zero emotion
    "🤦": "facepalm",            # Facepalm
    "🤦‍♀️": "facepalm",
    "🤦‍♂️": "facepalm",
    "👺": "furious_mask",        # Demonic rage

    # --- FEAR & SURPRISE ---
    "😱": "scream_shock",        # Hands on cheeks scream
    "😨": "fear_tremble",        # Shaking
    "😰": "sweat_drop",          # Nervous sweat
    "😮": "mouth_open_shock",    # Jaw drop
    "😯": "surprised_o",         # O face
    "😲": "shocked_gasp",        # Gasp
    "🤯": "mind_blown",          # Explosion mime
    "😳": "blush_shock",         # Blushing/Wide eyes
    "😬": "awkward_grimace",     # Grimace

    # --- LOVE & AFFECTION ---
    "❤️": "heart_hands",         # Making heart with hands
    "🧡": "heart_hands",
    "💛": "heart_hands",
    "💚": "heart_hands",
    "💙": "heart_hands",
    "💜": "heart_hands",
    "🖤": "heart_hands",
    "🤍": "heart_hands",
    "🤎": "heart_hands",
    "😘": "blow_kiss",           # Blowing a kiss
    "😗": "duck_lips",           # Kissy face
    "💋": "lip_touch",           # Touching lips
    "🫦": "bite_lip",            # Biting lip (flirty)

    # --- CONFUSION & THINKING ---
    "🤔": "thinking_chin",       # Hand on chin
    "🤨": "eyebrow_raise",       # The Rock eyebrow
    "🧐": "monocle_inspect",     # leaning in
    "🤷": "shrug",               # Shrug
    "🤷‍♀️": "shrug",
    "🤷‍♂️": "shrug",
    "😕": "confused_tilt",       # Confused head tilt
    "😶": "silent_mouth",        # No mouth
    "🤫": "shush_finger",        # Shh finger

    # --- COOL & CONFIDENT ---
    "😎": "cool_shades",         # Adjusting glasses
    "🤓": "nerd_adjust",         # Adjusting glasses (nerd)
    "🤠": "cowboy_tip",          # Tipping hat
    "😏": "smirk",               # Smirking
    "💪": "flex_bicep",          # Flexing
    "💅": "sassy_nails",         # Checking nails
    "👑": "crown_adjust",        # Adjusting invisible crown
    "😉": "wink",                # Winking
    "😜": "wink_tongue",         # Winking with tongue out
    "🤪": "zany_face",           # Goofy face

    # --- TIRED & SICK ---
    "😴": "sleeping",            # Zzz
    "🥱": "yawn_stretch",        # Yawning and stretching
    "🤒": "sick_thermometer",    # Shivering
    "🤕": "head_bandage",        # Holding head
    "🤢": "nauseous",            # Holding stomach
    "🤮": "vomit",               # (Maybe skip actual vomit)
    "🤧": "sneeze",              # Sneezing into elbow
    "🥴": "dizzy_wobble",        # Wobbling

    # --- ACTION / GESTURES ---
    "👋": "wave_hand",           # Waving
    "✋": "stop_hand",           # Stop gesture
    "👌": "ok_sign",             # OK sign
    "✌️": "peace_sign",          # Peace sign
    "🤞": "fingers_crossed",     # Fingers crossed
    "🤟": "rock_on",             # Rock on
    "🤘": "heavy_metal",         # Metal fingers
    "🤜": "fist_bump",           # Fist bump
    "🙏": "bow_namaste",         # Namaste/Bow
    "👏": "clapping",            # Clapping
    "🙌": "hands_up_cheer",      # Hands up
    "👐": "jazz_hands",          # Jazz hands
    "👍": "thumbs_up",
    "👎": "thumbs_down",
    "👉": "point_right",
    "👈": "point_left",
    "👆": "point_up",
    "👇": "point_down",
    "🤝": "shake_hand",          # Handshake

    # --- FOOD & DRINK (Interactables) ---
    "☕": "drink_coffee",        # Sipping cup
    "🍵": "drink_tea",           # Sipping tea
    "🥤": "drink_straw",         # Drinking with straw
    "🍷": "cheers_glass",        # Raising glass
    "🥂": "clink_glasses",       # Clinking
    "🍕": "eat_pizza",           # Eating slice
    "🍔": "eat_burger",          # Eating burger
    "🍿": "eat_popcorn",         # Eating popcorn
    "🎂": "blow_candles",        # Blowing candles

    # --- ACTIVITIES & OBJECTS ---
    "📖": "read_book",           # Reading/Flipping page
    "📚": "hold_books",          # Holding stack
    "📝": "taking_notes",        # Writing on pad
    "💻": "typing_laptop",       # Typing
    "📱": "check_phone",         # Looking at phone
    "🎮": "play_controller",     # Gaming
    "📷": "take_photo",          # Holding camera gesture
    "🎨": "paint_brush",         # Painting motion
    "🎤": "sing_mic",            # Holding mic
    "🎸": "air_guitar",          # Air guitar
    "🎻": "play_violin",         # Violin motion
    "🧹": "sweep_broom",         # Sweeping
    "🎁": "offer_gift",          # Holding out box
    "💐": "hold_flowers",        # Holding flowers
    "💌": "hold_letter",         # Holding letter

    # --- WEATHER & NATURE ---
    "🌧️": "rain_umbrella",       # Holding umbrella
    "☔": "rain_umbrella",
    "🥶": "shiver_cold",         # Shivering
    "🥵": "fan_hot",             # Fanning self
    "☀️": "shield_eyes",         # Shielding eyes from sun
    "❄️": "catch_snowflake",     # Catching snowflake
    "⛈️": "scared_thunder",      # Jumping from thunder

    # --- MISC / SYMBOLS ---
    "✨": "sparkle_pose",        # Magical pose
    "🔥": "fire_reaction",       # "That's hot" reaction
    "🎉": "party_popper",        # Throwing confetti
    "🎶": "dance_move",          # Dancing
    "🎵": "dance_move",
    "💃": "salsa_dance",
    "🕺": "disco_point",
    "👀": "peeking",             # Peeking through fingers
    "👻": "scare_boo",           # Boo gesture
    "🤖": "robot_dance",         # Robot dance
    "💩": "stinky_reaction",     # Pinching nose
    "💡": "idea_finger",         # Finger up (Idea)
    "❓": "confused_scratch",    # Head scratch
    "❔": "confused_scratch",
    "💤": "sleep_stand",         # Dozing off standing
    "💣": "duck_cover"           # Duck and cover
}

def get_animation_from_text(text: str):
    """
    Scans the text for emojis and returns the corresponding animation trigger.
    Priority: First valid emoji found in the text.
    Default: None (implies standard talking/idle loop)
    """
    if not text:
        return None
        
    for char in text:
        if char in ANIMATION_MAP:
            return ANIMATION_MAP[char]
            
    return None
