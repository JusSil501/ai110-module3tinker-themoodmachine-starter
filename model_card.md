# Model Card: Mood Machine

This model card covers **both** versions of the Mood Machine mood classifier:

1. A **rule-based model** implemented in `mood_analyzer.py`
2. A **machine learning model** implemented in `ml_experiments.py` using scikit-learn

---

## 1. Model Overview

**Model type:**
Both models were built and compared. The rule-based version was the primary focus; the ML version was used as a contrast.

**Intended purpose:**
Classify short social media-style posts as one of four mood labels: `positive`, `negative`, `neutral`, or `mixed`. The system is designed as a learning tool, not a production classifier.

**How it works (brief):**
The rule-based model preprocesses text (lowercase, strip punctuation, split on whitespace), then loops over tokens and adds +1 for each positive word match and −1 for each negative word match. If the preceding token is a negation word (e.g. `not`, `never`, `don't`), the score is flipped. The final integer score maps to a label: `> 0` → positive, `< 0` → negative, `== 0` → neutral. The ML model uses a bag-of-words representation (CountVectorizer) and trains a logistic regression classifier directly on the labeled posts.

---

## 2. Data

**Dataset description:**
The dataset contains 17 labeled posts total. 6 came from the starter; 8 were added to cover slang, emojis, sarcasm, and mixed emotion; 3 more were added as sensitivity tests for negation and flat language. All posts are short (1–2 sentences), written in informal English.

**Labeling process:**
Labels were chosen by reading each post and judging the dominant emotional tone. Posts with both clear positive and clear negative signals were labeled `mixed`. Posts designed as sarcasm were labeled by their *intended* meaning, not the surface keywords — e.g. "I love when my alarm goes off on a Saturday 🙄" was labeled `negative` even though `love` appears, because the 🙄 emoji and the framing signal sarcasm.

Hard-to-label posts:
- `"Feeling tired but kind of hopeful"` — `tired` is negative but `hopeful` is genuinely optimistic. `mixed` seems right, but `negative` is defensible.
- `"Feeling meh, nothing special going on"` — labeled `neutral` but `meh` could be read as mild dissatisfaction (`negative`).
- `"This is fine"` — culturally loaded; reads as resigned sarcasm in meme culture but was labeled `neutral` at face value.

**Important characteristics of the dataset:**
- Contains internet slang: `no cap`, `fire`, `lowkey`
- Contains emoji signals: 😊 🔥 🙄 😭 😤 🎉
- Contains one clear sarcasm example
- Contains mixed-emotion posts
- Contains negation patterns: `not bad`, `not happy`, `never want to`
- Small size (17 examples) — not representative of any real population

**Possible issues with the dataset:**
- Heavily English, Western, internet-centric — unlikely to generalize to other dialects or languages
- Tiny size means any single label change can shift ML accuracy significantly
- No held-out test split — evaluation is on training data only, so numbers are optimistic

---

## 3. How the Rule-Based Model Works

**Scoring rules:**
- `preprocess`: strips ASCII punctuation (`.,!?;:'"()[]{}`) using `re.sub`, lowercases, splits on whitespace. Emoji characters are preserved because they are multi-byte Unicode and survive the regex.
- `score_text`: loops over tokens, adds +1 for positive word matches and −1 for negative word matches. Checks the previous token against a negation set (`not`, `no`, `never`, `don't`, `can't`, `won't`, `isn't`, `doesn't`, `hardly`, `barely`) and flips the sign when negated.
- `predict_label`: score > 0 → `positive`, score < 0 → `negative`, score == 0 → `neutral`. No `mixed` label is ever predicted.
- Word lists were expanded with slang (`fire`, `lit`, `stoked`), common positives/negatives (`proud`, `failed`, `meh`, `ugh`), and emoji entries (😊 🔥 → positive; 😭 😤 🙄 → negative).

**Strengths:**
- Transparent and inspectable — `explain()` shows exactly which tokens matched and why
- Negation works for simple cases: "not happy" → negative ✓, "not bad" → positive ✓
- Emoji signals work when the emoji is in the word list
- Predictable: same input always gives same output

**Weaknesses:**
- Cannot predict `mixed` — the single net score collapses opposing signals into a number, losing the information that *both* were present
- Sarcasm is invisible: "I love when my alarm goes off on a Saturday 🙄" scores `love` (+1) and `🙄` (−1) → net = 0 → predicts `neutral` instead of `negative`
- Vocabulary gap: `hopeful`, `lowkey`, `vibe`, `🎉` have no entries and contribute 0
- Words dominate by frequency, not importance — a post with three weak positive words beats one with a single strong negative word

---

## 4. How the ML Model Works

**Features used:**
Bag of words using `CountVectorizer` — each unique word in the training set becomes a feature column, and each post is represented by raw word counts.

**Training data:**
The model trained on all 17 posts in `SAMPLE_POSTS` and their labels in `TRUE_LABELS`. The same data was used for evaluation (no train/test split).

**Training behavior:**
ML accuracy was 100% on 17 examples before the sensitivity posts were added (14 examples), and remained 100% after adding 3 more. This is expected: logistic regression can memorize small datasets almost perfectly. When a post was added that shared words with training posts but had a different label, accuracy dropped until the model weight adjusted — demonstrating sensitivity to label consistency.

**Strengths and weaknesses:**
The ML model correctly predicted all `mixed` labels and the sarcasm post — things the rule-based model entirely failed on. However, this is not because the ML model "understands" sarcasm. It likely memorized the word `alarm` or the emoji `🙄` from the single training example. Add a second sarcastic post with different vocabulary and it would likely fail. The model is entirely opaque — there is no equivalent of `explain()`.

---

## 5. Evaluation

**How the model was evaluated:**
Both models were run against the full 17-post labeled dataset using the evaluation functions in `main.py` and `ml_experiments.py`. This is training accuracy only — no held-out test set was used.

**Rule-based results: 71% accuracy (12/17 correct)**

Examples of correct predictions:
- `"I love this class so much"` → positive. `love` is in POSITIVE_WORDS, no negation before it, clean match.
- `"I am not happy about this"` → negative. Negation handling caught `not` before `happy` and flipped the signal.
- `"Not bad at all, actually kind of fun"` → positive. `not` negated `bad` (−1 → +1) and `fun` added +1, total = +2.

Examples of incorrect predictions:
- `"Feeling tired but kind of hopeful"` → predicted `negative`, true `mixed`. `tired` = −1, `hopeful` is not in any word list = 0, net = −1. The vocabulary gap for `hopeful` means the positive half of the emotion is completely invisible.
- `"I love when my alarm goes off on a Saturday 🙄"` → predicted `neutral`, true `negative`. `love` = +1, `🙄` = −1, net = 0. The sarcasm is structurally undetectable; the rule-based model balanced two opposing signals and landed on neutral, which is wrong for opposite reasons.
- `"Exhausted and drained but so proud we shipped it 🎉"` → predicted `neutral`, true `mixed`. `exhausted` = −1, `drained` = −1, `proud` = +1 (added to word list), `🎉` = 0 (not in list), net = −1. Actually predicted `negative` here, not `neutral` — still wrong but for a different reason than expected.

**ML results: 100% accuracy (17/17 correct)**
The ML model correctly predicted every post, including all three `mixed` labels and the sarcasm post that stumped the rule-based system. This result is misleading — see Limitations.

---

## 6. Limitations

**Rule-based model:**
- **Cannot represent `mixed` emotions.** The net score collapses all signals into one number. A post like "Exhausted but proud" will always be dominated by whichever side has more/stronger words. This is a fundamental architectural limit, not a tuning problem.
- **Sarcasm is structurally invisible.** `"I love when my alarm goes off on a Saturday 🙄"` is predicted `neutral` because `love` and `🙄` cancel out. No amount of threshold-tuning fixes this — the model would need word-order context or tone awareness it does not have.
- **Vocabulary coverage determines coverage.** Any word not in POSITIVE_WORDS or NEGATIVE_WORDS contributes zero. `hopeful`, `vibe`, `lowkey`, `🎉`, `whatever` are all invisible to the current model.
- **Negation window is one token.** "I really do not feel happy" fails because `not` is two positions before `happy`, outside the one-token look-back window.

**ML model:**
- **100% training accuracy is meaningless here.** The model trained and was tested on the same 17 examples. Logistic regression memorizes small datasets. This number says nothing about how the model would perform on new posts.
- **Brittle to dataset changes.** With only 17 examples, adding or relabeling two posts can shift accuracy by 10–15 percentage points. The model has no robust signal — it is fitting noise.
- **Opaque.** There is no `explain()` equivalent. When the ML model predicts `mixed` for the sarcasm post, we cannot easily determine which token(s) drove that decision.

---

## 7. Ethical Considerations

- **Misclassifying distress.** A message like "I'm fine 🙂" (a common deflection when someone is not fine) would likely be predicted `positive` by both models. Deploying mood detection in a mental health or crisis context using these rules would be actively harmful.
- **Dialect and slang bias.** The dataset is entirely Standard American Internet English — AAVE, regional slang, non-English code-switching, and cultural idioms are absent from the word lists. Posts from speakers outside that narrow range would have most of their vocabulary ignored (scored as zero), leading to systematic misclassification as `neutral`.
- **Emoji ambiguity.** `💀` is used in internet culture to signal something is extremely funny, but its literal meaning is death. Assigning it a sentiment label requires cultural context. This model makes no attempt to handle that ambiguity.
- **Privacy.** Any real deployment that analyzes personal messages for mood without explicit consent raises privacy concerns, regardless of how simple the model is.

---

## 8. ML vs. Rule-Based Comparison

| | Rule-Based | ML (Logistic Regression) |
|---|---|---|
| Accuracy (training) | 71% | 100% |
| Predicts `mixed`? | Never | Yes (by memorization) |
| Handles sarcasm? | No | Appears to (on this dataset) |
| Explainable? | Yes — `explain()` | No |
| Sensitive to dataset size? | Low | Very high |
| Generalizes to new posts? | Proportional to vocabulary | Unknown — no test set |

The rule-based model fails at `mixed` and sarcasm because its architecture cannot represent them. The ML model appears to succeed at both, but only because it has memorized 17 training examples. The most important difference is not accuracy — it is that the rule-based model's failures are *diagnosable*, while the ML model's successes are *unverifiable* on this dataset. Adding a real held-out test set of 10–20 unseen posts would almost certainly reduce ML accuracy significantly and bring it closer to the rule-based baseline.

## 9. Ideas for Improvement

- Add a real train/test split — even 12 train / 5 test would give more honest numbers
- Use TF-IDF instead of raw counts to reduce the weight of very common words
- Add a `mixed` threshold to the rule-based model: if both positive and negative hits exist and the net score is near zero, predict `mixed` instead of `neutral`
- Extend negation window from 1 token to 2 ("really not happy")
- Add a sarcasm signal: if a strong positive word appears alongside a sarcasm-marker emoji (🙄, 😒), downweight or flip the positive score
- Use a pre-trained embedding model (e.g. a small transformer) that encodes word context rather than treating words as independent bags
