from sklearn.linear_model import LinearRegression
import numpy as np


class ForecastingAI:

    @staticmethod
    def predict_stock(sales_history: list[int]):

        """
        sales_history
        contoh:

        [10,15,20,18,25,27]
        """

        if len(sales_history) < 2:

            return sales_history[-1]

        x = np.arange(
            len(sales_history)
        ).reshape(-1, 1)

        y = np.array(
            sales_history
        )

        model = LinearRegression()

        model.fit(
            x,
            y
        )

        next_day = np.array(
            [[len(sales_history)]]
        )

        prediction = model.predict(
            next_day
        )

        return round(
            float(prediction[0]),
            2
        )