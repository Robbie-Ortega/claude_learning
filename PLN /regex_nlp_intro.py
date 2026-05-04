"""
Regular Expressions in NLP — Introduction
Covers: tokenization, cleaning, pattern extraction, and text normalization
"""

import re

sample_text = """
Hello! My name is Dr. Jane Smith. I work at OpenAI (founded in 2015).
You can reach me at jane.smith@openai.com or call +1 (555) 867-5309.
Visit https://openai.com for more info. I'm excited about LLMs & NLP!
Today's date: 04/29/2026. Price: $1,299.99. #AI #MachineLearning
"""

# ─── 1. Basic matching ────────────────────────────────────────────────────────

print("=" * 60)
print("1. BASIC MATCHING")
print("=" * 60)

# re.search  — finds first match anywhere in the string
match = re.search(r"OpenAI", sample_text)
print(f"Found 'OpenAI' at position: {match.start()}–{match.end()}")

# re.findall — returns a list of all non-overlapping matches
words_with_digits = re.findall(r"\b\w*\d\w*\b", sample_text)
print(f"Words containing digits: {words_with_digits}")

# ─── 2. Character classes ─────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("2. CHARACTER CLASSES")
print("=" * 60)

# \d  digit, \w  word char, \s  whitespace, .  any char
# [abc]  one of, [^abc]  none of, [a-z]  range

vowels       = re.findall(r"[aeiouAEIOU]", sample_text)
non_alphanum = re.findall(r"[^\w\s]", sample_text)          # punctuation
capitalized  = re.findall(r"\b[A-Z][a-z]+\b", sample_text)  # Title-case words

print(f"Vowel count       : {len(vowels)}")
print(f"Punctuation chars : {set(non_alphanum)}")
print(f"Title-case words  : {capitalized}")

# ─── 3. Quantifiers ──────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("3. QUANTIFIERS  (*, +, ?, {n,m})")
print("=" * 60)

# *  zero or more   + one or more   ? zero or one   {n,m} between n and m

phone_numbers = re.findall(r"\+?\d[\d\s\-().]{7,}\d", sample_text)
dates         = re.findall(r"\b\d{1,2}/\d{1,2}/\d{4}\b", sample_text)
prices        = re.findall(r"\$[\d,]+(?:\.\d{2})?", sample_text)

print(f"Phone numbers : {phone_numbers}")
print(f"Dates         : {dates}")
print(f"Prices        : {prices}")

# ─── 4. Groups & capturing ───────────────────────────────────────────────────

print("\n" + "=" * 60)
print("4. GROUPS & CAPTURING")
print("=" * 60)

# (...)  capturing group   (?:...)  non-capturing   (?P<name>...)  named group

email_pattern = r"(?P<user>[\w.+-]+)@(?P<domain>[\w-]+\.[a-z]{2,})"
for m in re.finditer(email_pattern, sample_text):
    print(f"Email → user='{m.group('user')}', domain='{m.group('domain')}'")

url_pattern = r"https?://(?:www\.)?[\w./%-]+"
urls = re.findall(url_pattern, sample_text)
print(f"URLs : {urls}")

# ─── 5. Anchors & boundaries ─────────────────────────────────────────────────

print("\n" + "=" * 60)
print("5. ANCHORS & WORD BOUNDARIES")
print("=" * 60)

# ^  start of string/line   $  end   \b  word boundary

lines          = sample_text.strip().split("\n")
lines_with_i   = [l for l in lines if re.search(r"^I\b", l.strip())]
hashtags       = re.findall(r"(?<!\w)#\w+", sample_text)  # lookbehind
acronyms       = re.findall(r"\b[A-Z]{2,}\b", sample_text)

print(f"Lines starting with 'I' : {lines_with_i}")
print(f"Hashtags                : {hashtags}")
print(f"Acronyms                : {acronyms}")

# ─── 6. Common NLP cleaning tasks ────────────────────────────────────────────

print("\n" + "=" * 60)
print("6. NLP TEXT CLEANING")
print("=" * 60)

def clean_text(text: str) -> str:
    text = re.sub(r"https?://\S+", "", text)            # remove URLs
    text = re.sub(r"[\w.+-]+@[\w-]+\.[a-z]{2,}", "", text)  # remove emails
    text = re.sub(r"#\w+", "", text)                    # remove hashtags
    text = re.sub(r"[^\w\s]", " ", text)                # remove punctuation
    text = re.sub(r"\b\d+\b", "", text)                 # remove standalone numbers
    text = re.sub(r"\s+", " ", text)                    # collapse whitespace
    return text.strip().lower()

cleaned = clean_text(sample_text)
print(f"Cleaned:\n{cleaned}")

# ─── 7. Tokenization with regex ──────────────────────────────────────────────

print("\n" + "=" * 60)
print("7. REGEX TOKENIZATION")
print("=" * 60)

# Split on whitespace — simplest tokenizer
simple_tokens = re.split(r"\s+", cleaned)

# Smarter: keep contractions and hyphenated words together
token_pattern  = re.compile(r"\b\w+(?:'\w+|-\w+)*\b")
smart_tokens   = token_pattern.findall(sample_text.lower())

print(f"Simple token count : {len(simple_tokens)}")
print(f"Smart token sample : {smart_tokens[:12]}")

# ─── 8. Flags ────────────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("8. USEFUL FLAGS")
print("=" * 60)

multiline_text = "Hello world\nhello NLP\nHELLO REGEX"

# re.IGNORECASE  — case-insensitive matching
case_insensitive = re.findall(r"hello", multiline_text, re.IGNORECASE)

# re.MULTILINE   — ^ and $ match start/end of each line
line_starts      = re.findall(r"^\w+", multiline_text, re.MULTILINE)

# re.VERBOSE     — allows whitespace and comments inside pattern
verbose_email = re.compile(r"""
    [\w.+-]+        # local part
    @               # at sign
    [\w-]+          # domain name
    \.              # dot
    [a-z]{2,}       # TLD
""", re.VERBOSE | re.IGNORECASE)

emails_found = verbose_email.findall(sample_text)

print(f"Case-insensitive 'hello' matches : {case_insensitive}")
print(f"First word of each line          : {line_starts}")
print(f"Emails (verbose pattern)         : {emails_found}")

# ─── 9. Substitution — text normalization ────────────────────────────────────

print("\n" + "=" * 60)
print("9. SUBSTITUTION & NORMALIZATION")
print("=" * 60)

raw = "I luuuuv NLP!!! It's sooooo cooool 😊"

# Collapse repeated characters (common in social media text)
normalized = re.sub(r"(.)\1{2,}", r"\1\1", raw)   # keep at most 2 of any char
print(f"Original   : {raw}")
print(f"Normalized : {normalized}")

# Expand simple contractions
contractions = {"n't": " not", "'re": " are", "'ve": " have", "'ll": " will"}
expanded = sample_text
for contraction, expansion in contractions.items():
    expanded = re.sub(re.escape(contraction), expansion, expanded, flags=re.IGNORECASE)
print(f"\nContraction sample (first 120 chars):\n{expanded[:120].strip()}")

print("\n" + "=" * 60)
print("Done! Key takeaways:")
print("  re.search / re.findall / re.finditer — locate matches")
print("  re.sub                               — replace matches")
print("  Groups (...)  and named groups (?P<name>...) — capture parts")
print("  Flags: IGNORECASE, MULTILINE, VERBOSE")
print("=" * 60)
