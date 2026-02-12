from flask import jsonify, request

def register_transaction_routes(app, load_transactions, filter_transactions, mtd_summary, month_by_month_summary):

    @app.route("/api/transactions")
    def get_transactions():
        print("----------------------------------------")
        print("*** [API] GET /api/transactions ***")
        cardBrand = request.args.get("cardBrand")
        status = request.args.get("status")
        declineReasonCode = request.args.get("declineReasonCode")
        print(f"[API] Filters: cardBrand={cardBrand}, status={status}, declineReasonCode={declineReasonCode}")

        transactions = load_transactions()
        filtered = filter_transactions(
            transactions,
            cardBrand=cardBrand,
            status=status,
            declineReasonCode=declineReasonCode
        )

        print(f"[API] Returning {len(filtered)} transactions")
        return jsonify(filtered)


    @app.route("/api/summary/mtd")
    def get_mtd_summary():
        print("\n\n--------------------Month to Date--------------------")
        print("[API] GET /api/summary/mtd")
        cardBrand = request.args.get("cardBrand")
        status = request.args.get("status")
        declineReasonCode = request.args.get("declineReasonCode")
        print(f"[API] Filters: cardBrand={cardBrand}, status={status}, declineReasonCode={declineReasonCode}")

        result = mtd_summary(
            load_transactions(),
            cardBrand=cardBrand,
            status=status,
            declineReasonCode=declineReasonCode
        )
        print(f"[API] Returning MTD summary")
        return jsonify(result)


    @app.route("/api/summary/monthly")
    def get_monthly_summary():
        print("-------------------Monthly---------------------")
        print("[API] GET /api/summary/monthly")
        cardBrand = request.args.get("cardBrand")
        status = request.args.get("status")
        declineReasonCode = request.args.get("declineReasonCode")
        print(f"[API] Filters: cardBrand={cardBrand}, status={status}, declineReasonCode={declineReasonCode}")

        result = month_by_month_summary(
            load_transactions(),
            cardBrand=cardBrand,
            status=status,
            declineReasonCode=declineReasonCode
        )
        print(f"[API] Returning {len(result)} months of data")
        return jsonify(result)


    @app.route("/api/health")
    def health_check():
        print("----------------------------------------")
        print("[API] GET /api/health")
        return jsonify({"status": "ok"})
