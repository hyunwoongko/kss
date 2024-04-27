import pandas as pd

from kss._modules.safety.check_safety import is_unsafe

data = pd.read_csv("hatescore.csv").values
data = [d for d in data if d[-1] != "규칙 기반 생성"]
unsafe_data = [d[1] for d in data if d[-3] != "Clean"]
safe_data = [d[1] for d in data if d[-3] == "Clean"]

positive_output = [is_unsafe(d) for d in unsafe_data]
negative_output = [is_unsafe(d) for d in safe_data]
positive_accuracy = sum(positive_output) / len(positive_output)
negative_accuracy = (1 - sum(negative_output) / len(negative_output))

print("<Test KSS safety module>")
print("Accuracy: ", round((positive_accuracy + negative_accuracy) / 2, 2))
print("Positive Accuracy: ", round(positive_accuracy, 2))
print("Negative Accuracy: ", round(negative_accuracy, 2))
