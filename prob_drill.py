"""
MA206X Probability & Random Variables — Gamified Drill App
WPR I Review: Lessons 6-14 (Devore sections 2.1–4.4)
"""

import streamlit as st
import math
import random
import time
from dataclasses import dataclass, field
from typing import Optional

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="MA206X Prob Drill", page_icon="🎯", layout="wide")

# ── Data structures ──────────────────────────────────────────────────────────

TOPICS = [
    "Probability Basics",
    "Conditional Prob & Bayes",
    "Counting & Independence",
    "Discrete RVs & PMFs",
    "Binomial Distribution",
    "Poisson Distribution",
    "Continuous RVs & PDFs",
    "Normal Distribution",
    "Exponential Distribution",
]

TOPIC_COLORS = {
    "Probability Basics": "#4CAF50",
    "Conditional Prob & Bayes": "#2196F3",
    "Counting & Independence": "#FF9800",
    "Discrete RVs & PMFs": "#9C27B0",
    "Binomial Distribution": "#F44336",
    "Poisson Distribution": "#00BCD4",
    "Continuous RVs & PDFs": "#E91E63",
    "Normal Distribution": "#3F51B5",
    "Exponential Distribution": "#FF5722",
}

LEVELS = [
    (0, "Recruit"),
    (50, "Private"),
    (120, "Specialist"),
    (220, "Corporal"),
    (350, "Sergeant"),
    (500, "Staff Sergeant"),
    (700, "Sergeant First Class"),
    (950, "Master Sergeant"),
    (1250, "First Sergeant"),
    (1600, "Sergeant Major"),
    (2000, "Second Lieutenant"),
    (2500, "First Lieutenant"),
    (3100, "Captain"),
    (3800, "Major"),
    (4600, "Lieutenant Colonel"),
    (5500, "Colonel"),
    (6500, "Brigadier General"),
    (7600, "Major General"),
    (8800, "Lieutenant General"),
    (10000, "General"),
]

LEVEL_ICONS = {
    "Recruit": "🔰",
    "Private": "⭐",
    "Specialist": "⭐⭐",
    "Corporal": "🎖️",
    "Sergeant": "🎖️🎖️",
    "Staff Sergeant": "🎖️🎖️🎖️",
    "Sergeant First Class": "🏅",
    "Master Sergeant": "🏅🏅",
    "First Sergeant": "🏅🏅🏅",
    "Sergeant Major": "👑",
    "Second Lieutenant": "⚔️",
    "First Lieutenant": "⚔️⚔️",
    "Captain": "🛡️",
    "Major": "🛡️⚔️",
    "Lieutenant Colonel": "🦅",
    "Colonel": "🦅🦅",
    "Brigadier General": "💫",
    "Major General": "💫💫",
    "Lieutenant General": "💫💫💫",
    "General": "💫💫💫💫",
}


def get_level(xp):
    name = "Recruit"
    current_min = 0
    next_threshold = 50
    for i, (threshold, lname) in enumerate(LEVELS):
        if xp >= threshold:
            name = lname
            current_min = threshold
            next_threshold = LEVELS[i + 1][0] if i + 1 < len(LEVELS) else threshold + 1000
    return name, current_min, next_threshold


# ── Question bank ────────────────────────────────────────────────────────────

def build_questions():
    """Return the full question bank as a list of dicts."""
    Q = []

    def tf(topic, text, answer, explanation):
        Q.append(dict(topic=topic, type="tf", text=text, answer=answer, explanation=explanation))

    def mc(topic, text, options, answer, explanation):
        Q.append(dict(topic=topic, type="mc", text=text, options=options, answer=answer, explanation=explanation))

    def num(topic, text, answer, tol, explanation, unit=""):
        Q.append(dict(topic=topic, type="num", text=text, answer=answer, tol=tol, explanation=explanation, unit=unit))

    # ═══════════════════════════════════════════════════════════════════════
    # 1. PROBABILITY BASICS (Lessons 6-8, sections 2.1-2.4)
    # ═══════════════════════════════════════════════════════════════════════
    tf("Probability Basics",
       r"If $P(A) = 0.5$ and $P(B) = 0.3$, then $A$ and $B$ must be mutually exclusive.",
       False,
       r"Mutually exclusive means $P(A \cap B) = 0$, which is not determined by individual probabilities alone.")

    tf("Probability Basics",
       r"For any event $A$: $P(A) + P(A') = 1$.",
       True,
       "This is the complement rule — one of the axioms of probability.")

    tf("Probability Basics",
       r"If $A$ and $B$ are mutually exclusive, then $P(A \cup B) = P(A) + P(B)$.",
       True,
       r"When $A \cap B = \emptyset$, the addition rule simplifies to $P(A) + P(B)$.")

    tf("Probability Basics",
       r"$P(A \cup B) = P(A) + P(B)$ always holds for any two events.",
       False,
       r"The general addition rule is $P(A \cup B) = P(A) + P(B) - P(A \cap B)$. It only simplifies when $A$ and $B$ are mutually exclusive.")

    tf("Probability Basics",
       r"If $P(A \cup B) = P(A) + P(B)$, then $A$ and $B$ are mutually exclusive.",
       True,
       r"This equality holds iff $P(A \cap B) = 0$, which is the definition of mutually exclusive.")

    tf("Probability Basics",
       "A probability can be negative if the event is very unlikely.",
       False,
       r"Probabilities are always between 0 and 1 inclusive: $0 \leq P(A) \leq 1$. This is an axiom of probability.")

    num("Probability Basics",
        r"A survey of 500 students found 280 play video games ($V$), 200 play instruments ($I$), and 90 do both. Find $P(V \cup I)$.",
        0.78, 0.005,
        r"$P(V \cup I) = P(V) + P(I) - P(V \cap I) = \frac{280}{500} + \frac{200}{500} - \frac{90}{500} = \frac{390}{500} = 0.78$")

    num("Probability Basics",
        r"A survey of 500 students found 280 play video games ($V$), 200 play instruments ($I$), and 90 do both. Find the probability a student does neither activity, i.e. find $P(V' \cap I')$.",
        0.22, 0.005,
        r"$P(V' \cap I') = 1 - P(V \cup I) = 1 - 0.78 = 0.22$")

    mc("Probability Basics",
       r"A fair six-sided die is rolled twice. What is $P(\text{sum} \geq 9)$?",
       ["5/18 ≈ 0.278", "1/4 = 0.250", "1/6 ≈ 0.167", "1/3 ≈ 0.333"],
       "5/18 ≈ 0.278",
       r"Outcomes with sum $\geq 9$: $\{(3,6),(4,5),(4,6),(5,4),(5,5),(5,6),(6,3),(6,4),(6,5),(6,6)\}$ = 10 outcomes. $P = 10/36 = 5/18$.")

    num("Probability Basics",
        r"$P(A) = 0.3$, $P(B) = 0.5$, $A$ and $B$ are independent. Find $P(A \cup B)$.",
        0.65, 0.005,
        r"$P(A \cap B) = P(A) \cdot P(B) = 0.15$. $P(A \cup B) = 0.3 + 0.5 - 0.15 = 0.65$")

    num("Probability Basics",
        r"$P(A) = 0.3$, $P(B) = 0.5$, $A$ and $B$ are independent. Find $P(A' \cap B')$.",
        0.35, 0.005,
        r"$P(A' \cap B') = 1 - P(A \cup B) = 1 - 0.65 = 0.35$. Or $P(A')P(B') = 0.7 \times 0.5 = 0.35$.")

    mc("Probability Basics",
       r"A survey of 500 students found 280 play video games ($V$), 200 play instruments ($I$), and 90 do both. Are $V$ and $I$ independent? (Check whether $P(V) \cdot P(I) = P(V \cap I)$.)",
       ["No, because P(V)P(I) = 0.224 ≠ P(V∩I) = 0.18",
        "Yes, because both events can occur simultaneously",
        "Yes, because P(V∩I) > 0",
        "No, because they are mutually exclusive"],
       "No, because P(V)P(I) = 0.224 ≠ P(V∩I) = 0.18",
       r"Independence requires $P(A \cap B) = P(A)P(B)$. Here $0.56 \times 0.40 = 0.224 \neq 0.18$.")

    # ═══════════════════════════════════════════════════════════════════════
    # 2. CONDITIONAL PROB & BAYES (Lessons 7-8, section 2.4)
    # ═══════════════════════════════════════════════════════════════════════
    num("Conditional Prob & Bayes",
        r"A disease affects 2% of the population. A test has 95% sensitivity, i.e. $P(+ \mid \text{disease}) = 0.95$, and 90% specificity, i.e. $P(- \mid \text{no disease}) = 0.90$. Find $P(\text{positive test})$ using the Law of Total Probability.",
        0.117, 0.002,
        r"$P(T) = P(T|D)P(D) + P(T|D')P(D') = (0.95)(0.02) + (0.10)(0.98) = 0.019 + 0.098 = 0.117$")

    num("Conditional Prob & Bayes",
        r"A disease affects 2% of the population. A test has 95% sensitivity, i.e. $P(+ \mid \text{disease}) = 0.95$, and 90% specificity, i.e. $P(- \mid \text{no disease}) = 0.90$. A person tests positive. Find $P(\text{disease} \mid \text{positive})$ using Bayes' Rule.",
        0.162, 0.005,
        r"$P(D|T) = \frac{P(T|D)P(D)}{P(T)} = \frac{(0.95)(0.02)}{0.117} = \frac{0.019}{0.117} \approx 0.162$")

    mc("Conditional Prob & Bayes",
       r"A disease affects 2% of the population. A test has 95% sensitivity, i.e. $P(+ \mid \text{disease}) = 0.95$, and 90% specificity, i.e. $P(- \mid \text{no disease}) = 0.90$. Why is $P(\text{disease} \mid \text{positive})$ only about 16%?",
       ["Low base rate: most positives come from the large healthy population",
        "The test has poor sensitivity",
        "The test has poor specificity",
        "The disease is contagious"],
       "Low base rate: most positives come from the large healthy population",
       "Even with a good test, a rare disease means most positives are false positives from the 98% healthy group.")

    num("Conditional Prob & Bayes",
        r"A factory has two machines. Machine A produces 60% of items with a 3% defect rate, i.e. $P(\text{defective} \mid A) = 0.03$. Machine B produces 40% with a 5% defect rate, i.e. $P(\text{defective} \mid B) = 0.05$. An item is selected at random. Find $P(\text{defective})$.",
        0.038, 0.002,
        r"$P(D) = P(D|A)P(A) + P(D|B)P(B) = (0.03)(0.60) + (0.05)(0.40) = 0.018 + 0.020 = 0.038$")

    num("Conditional Prob & Bayes",
        r"A factory has two machines. Machine A produces 60% of items with $P(\text{defective} \mid A) = 0.03$. Machine B produces 40% with $P(\text{defective} \mid B) = 0.05$. An item is selected at random and found to be defective. Find $P(B \mid \text{defective})$ using Bayes' Rule.",
        0.526, 0.005,
        r"$P(B|D) = \frac{P(D|B)P(B)}{P(D)} = \frac{(0.05)(0.40)}{0.038} = \frac{0.020}{0.038} \approx 0.526$")

    tf("Conditional Prob & Bayes",
       r"Bayes' Rule allows us to 'flip' a conditional probability: compute $P(A \mid B)$ from $P(B \mid A)$.",
       True,
       r"Bayes' Rule: $P(A|B) = \frac{P(B|A)P(A)}{P(B)}$. It reverses the conditioning.")

    tf("Conditional Prob & Bayes",
       r"$P(A \mid B) = P(B \mid A)$ always.",
       False,
       r"In general $P(A|B) \neq P(B|A)$. They are related by Bayes' Rule but not equal unless $P(A) = P(B)$.")

    mc("Conditional Prob & Bayes",
       r"The Law of Total Probability states $P(B) = $ ?",
       ["P(B|A)P(A) + P(B|A')P(A')",
        "P(A|B)P(B|A)",
        "P(A∩B) + P(A'∩B')",
        "P(A) + P(B) − P(A∩B)"],
       "P(B|A)P(A) + P(B|A')P(A')",
       r"Total probability partitions the sample space: $P(B) = P(B|A)P(A) + P(B|A')P(A')$.")

    num("Conditional Prob & Bayes",
        r"$P(A) = 0.3$, $P(B) = 0.5$, $A$ and $B$ are independent. Find $P(B \mid A')$.",
        0.5, 0.005,
        r"Since $A$ and $B$ are independent, $P(B|A') = P(B) = 0.5$.")

    # ═══════════════════════════════════════════════════════════════════════
    # 3. COUNTING & INDEPENDENCE (Lesson 8, sections 2.3, 2.5)
    # ═══════════════════════════════════════════════════════════════════════
    num("Counting & Independence",
        r"A restaurant offers 3 appetizers, 5 entrées, and 4 desserts. How many different three-course meals (one of each) are possible?",
        60, 0,
        r"Multiplication rule: $3 \times 5 \times 4 = 60$")

    num("Counting & Independence",
        r"3 friends each independently pick one of 5 entrées at random. What is the probability all three choose different entrées?",
        0.48, 0.005,
        r"$P(\text{all different}) = \frac{5}{5} \cdot \frac{4}{5} \cdot \frac{3}{5} = \frac{60}{125} = 0.48$")

    mc("Counting & Independence",
       r"How many ways can you arrange 4 distinct books on a shelf?",
       ["24", "16", "12", "4"],
       "24",
       r"$4! = 4 \cdot 3 \cdot 2 \cdot 1 = 24$ (permutation of 4 distinct objects).")

    mc("Counting & Independence",
       r"How many ways can a committee of 3 be chosen from 8 people (order does not matter)?",
       ["56", "336", "24", "512"],
       "56",
       r"$\binom{8}{3} = \frac{8!}{3!\,5!} = 56$. Order doesn't matter → combination.")

    num("Counting & Independence",
        r"How many ways to choose 2 items from 10 distinct items, where order does not matter? (i.e. find $\binom{10}{2}$)",
        45, 0,
        r"$\binom{10}{2} = \frac{10!}{2!\,8!} = 45$")

    tf("Counting & Independence",
       r"If $A$ and $B$ are independent, then $A'$ and $B'$ are also independent.",
       True,
       r"If $A$ and $B$ are independent, then any combination of them and their complements are also independent.")

    tf("Counting & Independence",
       r"The number of permutations $P(n,r)$ is always greater than or equal to the number of combinations $\binom{n}{r}$ (when $1 < r < n$).",
       True,
       r"$P(n,r) = \frac{n!}{(n-r)!}$ while $\binom{n}{r} = \frac{n!}{r!(n-r)!}$. Since $r! \geq 1$, we have $P(n,r) \geq \binom{n}{r}$.")

    mc("Counting & Independence",
       r"A 5-character password must have exactly 3 digit positions (each 0–9) followed by 2 letter positions (each A–Z). If repetition is allowed, how many passwords are possible?",
       ["10³ × 26² = 676,000", "10² × 26³ = 1,757,600", "C(10,3) × C(26,2) = 39,000", "10 × 26 × 5! = 31,200"],
       "10³ × 26² = 676,000",
       r"Each digit has 10 choices, each letter has 26 choices. With repetition: $10^3 \cdot 26^2 = 676{,}000$.")

    # ═══════════════════════════════════════════════════════════════════════
    # 4. DISCRETE RVs & PMFs (Lesson 9, sections 3.1-3.3)
    # ═══════════════════════════════════════════════════════════════════════
    tf("Discrete RVs & PMFs",
       r"A valid PMF must satisfy $\sum_{\text{all } x} P(X = x) = 1$ and $P(X = x) \geq 0$ for all $x$.",
       True,
       "These are the two conditions for a valid PMF.")

    tf("Discrete RVs & PMFs",
       r"The CDF $F(x) = P(X \leq x)$ of any random variable is a non-decreasing function.",
       True,
       r"By definition, if $a < b$ then $F(a) \leq F(b)$.")

    tf("Discrete RVs & PMFs",
       r"$\text{Var}(X)$ can be negative.",
       False,
       r"$\text{Var}(X) = E[(X - \mu)^2]$, which is an expected value of squared terms, so it is always $\geq 0$.")

    mc("Discrete RVs & PMFs",
       r"Which formula computes $\text{Var}(X)$?",
       ["E(X²) − [E(X)]²", "E(X²) − E(X)", "[E(X)]² − E(X²)", "E(X) − [E(X)]²"],
       "E(X²) − [E(X)]²",
       r"The shortcut formula: $\text{Var}(X) = E(X^2) - [E(X)]^2$.")

    num("Discrete RVs & PMFs",
        r"$P(X=x) = c \cdot x^2$ for $x = 1, 2, 3$ (and 0 otherwise). Find the value of $c$ that makes this a valid PMF.",
        1/14, 0.002,
        r"$c(1 + 4 + 9) = 14c = 1$, so $c = 1/14 \approx 0.0714$",
        "")

    num("Discrete RVs & PMFs",
        r"A discrete RV $X$ has PMF $P(X=x) = \frac{x^2}{14}$ for $x = 1, 2, 3$ (and 0 otherwise). Find $E(X)$.",
        18/7, 0.01,
        r"$E(X) = 1 \cdot \frac{1}{14} + 2 \cdot \frac{4}{14} + 3 \cdot \frac{9}{14} = \frac{1+8+27}{14} = \frac{36}{14} = \frac{18}{7} \approx 2.571$")

    num("Discrete RVs & PMFs",
        r"A discrete RV $X$ has PMF $P(X=x) = \frac{x^2}{14}$ for $x = 1, 2, 3$ (and 0 otherwise). Find $\text{Var}(X)$. Hint: use $\text{Var}(X) = E(X^2) - [E(X)]^2$.",
        19/49, 0.01,
        r"$E(X^2) = 1 \cdot \frac{1}{14} + 4 \cdot \frac{4}{14} + 9 \cdot \frac{9}{14} = \frac{98}{14} = 7$. $\text{Var} = 7 - (18/7)^2 = 19/49 \approx 0.388$")

    num("Discrete RVs & PMFs",
        r"A discrete RV $X$ has PMF $P(X=x) = \frac{x^2}{14}$ for $x = 1, 2, 3$ (and 0 otherwise). Find $P(X \geq 2)$.",
        13/14, 0.005,
        r"$P(X \geq 2) = P(X=2) + P(X=3) = \frac{4}{14} + \frac{9}{14} = \frac{13}{14} \approx 0.929$")

    num("Discrete RVs & PMFs",
        r"A carnival game costs \$2 to play. You draw one card from a standard 52-card deck. Ace wins \$10, face card (J, Q, K) wins \$3, any other card wins \$0. Let $X$ = net profit (winnings minus \$2 cost). Find $E(X)$.",
        -28/52, 0.02,
        r"Net: Ace → \$8 (prob 4/52), Face → \$1 (prob 12/52), Other → −\$2 (prob 36/52). $E(X) = 8(4/52) + 1(12/52) + (-2)(36/52) = -28/52 \approx -\$0.54$")

    mc("Discrete RVs & PMFs",
       r"For the CDF of a discrete RV, $F(x) = P(X \leq x)$ is:",
       ["A step function that is right-continuous",
        "A smooth continuous curve",
        "Always a straight line",
        "Defined only at integer values"],
       "A step function that is right-continuous",
       "Discrete CDFs jump at each value in the support and are constant between jumps, right-continuous by convention.")

    # ═══════════════════════════════════════════════════════════════════════
    # 5. BINOMIAL DISTRIBUTION (Lesson 10, section 3.4)
    # ═══════════════════════════════════════════════════════════════════════
    tf("Binomial Distribution",
       r"If $X \sim \text{Bin}(n, p)$, then $E(X) = np$ and $\text{Var}(X) = np(1-p)$.",
       True,
       "These are the standard results for the binomial distribution.")

    mc("Binomial Distribution",
       r"Which is NOT a requirement for a Binomial distribution?",
       ["Trials must be dependent on each other",
        "Fixed number of trials n",
        "Constant probability p on each trial",
        "Two outcomes per trial (success/failure)"],
       "Trials must be dependent on each other",
       "Binomial requires INDEPENDENT trials, not dependent ones.")

    num("Binomial Distribution",
        r"A 15-question multiple-choice quiz has 4 options per question. A student guesses randomly on every question, so $X \sim \text{Bin}(15,\, 0.25)$. Find $E(X)$.",
        3.75, 0.01,
        r"$E(X) = np = 15(0.25) = 3.75$")

    num("Binomial Distribution",
        r"A 15-question multiple-choice quiz has 4 options per question. A student guesses randomly, so $X \sim \text{Bin}(15,\, 0.25)$. Find the standard deviation of $X$.",
        math.sqrt(15 * 0.25 * 0.75), 0.02,
        r"$\sigma = \sqrt{np(1-p)} = \sqrt{15 \cdot 0.25 \cdot 0.75} = \sqrt{2.8125} \approx 1.677$")

    num("Binomial Distribution",
        r"A student randomly guesses on a 15-question quiz with 4 options each, so $X \sim \text{Bin}(15,\, 0.25)$. Find $P(X = 5)$, the probability of exactly 5 correct.",
        math.comb(15, 5) * (0.25**5) * (0.75**10), 0.005,
        r"$P(X=5) = \binom{15}{5}(0.25)^5(0.75)^{10} = 3003 \cdot (0.25)^5 \cdot (0.75)^{10} \approx 0.165$")

    num("Binomial Distribution",
        r"A student randomly guesses on a 15-question quiz with 4 options each, so $X \sim \text{Bin}(15,\, 0.25)$. Find $P(X \geq 2)$, the probability of at least 2 correct. Round to 3 decimal places.",
        1 - 0.75**15 - 15*0.25*0.75**14, 0.005,
        r"$P(X \geq 2) = 1 - P(X=0) - P(X=1) = 1 - (0.75)^{15} - 15(0.25)(0.75)^{14} \approx 0.920$")

    num("Binomial Distribution",
        r"A batch of 20 light bulbs each independently has a 10% defect rate, so $X \sim \text{Bin}(20,\, 0.10)$. Find $P(X = 2)$, the probability exactly 2 are defective.",
        math.comb(20, 2) * (0.10**2) * (0.90**18), 0.005,
        r"$P(X=2) = \binom{20}{2}(0.10)^2(0.90)^{18} = 190 \cdot 0.01 \cdot (0.90)^{18} \approx 0.285$")

    num("Binomial Distribution",
        r"A batch of 20 light bulbs each independently has a 10% defect rate, so $X \sim \text{Bin}(20,\, 0.10)$. Find $P(X = 0)$, the probability none are defective.",
        0.90**20, 0.005,
        r"$P(X=0) = (0.90)^{20} \approx 0.122$")

    num("Binomial Distribution",
        r"A batch of 20 light bulbs each independently has a 10% defect rate, so $X \sim \text{Bin}(20,\, 0.10)$. Find $\text{Var}(X)$.",
        1.80, 0.01,
        r"$\text{Var}(X) = np(1-p) = 20 \cdot 0.10 \cdot 0.90 = 1.80$")

    mc("Binomial Distribution",
       r"50 coin flips of a fair coin. What distribution models the number of heads?",
       ["Bin(50, 0.5)", "Pois(25)", "N(25, 12.5)", "Exp(0.5)"],
       "Bin(50, 0.5)",
       r"Fixed $n=50$ trials, constant $p=0.5$, two outcomes (H/T), independent $\rightarrow$ Binomial.")

    # ═══════════════════════════════════════════════════════════════════════
    # 6. POISSON DISTRIBUTION (Lesson 11, section 3.6)
    # ═══════════════════════════════════════════════════════════════════════
    num("Poisson Distribution",
        r"A bookstore receives an average of 5 online orders per hour. Let $X$ = number of orders in one hour, so $X \sim \text{Pois}(5)$. Find $P(X = 3)$.",
        (math.exp(-5) * 5**3) / math.factorial(3), 0.005,
        r"$P(X=3) = \frac{e^{-5} \cdot 5^3}{3!} = \frac{125\,e^{-5}}{6} \approx 0.140$")

    num("Poisson Distribution",
        r"A bookstore receives an average of 5 online orders per hour, so $X \sim \text{Pois}(5)$. Find $P(X = 0)$, the probability of no orders in one hour.",
        math.exp(-5), 0.001,
        r"$P(X=0) = e^{-5} \approx 0.00674$")

    num("Poisson Distribution",
        r"A bookstore receives an average of 5 online orders per hour, so $X \sim \text{Pois}(5)$. Find $P(X \geq 2)$, the probability of at least 2 orders in one hour.",
        1 - math.exp(-5) - 5*math.exp(-5), 0.005,
        r"$P(X \geq 2) = 1 - P(X=0) - P(X=1) = 1 - e^{-5} - 5e^{-5} = 1 - 6e^{-5} \approx 0.960$")

    num("Poisson Distribution",
        r"A bookstore receives an average of 5 online orders per hour. What is $P(\text{exactly 8 orders in 2 hours})$? Hint: the Poisson rate scales — use $\lambda = 5 \times 2 = 10$ for the 2-hour window.",
        (math.exp(-10) * 10**8) / math.factorial(8), 0.005,
        r"2-hour rate $= 10$. $P(Y=8) = \frac{e^{-10} \cdot 10^8}{8!} \approx 0.113$")

    num("Poisson Distribution",
        r"A city averages 3 power outages per month. Assume outages follow a Poisson process, so $X \sim \text{Pois}(3)$. Find $P(X = 5)$, the probability of exactly 5 outages in a given month.",
        (math.exp(-3) * 3**5) / math.factorial(5), 0.005,
        r"$P(X=5) = \frac{e^{-3} \cdot 3^5}{5!} = \frac{243\,e^{-3}}{120} \approx 0.101$")

    num("Poisson Distribution",
        r"A city averages 3 power outages per month (Poisson process). Find $P(\text{no outages in 2 weeks})$. Assume 1 month $\approx$ 4 weeks, so the 2-week rate is $\lambda = 3/2 = 1.5$.",
        math.exp(-1.5), 0.005,
        r"Rate for 2 weeks $= 1.5$. $P(Y=0) = e^{-1.5} \approx 0.223$")

    mc("Poisson Distribution",
       "Which scenario best fits a Poisson distribution?",
       ["Number of typos per page in a novel (avg 1.5/page)",
        "Number of heads in 50 coin flips",
        "Weight of a bag of flour",
        "Time until next phone call"],
       "Number of typos per page in a novel (avg 1.5/page)",
       r"Poisson counts rare events in a fixed interval/area. Coin flips $\rightarrow$ Binomial, weight $\rightarrow$ Normal, time $\rightarrow$ Exponential.")

    tf("Poisson Distribution",
       r"For a Poisson random variable, the mean and variance are equal: $E(X) = \text{Var}(X) = \lambda$.",
       True,
       r"If $X \sim \text{Pois}(\lambda)$, then $E(X) = \text{Var}(X) = \lambda$.")

    mc("Poisson Distribution",
       r"If events occur at rate 6/hour as a Poisson process, what is the rate $\lambda$ for a 20-minute window?",
       ["2", "6", "3", "1"],
       "2",
       r"20 min $= 1/3$ hour. Rate $= 6 \times (1/3) = 2$.")

    # ═══════════════════════════════════════════════════════════════════════
    # 7. CONTINUOUS RVs & PDFs (Lesson 12, sections 4.1-4.2)
    # ═══════════════════════════════════════════════════════════════════════
    tf("Continuous RVs & PDFs",
       r"If $X$ is a continuous random variable, then $P(X = 3) = 0$.",
       True,
       "For continuous RVs, the probability at any single point is zero.")

    tf("Continuous RVs & PDFs",
       r"For a continuous RV with pdf $f(x)$: $P(a \leq X \leq b) = \int_a^b f(x)\,dx$.",
       True,
       "This is the fundamental definition of probability for continuous RVs.")

    num("Continuous RVs & PDFs",
        r"A continuous RV $X$ has pdf $f(x) = kx(1-x)$ for $0 \leq x \leq 1$ (and 0 otherwise). Find the value of $k$ that makes this a valid pdf.",
        6.0, 0.01,
        r"$\int_0^1 kx(1-x)\,dx = k\left[\frac{x^2}{2} - \frac{x^3}{3}\right]_0^1 = k\left(\frac{1}{6}\right) = 1$, so $k = 6$.")

    num("Continuous RVs & PDFs",
        r"A continuous RV $X$ has pdf $f(x) = 6x(1-x)$ for $0 \leq x \leq 1$ (and 0 otherwise). Find $P(0.25 \leq X \leq 0.75)$.",
        0.6875, 0.005,
        r"$F(x) = 3x^2 - 2x^3$. $F(0.75) - F(0.25) = 0.84375 - 0.15625 = 0.6875$")

    num("Continuous RVs & PDFs",
        r"A continuous RV $X$ has pdf $f(x) = 6x(1-x)$ for $0 \leq x \leq 1$ (and 0 otherwise). Find $E(X)$.",
        0.5, 0.005,
        r"$E(X) = \int_0^1 x \cdot 6x(1-x)\,dx = 6\int_0^1(x^2 - x^3)\,dx = 6\left(\frac{1}{3} - \frac{1}{4}\right) = 6 \cdot \frac{1}{12} = \frac{1}{2}$")

    num("Continuous RVs & PDFs",
        r"A continuous RV $X$ has pdf $f(x) = 6x(1-x)$ for $0 \leq x \leq 1$ (and 0 otherwise). Find $\text{Var}(X)$. Hint: use $\text{Var}(X) = E(X^2) - [E(X)]^2$.",
        0.05, 0.005,
        r"$E(X^2) = 6(1/4 - 1/5) = 6(1/20) = 3/10$. $\text{Var} = 3/10 - (1/2)^2 = 0.30 - 0.25 = 0.05$")

    num("Continuous RVs & PDFs",
        r"A continuous RV $Y$ has pdf $f(y) = \frac{3}{16}\sqrt{y}$ for $0 \leq y \leq 4$ (and 0 otherwise). Find $P(Y > 1)$.",
        7/8, 0.005,
        r"$P(Y>1) = \frac{3}{16}\left[\frac{2}{3}y^{3/2}\right]_1^4 = \frac{1}{8}(8 - 1) = \frac{7}{8} = 0.875$")

    num("Continuous RVs & PDFs",
        r"A continuous RV $Y$ has pdf $f(y) = \frac{3}{16}\sqrt{y}$ for $0 \leq y \leq 4$ (and 0 otherwise). Find $E(Y)$.",
        2.4, 0.01,
        r"$E(Y) = \frac{3}{16}\int_0^4 y^{3/2}\,dy = \frac{3}{16} \cdot \frac{2}{5} \cdot 32 = \frac{12}{5} = 2.4$")

    num("Continuous RVs & PDFs",
        r"A continuous RV $X$ has CDF $F(x) = \frac{x^2}{9}$ for $0 \leq x \leq 3$ (with $F(x)=0$ for $x<0$, $F(x)=1$ for $x>3$). Find $P(1 \leq X \leq 2)$. Recall: $P(a \leq X \leq b) = F(b) - F(a)$.",
        1/3, 0.005,
        r"$P(1 \leq X \leq 2) = F(2) - F(1) = \frac{4}{9} - \frac{1}{9} = \frac{3}{9} = \frac{1}{3}$")

    num("Continuous RVs & PDFs",
        r"A continuous RV $X$ has CDF $F(x) = \frac{x^2}{9}$ for $0 \leq x \leq 3$. Find the median of $X$, i.e. solve $F(m) = 0.5$.",
        math.sqrt(4.5), 0.01,
        r"$F(m) = 0.5 \Rightarrow m^2/9 = 0.5 \Rightarrow m = \sqrt{4.5} \approx 2.121$")

    num("Continuous RVs & PDFs",
        r"A continuous RV $X$ has CDF $F(x) = \frac{x^2}{9}$ for $0 \leq x \leq 3$. Find $E(X)$. Hint: first find the pdf by differentiating: $f(x) = F'(x) = \frac{2x}{9}$.",
        2.0, 0.01,
        r"$f(x) = 2x/9$. $E(X) = \int_0^3 x \cdot \frac{2x}{9}\,dx = \frac{2}{9}\left[\frac{x^3}{3}\right]_0^3 = \frac{2}{9} \cdot 9 = 2$")

    # ═══════════════════════════════════════════════════════════════════════
    # 8. NORMAL DISTRIBUTION (Lesson 13, section 4.3)
    # ═══════════════════════════════════════════════════════════════════════
    num("Normal Distribution",
        r"The time (in minutes) to complete an online checkout is normally distributed with $\mu = 8$ and $\sigma = 2$, i.e. $X \sim N(\mu=8,\, \sigma^2=4)$. Find $P(X > 12)$. Use the Z-table: $\Phi(2.0) = 0.9772$.",
        0.0228, 0.005,
        r"$Z = \frac{12-8}{2} = 2$. $P(X>12) = 1 - \Phi(2) = 1 - 0.9772 = 0.0228$")

    num("Normal Distribution",
        r"Online checkout time $X$ is normally distributed with $\mu = 8$ min and $\sigma = 2$ min. Find $P(5 < X < 11)$. Use the Z-table: $\Phi(1.5) = 0.9332$, $\Phi(-1.5) = 0.0668$.",
        0.8664, 0.005,
        r"$P(5 < X < 11) = \Phi(1.5) - \Phi(-1.5) = 0.9332 - 0.0668 = 0.8664$")

    num("Normal Distribution",
        r"Online checkout time $X$ is normally distributed with $\mu = 8$ min and $\sigma = 2$ min. Find the time exceeded by only 5% of customers, i.e. find $x$ such that $P(X > x) = 0.05$. Use $z_{0.95} = 1.645$.",
        11.29, 0.05,
        r"$P(X > x) = 0.05 \Rightarrow z = 1.645$. $x = 8 + 1.645(2) = 11.29$ minutes.")

    num("Normal Distribution",
        r"SAT math scores are approximately normal with $\mu = 520$ and $\sigma = 100$, i.e. $X \sim N(520,\, 100^2)$. What score corresponds to the 90th percentile? Use $z_{0.90} = 1.282$.",
        648.2, 1.0,
        r"$z_{0.90} = 1.282$. Score $= 520 + 1.282(100) = 648.2$")

    num("Normal Distribution",
        r"SAT math scores are approximately normal with $\mu = 520$ and $\sigma = 100$. Find $P(400 < X < 650)$. Use $\Phi(1.30) = 0.9032$ and $\Phi(-1.20) = 0.1151$.",
        0.7881, 0.01,
        r"$P = \Phi(1.30) - \Phi(-1.20) = 0.9032 - 0.1151 = 0.7881$")

    num("Normal Distribution",
        r"SAT math scores are approximately normal with $\mu = 520$ and $\sigma = 100$. A scholarship requires a score in the top 2%. What is the minimum qualifying score? Use $z_{0.98} = 2.054$.",
        725.4, 1.0,
        r"$z_{0.98} = 2.054$. Score $= 520 + 2.054(100) = 725.4$")

    mc("Normal Distribution",
       r"For a standard normal $Z$, what is $P(-1.96 < Z < 1.96)$?",
       ["0.95", "0.99", "0.90", "0.68"],
       "0.95",
       r"This is the well-known 95% interval: $P(-1.96 < Z < 1.96) = 0.95$.")

    tf("Normal Distribution",
       r"For a normal distribution, approximately 68% of values fall within 1 standard deviation of the mean.",
       True,
       r"The 68-95-99.7 rule: ~68% within $\pm 1\sigma$, ~95% within $\pm 2\sigma$, ~99.7% within $\pm 3\sigma$.")

    mc("Normal Distribution",
       r"The weight of a bag of flour follows a $N(5.0,\, 0.01)$ distribution. In the notation $N(\mu,\, \sigma^2)$, what are $\mu$ and $\sigma$?",
       ["Normal with μ=5.0, σ=0.1",
        "Normal with μ=5.0, σ=0.01",
        "Exponential with λ=5.0",
        "Poisson with λ=5.0"],
       "Normal with μ=5.0, σ=0.1",
       r"$N(5.0, 0.01)$ means $\mu=5.0$ and $\sigma^2=0.01$, so $\sigma=0.1$.")

    # ═══════════════════════════════════════════════════════════════════════
    # 9. EXPONENTIAL DISTRIBUTION (Lesson 14, section 4.4)
    # ═══════════════════════════════════════════════════════════════════════
    tf("Exponential Distribution",
       r"The exponential distribution has the memoryless property: $P(T > s+t \mid T > s) = P(T > t)$.",
       True,
       "The exponential is the only continuous distribution with this property.")

    num("Exponential Distribution",
        r"Customers arrive at a coffee shop at a rate of 10 per hour. Let $T$ = wait time (hours) between customers, so $T \sim \text{Exp}(\lambda=10)$. Find $E(T)$ in hours.",
        0.1, 0.005,
        r"$E(T) = 1/\lambda = 1/10 = 0.1$ hours = 6 minutes")

    num("Exponential Distribution",
        r"Customers arrive at a coffee shop at a rate of 10 per hour. Let $T$ be the waiting time (in hours) between customers, so $T \sim \text{Exp}(\lambda=10)$. Find $P(T > 0.25)$, the probability the wait exceeds 15 minutes.",
        math.exp(-2.5), 0.005,
        r"$P(T > 0.25) = e^{-10 \cdot 0.25} = e^{-2.5} \approx 0.0821$")

    num("Exponential Distribution",
        r"Customers arrive at a coffee shop at a rate of 10 per hour, so $T \sim \text{Exp}(\lambda=10)$ in hours. Find $P(T \leq 0.1)$, the probability the next customer arrives within 6 minutes (0.1 hours).",
        1 - math.exp(-1), 0.005,
        r"$P(T \leq 0.1) = 1 - e^{-10 \cdot 0.1} = 1 - e^{-1} \approx 0.632$")

    num("Exponential Distribution",
        r"Customers arrive at a coffee shop at a rate of 10 per hour, so $T \sim \text{Exp}(\lambda=10)$ in hours. Find the median wait time (in hours). Hint: set $F(m) = 0.5$ and solve for $m$.",
        math.log(2)/10, 0.002,
        r"$1 - e^{-10m} = 0.5 \Rightarrow m = \frac{\ln 2}{10} \approx 0.0693$ hours $\approx 4.16$ min")

    num("Exponential Distribution",
        r"Lightning strikes in a national park at a rate of 6 per week during summer. Let $T$ = time (in weeks) between strikes, so $T \sim \text{Exp}(\lambda=6)$. Find $P(T > 0.5)$, the probability of waiting more than half a week.",
        math.exp(-3), 0.005,
        r"$P(T > 0.5) = e^{-6 \cdot 0.5} = e^{-3} \approx 0.0498$")

    num("Exponential Distribution",
        r"Lightning strikes in a national park at 6 per week, so $T \sim \text{Exp}(\lambda=6)$ in weeks. Given that no strike has occurred for 2 days ($\frac{2}{7}$ weeks), what is the probability of no strike for 3 more days ($\frac{3}{7}$ weeks)? Use the memoryless property.",
        math.exp(-18/7), 0.005,
        r"Memoryless: $P(T > 2/7 + 3/7 \mid T > 2/7) = P(T > 3/7) = e^{-6 \cdot 3/7} = e^{-18/7} \approx 0.0773$")

    mc("Exponential Distribution",
       r"Calls arrive at 8/hour as a Poisson process. What distribution models the time until the next call?",
       ["Exp(λ=8)", "Pois(8)", "Bin(8, 0.5)", "N(8, 1)"],
       "Exp(λ=8)",
       "Waiting time between events in a Poisson process follows an Exponential distribution.")

    mc("Exponential Distribution",
       r"For $T \sim \text{Exp}(\lambda)$, the CDF is:",
       ["F(t) = 1 − e^(−λt) for t ≥ 0",
        "F(t) = e^(−λt) for t ≥ 0",
        "F(t) = λe^(−λt) for t ≥ 0",
        "F(t) = 1 − λe^(−t) for t ≥ 0"],
       "F(t) = 1 − e^(−λt) for t ≥ 0",
       r"The Exponential CDF is $F(t) = 1 - e^{-\lambda t}$. The pdf is $f(t) = \lambda e^{-\lambda t}$.")

    num("Exponential Distribution",
        r"Customers arrive at a rate of 10 per hour, so the wait time $T \sim \text{Exp}(\lambda=10)$ in hours. Find $\text{Var}(T)$.",
        0.01, 0.002,
        r"$\text{Var}(T) = 1/\lambda^2 = 1/100 = 0.01$")

    # ── Distribution identification (mixed) ──
    mc("Probability Basics",
       r"400 flights, each independently has a 15% chance of delay. Which distribution models the number of delays?",
       ["Bin(400, 0.15)", "Pois(60)", "N(60, 51)", "Exp(0.15)"],
       "Bin(400, 0.15)",
       r"Fixed $n=400$, constant $p=0.15$, independent, two outcomes $\rightarrow$ Binomial.")

    return Q


QUESTIONS = build_questions()


# ── Session state initialization ─────────────────────────────────────────────

def init_state():
    defaults = {
        "xp": 0,
        "streak": 0,
        "best_streak": 0,
        "total_answered": 0,
        "total_correct": 0,
        "topic_answered": {t: 0 for t in TOPICS},
        "topic_correct": {t: 0 for t in TOPICS},
        "achievements": [],
        "current_q_idx": None,
        "answered_indices": [],
        "show_result": False,
        "last_correct": None,
        "last_xp_gained": 0,
        "first_try": True,
        "selected_topics": list(TOPICS),
        "start_time": time.time(),
        "q_order": [],
        "user_answer": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


init_state()


# ── Helpers ──────────────────────────────────────────────────────────────────

def pick_next_question():
    """Pick a random unanswered question from selected topics."""
    available = [
        i for i, q in enumerate(QUESTIONS)
        if q["topic"] in st.session_state.selected_topics
        and i not in st.session_state.answered_indices
    ]
    if not available:
        return None
    return random.choice(available)


def award_xp(correct, first_try):
    gained = 0
    if correct:
        gained += 10
        if first_try:
            gained += 5
        gained += min(st.session_state.streak, 10) * 2  # streak bonus capped at 20
    st.session_state.last_xp_gained = gained
    st.session_state.xp += gained
    return gained


def check_achievements():
    s = st.session_state
    achs = s.achievements

    checks = [
        ("First Blood", "Get your first correct answer", s.total_correct >= 1),
        ("On Fire", "5 correct answers in a row", s.best_streak >= 5),
        ("Inferno", "10 correct answers in a row", s.best_streak >= 10),
        ("Perfect Ten", "Answer 10 questions correctly", s.total_correct >= 10),
        ("Quarter Century", "Answer 25 questions correctly", s.total_correct >= 25),
        ("Half Century", "Answer 50 questions correctly", s.total_correct >= 50),
        ("Sharpshooter", "Maintain 90%+ accuracy over 10+ questions",
         s.total_answered >= 10 and s.total_correct / max(s.total_answered, 1) >= 0.90),
        ("Centurion", "Earn 100 XP", s.xp >= 100),
        ("XP Machine", "Earn 500 XP", s.xp >= 500),
        ("Knowledge is Power", "Earn 1000 XP", s.xp >= 1000),
    ]

    # Topic mastery achievements
    for topic in TOPICS:
        total_in_topic = sum(1 for q in QUESTIONS if q["topic"] == topic)
        correct_in_topic = s.topic_correct.get(topic, 0)
        short = topic.split(" ")[0] if len(topic) > 15 else topic
        checks.append(
            (f"{short} Master", f"Get all {topic} questions correct",
             correct_in_topic >= total_in_topic and total_in_topic > 0)
        )

    new_achievements = []
    for name, desc, condition in checks:
        if condition and name not in achs:
            achs.append(name)
            new_achievements.append((name, desc))
    return new_achievements


ACHIEVEMENT_ICONS = {
    "First Blood": "🩸", "On Fire": "🔥", "Inferno": "🌋",
    "Perfect Ten": "🎯", "Quarter Century": "🏅", "Half Century": "💎",
    "Sharpshooter": "🎖️", "Centurion": "💰", "XP Machine": "⚡",
    "Knowledge is Power": "📚",
    "Probability Master": "🎲", "Conditional Master": "🔀",
    "Counting Master": "🔢", "Discrete Master": "📊",
    "Binomial Master": "🎰", "Poisson Master": "☢️",
    "Continuous Master": "📈", "Normal Master": "🔔",
    "Exponential Master": "⏱️",
}


# ── Custom CSS ───────────────────────────────────────────────────────────────

st.markdown("""
<style>
    .stApp { }
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border: 1px solid #0f3460;
        border-radius: 10px;
        padding: 12px 16px;
        color: white;
    }
    div[data-testid="stMetric"] label {
        color: #a0a0c0 !important;
    }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #e0e0ff !important;
    }
    .question-card {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        border-radius: 15px;
        padding: 25px 30px;
        margin: 10px 0;
        border: 1px solid #4a47a3;
        color: #e0e0ff;
    }
    .question-card h3 {
        color: #bb86fc;
        margin-bottom: 15px;
    }
    .correct-banner {
        background: linear-gradient(90deg, #00c853, #00e676);
        color: #000;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        font-size: 1.2em;
        margin: 10px 0;
    }
    .wrong-banner {
        background: linear-gradient(90deg, #ff1744, #ff5252);
        color: #fff;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        font-size: 1.2em;
        margin: 10px 0;
    }
    .xp-pill {
        display: inline-block;
        background: #ffd700;
        color: #000;
        padding: 3px 10px;
        border-radius: 15px;
        font-weight: bold;
        font-size: 0.9em;
    }
    .streak-display {
        font-size: 1.3em;
        font-weight: bold;
    }
    .topic-tag {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.8em;
        font-weight: 600;
        color: white;
        margin-bottom: 8px;
    }
    .achievement-card {
        background: linear-gradient(135deg, #2a2a4e, #1e3a5f);
        border: 1px solid #ffd700;
        border-radius: 8px;
        padding: 8px 12px;
        margin: 4px 0;
        font-size: 0.9em;
        color: #f0e6ff;
    }
    .calc-container {
        background: #1a1a2e;
        border: 1px solid #333;
        border-radius: 10px;
        padding: 15px;
    }
</style>
""", unsafe_allow_html=True)


# ── Sidebar ──────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## 🎯 MA206X Prob Drill")
    st.markdown("**WPR I Review** — Lessons 6-14")
    st.markdown("---")

    # Level display
    level_name, level_min, level_next = get_level(st.session_state.xp)
    level_icon = LEVEL_ICONS.get(level_name, "🔰")
    st.markdown(f"### {level_icon} {level_name}")
    xp_in_level = st.session_state.xp - level_min
    xp_needed = level_next - level_min
    st.progress(min(xp_in_level / max(xp_needed, 1), 1.0),
                text=f"XP: {st.session_state.xp} / {level_next}")

    st.markdown("---")

    # Stats
    st.markdown("### 📊 Session Stats")
    acc = (st.session_state.total_correct / max(st.session_state.total_answered, 1)) * 100
    elapsed = int(time.time() - st.session_state.start_time)
    mins, secs = divmod(elapsed, 60)

    col1, col2 = st.columns(2)
    col1.metric("Answered", st.session_state.total_answered)
    col2.metric("Correct", st.session_state.total_correct)
    col1.metric("Accuracy", f"{acc:.0f}%")
    col2.metric("Time", f"{mins}m {secs}s")
    col1.metric("Streak", f"🔥 {st.session_state.streak}")
    col2.metric("Best", f"⚡ {st.session_state.best_streak}")

    st.markdown("---")

    # Topic filter
    st.markdown("### 📚 Topics")
    selected = []
    for topic in TOPICS:
        total_in_topic = sum(1 for q in QUESTIONS if q["topic"] == topic)
        correct_in_topic = st.session_state.topic_correct.get(topic, 0)
        answered_in_topic = st.session_state.topic_answered.get(topic, 0)
        label = f"{topic} ({correct_in_topic}/{total_in_topic})"
        if st.checkbox(label, value=topic in st.session_state.selected_topics, key=f"topic_{topic}"):
            selected.append(topic)
    st.session_state.selected_topics = selected if selected else list(TOPICS)

    st.markdown("---")

    # Topic mastery bars
    st.markdown("### 🏆 Topic Mastery")
    for topic in TOPICS:
        total_in_topic = sum(1 for q in QUESTIONS if q["topic"] == topic)
        correct_in_topic = st.session_state.topic_correct.get(topic, 0)
        pct = correct_in_topic / max(total_in_topic, 1)
        color = TOPIC_COLORS.get(topic, "#666")
        short = topic[:20]
        st.markdown(f"**{short}**")
        st.progress(pct, text=f"{correct_in_topic}/{total_in_topic}")

    st.markdown("---")

    # Achievements
    st.markdown("### 🏅 Achievements")
    if st.session_state.achievements:
        for ach in st.session_state.achievements:
            icon = ACHIEVEMENT_ICONS.get(ach, "🏆")
            st.markdown(f'<div class="achievement-card">{icon} {ach}</div>', unsafe_allow_html=True)
    else:
        st.caption("None yet — keep drilling!")

    st.markdown("---")
    if st.button("🔄 Reset Session", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


# ── Main area ────────────────────────────────────────────────────────────────

# Top bar
top1, top2, top3 = st.columns([2, 1, 1])
with top1:
    level_name, _, _ = get_level(st.session_state.xp)
    level_icon = LEVEL_ICONS.get(level_name, "🔰")
    st.markdown(f"### {level_icon} {level_name} — {st.session_state.xp} XP")
with top2:
    streak = st.session_state.streak
    fire = "🔥" * min(streak, 5) if streak > 0 else "—"
    st.markdown(f'<div class="streak-display">Streak: {streak} {fire}</div>', unsafe_allow_html=True)
with top3:
    remaining = sum(
        1 for i, q in enumerate(QUESTIONS)
        if q["topic"] in st.session_state.selected_topics
        and i not in st.session_state.answered_indices
    )
    st.markdown(f"**{remaining}** questions remaining")

st.markdown("---")

# Get or pick question
if st.session_state.current_q_idx is None:
    st.session_state.current_q_idx = pick_next_question()
    st.session_state.show_result = False
    st.session_state.first_try = True

q_idx = st.session_state.current_q_idx

if q_idx is None:
    st.balloons()
    st.markdown("## 🎉 Congratulations!")
    st.markdown("You've answered all available questions! Reset to try again or select different topics.")
    acc = (st.session_state.total_correct / max(st.session_state.total_answered, 1)) * 100
    st.markdown(f"""
    ### Final Stats
    - **Total Answered:** {st.session_state.total_answered}
    - **Correct:** {st.session_state.total_correct} ({acc:.1f}%)
    - **Best Streak:** {st.session_state.best_streak}
    - **XP Earned:** {st.session_state.xp}
    - **Level:** {get_level(st.session_state.xp)[0]}
    - **Achievements:** {len(st.session_state.achievements)}
    """)
    st.stop()

q = QUESTIONS[q_idx]
topic_color = TOPIC_COLORS.get(q["topic"], "#666")

# Question card
st.markdown(f'<span class="topic-tag" style="background:{topic_color}">{q["topic"]}</span>',
            unsafe_allow_html=True)

q_num = st.session_state.total_answered + 1
type_label = {"tf": "True / False", "mc": "Multiple Choice", "num": "Numeric"}[q["type"]]
st.markdown(f"#### Question {q_num} — {type_label}")

st.markdown(f"""
<div class="question-card">
<h3>📝</h3>
</div>
""", unsafe_allow_html=True)
st.markdown(q["text"])

# Built-in calculator
with st.expander("🧮 Calculator"):
    calc_col1, calc_col2 = st.columns(2)
    with calc_col1:
        calc_expr = st.text_input("Enter expression:", placeholder="e.g. 0.95*0.02/0.117", key="calc_input")
    with calc_col2:
        st.markdown("")  # spacer
        st.markdown("")
        if calc_expr:
            try:
                import re as _re
                safe = calc_expr
                # Allow: digits, operators, parens, decimal points, and math functions
                allowed_names = {
                    "sqrt": math.sqrt, "exp": math.exp, "log": math.log,
                    "ln": math.log, "log10": math.log10,
                    "factorial": math.factorial, "comb": math.comb,
                    "pi": math.pi, "e": math.e,
                    "sin": math.sin, "cos": math.cos, "tan": math.tan,
                    "abs": abs, "pow": pow, "round": round,
                }
                result = eval(safe, {"__builtins__": {}}, allowed_names)
                st.success(f"**= {result:.6g}**")
            except Exception as ex:
                st.error(f"Error: {ex}")

    st.caption("Available: `sqrt()`, `exp()`, `log()` (natural), `log10()`, `factorial()`, `comb(n,k)`, `pi`, `e`, `abs()`, `+`, `-`, `*`, `/`, `**` (power)")

# Answer input
if not st.session_state.show_result:
    if q["type"] == "tf":
        col_t, col_f = st.columns(2)
        with col_t:
            if st.button("✅ True", use_container_width=True, key="btn_true"):
                st.session_state.user_answer = True
        with col_f:
            if st.button("❌ False", use_container_width=True, key="btn_false"):
                st.session_state.user_answer = False

        if st.session_state.user_answer is not None:
            correct = (st.session_state.user_answer == q["answer"])
            st.session_state.last_correct = correct
            st.session_state.show_result = True
            # Update stats
            st.session_state.total_answered += 1
            st.session_state.topic_answered[q["topic"]] = st.session_state.topic_answered.get(q["topic"], 0) + 1
            if correct:
                st.session_state.total_correct += 1
                st.session_state.streak += 1
                st.session_state.best_streak = max(st.session_state.best_streak, st.session_state.streak)
                st.session_state.topic_correct[q["topic"]] = st.session_state.topic_correct.get(q["topic"], 0) + 1
            else:
                st.session_state.streak = 0
            award_xp(correct, st.session_state.first_try)
            st.session_state.answered_indices.append(q_idx)
            check_achievements()
            st.rerun()

    elif q["type"] == "mc":
        for i, opt in enumerate(q["options"]):
            if st.button(opt, key=f"mc_{i}", use_container_width=True):
                correct = (opt == q["answer"])
                st.session_state.last_correct = correct
                st.session_state.show_result = True
                st.session_state.total_answered += 1
                st.session_state.topic_answered[q["topic"]] = st.session_state.topic_answered.get(q["topic"], 0) + 1
                if correct:
                    st.session_state.total_correct += 1
                    st.session_state.streak += 1
                    st.session_state.best_streak = max(st.session_state.best_streak, st.session_state.streak)
                    st.session_state.topic_correct[q["topic"]] = st.session_state.topic_correct.get(q["topic"], 0) + 1
                else:
                    st.session_state.streak = 0
                    st.session_state.first_try = False
                award_xp(correct, st.session_state.first_try)
                st.session_state.answered_indices.append(q_idx)
                check_achievements()
                st.rerun()

    elif q["type"] == "num":
        unit = q.get("unit", "")
        with st.form("num_form", clear_on_submit=False):
            user_val = st.number_input(
                f"Enter your answer{' (' + unit + ')' if unit else ''} (round to 3 decimals if needed):",
                format="%.4f", value=0.0, step=0.001, key="num_input"
            )
            submitted = st.form_submit_button("Submit Answer", use_container_width=True)
            if submitted:
                diff = abs(user_val - q["answer"])
                correct = diff <= q["tol"]
                st.session_state.last_correct = correct
                st.session_state.show_result = True
                st.session_state.total_answered += 1
                st.session_state.topic_answered[q["topic"]] = st.session_state.topic_answered.get(q["topic"], 0) + 1
                if correct:
                    st.session_state.total_correct += 1
                    st.session_state.streak += 1
                    st.session_state.best_streak = max(st.session_state.best_streak, st.session_state.streak)
                    st.session_state.topic_correct[q["topic"]] = st.session_state.topic_correct.get(q["topic"], 0) + 1
                else:
                    st.session_state.streak = 0
                    st.session_state.first_try = False
                award_xp(correct, st.session_state.first_try)
                st.session_state.answered_indices.append(q_idx)
                check_achievements()
                st.rerun()

# Show result
if st.session_state.show_result:
    correct = st.session_state.last_correct
    xp_gained = st.session_state.last_xp_gained

    if correct:
        st.markdown(f'<div class="correct-banner">✅ Correct! &nbsp; <span class="xp-pill">+{xp_gained} XP</span></div>',
                    unsafe_allow_html=True)
        if st.session_state.streak >= 3:
            st.markdown(f"🔥 **{st.session_state.streak} streak!** (+{min(st.session_state.streak, 10)*2} streak bonus)")
    else:
        st.markdown(f'<div class="wrong-banner">❌ Incorrect</div>', unsafe_allow_html=True)
        if q["type"] == "num":
            st.info(f"**Correct answer:** {q['answer']:.4f}")
        elif q["type"] == "tf":
            st.info(f"**Correct answer:** {'True' if q['answer'] else 'False'}")
        elif q["type"] == "mc":
            st.info(f"**Correct answer:** {q['answer']}")

    # Always show explanation
    with st.expander("📖 See Explanation", expanded=not correct):
        st.markdown(q["explanation"])

    # Check for new achievements
    new_achs = check_achievements()
    if new_achs:
        for name, desc in new_achs:
            icon = ACHIEVEMENT_ICONS.get(name, "🏆")
            st.success(f"{icon} **Achievement Unlocked: {name}** — {desc}")

    st.markdown("")
    if st.button("➡️ Next Question", use_container_width=True, type="primary"):
        st.session_state.current_q_idx = pick_next_question()
        st.session_state.show_result = False
        st.session_state.last_correct = None
        st.session_state.first_try = True
        st.session_state.user_answer = None
        st.rerun()
