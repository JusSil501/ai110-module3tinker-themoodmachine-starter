"""
Shared data for the Mood Machine lab.

This file defines:
  - POSITIVE_WORDS: starter list of positive words
  - NEGATIVE_WORDS: starter list of negative words
  - SAMPLE_POSTS: short example posts for evaluation and training
  - TRUE_LABELS: human labels for each post in SAMPLE_POSTS
"""

# ---------------------------------------------------------------------
# Starter word lists
# ---------------------------------------------------------------------

POSITIVE_WORDS = [
    "happy",
    "great",
    "good",
    "love",
    "excited",
    "awesome",
    "fun",
    "chill",
    "relaxed",
    "amazing",
    # expanded: slang and common positives
    "best",
    "proud",
    "thrilled",
    "fire",      # slang for excellent
    "lit",       # slang for exciting
    "stoked",
    "hyped",
    "blessed",
    "grateful",
    "winning",
    # emoji signals
    "😊",
    "😄",
    "🎉",
    "❤️",
    "🔥",
]

NEGATIVE_WORDS = [
    "sad",
    "bad",
    "terrible",
    "awful",
    "angry",
    "upset",
    "tired",
    "stressed",
    "hate",
    "boring",
    # expanded: slang and common negatives
    "failed",
    "exhausted",
    "meh",
    "ugh",
    "miserable",
    "drained",
    "frustrated",
    "dread",
    "sick",      # context-dependent; treated as negative here
    "rough",
    # emoji signals
    "😭",
    "😤",
    "😡",
    "💔",
    "🙄",        # eye-roll — often marks sarcasm or annoyance
]

# ---------------------------------------------------------------------
# Starter labeled dataset
# ---------------------------------------------------------------------

# Short example posts written as if they were social media updates or messages.
SAMPLE_POSTS = [
    "I love this class so much",
    "Today was a terrible day",
    "Feeling tired but kind of hopeful",
    "This is fine",
    "So excited for the weekend",
    "I am not happy about this",
    # --- new posts added ---
    "Best day ever I literally cannot stop smiling 😊",           # easy positive
    "Failed my exam and missed the bus ugh",                       # easy negative
    "Lowkey stressed but the vibe is good today",                  # mixed: stress + good
    "I love when my alarm goes off on a Saturday 🙄",             # sarcasm — rule-based trap
    "Exhausted and drained but so proud we shipped it 🎉",        # mixed: negative + positive
    "no cap this is straight fire 🔥",                            # slang positive
    "Feeling meh, nothing special going on",                       # neutral/flat
    "So sick of everything honestly 😤",                           # negative (sick = ill here)
    # --- sensitivity test posts ---
    "Not bad at all, actually kind of fun",                        # negation flips bad -> positive
    "I never want to do that again 😭",                            # negation + emoji, clear negative
    "Whatever, it is what it is",                                  # flat neutral
]

# Human labels for each post above.
# Allowed labels in the starter:
#   - "positive"
#   - "negative"
#   - "neutral"
#   - "mixed"
TRUE_LABELS = [
    "positive",  # "I love this class so much"
    "negative",  # "Today was a terrible day"
    "mixed",     # "Feeling tired but kind of hopeful"
    "neutral",   # "This is fine"
    "positive",  # "So excited for the weekend"
    "negative",  # "I am not happy about this"
    # --- new labels ---
    "positive",  # "Best day ever I literally cannot stop smiling 😊"
    "negative",  # "Failed my exam and missed the bus ugh"
    "mixed",     # "Lowkey stressed but the vibe is good today"
    "negative",  # "I love when my alarm goes off on a Saturday 🙄"  (sarcasm)
    "mixed",     # "Exhausted and drained but so proud we shipped it 🎉"
    "positive",  # "no cap this is straight fire 🔥"
    "neutral",   # "Feeling meh, nothing special going on"
    "negative",  # "So sick of everything honestly 😤"
    # --- sensitivity test labels ---
    "positive",  # "Not bad at all, actually kind of fun"
    "negative",  # "I never want to do that again 😭"
    "neutral",   # "Whatever, it is what it is"
]

# TODO: Add 5-10 more posts and labels.
#
# Requirements:
#   - For every new post you add to SAMPLE_POSTS, you must add one
#     matching label to TRUE_LABELS.
#   - SAMPLE_POSTS and TRUE_LABELS must always have the same length.
#   - Include a variety of language styles, such as:
#       * Slang ("lowkey", "highkey", "no cap")
#       * Emojis (":)", ":(", "🥲", "😂", "💀")
#       * Sarcasm ("I absolutely love getting stuck in traffic")
#       * Ambiguous or mixed feelings
#
# Tips:
#   - Try to create some examples that are hard to label even for you.
#   - Make a note of any examples that you and a friend might disagree on.
#     Those "edge cases" are interesting to inspect for both the rule based
#     and ML models.
#
# Example of how you might extend the lists:
#
# SAMPLE_POSTS.append("Lowkey stressed but kind of proud of myself")
# TRUE_LABELS.append("mixed")
#
# Remember to keep them aligned:
#   len(SAMPLE_POSTS) == len(TRUE_LABELS)
