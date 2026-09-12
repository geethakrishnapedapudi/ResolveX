def analyze_request(customer_request):

    request = customer_request.lower()

    if "replace" in request or "replacement" in request:

        return {
            "intent": "replacement",
            "reason": "Customer requested a replacement."
        }

    if "refund" in request or "money back" in request:

        return {
            "intent": "refund",
            "reason": "Customer requested a refund."
        }

    if "cancel" in request or "cancellation" in request:

        return {
            "intent": "cancellation",
            "reason": "Customer requested cancellation."
        }

    return {
        "intent": "unknown",
        "reason":
            "Customer's requested resolution could not be identified."
    }


if __name__ == "__main__":

    request = input(
        "Enter customer request: "
    )

    result = analyze_request(request)

    print("\nRequest analysis:")
    print(result)