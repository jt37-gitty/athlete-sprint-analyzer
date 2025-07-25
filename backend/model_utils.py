import joblib
import pandas as pd
import os

t1_model = joblib.load("backend/models/t1_model.pkl")
t2_model = joblib.load("backend/models/t2_model.pkl")

user_runs = {}

def load_model(name):
    return joblib.load(os.path.join("backend", "models", f"{name}.pkl"))

def predict_t1_from_total(total_time):
    df = pd.DataFrame([[total_time]], columns=["TotalTime"])
    return float(t1_model.predict(df))

def predict_t2_from_total(total_time):
    df = pd.DataFrame([[total_time]], columns=["TotalTime"])
    return float(t2_model.predict(df))

def predict_t3(total_time, t1, t2):
    return round(total_time - t1 - t2, 2)

def analyze_performance(t1, t2, t3, category):
    d1, d2, d3 = 60, 30, 10
    max_acc = 4.2
    baseline_ratio = 0.80
    strength_baseline = 0.92

    acceleration = (2 * d1) / (t1 ** 2)
    explosiveness = round((acceleration / max_acc) * 100, 2)

    v_max = (2 * d1) / t1
    v_t2 = d2 / t2
    endurance = round((v_t2 / v_max) / baseline_ratio * 100, 2)

    v_t3 = d3 / t3
    strength = round((v_t3 / v_t2) / strength_baseline * 100, 2)

    weaknesses = []

    category_thresholds = {
        "Elite": {"exp": 86, "end": 68, "str": 79},
        "Pro": {"exp": 74, "end": 67, "str": 76},
        "Intermediate": {"exp": 67, "end": 67, "str": 74},
        "Beginner": {"exp": 54, "end": 66, "str": 71}
    }

    thresholds = category_thresholds[category]

    def evaluate_metric(score, key, label):
        threshold = thresholds[key]
        delta = threshold - score

        if delta <= 0:
            return  # no weakness
        elif delta <= 2:
            weaknesses.append(f"Slightly low {label} – Add targeted drills and monitor.")
        elif delta <= 4:
            if key == "exp":
                weaknesses.append(f"Moderate explosiveness issue – Focus on sprint starts, resistance drills.")
            elif key == "end":
                weaknesses.append(f"Moderate endurance loss – Work on fly-ins and pacing in middle phase.")
            elif key == "str":
                weaknesses.append(f"Moderate strength drop – Focus on form retention and explosive finish.")
        else:
            if key == "exp":
                weaknesses.append(f"Severe explosiveness issue – Do reaction drills, sled sprints, and gym work.")
            elif key == "end":
                weaknesses.append(f"Severe endurance loss – Interval sprints and VO2 max development needed.")
            elif key == "str":
                weaknesses.append(f"Severe strength deficit – Include resistance work, hill sprints, and core.")

    # Evaluate each metric
    evaluate_metric(explosiveness, "exp", "explosiveness")
    evaluate_metric(endurance, "end", "endurance")
    evaluate_metric(strength, "str", "strength")

    return {
        "explosiveness": explosiveness,
        "endurance": endurance,
        "strength": strength,
        "weaknesses": weaknesses
    }


def categorize_athlete(total_time):
    if total_time < 10.4:
        return "Elite"
    elif total_time < 11.0:
        return "Pro"
    elif total_time < 12.4:
        return "Intermediate"
    else:
        return "Beginner"


def analyze_run(total_time, t1=None, t2=None):
    if t1 is None:
        t1 = predict_t1_from_total(total_time)
    if t2 is None:
        t2 = predict_t2_from_total(total_time)

    t3 = round(total_time - t1 - t2, 2)
    category = categorize_athlete(total_time)
    perf = analyze_performance(t1, t2, t3, category)

    return {
        "t1": round(t1, 2),
        "t2": round(t2, 2),
        "t3": round(t3, 2),
        "total_time": total_time,
        "category": category,
        **perf
    }


def save_run(username, result):
    if username not in user_runs:
        user_runs[username] = []
    user_runs[username].append(result)
    return True

def get_user_runs(username):
    return user_runs.get(username, [])