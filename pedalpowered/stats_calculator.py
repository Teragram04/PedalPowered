from pedalpowered import db
from pedalpowered.models import rides
from sqlalchemy import func
from datetime import datetime

def get_user_stats(user_id):
    stats_query = db.session.query(
        func.count(rides.id).label('total_rides'),
        func.sum(rides.distance).label('total_distance'),
        func.sum(rides.gas_money_saved).label('total_gas_money_saved'),
        func.max(rides.distance).label('longest_distance'),
        func.min(rides.distance).label('shortest_distance')
    ).filter_by(user_id=user_id).first()

    cumulative_statistics = {
        'total_rides' : stats_query.total_rides or 0,
        'total_distance': round(stats_query.total_distance or 0,2),
        'total_money_saved': round(stats_query.total_gas_money_saved or 0,2),
        'longest_ride': round(stats_query.longest_distance or 0,2) if stats_query.longest_distance else 0,
        'shortest_ride': round(stats_query.shortest_distance or 0,2) if stats_query.longest_distance else 0,
    }

    return cumulative_statistics
        