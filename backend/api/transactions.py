from flask import jsonify, request

def register_transaction_routes(app, load_transactions, filter_transactions, mtd_summary, month_by_month_summary):

    @app.route("/api/transactions")
    def get_transactions():
        cardBrand = request.args.get("cardBrand")
        status = request.args.get("status")
        declineReasonCode = request.args.get("declineReasonCode")

        transactions = load_transactions()
        filtered = filter_transactions(
            transactions,
            cardBrand=cardBrand,
            status=status,
            declineReasonCode=declineReasonCode
        )

        return jsonify(filtered)


    @app.route("/api/summary/mtd")
    def get_mtd_summary():
        cardBrand = request.args.get("cardBrand")
        status = request.args.get("status")
        declineReasonCode = request.args.get("declineReasonCode")

        return jsonify(mtd_summary(
            load_transactions(),
            cardBrand=cardBrand,
            status=status,
            declineReasonCode=declineReasonCode
        ))


    @app.route("/api/summary/monthly")
    def get_monthly_summary():
        cardBrand = request.args.get("cardBrand")
        status = request.args.get("status")
        declineReasonCode = request.args.get("declineReasonCode")

        return jsonify(month_by_month_summary(
            load_transactions(),
            cardBrand=cardBrand,
            status=status,
            declineReasonCode=declineReasonCode
        ))


    @app.route("/api/health")
    def health_check():
        return jsonify({"status": "ok"})
