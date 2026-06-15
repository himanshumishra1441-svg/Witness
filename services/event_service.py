from repositories.event_repository import get_loan_history


def get_loan_history_service(loan_id):

    rows = get_loan_history(loan_id)

    history = []

    for row in rows:

        history.append(
            {
                "event_type": row.event_type,
                "payload": row.payload,
                "created_at": str(row.created_at)
            }
        )

    return history