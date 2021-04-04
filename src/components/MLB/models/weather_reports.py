from utils.database import mlbdb
from sqlalchemy.dialects.postgresql import UUID, JSON
from uuid import uuid4


class WeatherReportModel(mlbdb.Model):
    __tablename__ = 'weather_reports'
    weather_report_id = mlbdb.Column(UUID(as_uuid=True), primary_key=True)
    temperature = mlbdb.Column(mlbdb.String, nullable=False)
    wind = mlbdb.Column(mlbdb.String, nullable=False)
    precipitation = mlbdb.Column(mlbdb.String, nullable=False)
    location = mlbdb.Column(mlbdb.String, nullable=False)
    date = mlbdb.Column(mlbdb.String, nullable=False)

    def as_dict(self):
        return {
            'weather_report_id': self.weather_report_id,
            'temperature': self.temperature,
            'wind': self.wind,
            'precipitation': self.precipitation,
            'location': self.location,
            'date': self.date
        }

    @staticmethod
    def get_all_weather_reports(**filters):
        return_as_model = False

        if filters.get('return_as_model', None) is not None:
            return_as_model = filters.get('return_as_model', False)
            del filters['return_as_model']

        return WeatherReportModel.query.filter_by(filters).all() if return_as_model is False else [weather_report_model.as_dict() for weather_report_model in WeatherReportModel.query.filter_by(filters).all()]

    @staticmethod
    def get_weather_report_by_id(weather_report_id, return_as_model=False):
        weather_report_model = WeatherReportModel.query.filter_by(weather_report_id=weather_report_id).first()

        if return_as_model is False:
            return weather_report_model.as_dict() if weather_report_model else None

        else:
            return weather_report_model if weather_report_model else None

    @staticmethod
    def update_weather_report(weather_report_id, temperature, wind, precipitation, location, date, return_as_model=False):
        weather_report_model = WeatherReportModel.get_weather_report_by_id(weather_report_id=weather_report_id,
                                                                           temperature=temperature,
                                                                           wind=wind,
                                                                           precipitation=precipitation,
                                                                           location=location,
                                                                           return_as_model=True)

        if weather_report_model:
            if temperature is not None:
                weather_report_model.temperature = temperature

            if wind is not None:
                weather_report_model.wind = wind

            if precipitation is not None:
                weather_report_model.precipitation = precipitation

            if location is not None:
                weather_report_model.location = location

            if date is not None:
                weather_report_model.date = date

            weather_report_model.commit()
            return weather_report_model if return_as_model else weather_report_model.as_dict()

        return None

    @staticmethod
    def create_weather_report(temperature, wind, precipitation, location, date):
        weather_report_models = WeatherReportModel.get_all_weather_reports(temperature=temperature,
                                                                           wind=wind,
                                                                           precipitation=precipitation,
                                                                           location=location,
                                                                           date=date)

        if weather_report_models:
            return [weather_report_model.as_dict() for weather_report_model in weather_report_models]

        weather_report_id = str(uuid4())
        weather_report_model = WeatherReportModel(weather_report_id=weather_report_id,
                                                  temperature=temperature,
                                                  wind=wind,
                                                  precipitation=precipitation,
                                                  location=location,
                                                  date=date)

        mlbdb.add(weather_report_model)
        mlbdb.commit()

        return weather_report_model.as_dict()

    @staticmethod
    def delete_weather_report(weather_report_id):
        weather_report_model = WeatherReportModel.get_weather_report_by_id(weather_report_id=weather_report_id, return_as_model=True)

        if weather_report_model:
            mlbdb.delete(weather_report_model)
            mlbdb.commit()

            return weather_report_model.as_dict()

        return None

