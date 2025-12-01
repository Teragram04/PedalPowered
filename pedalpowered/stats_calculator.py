from pedalpowered import db
from pedalpowered.models import rides
from sqlalchemy import func
from datetime import datetime,timezone
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import io
import base64


def get_user_stats(user_id, start_date = None, end_date = None):
    query = db.session.query(
        func.count(rides.id).label('total_rides'),
        func.sum(rides.distance).label('total_distance'),
        func.sum(rides.gas_money_saved).label('total_gas_money_saved'),
        func.max(rides.distance).label('longest_distance'),
        func.min(rides.distance).label('shortest_distance')
    ).filter_by(user_id=user_id)

    if start_date:
        query = query.filter(rides.ride_date >= start_date)
        
    if end_date:
        end_datetime = datetime.combine(end_date, datetime.max.time())
        query = query.filter(rides.ride_date <= end_date)

    stats_query = query.first()

    cumulative_statistics = {
        'total_rides' : stats_query.total_rides or 0,
        'total_distance': round(stats_query.total_distance or 0,2),
        'total_money_saved': round(stats_query.total_gas_money_saved or 0,2),
        'longest_ride': round(stats_query.longest_distance or 0,2) if stats_query.longest_distance else 0,
        'shortest_ride': round(stats_query.shortest_distance or 0,2) if stats_query.longest_distance else 0,
    }

    return cumulative_statistics

def graph_money_saved(user_id, start_date = None, end_date = None):

    query = rides.query.filter_by(user_id=user_id)\
    .order_by(rides.ride_date.asc())

    if start_date:
        query = query.filter(rides.ride_date >= start_date)
        
    if end_date:
        end_datetime = datetime.combine(end_date, datetime.max.time())
        query = query.filter(rides.ride_date <= end_date)

    user_rides = query.order_by(rides.ride_date.asc()).all()


    if not user_rides:
        return None
    
   
    
    dates = []
    cumulative_money = []
    total = 0

    for ride in user_rides:
        dates.append(ride.ride_date)
        total += ride.gas_money_saved if ride.gas_money_saved else 0
        cumulative_money.append(total)

    # Create the graph
    plt.figure(figsize=(10,6))
    plt.plot(dates, cumulative_money)
    plt.title('Money saved over time')
    plt.xlabel('Date')
    plt.ylabel('Money saved ($)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(color='b', linestyle='--', linewidth=.5)


    # Save plot to a bytes buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    
    # Encode to base64
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    
    data_uri = f"data:image/png;base64,{image_base64}"

    return data_uri


def graph_distance_ridden(user_id, start_date = None, end_date = None):
    query = rides.query.filter_by(user_id=user_id)\
    .order_by(rides.ride_date.asc())

    if start_date:
        query = query.filter(rides.ride_date >= start_date)
        
    if end_date:
        end_datetime = datetime.combine(end_date, datetime.max.time())
        query = query.filter(rides.ride_date <= end_date)

    user_rides = query.order_by(rides.ride_date.asc()).all()

    
    if not user_rides:
        return None
    
    dates = []
    cumulative_distance = []
    total = 0

    for ride in user_rides:
        dates.append(ride.ride_date)
        total += ride.distance if ride.distance else 0
        cumulative_distance.append(total)

        # Create the graph
    plt.figure(figsize=(10,6))
    plt.plot(dates, cumulative_distance)
    plt.title('Distance biked over time')
    plt.xlabel('Date')
    plt.ylabel('Distance biked (miles)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(color='b', linestyle='--', linewidth=.5)

    # Save plot to a bytes buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    
    # Encode to base64
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    
    data_uri = f"data:image/png;base64,{image_base64}"

    return data_uri