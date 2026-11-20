"""Training + validation tickets for the detector (spec v2). All invented. Run from the repo root.

Writes data/tickets_train.csv (templated + hand-written, ~300 rows) and data/tickets_val.csv (hand-written, disjoint).
The validation set is used ONLY to choose the confidence threshold (prototype/tune_threshold.py), never the eval-set.
"""
import csv, random

random.seed(11)

OPEN = ["", "", "Hello, ", "Hi team, ", "Quick question: ", "Urgent: ", "Dear support, ", "Hey, "]
SUBJ = ["our rating", "our score", "our review score", "our average rating", "the rating of our hotel", "our guest score",
        "the score of our property", "our reviews score", "our overall rating", "our satisfaction score"]
DROP = ["dropped", "went down", "fell", "decreased", "is lower", "is falling", "has declined", "slipped", "is down", "got worse"]
WHEN = ["", " this quarter", " since the summer", " compared with last quarter", " lately", " this month", " since spring", " recently"]
ASK = ["why?", "can you tell us why?", "what happened?", "what are guests unhappy about?", "can you analyse it?",
       "what changed?", "can you explain?", "what do the reviews say?", "we need the reasons.", "please look into it."]
ALT = ["why are guests rating us lower than before", "guests seem less happy with us, what is going on",
       "what are guests complaining about, the score keeps going down", "we are getting worse reviews than last quarter, why",
       "why is our reputation score declining", "what is behind our lower guest ratings", "reviews got worse, what changed",
       "something is wrong with our rating, can you check the reviews", "explain the decline in our review score please",
       "the owner asks why our rating is lower, can you help"]
TYPO = [("rating", "ratng"), ("why", "wy"), ("score", "scor"), ("dropped", "droped"), ("our", "ur"), ("guests", "gests")]

NEG_TOPICS = ["I cannot log in to my account", "please change the email address on our account", "how do I add a new user",
              "the export to excel does not work", "we want to cancel our contract", "can you send me the API documentation",
              "how do I change the language of the dashboard", "please update our billing address", "the widget on our site is not showing",
              "I need a copy of the data processing agreement", "how do I connect my booking system", "the mobile app crashes on the reviews tab",
              "I did not receive the notification emails", "can you add our second property", "how is the score calculated",
              "the dashboard does not load", "please reset my password", "where can I find my invoices", "there is a bug in the calendar view",
              "we need training for new staff on the platform", "can you upgrade us to the annual plan", "how to invite a colleague",
              "our invoice looks wrong", "what is the price of the premium plan", "I want a demo of the new features",
              "please remove a comment that contains personal data", "how can I download the monthly report", "the page is very slow today"]
NEG_WONT = ["can you reply to this angry review for us", "please write an answer to the review posted yesterday",
            "we want to respond publicly to a guest comment, can you draft it", "how do we compare with the other hotels in our city",
            "why is the hotel next door rated higher than us", "what should we change in the hotel to get better scores",
            "give us advice to improve our breakfast", "what do you recommend to raise our rating", "how can we beat our competitors on reviews",
            "can you benchmark us against similar hotels", "how can we improve guest satisfaction", "write a public response to the one star review"]
NEG_OTHERLANG = ["Pourquoi la note de notre hôtel a baissé", "Warum ist unsere Bewertung gesunken", "Perché la nostra valutazione è scesa",
                 "¿Por qué ha bajado nuestra puntuación?", "Wir können uns nicht einloggen", "Je n'arrive pas à me connecter à mon compte",
                 "Come posso aggiungere un utente", "Wie ändere ich meine Rechnungsadresse"]

# Support tickets that contain "rating" or "review" but are NOT rating-drop requests (fix for C07/C100, spec v3).
NEG_RATING_WORDS = ["our review widget shows the wrong rating on our website", "how do I change the rating display on the page",
                    "the review export is empty", "please delete the test review we posted", "this review about our hotel is fake, remove it",
                    "can I hide the rating from our public page", "I cannot see the rating of my second hotel in the dashboard",
                    "invoice for the review platform subscription is wrong", "how do I invite a colleague to see our reviews",
                    "the review notification emails go to the wrong address", "update the name shown next to our rating",
                    "why is my login to the reviews dashboard refused", "the rating badge on our site does not load",
                    "we want to dispute a review from a person who never stayed", "please add the rating widget to our booking page",
                    "can you send the review report as a PDF", "our reviews page address is wrong", "how is the rating displayed on mobile",
                    "cancel the reviews subscription at the end of the month", "the API for reviews returns an error"]
POS_HAND = ["why has our guest rating gone down recently", "our review score fell this quarter can you explain",
            "rating went from 8.5 to 8.0, help us understand why", "we lost half a point on our rating, what happened",
            "our guests seem unhappy, the rating is lower, what changed", "what changed in our reviews between last quarter and this one",
            "we need to explain to the owner why our rating dropped", "our satisfaction score is down, which topics do guests mention most",
            "the average score of our hotel decreased, why", "can you find the reasons for our lower scores",
            "we think the new carpet made our score drop, is that right", "score dropped and we got two bad reviews about parking, is that it",
            "my rating is falling and I do not know why", "ratings are worse since June, please investigate",
            "we dropped from 4.4 to 4.1 on your platform, any explanation", "guests are scoring us lower, what is the main complaint",
            "can you check why our score is falling", "what is going on with our reviews, the average is lower",
            "we need an analysis of why our rating went down", "after the renovation our score went down, why"]

# --- spec v4: more varied wording, written WITHOUT copying any eval case (C01-C200), to raise recall without lowering the threshold ---
POS_VARIED = ["guest satisfaction has been decreasing, what is the reason", "why are our marks worse than last year", "reviews keep getting worse, what is wrong",
              "our hotel is losing points on the platform, what is happening", "can someone explain our weaker guest feedback", "why did the average of our reviews go down",
              "what is behind the deterioration of our score", "we see a negative trend in guest comments, can you analyse it", "the reputation of our hotel is dropping, why",
              "which complaints are pulling our rating down", "our review average has slipped, we need to know why", "lower marks from guests since the summer, what changed",
              "why do guests like us less than before", "something changed in what guests write, our score is down", "we lost points this quarter, please explain",
              "what are the main reasons for our worse ratings", "our ranking score fell and the owner wants an explanation", "why is the guest score of our property declining",
              "please investigate the fall in our review score", "we are rated lower now, what do guests complain about", "reasons for the decline in satisfaction please",
              "our feedback score is deteriorating, please look at the comments", "guests are less pleased lately, why", "what lies behind our lower average rating",
              "why have the ratings of our hotel worsened", "the numbers on our page are lower than before, what happened in the reviews", "can you tell us what hurts our score",
              "why is the quality perception of our hotel worse in the reviews", "explain the downturn in our guest scores", "what drives our lower reviews this quarter"]
VARIED_START = ["", "", "Hello, ", "Hi, ", "Dear team, ", "Please, ", "Hello team, "]
VARIED_END = ["", "", " Thank you.", " Thanks!", " Many thanks.", " Please help.", " It is urgent."]


def pos_varied(n):
    out = set()
    while len(out) < n:
        t = random.choice(VARIED_START) + random.choice(POS_VARIED)
        t += random.choice(["", "", "?", "."]) + random.choice(VARIED_END)
        out.add(t.strip())
    return sorted(out)


def pos_templated(n):
    out = set()
    while len(out) < n:
        if random.random() < 0.3:
            t = random.choice(OPEN) + random.choice(ALT)
            if random.random() < 0.5:
                t += random.choice(WHEN)
        else:
            t = random.choice(OPEN) + random.choice(SUBJ) + " " + random.choice(DROP) + random.choice(WHEN) + ", " + random.choice(ASK)
        if random.random() < 0.15:
            a, b = random.choice(TYPO); t = t.replace(a, b)
        if random.random() < 0.1:
            t += " Also please check my invoice."
        out.add(t.strip())
    return sorted(out)


def neg_templated(n):
    out = set()
    pool = NEG_TOPICS * 3 + NEG_WONT * 4 + NEG_OTHERLANG * 2 + NEG_RATING_WORDS * 3
    while len(out) < n:
        t = random.choice(OPEN) + random.choice(pool)
        if random.random() < 0.3:
            t += random.choice([" please", ", thanks", " as soon as possible", "??"])
        out.add(t.strip())
    return sorted(out)


VAL_POS = ["Our hotel's guest rating has been sliding for weeks and we are puzzled", "Could you look at our reviews? the score is lower than in March",
           "we are at 7.6 now, it was 8.2, what is hurting us", "Any idea what guests dislike now? Our average keeps dropping",
           "the score of our B&B fell this season, what are the main complaints", "why do we have worse reviews this quarter than the last one",
           "please explain why our overall rating decreased", "What happened to our score? Owners are asking",
           "ratings down again, can someone dig into what guests say", "we lost 0.3 points since the summer, why is that",
           "hi, our reviews average is lower, please find out why", "I would like to understand the drop in our guest ratings",
           "our guests are giving lower marks lately, what is behind it", "rating down since the pool closed, is it that or something else",
           "our satisfaction numbers declined in Q3, what are the drivers", "can you tell me what changed in what guests write about us",
           "the hotel score went from 8.7 to 8.1, please analyse the comments", "worse and worse reviews recently, what are the top issues",
           "we got a lower rating than last quarter and the GM wants the causes", "analysis request: why did our score fall"]
VAL_POS += ["why are guests more critical of us than last quarter", "what is lowering our guest score", "our reviews turned worse, can you explain why",
            "reasons for the lower rating of our hotel please", "what changed in our feedback this quarter, the score fell",
            "why do we get lower marks now", "the guest rating of our property is declining, what are the causes",
            "our score is going down on your platform, please check why", "what makes guests rate us worse", "worse average on our page, please analyse"]
VAL_NEG = ["I forgot my password and the reset email never arrives", "Please send us the contract renewal conditions", "how can I export all my reviews to a file",
           "our invoice shows two charges this month", "the mobile app shows a blank screen", "we want to reply to the 1 star review from Saturday",
           "what should we improve to climb the ranking", "how are we doing compared with the other hotels nearby", "can you add my colleague as an admin",
           "the integration with our PMS stopped syncing", "I need the list of API endpoints", "cancel my subscription please",
           "est-ce que vous pouvez m'expliquer pourquoi notre note est plus basse", "wie kann ich ein neues Konto anlegen",
           "give me tips to get better reviews", "please translate the dashboard into Spanish", "where do I see the number of reviews per month",
           "we need a certificate for our auditor", "the widget shows the wrong hotel name", "can you delete our test account",
           "the review count on our public page looks wrong", "please remove an abusive review that insults our staff",
           "how do I embed the rating on our homepage", "my account was locked after I opened the reviews tab",
           "our review plan invoice is higher than agreed", "can you correct the hotel name next to our rating",
           "a competitor wrote a fake review, take it down", "the reviews export misses the last week",
           "how do I turn off review emails", "I need the contract for the review service"]


def write(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["text", "label"]); w.writerows(rows)


if __name__ == "__main__":
    pos = POS_HAND + pos_templated(130) + pos_varied(70)
    neg = neg_templated(150)
    write("data/tickets_train.csv", [(t, "rating_drop") for t in pos] + [(t, "other") for t in neg])
    write("data/tickets_val.csv", [(t, "rating_drop") for t in VAL_POS] + [(t, "other") for t in VAL_NEG])
    print(len(pos), len(neg), "train;", len(VAL_POS), len(VAL_NEG), "validation")
