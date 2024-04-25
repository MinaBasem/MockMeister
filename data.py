from pandas import json_normalize
import requests
import json
import random
import string

common_verbs = [
    "running", "walking", "talking", "thinking", "eating", "drinking", "sleeping",
    "working", "reading", "writing", "watching", "listening", "cooking", "cleaning",
    "playing", "singing", "dancing", "laughing", "crying", "smiling", "frowning",
    "sitting", "standing", "lying", "kneeling", "jumping", "hopping", "skipping",
    "climbing", "swimming", "flying", "driving", "riding", "walking", "jogging",
    "sprinting", "cycling", "rowing", "sailing", "fishing", "hunting", "camping",
    "hiking", "shopping", "traveling", "learning", "teaching", "studying", "researching",
    "practicing", "exercising", "relaxing", "resting", "sleeping", "dreaming", "waking",
    "worrying", "hoping", "dreaming", "believing", "wondering", "arguing", "discussing",
    "debating", "agreeing", "disagreeing", "helping", "sharing", "caring", "loving",
    "hating", "fearing", "trusting", "respecting", "needing", "wanting", "desiring",
    "wishing", "planning", "organizing", "preparing", "deciding", "choosing", "solving",
    "fixing", "building", "creating", "destroying", "changing", "transforming",
    "developing", "growing", "evolving", "learning", "adapting", "surviving", "thriving"
]

common_nouns = [
    "computer", "phone", "book", "table", "chair", "house", "car", "street", "city", "country",
    "person", "man", "woman", "child", "parent", "friend", "teacher", "student", "doctor", "nurse",
    "animal", "dog", "cat", "bird", "fish", "tree", "flower", "fruit", "vegetable", "food",
    "water", "milk", "coffee", "tea", "juice", "money", "paper", "pen", "pencil", "computer",
    "shirt", "pants", "dress", "shoes", "hat", "bag", "bed", "sofa", "television", "radio",
    "game", "music", "movie", "book", "sport", "player", "team", "ball", "field", "court",
    "weather", "sun", "moon", "rain", "snow", "wind", "cloud", "day", "night", "time",
    "room", "window", "door", "floor", "ceiling", "wall", "kitchen", "bathroom", "bedroom", "living room",
    "school", "hospital", "store", "restaurant", "office", "park", "beach", "mountain", "river", "lake"
]

class DataGeneration():
    def generate_data(self, count, requested_data_fields):
        random_data_generator_url = "https://random-data-api.com/api/v2/users?size=" + str(count) + "&is_xml=true"
        response = requests.get(random_data_generator_url)
        df = json_normalize(json.loads(response.text))
        df = DataTransformation.transform_data(self, df, requested_data_fields)
        print(df[requested_data_fields])
        return df[requested_data_fields]
    
class DataTransformation():
    @staticmethod
    def generate_completely_random_email():    
        
        # Generates completely random emails from scratch
        separator_options = ['', '_', '.']
        verb_part = ''.join(random.choices(common_verbs))
        username = verb_part + random.choice(separator_options) + ''.join(random.choices(common_nouns))
        return username

    @staticmethod
    def randomize_email(email):   # Either randomizes obtained email or creates a completely new one
        
        domain_options, domain_probabilities = ['@gmail', '@yahoo', '@hotmail'], [0.6, 0.3, 0.1]    # Probability of domain occurence
        separator_options = ['', '_', '.']
        
        selected_domain = random.choices(domain_options, weights=domain_probabilities)[0]

        modify_or_generate_email = [0, 1]
        modify_or_generate_email_probabilites = [0.7, 0.3]
        modify_or_generate_email_probability = random.choices(modify_or_generate_email, weights=modify_or_generate_email_probabilites)[0]

        if modify_or_generate_email_probability == 1:      # Generates new email
            new_email_username = DataTransformation.generate_completely_random_email()
            new_random_email = new_email_username + selected_domain
            return new_random_email
        else:                               # modifies API obtained email
            email = email.replace('@email', selected_domain)
            separator_option = random.choice(separator_options)
            email = email.replace('.', separator_option, 1)

            if random.choice([0, 1]) == 1:  # Adds a random number to email or not
                random_number_str = str(random.randint(0, 9999)).zfill(4) # possibly remove zfill
                email_parts = email.split('@')
                email = email_parts[0] + separator_option + random_number_str + "@" + email_parts[1]
            return email

    def transform_data(self, df, requested_data_fields):
        if 'email' in requested_data_fields:
            df['email'] = df['email'].apply(DataTransformation.randomize_email)
            return df
        else:
            return df
    