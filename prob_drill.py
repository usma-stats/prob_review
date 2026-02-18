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
       "If P(A) = 0.5 and P(B) = 0.3, then A and B must be mutually exclusive.",
       False,
       "Mutually exclusive means P(A∩B) = 0, which is not determined by individual probabilities alone.")

    tf("Probability Basics",
       "For any event A, P(A) + P(A') = 1.",
       True,
       "This is the complement rule — one of the axioms of probability.")

    tf("Probability Basics",
       "If A and B are mutually exclusive, then P(A∪B) = P(A) + P(B).",
       True,
       "When A∩B = ∅, the addition rule simplifies to P(A) + P(B).")

    tf("Probability Basics",
       "P(A∪B) = P(A) + P(B) always holds for any two events.",
       False,
       "The general addition rule is P(A∪B) = P(A) + P(B) − P(A∩B). It only simplifies when A and B are mutually exclusive.")

    tf("Probability Basics",
       "If P(A∪B) = P(A) + P(B), then A and B are mutually exclusive.",
       True,
       "This equality holds iff P(A∩B) = 0, which is the definition of mutually exclusive.")

    tf("Probability Basics",
       "A probability can be negative if the event is very unlikely.",
       False,
       "Probabilities are always between 0 and 1 inclusive. This is an axiom of probability.")

    num("Probability Basics",
        "A survey of 500 students found 280 play video games (V), 200 play instruments (I), and 90 do both. Find P(V∪I).",
        0.78, 0.005,
        "P(V∪I) = P(V) + P(I) − P(V∩I) = 280/500 + 200/500 − 90/500 = 390/500 = 0.78")

    num("Probability Basics",
        "A survey of 500 students found 280 play video games (V), 200 play instruments (I), and 90 do both. Find the probability a randomly selected student does neither activity, i.e. find P(V' ∩ I').",
        0.22, 0.005,
        "P(V'∩I') = 1 − P(V∪I) = 1 − 0.78 = 0.22")

    mc("Probability Basics",
       "A fair six-sided die is rolled twice. What is P(sum ≥ 9)?",
       ["5/18 ≈ 0.278", "1/4 = 0.250", "1/6 ≈ 0.167", "1/3 ≈ 0.333"],
       "5/18 ≈ 0.278",
       "Outcomes with sum ≥ 9: {(3,6),(4,5),(4,6),(5,4),(5,5),(5,6),(6,3),(6,4),(6,5),(6,6)} = 10 outcomes. P = 10/36 = 5/18.")

    num("Probability Basics",
        "P(A) = 0.3, P(B) = 0.5, A and B independent. Find P(A∪B).",
        0.65, 0.005,
        "P(A∩B) = P(A)·P(B) = 0.15. P(A∪B) = 0.3 + 0.5 − 0.15 = 0.65")

    num("Probability Basics",
        "P(A) = 0.3, P(B) = 0.5, A and B independent. Find P(A'∩B').",
        0.35, 0.005,
        "P(A'∩B') = 1 − P(A∪B) = 1 − 0.65 = 0.35. Or P(A')P(B') = 0.7·0.5 = 0.35.")

    mc("Probability Basics",
       "A survey of 500 students found 280 play video games (V), 200 play instruments (I), and 90 do both. Are V and I independent? (Check whether P(V)·P(I) = P(V∩I).)",
       ["No, because P(V)P(I) = 0.224 ≠ P(V∩I) = 0.18",
        "Yes, because both events can occur simultaneously",
        "Yes, because P(V∩I) > 0",
        "No, because they are mutually exclusive"],
       "No, because P(V)P(I) = 0.224 ≠ P(V∩I) = 0.18",
       "Independence requires P(A∩B) = P(A)P(B). Here 0.56·0.40 = 0.224 ≠ 0.18.")

    # ═══════════════════════════════════════════════════════════════════════
    # 2. CONDITIONAL PROB & BAYES (Lessons 7-8, section 2.4)
    # ═══════════════════════════════════════════════════════════════════════
    num("Conditional Prob & Bayes",
        "A disease affects 2% of the population. A test has 95% sensitivity, i.e. P(+|disease) = 0.95, and 90% specificity, i.e. P(−|no disease) = 0.90. Find P(positive test) using the Law of Total Probability.",
        0.117, 0.002,
        "P(T) = P(T|D)P(D) + P(T|D')P(D') = 0.95·0.02 + 0.10·0.98 = 0.019 + 0.098 = 0.117")

    num("Conditional Prob & Bayes",
        "A disease affects 2% of the population. A test has 95% sensitivity, i.e. P(+|disease) = 0.95, and 90% specificity, i.e. P(−|no disease) = 0.90. A person tests positive. Find P(disease | positive) using Bayes' Rule.",
        0.162, 0.005,
        "P(D|T) = P(T|D)P(D)/P(T) = (0.95·0.02)/0.117 = 0.019/0.117 ≈ 0.162")

    mc("Conditional Prob & Bayes",
       "A disease affects 2% of the population. A test has 95% sensitivity, i.e. P(+|disease) = 0.95, and 90% specificity, i.e. P(−|no disease) = 0.90. Why is P(disease | positive) only about 16%?",
       ["Low base rate: most positives come from the large healthy population",
        "The test has poor sensitivity",
        "The test has poor specificity",
        "The disease is contagious"],
       "Low base rate: most positives come from the large healthy population",
       "Even with a good test, a rare disease means most positives are false positives from the 98% healthy group.")

    num("Conditional Prob & Bayes",
        "A factory has two machines. Machine A produces 60% of items with a 3% defect rate, i.e. P(defective|A) = 0.03. Machine B produces 40% with a 5% defect rate, i.e. P(defective|B) = 0.05. An item is selected at random. Find P(defective).",
        0.038, 0.002,
        "P(D) = P(D|A)P(A) + P(D|B)P(B) = 0.03·0.60 + 0.05·0.40 = 0.018 + 0.020 = 0.038")

    num("Conditional Prob & Bayes",
        "A factory has two machines. Machine A produces 60% of items with P(defective|A) = 0.03. Machine B produces 40% with P(defective|B) = 0.05. An item is selected at random and found to be defective. Find P(Machine B | defective) using Bayes' Rule.",
        0.526, 0.005,
        "P(B|D) = P(D|B)P(B)/P(D) = (0.05·0.40)/0.038 = 0.020/0.038 ≈ 0.526")

    tf("Conditional Prob & Bayes",
       "Bayes' Rule allows us to 'flip' a conditional probability: compute P(A|B) from P(B|A).",
       True,
       "Bayes' Rule: P(A|B) = P(B|A)P(A)/P(B). It reverses the conditioning.")

    tf("Conditional Prob & Bayes",
       "P(A|B) = P(B|A) always.",
       False,
       "In general P(A|B) ≠ P(B|A). They are related by Bayes' Rule but not equal unless P(A) = P(B).")

    mc("Conditional Prob & Bayes",
       "The Law of Total Probability states P(B) = ?",
       ["P(B|A)P(A) + P(B|A')P(A')",
        "P(A|B)P(B|A)",
        "P(A∩B) + P(A'∩B')",
        "P(A) + P(B) − P(A∩B)"],
       "P(B|A)P(A) + P(B|A')P(A')",
       "Total probability partitions the sample space through A and A', weighting P(B) by each branch.")

    num("Conditional Prob & Bayes",
        "P(A) = 0.3, P(B) = 0.5, A and B independent. Find P(B|A').",
        0.5, 0.005,
        "Since A and B are independent, P(B|A') = P(B) = 0.5.")

    # ═══════════════════════════════════════════════════════════════════════
    # 3. COUNTING & INDEPENDENCE (Lesson 8, sections 2.3, 2.5)
    # ═══════════════════════════════════════════════════════════════════════
    num("Counting & Independence",
        "A restaurant offers 3 appetizers, 5 entrées, and 4 desserts. How many different three-course meals are possible?",
        60, 0,
        "Multiplication rule: 3 × 5 × 4 = 60")

    num("Counting & Independence",
        "3 friends each pick one of 5 entrées at random. What is the probability all three choose different entrées?",
        0.48, 0.005,
        "P(all different) = (5/5)(4/5)(3/5) = 60/125 = 12/25 = 0.48")

    mc("Counting & Independence",
       "How many ways can you arrange 4 books on a shelf?",
       ["24", "16", "12", "4"],
       "24",
       "4! = 4·3·2·1 = 24 (permutation of 4 distinct objects).")

    mc("Counting & Independence",
       "How many ways can a committee of 3 be chosen from 8 people?",
       ["56", "336", "24", "512"],
       "56",
       "C(8,3) = 8!/(3!5!) = 56. Order doesn't matter → combination.")

    num("Counting & Independence",
        "How many ways to choose 2 items from 10 distinct items? (Combination)",
        45, 0,
        "C(10,2) = 10!/(2!·8!) = 45")

    tf("Counting & Independence",
       "If A and B are independent, then A' and B' are also independent.",
       True,
       "If A and B are independent, then any combination of them and their complements are also independent.")

    tf("Counting & Independence",
       "The number of permutations of n objects is always greater than the number of combinations of r objects from n (when r < n).",
       True,
       "P(n,r) = n!/(n-r)! while C(n,r) = n!/(r!(n-r)!). Since r! ≥ 1, P(n,r) ≥ C(n,r).")

    mc("Counting & Independence",
       "A 5-character password must have exactly 3 digit positions (each 0-9) followed by 2 letter positions (each A-Z). If repetition is allowed, how many passwords are possible?",
       ["10³ × 26² = 676,000", "10² × 26³ = 1,757,600", "C(10,3) × C(26,2) = 39,000", "10 × 26 × 5! = 31,200"],
       "10³ × 26² = 676,000",
       "Each digit has 10 choices, each letter has 26 choices. With repetition: 10³ · 26² = 676,000.")

    # ═══════════════════════════════════════════════════════════════════════
    # 4. DISCRETE RVs & PMFs (Lesson 9, sections 3.1-3.3)
    # ═══════════════════════════════════════════════════════════════════════
    tf("Discrete RVs & PMFs",
       "A valid PMF must satisfy Σ P(X = x) = 1 and P(X = x) ≥ 0 for all x.",
       True,
       "These are the two conditions for a valid PMF.")

    tf("Discrete RVs & PMFs",
       "The CDF of any random variable is a non-decreasing function.",
       True,
       "By definition, if a < b then F(a) ≤ F(b).")

    tf("Discrete RVs & PMFs",
       "Var(X) can be negative.",
       False,
       "Var(X) = E[(X − μ)²] which is an expected value of squared terms, so it's always ≥ 0.")

    mc("Discrete RVs & PMFs",
       "Which formula computes Var(X)?",
       ["E(X²) − [E(X)]²", "E(X²) − E(X)", "[E(X)]² − E(X²)", "E(X) − [E(X)]²"],
       "E(X²) − [E(X)]²",
       "The shortcut formula: Var(X) = E(X²) − [E(X)]².")

    num("Discrete RVs & PMFs",
        "P(X=x) = c·x² for x = 1, 2, 3 (0 otherwise). Find c to make this a valid PMF.",
        1/14, 0.002,
        "c(1 + 4 + 9) = 14c = 1, so c = 1/14 ≈ 0.0714",
        "")

    num("Discrete RVs & PMFs",
        "A discrete RV X has PMF P(X=x) = x²/14 for x = 1, 2, 3 (and 0 otherwise). Find E(X).",
        18/7, 0.01,
        "E(X) = 1·(1/14) + 2·(4/14) + 3·(9/14) = (1+8+27)/14 = 36/14 = 18/7 ≈ 2.571")

    num("Discrete RVs & PMFs",
        "A discrete RV X has PMF P(X=x) = x²/14 for x = 1, 2, 3 (and 0 otherwise). Find Var(X). Hint: use Var(X) = E(X²) − [E(X)]².",
        19/49, 0.01,
        "E(X²) = 1·(1/14) + 4·(4/14) + 9·(9/14) = 98/14 = 7. Var = 7 − (18/7)² = 19/49 ≈ 0.388")

    num("Discrete RVs & PMFs",
        "A discrete RV X has PMF P(X=x) = x²/14 for x = 1, 2, 3 (and 0 otherwise). Find P(X ≥ 2).",
        13/14, 0.005,
        "P(X≥2) = P(X=2) + P(X=3) = 4/14 + 9/14 = 13/14 ≈ 0.929")

    num("Discrete RVs & PMFs",
        "A carnival game costs $2 to play. You draw one card from a standard 52-card deck. Ace wins $10, face card (J, Q, K) wins $3, any other card wins $0. Let X = net profit (winnings minus $2 cost). Find E(X).",
        -28/52, 0.02,
        "Net: Ace → $8 (prob 4/52), Face → $1 (prob 12/52), Other → −$2 (prob 36/52). E(X) = 8(4/52) + 1(12/52) + (−2)(36/52) = −28/52 ≈ −$0.54")

    mc("Discrete RVs & PMFs",
       "For the CDF of a discrete RV, F(x) = P(X ≤ x) is:",
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
       "If X ~ Bin(n,p), then E(X) = np and Var(X) = np(1−p).",
       True,
       "These are the standard results for the binomial distribution.")

    mc("Binomial Distribution",
       "Which is NOT a requirement for a Binomial distribution?",
       ["Trials must be dependent on each other",
        "Fixed number of trials n",
        "Constant probability p on each trial",
        "Two outcomes per trial (success/failure)"],
       "Trials must be dependent on each other",
       "Binomial requires INDEPENDENT trials, not dependent ones.")

    num("Binomial Distribution",
        "15-question MC quiz, 4 options each, random guessing. X ~ Bin(15, 0.25). Find E(X).",
        3.75, 0.01,
        "E(X) = np = 15(0.25) = 3.75")

    num("Binomial Distribution",
        "A 15-question multiple-choice quiz has 4 options per question. A student guesses randomly, so X ~ Bin(15, 0.25). Find the standard deviation of X.",
        math.sqrt(15 * 0.25 * 0.75), 0.02,
        "σ = √(np(1−p)) = √(15·0.25·0.75) = √2.8125 ≈ 1.677")

    num("Binomial Distribution",
        "A student randomly guesses on a 15-question quiz with 4 options each, so X ~ Bin(15, 0.25). Find P(X = 5), the probability of exactly 5 correct.",
        math.comb(15, 5) * (0.25**5) * (0.75**10), 0.005,
        "P(X=5) = C(15,5)·(0.25)⁵·(0.75)¹⁰ = 3003·(0.25)⁵·(0.75)¹⁰ ≈ 0.165")

    num("Binomial Distribution",
        "A student randomly guesses on a 15-question quiz with 4 options each, so X ~ Bin(15, 0.25). Find P(X ≥ 2), the probability of getting at least 2 correct. Round to 3 decimal places.",
        1 - 0.75**15 - 15*0.25*0.75**14, 0.005,
        "P(X≥2) = 1 − P(X=0) − P(X=1) = 1 − (0.75)¹⁵ − 15·(0.25)·(0.75)¹⁴ ≈ 0.920")

    num("Binomial Distribution",
        "A batch of 20 light bulbs each independently has a 10% defect rate, so X ~ Bin(20, 0.10). Find P(X = 2), the probability exactly 2 are defective.",
        math.comb(20, 2) * (0.10**2) * (0.90**18), 0.005,
        "P(X=2) = C(20,2)·(0.10)²·(0.90)¹⁸ = 190·0.01·(0.90)¹⁸ ≈ 0.285")

    num("Binomial Distribution",
        "A batch of 20 light bulbs each independently has a 10% defect rate, so X ~ Bin(20, 0.10). Find P(X = 0), the probability none are defective.",
        0.90**20, 0.005,
        "P(X=0) = (0.90)²⁰ ≈ 0.122")

    num("Binomial Distribution",
        "A batch of 20 light bulbs each independently has a 10% defect rate, so X ~ Bin(20, 0.10). Find Var(X).",
        1.80, 0.01,
        "Var(X) = np(1−p) = 20·0.10·0.90 = 1.80")

    mc("Binomial Distribution",
       "50 coin flips of a fair coin. What distribution models the number of heads?",
       ["Bin(50, 0.5)", "Pois(25)", "N(25, 12.5)", "Exp(0.5)"],
       "Bin(50, 0.5)",
       "Fixed n=50 trials, constant p=0.5, two outcomes (H/T), independent → Binomial.")

    # ═══════════════════════════════════════════════════════════════════════
    # 6. POISSON DISTRIBUTION (Lesson 11, section 3.6)
    # ═══════════════════════════════════════════════════════════════════════
    num("Poisson Distribution",
        "A bookstore receives an average of 5 online orders per hour. Let X = number of orders in one hour, so X ~ Pois(5). Find P(X = 3).",
        (math.exp(-5) * 5**3) / math.factorial(3), 0.005,
        "P(X=3) = e⁻⁵·5³/3! = 125e⁻⁵/6 ≈ 0.140")

    num("Poisson Distribution",
        "A bookstore receives an average of 5 online orders per hour, so X ~ Pois(5). Find P(X = 0), the probability of no orders in one hour.",
        math.exp(-5), 0.001,
        "P(X=0) = e⁻⁵ ≈ 0.00674")

    num("Poisson Distribution",
        "A bookstore receives an average of 5 online orders per hour, so X ~ Pois(5). Find P(X ≥ 2), the probability of at least 2 orders in one hour.",
        1 - math.exp(-5) - 5*math.exp(-5), 0.005,
        "P(X≥2) = 1 − P(X=0) − P(X=1) = 1 − e⁻⁵ − 5e⁻⁵ = 1 − 6e⁻⁵ ≈ 0.960")

    num("Poisson Distribution",
        "A bookstore receives an average of 5 online orders per hour. What is P(exactly 8 orders in a 2-hour period)? Hint: the Poisson rate scales — use λ = 5 × 2 = 10 for the 2-hour window.",
        (math.exp(-10) * 10**8) / math.factorial(8), 0.005,
        "2-hour rate = 10. P(Y=8) = e⁻¹⁰·10⁸/8! ≈ 0.113")

    num("Poisson Distribution",
        "A city averages 3 power outages per month. Assume outages follow a Poisson process, so X ~ Pois(3). Find P(X = 5), the probability of exactly 5 outages in a given month.",
        (math.exp(-3) * 3**5) / math.factorial(5), 0.005,
        "X ~ Pois(3). P(X=5) = e⁻³·3⁵/5! = 243e⁻³/120 ≈ 0.101")

    num("Poisson Distribution",
        "A city averages 3 power outages per month (Poisson process). Find P(no outages in a 2-week period). Assume 1 month ≈ 4 weeks, so the 2-week rate is λ = 3/2 = 1.5.",
        math.exp(-1.5), 0.005,
        "Rate for 2 weeks = 1.5. P(Y=0) = e⁻¹·⁵ ≈ 0.223")

    mc("Poisson Distribution",
       "Which scenario best fits a Poisson distribution?",
       ["Number of typos per page in a novel (avg 1.5/page)",
        "Number of heads in 50 coin flips",
        "Weight of a bag of flour",
        "Time until next phone call"],
       "Number of typos per page in a novel (avg 1.5/page)",
       "Poisson counts rare events in a fixed interval/area. Coin flips → Binomial, weight → Normal, time → Exponential.")

    tf("Poisson Distribution",
       "For a Poisson random variable, the mean and variance are equal.",
       True,
       "If X ~ Pois(λ), then E(X) = Var(X) = λ.")

    mc("Poisson Distribution",
       "If events occur at rate 6/hour as a Poisson process, what is the rate for a 20-minute window?",
       ["2", "6", "3", "1"],
       "2",
       "20 min = 1/3 hour. Rate = 6 × (1/3) = 2.")

    # ═══════════════════════════════════════════════════════════════════════
    # 7. CONTINUOUS RVs & PDFs (Lesson 12, sections 4.1-4.2)
    # ═══════════════════════════════════════════════════════════════════════
    tf("Continuous RVs & PDFs",
       "If X is a continuous random variable, then P(X = 3) = 0.",
       True,
       "For continuous RVs, the probability at any single point is zero.")

    tf("Continuous RVs & PDFs",
       "For a continuous RV with pdf f(x), P(a ≤ X ≤ b) = ∫ₐᵇ f(x) dx.",
       True,
       "This is the fundamental definition of probability for continuous RVs.")

    num("Continuous RVs & PDFs",
        "A continuous RV X has pdf f(x) = kx(1−x) for 0 ≤ x ≤ 1 (and 0 otherwise). Find the value of k that makes this a valid pdf.",
        6.0, 0.01,
        "∫₀¹ kx(1−x)dx = k[x²/2 − x³/3]₀¹ = k(1/6) = 1, so k = 6.")

    num("Continuous RVs & PDFs",
        "A continuous RV X has pdf f(x) = 6x(1−x) for 0 ≤ x ≤ 1 (and 0 otherwise). Find P(0.25 ≤ X ≤ 0.75).",
        0.6875, 0.005,
        "F(x) = 3x² − 2x³. F(0.75) − F(0.25) = 0.84375 − 0.15625 = 0.6875")

    num("Continuous RVs & PDFs",
        "A continuous RV X has pdf f(x) = 6x(1−x) for 0 ≤ x ≤ 1 (and 0 otherwise). Find E(X).",
        0.5, 0.005,
        "E(X) = ∫₀¹ x·6x(1−x)dx = 6∫₀¹(x²−x³)dx = 6(1/3 − 1/4) = 6(1/12) = 1/2")

    num("Continuous RVs & PDFs",
        "A continuous RV X has pdf f(x) = 6x(1−x) for 0 ≤ x ≤ 1 (and 0 otherwise). Find Var(X). Hint: use Var(X) = E(X²) − [E(X)]².",
        0.05, 0.005,
        "E(X²) = 6(1/4 − 1/5) = 6(1/20) = 3/10. Var = 3/10 − (1/2)² = 0.30 − 0.25 = 0.05")

    num("Continuous RVs & PDFs",
        "A continuous RV Y has pdf f(y) = (3/16)√y for 0 ≤ y ≤ 4 (and 0 otherwise). Find P(Y > 1).",
        7/8, 0.005,
        "P(Y>1) = (3/16)·[2y^(3/2)/3] from 1 to 4 = (1/8)(8−1) = 7/8 = 0.875")

    num("Continuous RVs & PDFs",
        "A continuous RV Y has pdf f(y) = (3/16)√y for 0 ≤ y ≤ 4 (and 0 otherwise). Find E(Y).",
        2.4, 0.01,
        "E(Y) = (3/16)∫₀⁴ y^(3/2) dy = (3/16)(2/5)(32) = 12/5 = 2.4")

    num("Continuous RVs & PDFs",
        "A continuous RV X has CDF F(x) = x²/9 for 0 ≤ x ≤ 3 (with F(x)=0 for x<0, F(x)=1 for x>3). Find P(1 ≤ X ≤ 2). Recall: P(a ≤ X ≤ b) = F(b) − F(a).",
        1/3, 0.005,
        "P(1≤X≤2) = F(2) − F(1) = 4/9 − 1/9 = 3/9 = 1/3")

    num("Continuous RVs & PDFs",
        "A continuous RV X has CDF F(x) = x²/9 for 0 ≤ x ≤ 3. Find the median of X, i.e. solve F(m) = 0.5.",
        math.sqrt(4.5), 0.01,
        "F(m) = 0.5 → m²/9 = 0.5 → m = √4.5 ≈ 2.121")

    num("Continuous RVs & PDFs",
        "A continuous RV X has CDF F(x) = x²/9 for 0 ≤ x ≤ 3. Find E(X). Hint: first find the pdf by differentiating: f(x) = F'(x) = 2x/9.",
        2.0, 0.01,
        "f(x) = 2x/9. E(X) = ∫₀³ x·(2x/9)dx = (2/9)·[x³/3]₀³ = (2/9)·9 = 2")

    # ═══════════════════════════════════════════════════════════════════════
    # 8. NORMAL DISTRIBUTION (Lesson 13, section 4.3)
    # ═══════════════════════════════════════════════════════════════════════
    num("Normal Distribution",
        "The time (in minutes) to complete an online checkout is normally distributed with μ = 8 and σ = 2, i.e. X ~ N(μ=8, σ²=4). Find P(X > 12). Use the Z-table: Φ(2.0) = 0.9772.",
        0.0228, 0.005,
        "Z = (12−8)/2 = 2. P(X>12) = 1 − Φ(2) = 1 − 0.9772 = 0.0228")

    num("Normal Distribution",
        "Online checkout time X is normally distributed with μ = 8 min and σ = 2 min. Find P(5 < X < 11). Use the Z-table: Φ(1.5) = 0.9332, Φ(−1.5) = 0.0668.",
        0.8664, 0.005,
        "P(5<X<11) = Φ(1.5) − Φ(−1.5) = 0.9332 − 0.0668 = 0.8664")

    num("Normal Distribution",
        "Online checkout time X is normally distributed with μ = 8 min and σ = 2 min. Find the checkout time exceeded by only 5% of customers, i.e. find x such that P(X > x) = 0.05. Use z₀.₉₅ = 1.645.",
        11.29, 0.05,
        "P(X > x) = 0.05 → z = 1.645. x = 8 + 1.645(2) = 11.29 minutes.")

    num("Normal Distribution",
        "SAT math scores are approximately normal with μ = 520 and σ = 100, i.e. X ~ N(520, 100²). What score corresponds to the 90th percentile? Use z₀.₉₀ = 1.282.",
        648.2, 1.0,
        "z₉₀ = 1.282. Score = 520 + 1.282(100) = 648.2")

    num("Normal Distribution",
        "SAT math scores are approximately normal with μ = 520 and σ = 100. Find P(400 < X < 650). Use Φ(1.30) = 0.9032 and Φ(−1.20) = 0.1151.",
        0.7881, 0.01,
        "P = Φ(1.30) − Φ(−1.20) = 0.9032 − 0.1151 = 0.7881")

    num("Normal Distribution",
        "SAT math scores are approximately normal with μ = 520 and σ = 100. A scholarship requires a score in the top 2%. What is the minimum qualifying score? Use z₀.₉₈ = 2.054.",
        725.4, 1.0,
        "z₉₈ = 2.054. Score = 520 + 2.054(100) = 725.4")

    mc("Normal Distribution",
       "For a standard normal Z, what is P(−1.96 < Z < 1.96)?",
       ["0.95", "0.99", "0.90", "0.68"],
       "0.95",
       "The 95% confidence interval for Z is (−1.96, 1.96).")

    tf("Normal Distribution",
       "For a normal distribution, approximately 68% of values fall within 1 standard deviation of the mean.",
       True,
       "The 68-95-99.7 rule: ~68% within ±1σ, ~95% within ±2σ, ~99.7% within ±3σ.")

    mc("Normal Distribution",
       "The weight of a bag of flour follows a N(5.0, 0.01) distribution. In the notation N(μ, σ²), what are μ and σ?",
       ["Normal with μ=5.0, σ=0.1",
        "Normal with μ=5.0, σ=0.01",
        "Exponential with λ=5.0",
        "Poisson with λ=5.0"],
       "Normal with μ=5.0, σ=0.1",
       "N(5.0, 0.01) means μ=5.0 and σ²=0.01, so σ=0.1.")

    # ═══════════════════════════════════════════════════════════════════════
    # 9. EXPONENTIAL DISTRIBUTION (Lesson 14, section 4.4)
    # ═══════════════════════════════════════════════════════════════════════
    tf("Exponential Distribution",
       "The exponential distribution has the memoryless property: P(T > s+t | T > s) = P(T > t).",
       True,
       "The exponential is the only continuous distribution with this property.")

    num("Exponential Distribution",
        "Customers arrive at 10/hour. T ~ Exp(10). Find E(T) in hours.",
        0.1, 0.005,
        "E(T) = 1/λ = 1/10 = 0.1 hours = 6 minutes")

    num("Exponential Distribution",
        "Customers arrive at a coffee shop at a rate of 10 per hour. Let T be the waiting time (in hours) between customers, so T ~ Exp(λ=10). Find P(T > 0.25), the probability the wait exceeds 15 minutes.",
        math.exp(-2.5), 0.005,
        "P(T > 0.25) = e^(−10·0.25) = e^(−2.5) ≈ 0.0821")

    num("Exponential Distribution",
        "Customers arrive at a coffee shop at a rate of 10 per hour, so T ~ Exp(λ=10) in hours. Find P(T ≤ 0.1), the probability the next customer arrives within 6 minutes (0.1 hours).",
        1 - math.exp(-1), 0.005,
        "P(T ≤ 0.1) = 1 − e^(−10·0.1) = 1 − e⁻¹ ≈ 0.632")

    num("Exponential Distribution",
        "Customers arrive at a coffee shop at a rate of 10 per hour, so T ~ Exp(λ=10) in hours. Find the median wait time (in hours). Hint: set F(m) = 0.5 and solve for m.",
        math.log(2)/10, 0.002,
        "1 − e^(−10m) = 0.5 → m = ln(2)/10 ≈ 0.0693 hours ≈ 4.16 min")

    num("Exponential Distribution",
        "Lightning strikes in a national park at a rate of 6 per week during summer. Let T = time (in weeks) between strikes, so T ~ Exp(λ=6). Find P(T > 0.5), the probability of waiting more than half a week.",
        math.exp(-3), 0.005,
        "P(T > 0.5) = e^(−6·0.5) = e⁻³ ≈ 0.0498")

    num("Exponential Distribution",
        "Lightning strikes in a national park at 6 per week, so T ~ Exp(λ=6) in weeks. Given that no strike has occurred for 2 days (2/7 weeks), what is the probability of no strike for 3 more days (3/7 weeks)? Use the memoryless property.",
        math.exp(-18/7), 0.005,
        "Memoryless: P(T > 2/7 + 3/7 | T > 2/7) = P(T > 3/7) = e^(−6·3/7) = e^(−18/7) ≈ 0.0773")

    mc("Exponential Distribution",
       "Calls arrive at 8/hour. What distribution models the time until the next call?",
       ["Exp(λ=8)", "Pois(8)", "Bin(8, 0.5)", "N(8, 1)"],
       "Exp(λ=8)",
       "Waiting time between events in a Poisson process follows an Exponential distribution.")

    mc("Exponential Distribution",
       "For T ~ Exp(λ), the CDF is:",
       ["F(t) = 1 − e^(−λt) for t ≥ 0",
        "F(t) = e^(−λt) for t ≥ 0",
        "F(t) = λe^(−λt) for t ≥ 0",
        "F(t) = 1 − λe^(−t) for t ≥ 0"],
       "F(t) = 1 − e^(−λt) for t ≥ 0",
       "The Exponential CDF is F(t) = 1 − e^(−λt). The pdf is f(t) = λe^(−λt).")

    num("Exponential Distribution",
        "Customers arrive at a rate of 10 per hour, so the wait time T ~ Exp(λ=10) in hours. Find Var(T).",
        0.01, 0.002,
        "Var(T) = 1/λ² = 1/100 = 0.01")

    # ── Distribution identification (mixed) ──
    mc("Probability Basics",
       "400 flights, each independently 15% chance of delay. Which distribution models number of delays?",
       ["Bin(400, 0.15)", "Pois(60)", "N(60, 51)", "Exp(0.15)"],
       "Bin(400, 0.15)",
       "Fixed n=400, constant p=0.15, independent, two outcomes → Binomial.")

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
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border: 1px solid #ffd700;
        border-radius: 8px;
        padding: 8px 12px;
        margin: 4px 0;
        font-size: 0.9em;
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

st.markdown(f'<div class="question-card"><h3>📝</h3>{q["text"]}</div>', unsafe_allow_html=True)

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
