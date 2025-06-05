import random
import string
import pyperclip

class PasswordGenerator:
    def __init__(self,
                 length=16,
                 use_upper=True,
                 use_lower=True,
                 use_digits=True,
                 use_special=True,
                 avoid_similar=True,
                 avoid_ambiguous=True):
        
        self.length = length
        self.use_upper = use_upper
        self.use_lower = use_lower
        self.use_digits = use_digits
        self.use_special = use_special
        self.avoid_similar = avoid_similar
        self.avoid_ambiguous = avoid_ambiguous

        self.similar_chars = 'ilLI|`oO0'
        self.ambiguous_chars = '{}[]()/\\\'"`~,;:.<>'

        self.char_sets = {
            'upper': string.ascii_uppercase,
            'lower': string.ascii_lowercase,
            'digits': string.digits,
            'special': '!@#$%^&*()-_=+'
        }

    def _filter_characters(self, charset):
        if self.avoid_similar:
            charset = ''.join(c for c in charset if c not in self.similar_chars)
        if self.avoid_ambiguous and charset == self.char_sets['special']:
            charset = ''.join(c for c in charset if c not in self.ambiguous_chars)
        return charset

    def generate(self):
        selected_sets = []
        all_chars = ''

        if self.use_upper:
            upper = self._filter_characters(self.char_sets['upper'])
            selected_sets.append(upper)
            all_chars += upper
        if self.use_lower:
            lower = self._filter_characters(self.char_sets['lower'])
            selected_sets.append(lower)
            all_chars += lower
        if self.use_digits:
            digits = self._filter_characters(self.char_sets['digits'])
            selected_sets.append(digits)
            all_chars += digits
        if self.use_special:
            special = self._filter_characters(self.char_sets['special'])
            selected_sets.append(special)
            all_chars += special

        if not all_chars:
            raise ValueError("At least one character type must be selected.")

        # Ensure at least one character from each selected set is in the password
        password = [random.choice(char_set) for char_set in selected_sets]

        # Fill the rest of the password length with random choices from all valid characters
        password += random.choices(all_chars, k=self.length - len(password))

        # Shuffle to prevent predictable pattern
        random.shuffle(password)

        final_password = ''.join(password)
        pyperclip.copy(final_password)  # Copy to clipboard
        return final_password


# Example usage
if __name__ == "__main__":
    generator = PasswordGenerator(length=10, avoid_similar=True, avoid_ambiguous=True)
    password = generator.generate()
    print("Generated Password:", password)
    print("✅ Copied to clipboard!")
