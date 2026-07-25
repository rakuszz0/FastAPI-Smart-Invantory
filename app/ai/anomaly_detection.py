import numpy as np

from sklearn.ensemble import IsolationForest


class AnomalyDetectionAI:

    @staticmethod
    def detect(
        transactions: list[float]
    ):

        data = np.array(
            transactions
        ).reshape(-1, 1)

        model = IsolationForest(

            contamination=0.05,

            random_state=42

        )

        model.fit(
            data
        )

        prediction = model.predict(
            data
        )

        result = []

        for amount, label in zip(

            transactions,

            prediction

        ):

            result.append(

                {

                    "amount": amount,

                    "anomaly": bool(label == -1)

                }

            )

        return result