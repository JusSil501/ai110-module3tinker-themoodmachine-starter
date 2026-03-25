# The Mood Machine

The Mood Machine is a text mood classifier built in two versions: a transparent rule-based system and a tiny machine learning model. Given a short post, it predicts whether the mood is **positive**, **negative**, **neutral**, or **mixed**.

This lab is about reasoning through how models work, where they fail, and why even small design choices — word lists, thresholds, negation rules — shape what a system can and cannot do.

---

## Repo Structure

```plaintext
├── dataset.py         # Word lists and 17 labeled example posts
├── mood_analyzer.py   # Rule-based classifier (preprocess → score → label)
├── main.py            # Runs evaluation, batch demo, and interactive mode
├── ml_experiments.py  # Logistic regression classifier trained on the same data
├── model_card.md      # Completed documentation of both models
└── requirements.txt   # scikit-learn dependency for ml_experiments.py
```

---

## Getting Started

1. Make sure your Python environment is active.
2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the rule-based model:

    ```bash
    python main.py
    ```

4. Run the ML model:

    ```bash
    python ml_experiments.py
    ```

---

## What Was Built

### dataset.py
- Started with 6 labeled posts and two small word lists.
- Expanded `POSITIVE_WORDS` with slang (`fire`, `lit`, `stoked`) and emoji signals (😊 🔥).
- Expanded `NEGATIVE_WORDS` with common negatives (`failed`, `meh`, `ugh`, `drained`) and emoji signals (😭 😤 🙄).
- Added 11 new posts covering: slang, emojis, sarcasm, mixed emotion, negation, and flat neutral language.
- Final dataset: **17 posts**, all labeled. `len(SAMPLE_POSTS) == len(TRUE_LABELS)`.

### mood_analyzer.py
- `preprocess`: strips ASCII punctuation with `re.sub` while preserving emoji characters; lowercases and splits on whitespace.
- `score_text`: loops over tokens, scores +1 for positive word matches and −1 for negative. Implements **negation handling** — if the preceding token is a negation word (`not`, `never`, `don't`, `can't`, etc.), the score is flipped.
- `predict_label`: maps score to label — `> 0` → positive, `< 0` → negative, `== 0` → neutral.

---

## Evaluation Results

### Rule-based model — 71% accuracy (12/17)

| Post | Predicted | True | Notes |
|---|---|---|---|
| "I love this class so much" | positive | positive | Clean keyword match |
| "I am not happy about this" | negative | negative | Negation handled correctly |
| "Not bad at all, actually kind of fun" | positive | positive | Double negation + keyword |
| "Feeling tired but kind of hopeful" | negative | mixed | `hopeful` not in word list |
| "I love when my alarm goes off on a Saturday 🙄" | neutral | negative | Sarcasm — `love` and `🙄` cancel out |
| "Exhausted and drained but so proud we shipped it 🎉" | negative | mixed | `🎉` not in word list, negatives dominate |

**Failure pattern:** The model cannot predict `mixed` at all — a single net score collapses both positive and negative signals into one number. Sarcasm fails because opposing keyword signals cancel each other.

### ML model — 100% accuracy (17/17)

Correctly predicted all `mixed` labels and the sarcasm post. **This number is misleading** — the model trained and tested on the same 17 examples. It has memorized the dataset, not learned to generalize. No held-out test set was used.

### Key difference

The rule-based model's failures are **diagnosable** — `explain()` shows exactly which tokens matched. The ML model's apparent successes are **unverifiable** on this dataset. A real test set would close most or all of that accuracy gap.

---

## Known Limitations

- **`mixed` is architecturally unpredictable** in the rule-based model. The net score cannot represent simultaneous positive and negative signals.
- **Sarcasm is invisible** to keyword matching. "I love when my alarm goes off" has the same word fingerprint as a genuine compliment.
- **Vocabulary gaps** mean any word not in the lists scores zero — `hopeful`, `vibe`, `whatever`, `🎉` are all ignored.
- **ML accuracy is overfitted.** 100% on 17 training examples reflects memorization, not generalization.
- **No dialect coverage.** The dataset is Standard American Internet English. AAVE, regional slang, and non-English text are not represented.

---

## TF Notes

The core concept students need to internalize is that a numeric score is a **lossy compression** of language — it flattens every word to +1 or −1 and discards word order, context, and tone, which is exactly why sarcasm and mixed emotion are structurally impossible to capture with this design.

**Where students most often get stuck:** `score_text` returning `None` because the loop runs but there is no `return` statement outside it, and then `predict_label` silently propagating `None` through the accuracy calculation with no obvious error.

**Where AI was helpful:** Brainstorming edge-case posts, walking through token-level scoring for a specific sentence, and explaining *why* a prediction is wrong without giving away the fix. Asking "what does `explain()` show for this post?" is a productive prompt structure.

**Where AI was misleading:** When I asked for "a fix for sarcasm," suggested regex or keyword patches appeared to work on the training examples but generalized poorly. The better framing is: sarcasm is not a bug to patch, it is a fundamental limit of keyword matching — and recognizing that is the point.

**Guiding question without giving the answer:** "What does `analyzer.explain(text)` print — which tokens actually matched, and what was the net score?" That surfaces the data flow without solving the problem for them.
