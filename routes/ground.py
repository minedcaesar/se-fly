# UC13 - See Weather
# mock api to show the weather forecast 
# UC14 - See Shift
# Shows to the authorised personnel the programmed shifts
# UC16 - Move Aircraft
# Allowing the personnel to move the resources

from flask import Blueprint, redirect, render_template, url_for

# Import the custom authorization decorator from your local routes module
from routes import role_required

# Initialize a Flask Blueprint named 'ground' to compartmentalize ground operations routes under /ground
bp = Blueprint('ground', __name__, url_prefix='/ground')

# Tuple defining all authorization roles permitted to access ground-handling view endpoints
GROUND_ROLES = ('ground_op_manager', 'shift_manager', 'operation_staff')


@bp.route('/')
# Unpack the GROUND_ROLES tuple using '*' to pass all allowed roles to the authorization decorator
@role_required(*GROUND_ROLES)
def dashboard():
    return render_template('ground/dashboard.html')


# Temporary login for operation staff
@bp.route('/tasks')
@role_required(*GROUND_ROLES)
def tasks():
    return redirect(url_for('ground.dashboard'))


@bp.route('/weather')
@role_required(*GROUND_ROLES)
def weather():
    # production: WeatherForecastAPI.getWeeklyForecast() -> OpenWeatherMap.
    #   requests.get("https://api.openweathermap.org/data/2.5/forecast", params={...})
    # mocked 5-day forecast for the deliverable:
    forecast = [
        {'day': 'Mon', 'temp': 18, 'desc': 'Clear'},
        {'day': 'Tue', 'temp': 21, 'desc': 'Sunny'},
        {'day': 'Wed', 'temp': 16, 'desc': 'Rain'},
        {'day': 'Thu', 'temp': 17, 'desc': 'Cloudy'},
        {'day': 'Fri', 'temp': 20, 'desc': 'Clear'},
    ]

    # Render the weather template interface and inject the forecast dictionary list into its scope
    return render_template('ground/weather.html', forecast=forecast)