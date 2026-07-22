class RecommendationAI:

    @staticmethod
    def recommend(

        stock: int,

        predicted_sales: float,

        minimum_stock: int = 20

    ):

        if stock <= minimum_stock:

            return {

                "status": "LOW",

                "recommendation":
                "Restock immediately"

            }

        if predicted_sales > stock:

            return {

                "status": "HIGH DEMAND",

                "recommendation":
                "Increase stock"

            }

        return {

            "status": "NORMAL",

            "recommendation":
            "Current stock is sufficient"

        }